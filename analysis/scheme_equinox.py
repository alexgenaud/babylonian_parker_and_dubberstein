#!/usr/bin/env python
#
# Tests the calendar against Babylon's own equinox schemes, documented in
# babylonian_equinox_schemes.md:
#
#   1. Where does the TRUE (astronomical) equinox fall in the Babylonian
#      calendar, era by era?  MUL.APIN's ideal puts it at Nisanu 15; the
#      Uruk scheme puts it between the 16th of the last month of the year
#      and Nisanu 4.  This shows the norm tightening over time.
#   2. From the year the standardized 19-year cycle demonstrably holds,
#      convert the Uruk scheme's vernal equinox to a Julian day and
#      measure (a) Nisanu 1 against it and (b) its drift against the
#      true equinox.
#
# USAGE:  python analysis/scheme_equinox.py

import bisect
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def equinox_jd(year):
    """True March equinox as a Julian day, Babylon local time (Meeus mean
    equinox, Delta-T per Morrison & Stephenson 2004)."""
    Y = year / 1000.0
    jde = (1721139.29189 + 365242.13740 * Y + 0.06134 * Y**2
           + 0.00111 * Y**3 - 0.00071 * Y**4)
    delta_t = (-20 + 32 * ((year - 1820) / 100.0) ** 2) / 86400.0
    return jde - delta_t + 2.96 / 24.0


def bce(year):
    return f"{1 - year} BCE" if year <= 0 else f"AD {year}"


# Uruk scheme vernal equinox per cycle year: (month name, tithi, in
# preceding Babylonian year?).  Cycle year 1 = 1 SE; see the .md file.
SCHEME_VE = {
    1: ("Addaru", 27, True),    2: ("Addaru II", 8, True),
    3: ("Addaru", 19, True),    4: ("Addaru", 30, True),
    5: ("Addaru II", 11, True), 6: ("Addaru", 22, True),
    7: ("Nisanu", 3, False),    8: ("Addaru II", 14, True),
    9: ("Addaru", 25, True),    10: ("Addaru II", 6, True),
    11: ("Addaru", 17, True),   12: ("Addaru", 28, True),
    13: ("Addaru II", 9, True), 14: ("Addaru", 20, True),
    15: ("Nisanu", 1, False),   16: ("Addaru II", 12, True),
    17: ("Addaru", 23, True),   18: ("Nisanu", 4, False),
    19: ("Addaru", 16, True),
}
SCHEME_INTERCALARY = {1: "Addaru II", 4: "Addaru II", 7: "Addaru II",
                      9: "Addaru II", 12: "Addaru II", 15: "Addaru II",
                      18: "Ululu II"}


def cycle_year(nisanu_year):
    return (nisanu_year + 311 - 1) % 19 + 1     # SE 1 begins in -310


# Group the tables into Babylonian years: nisanu_year -> {month name: jdn}
tsv = list(csv.reader(open(f"{REPO}/parker_and_dubberstein.tsv"), delimiter="\t"))[1:]
years = {}
order = []
for r in tsv:
    if r[4] == "1":
        y = int(r[1])
        years[y] = {}
        order.append(y)
    years[y][r[5]] = int(r[0])

# From which year does the standardized cycle hold without interruption?
cycle_start = None
for y in order:
    expected = SCHEME_INTERCALARY.get(cycle_year(y))
    actual = ("Addaru II" if "Addaru II" in years[y]
              else "Ululu II" if "Ululu II" in years[y] else None)
    if expected != actual:
        cycle_start = None
    elif cycle_start is None:
        cycle_start = y

print("BABYLON'S OWN EQUINOX SCHEMES AGAINST THE TABLES")
print("=" * 70)
print()
print(f"The standardized 19-year cycle (Addaru II in cycle years 1, 4, 7,")
print(f"9, 12, 15, Ululu II in 18; cycle year 1 = 1 SE) holds without")
print(f"interruption from {bce(cycle_start)} to the end of the tables.")
print()

# 1. Where does the TRUE equinox fall in the Babylonian calendar?
BANDS = (
    ("earlier", lambda d: d > 30),
    ("last mo 1-15", lambda d: 15 < d <= 30),
    ("last mo 16-30", lambda d: 0 < d <= 15),
    ("Nisanu 1-4", lambda d: -4 < d <= 0),
    ("Nisanu 5-15", lambda d: -15 < d <= -4),
    ("after I 15", lambda d: d <= -15),
)
ERAS = (
    ("Chaldean (626-539 BCE)", -625, -538),
    ("Cyrus to Darius I (538-486)", -537, -485),
    ("Xerxes to cycle era (485-384)", -484, -383),
    (f"fixed cycle ({bce(cycle_start)}-)", cycle_start, 45),
)

print("1. The TRUE equinox's seat in the Babylonian calendar (percent of")
print("   years; MUL.APIN's ideal seat is Nisanu 15, the Uruk scheme's")
print("   runs from the 6th of the last month to Nisanu 4):")
print()
print(f"   {'era':30}" + "".join(f"{b[0]:>14}" for b in BANDS))
deltas = {y: years[y]["Nisanu"] - equinox_jd(y) for y in order}
for name, a, b in ERAS:
    ds = [deltas[y] for y in order if a <= y <= b]
    row = "".join(f"{100 * sum(f(d) for d in ds) / len(ds):13.0f}%" for _, f in BANDS)
    print(f"   {name:30}{row}")
print()
print("   (columns: equinox earlier ... later in the calendar year)")
print()

# 2. The Uruk scheme, applied where the cycle holds
rows = []
for y in order:
    if y < cycle_start:
        continue
    m, tithi, prev = SCHEME_VE[cycle_year(y)]
    src = years[order[order.index(y) - 1]] if prev else years[y]
    if m not in src:
        # the preceding year predates the fixed cycle; skip this one year
        continue
    ve_jdn = src[m] + tithi - 1
    rows.append((y, years[y]["Nisanu"] - ve_jdn, ve_jdn + 0.5 - equinox_jd(y)))

d1 = [r[1] for r in rows]
print(f"2. Nisanu 1 against the Uruk scheme's vernal equinox,")
print(f"   {bce(cycle_start)} - AD 45 ({len(rows)} years):")
print()
print(f"   Nisanu 1 - scheme equinox: {min(d1):+d} to {max(d1):+d} days;"
      f" {sum(v < -3 for v in d1)} years below -3,"
      f" {sum(v > 25 for v in d1)} years above +25.")
print(f"   The rule the scheme encodes is one-sided and the calendar")
print(f"   realizes it exactly: Nisanu 1 never precedes the scheme's")
print(f"   equinox by more than 3 days (the intercalary years trail it")
print(f"   by up to 25, the inserted month pushing the new year late).")
print()

print("3. Drift of the scheme's equinox against the TRUE equinox")
print("   (positive = scheme late; tithi-to-day conversion adds ~1 day of")
print("   noise):")
print()
for start in range(-375, 46, 50):
    ds = [r[2] for r in rows if start <= r[0] < start + 50]
    if ds:
        mean = sum(ds) / len(ds)
        print(f"   {bce(start):>8} .. {bce(min(start + 49, 45)):>8}: "
              f"mean {mean:+5.1f} d  (range {min(ds):+5.1f} .. {max(ds):+5.1f})")
print()
print("The scheme runs LATE against the true equinox for its whole")
print("attested life: about +4 days when the fixed cycle begins, growing")
print("~0.5 day per century (the Metonic year of 365.2467 d exceeds the")
print("tropical year) to about +6 days by the turn of the era. The")
print("calendar followed the scheme, not the sky: Nisanu 1 keeps its")
print("exact one-sided band around the scheme's equinox throughout,")
print("while both drift late together against the true equinox - which")
print("is why nisanu_equinox.py sees the calendar's floor above the true")
print("equinox slowly rising. Babylon's 'equinox rule' was kept, to the")
print("day, against Babylon's own computed equinox.")
