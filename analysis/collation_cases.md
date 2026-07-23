# The ten disputed intercalations: a case-by-case dossier

The ten differences between our tables (P&D 1942, verified against the
scan) and the third-party transcription of the 1956/1971 edition (see
`collation_1956.md`). None of the ten has been adjudicated - by us or,
to our knowledge, by any publication that compares the two editions row
by row. Each is either a genuine 1942-to-1956 revision or an error in
the third-party transcription; only the printed 1956 book (and, for
some, the tablets themselves or later scholarship) can decide.

`collation_cases.py` prints, for every case, the surrounding years'
Nisanu dates and their equinox geometry under both variants (output in
`collation_cases.txt`). The early-era operating rule - the full moon of
Nisanu does not precede the equinox - can then favor or disfavor a
variant. **Caution: circularity.** P&D 1942 reconstructed the
unattested intercalations partly to satisfy their own equinox
expectations, so "geometry favors 1942" partly restates their
assumptions. Treat the geometry as a hypothesis generator; documents
decide.

Two structural observations first:

- Four cases (3, 4, 9, 10) change only the TYPE within the same year
  (Ululu II versus Addaru II). No year boundary moves, so equinox
  geometry cannot discriminate at all; only texts can.
- Six cases (1, 2, 5, 6, 7, 8) move the intercalation across a year
  boundary, shifting one year's Nisanu by a whole month - these the
  geometry can judge.

## Case 1 - Nabopolassar 1 (625/4 BCE). 1942: Addaru II; variant: one year later

- 1942 note (p. 7): "a is probable, u possible, year very probable."
  The variant is a year P&D considered movable.
- Geometry: the variant puts Nisanu of 624 BCE at March 14, full moon
  0.9 days BEFORE the equinox - a (marginal) violation of the era's
  rule. The 1942 arrangement violates nothing.
- Hypothesis: 1942 reading stands; verify in the book.

## Case 2 - Nabopolassar 4 (622/1 BCE). 1942: Ululu II; variant: one year later

- 1942 note: "u and year are very probable."
- Geometry: variant puts Nisanu of 621 BCE at March 11, full moon 3.4
  days before the equinox - violation. 1942 arrangement clean.
- Hypothesis: as case 1.

## Case 3 - Nabopolassar 7 (619/8 BCE). 1942: Ululu II (ATTESTED); variant: Addaru II, same year

- 1942 evidence: Dougherty GCCI II 74, "month name somewhat damaged
  but certain because of KAM that follows" (p. 4).
- Type-only change: geometry silent.
- Hypothesis: the damaged reading is exactly the kind a 1956 revision
  OR a transcription slip could touch. Check the book first, then the
  tablet literature.

## Case 4 - Nabopolassar 12 (614/3 BCE). 1942: Ululu II; variant: Addaru II, same year

- 1942 note: "u is probable, a possible" - the variant IS P&D's own
  stated alternative. Type-only; geometry silent.
- Hypothesis: plausibly a genuine 1956 revision.

## Case 5 - Nabopolassar 17 (609/8 BCE). 1942: Ululu II; variant: Ululu II two years later

- 1942 note: "u is probable, a in this or the preceding year
  possible." The variant (TWO years later) is NOT among P&D's stated
  alternatives.
- Geometry: the variant is the worst of all ten - Nisanu of 606 BCE
  lands March 6, full moon 8.6 days before the equinox.
- Hypothesis: transcription error in the third-party source. Highest
  priority for checking against the book.

## Case 6 - Nebuchadnezzar 4 (601/0 BCE). 1942: Addaru II (ATTESTED); variant: Ululu II, following year

- 1942 evidence: VAS VI 265, a broken text assigned to Nebuchadnezzar
  by elimination (p. 4 n. 10 - P&D themselves list the other candidate
  kings).
- Geometry: BOTH variants satisfy the full-moon rule; cannot decide.
- Hypothesis: genuinely open. If 1956 re-assigned the broken text,
  this is a real revision; the footnote's own hedging makes that
  credible. A good case for deeper tablet-literature work.

## Case 7 - Nebuchadnezzar 12 (593/2 BCE). 1942: Ululu II; variant: Addaru II, preceding year

- 1942 note: "u and year are very probable."
- Geometry: the variant makes Nisanu of 592 BCE fall on April 30 -
  N1-eq +34.1, later than any New Year in the entire 671-year series
  (ceiling elsewhere about +30). Disfavored, though not impossible.
- Hypothesis: leans transcription error; check the book.

## Case 8 - Xerxes 5 (481/0 BCE). 1942: Addaru II (ATTESTED); variant: same, one year earlier (Xerxes 4)

- 1942 evidence: unpublished Persepolis text PT 4 996 (Cameron). Note
  p. 4 n. 10 also remarks that "the newly discovered intercalation
  dated to Xerxes' 5th year practically rules his 4th year out" - for a
  different text, but showing the 4-vs-5 question was already live in
  1942.
- Geometry: both variants admissible (the 1942 reading has Nisanu of
  480 BCE 3 days before the true equinox, tolerable in the
  transitional era).
- Hypothesis: decidable from Ossendrijver 2018 (open access), which
  reconstructs exactly this stretch. Check there first; this is also
  the case with the most bearing on Achaemenid cycle chronology.

## Case 9 - Artaxerxes I 19 (446/5 BCE). 1942: Ululu II; variant: Addaru II, same year

- Unattested in 1942 ("highly probable" class). Type-only; geometry
  silent.
- CAUTION: 446/5 sits next to the biblically sensitive Artaxerxes 20
  (Nehemiah chronology), and the third-party source has an apologetic
  agenda. A transcription bias here would not be surprising; equally,
  a genuine 1956 revision is possible. Verify with unusual care.

## Case 10 - Artaxerxes I 38 (427/6 BCE). 1942: Ululu II; variant: Addaru II, same year

- Unattested in 1942. Type-only; geometry silent. As case 9, minus the
  sensitivity.

## Suggested order of attack

1. Borrow the 1956/1971 book (archive.org) and check all ten rows -
   settles the transcription-vs-revision question wholesale.
2. Read Ossendrijver 2018 for case 8 (and the Xerxes-era sequence
   generally).
3. For whichever of cases 3, 6 survive as real revisions, chase the
   tablet literature (GCCI II 74; VAS VI 265) forward from 1942 -
   later editions or collations of those tablets may exist.
4. Record every verdict as an evidence line in `intercalations.tsv`
   (annotate, never overwrite the 1942 reading).
