# Collation against the 1956 edition (via a third-party transcription)

Parker and Dubberstein revised their chronology in 1956 (_Babylonian
Chronology 626 B.C.-A.D. 75_, Brown University Press; reprinted 1971),
extending the tables to AD 75 and revising some of the reconstructed
intercalations. This repository transcribes the 1942 edition, so the
differences matter.

## Source and its limits

No open scan of the 1956 edition is available (archive.org holds a
lending-restricted copy). As a first pass, `collation_1956.py` collates
our tables against a complete third-party transcription of the 1971
printing published at bible.ca ("Babylon Chronology by Parker and
Dubberstein 1971 AD"). That transcription is unreviewed, its method is
undocumented (it may derive in part from a modern converter rather than
the printed book), and the site has an apologetic agenda. Every
difference below is therefore a *candidate* 1956 revision, to be
verified against the printed 1956/1971 edition before use. The
archive.org copy can be borrowed page by page for exactly that.

## Findings

Both series contain the same 8,299 lunations over 626 BCE - AD 45, and
237 of our 247 intercalary months agree in place and type. The ten
differences, with our attestation grades from `intercalations.tsv`:

| ours (1942)                          | conf | theirs (1956-derived)         | P&D 1942 already said (p. 7)          |
| ------------------------------------ | ---- | ----------------------------- | ------------------------------------- |
| Addaru II, Nabopolassar 1 (625/4)    | 2    | Addaru II one year later      | "a is probable, u possible"           |
| Ululu II, Nabopolassar 4 (622/1)     | 3    | Ululu II one year later       | "u and year are very probable"        |
| Ululu II, Nabopolassar 7 (619/8)     | 5    | Addaru II, same year          | attested (GCCI II 74, "damaged")      |
| Ululu II, Nabopolassar 12 (614/3)    | 2    | Addaru II, same year          | "u is probable, a possible"           |
| Ululu II, Nabopolassar 17 (609/8)    | 2    | Ululu II two years later      | "u probable, a this/preceding year"   |
| Addaru II, Nebuchadnezzar 4 (601/0)  | 5    | Ululu II, following year      | attested (VAS VI 265, broken text)    |
| Ululu II, Nebuchadnezzar 12 (593/2)  | 3    | Addaru II, preceding year     | "u and year are very probable"        |
| Addaru II, Xerxes 5 (481/0)          | 5    | Addaru II one year earlier    | attested (Teheran PT 4 996)           |
| Ululu II, Artaxerxes I 19 (446/5)    | 4    | Addaru II, same year          | unattested, "highly probable"         |
| Ululu II, Artaxerxes I 38 (427/6)    | 4    | Addaru II, same year          | unattested, "highly probable"         |

Reading of the pattern:

- Seven of the ten fall on years we graded 2-4 (reconstructed), and
  several are exactly the alternative P&D's own 1942 notes offered.
  These look like genuine 1956 revisions, presumably on new evidence or
  reconsideration.
- Three fall on years graded 5 (attested by a dated tablet in 1942).
  Either the 1956 edition re-read those tablets (the Nabopolassar 7 and
  Nebuchadnezzar 4 attestations were both explicitly flagged as damaged
  or disputed in 1942), or the third-party transcription is wrong
  there. These three are the priority for verification, and the
  Xerxes 5 case matters for the Achaemenid cycle chronology
  (cf. Ossendrijver 2018).
- All ten predate 384 BCE except none - every intercalation from the
  fixed 19-year cycle onward agrees exactly.

At the day level the two series differ in 2,155 of 8,299 dates (26%),
almost all by one day (1,281 later, 870 earlier, 4 two days earlier).
This is too many to be printing corrections and does not match the
profile of a modern recomputation either (van Gent's modern check moves
7.8% of dates, mostly earlier). Until the day columns of the printed
1956 edition are inspected, the day-level comparison should be treated
as unresolved and the third-party day values as suspect.

## Verification protocol

1. Borrow the 1956/1971 edition (archive.org, item
   babylonianchrono0000park) or obtain it via a library.
2. Check the ten intercalation rows above against the printed tables;
   record each as "1956 revision" or "transcription error".
3. Spot-check about twenty day-level differences across the span to
   determine whether the printed 1956 day columns were recomputed.
4. Fold confirmed revisions into `intercalations.tsv` as additional
   evidence lines (do not overwrite the 1942 readings; this repository
   transcribes 1942 and annotates).
