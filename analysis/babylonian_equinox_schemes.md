# Babylon's own equinox: the two native schemes

The analysis in `nisanu_equinox.py` measures the calendar against the
astronomical (true) March equinox. The Babylonians, however, worked with
their own normative dates for the equinox, and any claim about the
*intent* of intercalation should also be tested against those. Two native
schemes cover the span of Parker and Dubberstein's tables.

## 1. The MUL.APIN ideal calendar (early first millennium BCE)

The astronomical compendium MUL.APIN (compiled from older material by
about 700 BCE) uses a schematic year of 12 months of 30 days and places
the cardinal points of the sun's year on the 15th of the equinoctial and
solstitial months:

    vernal equinox    Nisanu 15   (month I)
    summer solstice   Duzu 15     (month IV)
    autumnal equinox  Tashritu 15 (month VII)
    winter solstice   Tebetu 15   (month X)

This is an ideal, not an ephemeris: it states where in the calendar the
equinox *ought* to fall. Read as a bound on intercalation, it means the
vernal equinox should come no later than the middle of Nisanu - that is,
on or before the full moon of Nisanu. That is precisely the "full-moon
rule" that `nisanu_equinox.py` finds operating through the reign of
Darius I (in practice the equinox usually sat earlier, in the last month
of the old year; Nisanu 15 was the limit, not the target).

Source: Hunger and Pingree, _MUL.APIN: An Astronomical Compendium in
Cuneiform_ (1989); tablet II discusses the intercalation rules built on
the scheme.

## 2. The Uruk scheme (Seleucid period, roots in the 5th century BCE)

Late Babylonian astronomical texts (diaries, almanacs, and the Uruk
solstice tables) list *predicted* dates for solstices, equinoxes, and the
Sirius phenomena from a fixed arithmetic scheme, the "Uruk scheme":

- Year 1 of its 19-year cycle is year 1 of the Seleucid Era (311 BCE);
  cycle year = ((SE - 1) mod 19) + 1.
- Successive summer solstices are separated by 12 months + 11;3,10 tithis
  (a tithi is 1/30 of a synodic month, about 0.984 days; dates written in
  tithis differ from civil dates by at most about a day).
- The other cardinal points follow by successive addition of 3 months +
  3 tithis (the scheme uses equal seasons for calendrical purposes even
  though Babylonian astronomers knew the seasons are unequal).
- The scheme presupposes the standardized intercalations: cycle years
  1, 4, 7, 9, 12, 15 take an Addaru II and cycle year 18 an Ululu II -
  the same pattern our tables show throughout the Seleucid era.

The vernal equinox dates implied by the scheme, per cycle year (derived
from the scheme table; "preceding" means the equinox falls in the last
month of the preceding Babylonian year):

    cycle  1: Addaru 27, preceding      cycle 11: Addaru 17, preceding
    cycle  2: Addaru II 8, preceding    cycle 12: Addaru 28, preceding
    cycle  3: Addaru 19, preceding      cycle 13: Addaru II 9, preceding
    cycle  4: Addaru 30, preceding      cycle 14: Addaru 20, preceding
    cycle  5: Addaru II 11, preceding   cycle 15: Nisanu 1
    cycle  6: Addaru 22, preceding      cycle 16: Addaru II 12, preceding
    cycle  7: Nisanu 3                  cycle 17: Addaru 23, preceding
    cycle  8: Addaru II 14, preceding   cycle 18: Nisanu 4
    cycle  9: Addaru 25, preceding      cycle 19: Addaru 16, preceding
    cycle 10: Addaru II 6, preceding

The scheme therefore *encodes* the late rule, and it is one-sided: the
vernal equinox falls no later than Nisanu 4, so Nisanu 1 never precedes
the scheme's equinox by more than about 3 tithis. In the other direction
Nisanu 1 may trail the equinox by up to about 25 tithis - the intercalary
years place the equinox as early as the 6th of an Addaru II, since the
inserted month pushes the new year late.

Sources: O. Neugebauer, "A Table of Solstices from Uruk", JCS 1 (1947)
143-148, and "Solstices and Equinoxes in Babylonian Astronomy during the
Seleucid Period", JCS 2 (1948) 209-222; J. P. Britton, "Calendars,
Intercalations and Year-Lengths in Mesopotamian Astronomy", in J. M.
Steele (ed.), _Calendars and Years_ (2007) 115-132, which reconstructs
the scheme's 5th-century precursors; the scheme table is conveniently
tabulated by R. H. van Gent,
https://webspace.science.uu.nl/~gent0113/babylon/babycal_seasons.htm

## Caveats

- The Uruk scheme is directly attested only in Seleucid-period texts.
  `scheme_equinox.py` applies it to every year in which the standardized
  intercalation cycle demonstrably holds in the tables, and reports from
  which year that is; earlier application would be anachronistic.
- Scheme dates are in tithis, civil dates in days: allow one day of slack.
- The scheme's equinox is arithmetic, not observed, and drifts slowly
  against the true equinox (the script measures this drift).
