#!/usr/bin/env python
#
# Builds parker_and_dubberstein.tsv from the aligned plain-text
# transcription of Parker and Dubberstein's tables.
#
# Each data line in the input is one Babylonian year:
#
#   regnal (or Seleucid Era) year, Julian year, then the Julian dates
#   (month/day) of each visible new moon. A run of two or more spaces
#   separates the two halves of the year: Nisanu-Ululu (+ Ululu II)
#   and Tashritu-Addaru (+ Addaru II). A seventh date in a half marks
#   the intercalary month.
#
# The Julian year is listed once per line; it decreases through the
# BCE years and increases from 1 CE. The year of each individual date
# is inferred from the December-to-January rollover mid-line.
#
# USAGE:
#     python parse_pdubs.py < parker_and_dubberstein.raw.txt > parker_and_dubberstein.tsv

import bisect
import csv
import re
import sys

MAX_DIFF = 5.0

MONTHS = (
    ("Nisanu", "Aiaru", "Simanu", "Duzu", "Abu", "Ululu", "Ululu II"),
    ("Tashritu", "Arahsamnu", "Kislimu", "Tebetu", "Shabatu", "Addaru", "Addaru II"),
)


class ParseError(Exception):
    pass


def to_jdn(year, month, day):
    """Julian day number of a (proleptic) Julian calendar date.
    BCE years are astronomical: 1 BCE is 0, 2 BCE is -1, etc."""
    a = int((14 - month) / 12)
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + int((153 * m + 2) / 5) + y * 365 + int(y / 4) - 32083


def nearest_new_moon(jdn, new_moons):
    i = bisect.bisect(new_moons, jdn)
    return min(new_moons[max(i - 1, 0):i + 1], key=lambda n: abs(jdn - n))


def check_year_label(label, year):
    """The Julian year printed on the line, checked against the year
    inferred from counting months. Labels have no sign or era: 626 is
    626 BCE (astronomical -625) on the way down, 45 is 45 CE at the end."""
    expected = 1 - year if year <= 0 else year
    if label != expected:
        raise ParseError(f"Year label {label} does not match inferred year {expected}")


def parse_year(line, year, last_month, last_jdn, new_moons):
    halves = re.split(r"\s{2,}", line)
    if len(halves) != 2:
        raise ParseError(f"Expected two half-years, got {len(halves)}")

    dates = [tuple(int(n) for n in d.split("/")) for d in " ".join(halves).split(" ")[2:]]
    counts = (len(halves[0].split(" ")) - 2, len(halves[1].split(" ")))

    if sorted(counts) not in ([6, 6], [6, 7]):
        raise ParseError(f"Impossible half-year month counts: {counts}")

    names = MONTHS[0][:counts[0]] + MONTHS[1][:counts[1]]

    rows = []
    for number, (name, (month, day)) in enumerate(zip(names, dates), 1):
        if month < last_month:
            year += 1
        if number == 1:
            check_year_label(int(line.split(" ")[1]), year)

        jdn = to_jdn(year, month, day)
        if jdn - last_jdn not in (28, 29, 30, 31):
            raise ParseError(f"{jdn - last_jdn} days between {last_jdn} and {jdn}")

        nearest = nearest_new_moon(jdn, new_moons)
        if jdn - nearest > MAX_DIFF:
            raise ParseError(f"No conjunction within {MAX_DIFF} days of {jdn}")

        rows.append((jdn, year, month, day, number, name, jdn - last_jdn, nearest, jdn - nearest))
        last_month, last_jdn = month, jdn

    return rows, year, last_month, last_jdn


with open("new_moons_jdn.txt") as nm:
    new_moons = sorted(float(m) for m in nm if "#" not in m)

year, last_month, last_jdn = -625, 0, 1492841

writer = csv.writer(
    sys.stdout, delimiter="\t", quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n"
)
writer.writerow(
    ("jdn", "julian_year", "julian_month", "julian_day", "month_number",
     "month_name", "month_days", "new_moon", "diff")
)

for n, line in enumerate(sys.stdin, 1):
    line = line.strip()
    if not line or not line[0].isdigit():
        continue  # blank lines, comments, and kings' names
    try:
        rows, year, last_month, last_jdn = parse_year(
            line, year, last_month, last_jdn, new_moons
        )
    except ParseError as e:
        sys.exit(f"line {n}: {line}\n{e}")
    writer.writerows(rows)
