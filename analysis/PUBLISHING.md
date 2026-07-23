# Publication plan and open tasks

Companion to `READING.md` (what to read) - this file records where and
how to publish, the error budget any paper must state, and what remains
to be done.

## What is publishable

1. **The dataset** (solid): corrected machine-readable P&D with the
   attestation-graded `intercalations.tsv` - no equivalent exists
   openly. Publishable as a data/resource paper regardless of anything
   else.
2. **The replication** (solid): open-code confirmation and sharpening
   of published claims - Britton's equinox rule (0 violations of the
   Uruk-scheme band in 427 years), the scheme's +4 to +6 day lateness,
   the 383 BCE cycle lock, attestation-weighted robustness.
3. **The early full-moon rule** (contingent): the formulation "the full
   moon of Nisanu does not precede the equinox, enforced by attested
   catch-up Ululu IIs (616, 564, 537 BCE)" is publishable as a claim
   ONLY if the Britton 2007 / Stern 2012 reading (READING.md items 1-2)
   confirms nobody has stated it in this form, and after engaging the
   barley-harvest alternative. Otherwise fold it into (2) as a
   replication.

## Venues

- **Centaurus** (European Society for the History of Science; founded
  Copenhagen 1950, the closest thing to a Nordic home venue). Diamond
  open access since 2022: no author fees, no reader fees, double-blind
  peer review. History of exact sciences in scope. First choice.
- **ISAW Papers** (NYU): diamond OA, ancient exact sciences. Strong
  alternative.
- **Journal for the History of Astronomy** (SAGE): traditional, no fee
  to publish (OA optional at cost).
- **Journal of Open Humanities Data**: dataset-paper format, APC in the
  few-hundred-GBP range - only if the dataset-paper framing is chosen.
- **Hungarian Assyriological Review**: diamond OA Assyriology venue.
- Norwegian-language outreach afterward: Naturen (UiB) or Astronomi
  (Norsk Astronomisk Selskap).

No university affiliation is required anywhere above; sign as
independent researcher. Get an ORCID (free).

## Mechanics, in order

1. Make the repository public; confirm LICENSE.md and CITATION.cff
   render.
2. Wire the GitHub repo to Zenodo; cut a v1.0 release -> DOI. The
   dataset is citable from that moment.
3. Complete the verification tasks below; read per READING.md.
4. Draft; post a preprint (Zenodo or arXiv physics.hist-ph, which may
   need an endorser).
5. Friendly review: short notes with the repo link to Steele,
   Ossendrijver, and/or Stern (contacts in READING.md); courtesy
   issue/PR to Sean Redmond with the five transcription corrections.
6. Submit once, to Centaurus first.

Costs: $0 on this path. Time is the only spend.

## Error budget (numbers any paper must state)

- **Month identity, sequence, intercalation**: exact where attested;
  see `intercalations.tsv` grades. From 383 BCE the cycle is exact.
  Ten pre-383 placements are disputed between editions
  (`collation_cases.md`).
- **Day level**: P&D's days are COMPUTED first visibility (Schoch
  1928). Van Gent's recomputation (modern ephemerides + Yallop) moves
  680 of 8,670 lunations (7.84%), 583 earlier / 95 later
  (https://webspace.science.uu.nl/~gent0113/babylon/babycal_converter.htm).
  Real (observed) month starts occasionally differ from any
  computation (weather; the 30-day cap limits drift to one day).
  Practical rule: unanchored dates correct with ~85-90% probability,
  else off by one day.
- **Astronomically anchored dates are exact**: eclipse texts and
  diaries (e.g. VAT 4956, Nebuchadnezzar 37 = 568/7 BCE) pin those
  months to the day, and a documented 29/30-day chain around an anchor
  is day-exact throughout.
- **Month-scale windows**: in the confidence-2 years P&D themselves
  say whole spans "might be a month later/earlier" - the windows are
  quoted in `intercalations.tsv`. Exclude or sensitivity-test them.
- **Equinox computation** (our analyses): Meeus mean equinox, Delta-T
  per Morrison & Stephenson 2004, Babylon local - good to well under a
  day. The Uruk-scheme comparison adds ~1 day of tithi-to-civil-day
  slack.

## Open tasks

1. **Verify the ten disputed intercalations** against the printed
   1956/1971 edition (protocol in `collation_1956.md`; case analyses
   in `collation_cases.md`). Settles transcription-vs-revision.
2. **Read the gatekeepers** (READING.md items 1-2) to fix the
   replication/novelty line for the full-moon rule.
3. **Attested-only robustness run**: repeat nisanu_equinox.py's era
   table using only years adjacent to confidence-5 intercalations, as
   the strongest answer to the circularity objection.
4. **Per-day visibility probabilities** (planned "#3"): for each month
   start, modern first-visibility computation with probabilities for
   the surrounding days (e.g. Skyfield + Yallop criterion), as a
   separate companion file. Quantifies the day-level budget above per
   month instead of in aggregate.
5. **Fold verified 1956 revisions into `intercalations.tsv`** as
   added evidence lines - annotate, never overwrite the 1942 readings.
6. **Upstream courtesy PR** with the five corrections (see README,
   "What was changed, and why").
