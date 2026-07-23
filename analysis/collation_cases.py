#!/usr/bin/env python
#
# The ten intercalation differences between our tables (P&D 1942) and
# the third-party transcription of the 1956/1971 edition, examined one
# by one: for each case, print the surrounding years' Nisanu dates and
# their position against the true March equinox under BOTH variants
# (N1-eq = Nisanu 1 minus equinox; full-eq = Nisanu full moon minus
# equinox, in days). The early-era operating rule (full moon not before
# the equinox; see nisanu_equinox.py) then favors, disfavors, or cannot
# discriminate each variant. See collation_cases.md for the readings.
#
# CAUTION: the rule was itself inferred largely from the 1942
# arrangement, so "geometry favors 1942" partly restates P&D's own
# equinox expectations. Use as a hypothesis generator, not a verdict.
#
# USAGE:  python analysis/collation_cases.py [saved-bible-ca-copy.htm]

import bisect
import csv
import html
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
URL = ("https://www.bible.ca/revelation/Babylon-Chronology-Parker-Dubberstein"
       "-Jewish-Hebrew-Julian-calendar-625BC-75AD-date-converter-1971AD.htm")

# jdn of our (1942) intercalary month for each disputed case
CASES = (1493580, 1494495, 1495588, 1497419, 1499250,
         1502350, 1505097, 1546174, 1558783, 1565723)


def to_jdn(year, month, day):
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + y * 365 + y // 4 - 32083


def from_jdn(jdn):
    c = jdn + 32082
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    return (d - 4800 + m // 10, m + 3 - 12 * (m // 10), e - (153 * m + 2) // 5 + 1)


def date(jdn):
    y, m, d = from_jdn(jdn)
    return f"{y}-{m:02d}-{d:02d}"


def equinox_jd(year):
    Y = year / 1000.0
    jde = (1721139.29189 + 365242.13740 * Y + 0.06134 * Y**2
           + 0.00111 * Y**3 - 0.00071 * Y**4)
    return jde - (-20 + 32 * ((year - 1820) / 100.0) ** 2) / 86400.0 + 2.96 / 24.0


moons = sorted(float(m) for m in open(f"{REPO}/new_moons_jdn.txt") if "#" not in m)


def geometry(nisanu_jdn):
    eq = equinox_jd(from_jdn(nisanu_jdn)[0])
    i = bisect.bisect(moons, nisanu_jdn) - 1
    full = (moons[i] + moons[i + 1]) / 2.0
    return nisanu_jdn - eq, full - eq


def year_series(lunations):
    """lunations: (jdn, is_nisanu, intercalary_name_or_None) ->
    [(nisanu_jdn, intercalary text)]"""
    out, cur = [], None
    for j, is_nis, inter in lunations:
        if is_nis:
            cur = j
            out.append([j, "regular year"])
        if inter and cur is not None:
            out[-1][1] = f"{inter} at {date(j)}"
    return out


ours = []
for r in list(csv.reader(open(f"{REPO}/parker_and_dubberstein.tsv"),
                         delimiter="\t"))[1:]:
    name = r[5]
    ours.append((int(r[0]), name == "Nisanu",
                 name if name in ("Ululu II", "Addaru II") else None))

if len(sys.argv) > 1:
    raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
else:
    print("downloading third-party transcription ...")
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "replace")

their = []
for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", raw, flags=re.S):
    cells = [html.unescape(re.sub(r"<[^>]+>|\s+", " ", c)).strip()
             for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
    if len(cells) != 5:
        continue
    m = re.fullmatch(r"(\d+)(b?)", cells[1])
    d = re.match(r"(\d+)", cells[3])
    if (m and d and re.fullmatch(r"-?\d+", cells[0])
            and re.fullmatch(r"-?\d+", cells[2])):
        mn = int(m.group(1))
        their.append((to_jdn(int(cells[0]), int(cells[2]), int(d.group(1))),
                      mn == 1 and not m.group(2),
                      ("Ululu II" if mn == 6 else "Addaru II")
                      if m.group(2) else None))
their.sort()

series = (("1942 (ours)", year_series(ours)),
          ("1956-derived", year_series(their)))

for n, cj in enumerate(CASES, 1):
    print("=" * 76)
    print(f"CASE {n}: our intercalary month at jdn {cj} ({date(cj)})")
    for label, ys in series:
        print(f"  {label}:")
        for j, itxt in ys:
            if cj - 800 < j < cj + 800:
                d1, d15 = geometry(j)
                print(f"    Nisanu {date(j)}  N1-eq {d1:+6.1f}"
                      f"  full-eq {d15:+6.1f}  {itxt}")
