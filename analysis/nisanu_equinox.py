#!/usr/bin/env python
#
# Nisanu 1 and the March equinox, 626 BCE - AD 45.
#
# Tests the placement of the Babylonian new year against the equinox in
# each era, using the Parker & Dubberstein tables in this repository:
#
#   - the "full-moon rule": the full moon of Nisanu (mid-month) does not
#     fall before the equinox, so Nisanu 1 itself may;
#   - the "new-moon rule": Nisanu 1 itself does not fall before the equinox.
#
# Methods and precision:
#   - Equinox: mean March equinox (Meeus, Astronomical Algorithms, ch. 27,
#     valid -1000..+1000; periodic terms omitted, error under an hour),
#     converted from Terrestrial Time with Delta-T (Morrison & Stephenson
#     2004) and to Babylon local time (+2.96h). Good to well under a day.
#   - Nisanu 1: Parker & Dubberstein's computed first crescent visibility
#     (integer Julian day number). One day of model uncertainty.
#   - Full moon: midpoint of the bracketing conjunctions, good to ~0.4 days.
#   - Intercalation placement: years affected by P&D's low-confidence
#     intercalations (confidence 2-3 in intercalations.tsv) can shift by a
#     whole month; the robustness section excludes them.
#
# USAGE:  python analysis/nisanu_equinox.py

import bisect
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

ERAS = (
    ("Chaldean (626-539 BCE)", -625, -538),
    ("Cyrus to Darius I (538-486)", -537, -485),
    ("Xerxes to cycle era (485-384)", -484, -383),
    ("fixed 19-yr cycle (383-312)", -382, -311),
    ("Seleucid (311-141 BCE)", -310, -140),
    ("Arsacid (140 BCE-AD 45)", -139, 45),
)


def equinox_jd(year):
    """March equinox as a Julian day, Babylon local time.
    Years are astronomical (1 BCE is 0)."""
    Y = year / 1000.0
    jde = (1721139.29189 + 365242.13740 * Y + 0.06134 * Y**2
           + 0.00111 * Y**3 - 0.00071 * Y**4)
    delta_t = (-20 + 32 * ((year - 1820) / 100.0) ** 2) / 86400.0
    return jde - delta_t + 2.96 / 24.0


def from_jdn(jdn):
    """Julian day number to (year, month, day) in the Julian calendar."""
    c = jdn + 32082
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    return (d - 4800 + m // 10, m + 3 - 12 * (m // 10), e - (153 * m + 2) // 5 + 1)


def bce(year):
    return f"{1 - year} BCE" if year <= 0 else f"AD {year}"


tsv = list(csv.reader(open(f"{REPO}/parker_and_dubberstein.tsv"), delimiter="\t"))[1:]
moons = sorted(float(m) for m in open(f"{REPO}/new_moons_jdn.txt") if "#" not in m)
inter = list(csv.reader(open(f"{REPO}/intercalations.tsv"), delimiter="\t"))[1:]

years = []      # (nisanu_year, nisanu1 - equinox, fullmoon - equinox, jdn)
for r in tsv:
    if r[4] != "1":
        continue
    jdn, year, conj = int(r[0]), int(r[1]), float(r[7])
    eq = equinox_jd(year)
    full = (conj + moons[bisect.bisect(moons, conj + 1)]) / 2.0
    years.append((year, jdn - eq, full - eq, jdn))

# Years whose Nisanu could shift a month if a low-confidence intercalation
# is misplaced: the flagged year and the year after it.
shaky = set()
for r in inter:
    if int(r[6]) <= 3:
        shaky.update((int(r[1]), int(r[1]) + 1))


def summarize(rows, title):
    print(title)
    print(f"  {'era':30} {'n':>4} {'Nisanu1 - equinox':>19} {'<0':>4}"
          f" {'fullmoon - equinox':>20} {'<0':>4}")
    for name, a, b in ERAS:
        d = [x for x in rows if a <= x[0] <= b]
        if not d:
            continue
        d1 = [x[1] for x in d]
        d15 = [x[2] for x in d]
        print(f"  {name:30} {len(d):4} {min(d1):+7.1f} to {max(d1):+6.1f}"
              f" {sum(v < 0 for v in d1):4} {min(d15):+8.1f} to {max(d15):+6.1f}"
              f" {sum(v < 0 for v in d15):4}")
    print()


print("NISANU 1 AND THE MARCH EQUINOX (positive = after the equinox, days)")
print("=" * 70)
print()
summarize(years, "All 671 years:")
summarize([x for x in years if x[0] not in shaky],
          "Excluding years within reach of a low-confidence intercalation:")

print("Breaches (full moon before equinox, or Nisanu 1 > 10 days early),")
print("with the corrective intercalation of the same Babylonian year:")
for year, d1, d15, jdn in years:
    if d15 < 0 or d1 < -10:
        y, m, d = from_jdn(jdn)
        fix = [r for r in inter if int(r[1]) == year]
        note = (f"{fix[0][4]} that year, confidence {fix[0][6]} ({fix[0][7]})"
                if fix else "no intercalation that year")
        print(f"  {bce(year):>8}: Nisanu 1 = {m}/{d}, {d1:+5.1f} d;"
              f" full moon {d15:+5.1f} d -> {note}")
print()

print("Floor and ceiling of (Nisanu 1 - equinox) per half-century:")
for start in range(-625, 46, 50):
    d = [x[1] for x in years if start <= x[0] < start + 50]
    if d:
        lo, hi = min(d), max(d)
        bar = " " * int(lo + 17) + "#" * max(1, int(hi - lo))
        print(f"  {bce(start):>8} .. {bce(min(start + 49, 45)):>8}"
              f"  {lo:+6.1f} .. {hi:+6.1f}  |{bar}")
print()

last = max((x for x in years if x[1] < -2), key=lambda x: x[0])
print(f"Last year with Nisanu 1 more than 2 days before the equinox: {bce(last[0])}.")
print("After the fixed cycle the floor rises ~0.5 day/century: the Metonic")
print("year (365.2467 d) is longer than the tropical year, so a frozen cycle")
print("drifts late against the equinox once observation stops correcting it.")
