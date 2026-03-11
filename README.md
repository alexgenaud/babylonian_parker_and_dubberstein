# Parker and Dubberstein's Babylonian Chronology

In _Babylonian Chronology 626 B.C.-A.D. 45_, Richard Parker and Waldo
Dubberstein published tables of the calculated dates of visible new moons
across nearly seven centuries, together with the Babylonian months and years
each new moon began, and the intercalary months inserted to keep the
[lunisolar calendar](https://en.wikipedia.org/wiki/Babylonian_calendar)
aligned with the seasons.

A Babylonian month began when the first waxing crescent became visible to the
eye, one to a few days after the astronomical new moon (the
[conjunction](<https://en.wikipedia.org/wiki/Conjunction_(astronomy)>) of Sun
and Moon). The Babylonian calendar shaped many calendars of the ancient
Mediterranean -- including [Greek](https://github.com/seanredmond/heniautos),
Jewish, and Islamic calendars -- and Parker and Dubberstein's tables remain a
standard reference for dating ancient Near Eastern documents and astronomical
records.

This repository provides those tables in machine-readable form. It is a fork
of [Sean Redmond's transcription](https://github.com/seanredmond/parker_and_dubberstein),
realigned and with five corrections described below.

## Files

| file                             | description                                                                        |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| `parker_and_dubberstein.raw.txt` | The tables (pp. 25-46 of the original) as aligned plain text                        |
| `parker_and_dubberstein.tsv`     | The same data as tab-separated values, one row per Babylonian month                 |
| `new_moons_jdn.txt`              | Julian days of the astronomical new moons (conjunctions) covering the whole period |
| `parse_pdubs.py`                 | Script that builds the `.tsv` from the plain-text tables                            |
| `parker_and_dubberstein.sql`     | `CREATE TABLE` statement for importing the `.tsv` into a database                   |

## The plain-text tables

Kings' names introduce each reign. Every other line is one Babylonian year:

    004 622 03/22 04/20 05/20 06/19 07/18 08/17 09/15    10/15 11/14 12/13 01/12 02/11 03/11

- The first column is the year of the king's reign (later, of the Seleucid
  Era).
- The second column is the Julian year in which the Babylonian year began:
  counting down through the BCE years, then up again from 1 CE. The year of
  each following date is implied -- it advances at the December to January
  rollover midway through the line.
- The remaining columns are the Julian `month/day` dates of the visible new
  moons, i.e. the first day of each Babylonian month.
- The wide gap divides the year into its two halves: Nisanu, Aiaru, Simanu,
  Duzu, Abu, Ululu before it; Tashritu, Arahsamnu, Kislimu, Tebetu, Shabatu,
  Addaru after it. A **seventh** date in the first half is an intercalary
  second Ululu (Ululu II); a seventh date in the second half is a second Addaru
  (Addaru II). In the example above, 09/15 is an Ululu II.

### A note on intercalary months

The intercalary month was a repetition of its namesake: the year ran Ululu,
"second Ululu" (Akkadian Ululu shanu, written ITI.KIN.2.KAM), then Tashritu;
or ended Addaru, "second Addaru" (Addaru shanu, also written with DIRI,
"extra"). The doubled month normally _followed_ the regular one, and the
second occurrence carried the mark. The practice was not perfectly uniform:
a few Neo-Babylonian texts attest an inserted Addaru _before_ the regular
Addaru (San Nicolo 1933; Kleber 2008; cf. Csabai, _Hungarian Assyriological
Review_ 1, 2020), though by the Achaemenid period the intercalary Addaru
always followed (Ossendrijver 2018). Parker and Dubberstein note (pp. 3-6)
an early preference for doubling Ululu, shifting toward Addaru until the
standardized 19-year cycle (4th century BCE onward) used a second Addaru in
six of its seven intercalations and a second Ululu in one fixed year.

## What was changed, and why

In the printed tables, the column a date is printed in _is_ data: it
determines the month's name and whether the year has an intercalary month.
The transcription this repository was forked from had ragged, inconsistent
spacing, and in five years a date had drifted to the wrong side of the
half-year divide. Two of those years became internally impossible (twelve
months with no Ululu, yet ending in an intercalary Addaru II), and three were
assigned the wrong intercalary month (Ululu II instead of Addaru II).

The text was therefore realigned into fixed columns -- zero-padded dates,
three-digit regnal years, one consistent gap between the half-years, and the
repeated mid-line Julian year removed -- so that every date stands in the
column that names it, and the five misplaced dates were restored to the
columns where Parker and Dubberstein printed them:

| Babylonian year | king              | was                       | now                   |
| --------------- | ----------------- | ------------------------- | --------------------- |
| 583/582 BCE     | Nebuchadnezzar 22 | months misnamed, no Ululu | regular 12-month year |
| 582/581 BCE     | Nebuchadnezzar 23 | intercalary Ululu II      | intercalary Addaru II |
| 581/580 BCE     | Nebuchadnezzar 24 | months misnamed, no Ululu | regular 12-month year |
| 572/571 BCE     | Nebuchadnezzar 33 | intercalary Ululu II      | intercalary Addaru II |
| 553/552 BCE     | Nabonidus 3       | intercalary Ululu II      | intercalary Addaru II |

Each correction was verified against the scan of the original publication
(pp. 26-27): in all five years the Ululu II column is empty there, and in the
three intercalary years the final date stands in the Addaru II column.
Nebuchadnezzar 23's Addaru II is further confirmed by Parker and Dubberstein's
own list of intercalary months attested in cuneiform texts (p. 4: "Addaru II,
23d year"). The regenerated `.tsv` differs from the earlier version only in
the month names and numbers of these five years; every date, Julian day
number, and conjunction is unchanged.

## The TSV

`parker_and_dubberstein.tsv` contains one row per Babylonian month, with 9
tab-delimited columns:

| Field        | Explanation                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| jdn          | [Julian day number](https://en.wikipedia.org/wiki/Julian_day) of the visible new moon beginning the month |
| julian_year  | The Julian year; BCE is negative, and 1 BCE is 0                                                        |
| julian_month | The number of the Julian month (1-12)                                                                   |
| julian_day   | The Julian day of the month                                                                             |
| month_number | The number of the month (1-13) in the Babylonian year                                                   |
| month_name   | The Babylonian month; intercalated months are "Ululu II" and "Addaru II"                                |
| month_days   | Days elapsed since the preceding visible new moon                                                       |
| new_moon     | The exact Julian day of the conjunction (astronomical new moon)                                         |
| diff         | Days between the conjunction and the visible new moon                                                   |

For example, the row `1494495  -621  9  15  7  Ululu II  29  1494492.926628183
2.073371816892177` means: September 15, 622 BCE (Julian day 1494495) was a
visible new moon, beginning the 7th month of the Babylonian year, an
intercalated Ululu, 2.07 days after the conjunction.

To regenerate the TSV from the plain-text tables:

    python parse_pdubs.py < parker_and_dubberstein.raw.txt > parker_and_dubberstein.tsv

To import it into a Sqlite3 database:

    > sqlite3 your_database.db
    sqlite> .read parker_and_dubberstein.sql
    sqlite> .mode tabs
    sqlite> .import parker_and_dubberstein.tsv parker_and_dubberstein

## Sources and credits

All of the data is the work of Parker and Dubberstein:

> Parker, Richard A., and Waldo H. Dubberstein. 1942. _Babylonian Chronology
> 626 B.C.-A.D. 45._ Studies in Ancient Oriental Civilization 24. Chicago:
> The University of Chicago Press.

The original can be downloaded from the [Institute for the Study of Ancient
Cultures, University of Chicago](https://isac.uchicago.edu/sites/default/files/uploads/shared/docs/saoc24.pdf),
whose scan was also used to verify the corrections above.

The transcription and machine-readable conversion were pioneered by Sean
Redmond in [seanredmond/parker_and_dubberstein](https://github.com/seanredmond/parker_and_dubberstein),
from which this repository is forked with gratitude.
