#!/usr/bin/env python
#
# Collates this repository's tables (Parker & Dubberstein 1942) against a
# third-party transcription of the 1971 printing of the 1956 edition,
# published at bible.ca. See collation_1956.md for what that source is
# and is not. Downloads the page (~15 MB) on each run; nothing from it
# is stored in this repository.
#
# USAGE:  python analysis/collation_1956.py [saved-copy.htm]

import csv
import html
import os
import re
import urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
URL = ("https://www.bible.ca/revelation/Babylon-Chronology-Parker-Dubberstein"
       "-Jewish-Hebrew-Julian-calendar-625BC-75AD-date-converter-1971AD.htm")

MONTHS = {"Nisanu": 1, "Aiaru": 2, "Simanu": 3, "Duzu": 4, "Abu": 5,
          "Ululu": 6, "Tashritu": 7, "Arahsamnu": 8, "Kislimu": 9,
          "Tebetu": 10, "Shabatu": 11, "Addaru": 12}


def to_jdn(year, month, day):
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + y * 365 + y // 4 - 32083


import sys
if len(sys.argv) > 1:
    raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
else:
    print("downloading third-party transcription ...")
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "replace")

their = []          # (jdn, month number 1-12, intercalary?)
for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", raw, flags=re.S):
    cells = [html.unescape(re.sub(r"<[^>]+>|\s+", " ", c)).strip()
             for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
    if len(cells) != 5:
        continue
    m = re.fullmatch(r"(\d+)(b?)", cells[1])
    d = re.match(r"(\d+)", cells[3])
    if (m and d and re.fullmatch(r"-?\d+", cells[0])
            and re.fullmatch(r"-?\d+", cells[2])):
        their.append((to_jdn(int(cells[0]), int(cells[2]), int(d.group(1))),
                      int(m.group(1)), bool(m.group(2))))
their.sort()

ours = [(int(r[0]), r[5]) for r in
        list(csv.reader(open(f"{REPO}/parker_and_dubberstein.tsv"),
                        delimiter="\t"))[1:]]
inter = list(csv.reader(open(f"{REPO}/intercalations.tsv"), delimiter="\t"))[1:]

lo, hi = ours[0][0], ours[-1][0]
tw = [t for t in their if lo - 5 <= t[0] <= hi + 5]
print(f"lunations in our span: ours {len(ours)}, theirs {len(tw)}")
if len(tw) != len(ours):
    raise SystemExit("series do not pair 1:1; inspect the source")

daydiff = Counter(t[0] - o[0] for t, o in zip(tw, ours))
n = sum(v for k, v in daydiff.items() if k != 0)
print(f"day-level: {n} of {len(ours)} dates differ "
      f"({dict(sorted(daydiff.items()))}) - see the .md on why these are"
      f" suspect")
print()

theirs_b = [(t[0], "U" if t[1] == 6 else "A") for t in tw if t[2]]
matched = set()
print("intercalary months in ours (1942) with no match in the 1956-derived")
print("series (see collation_1956.md for the full comparison table):")
for r in inter:
    j, typ = int(r[0]), r[4][0]
    hit = [t for t in theirs_b if abs(t[0] - j) <= 3 and t[1] == typ]
    if hit:
        matched.add(hit[0])
    else:
        print(f"  {r[4]:9} jdn {j}  {r[2]} {r[3]}  confidence {r[6]}")
print()
print("intercalary months in the 1956-derived series with no match in ours:")
for t in theirs_b:
    if t not in matched:
        print(f"  {'Ululu II' if t[1] == 'U' else 'Addaru II':9} jdn {t[0]}")
print()
print(f"agreement: {len(matched)} of {len(inter)} intercalations")
