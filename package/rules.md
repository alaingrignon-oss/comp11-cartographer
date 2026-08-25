# Cartographer — rules

## 1. Coordinate grammar

- Grammar: `<territory>.<district>-<parcel>` — e.g., `ULT.OFR-001`.
- **Districts are immutable cadastral zones.** Ratified district codes never change
  meaning; evolving semantics are expressed through display names and cross-routes.
- **Parcels are append-only.** New nouns get new parcels; existing coordinates are
  never renumbered, compacted, or reused.
- Landmark names always display beside codes; humans never memorize IDs.
- Zoom levels: `Z0` catalog → `Z1` district → `Z2` card → `Z3` cited source.
- Source position is not a coordinate axis: current `path#heading` / `path#symbol` /
  optional `path:line` locators attach to the coordinate as mutable citations.

## 2. Reader journey contract

`workspace.md` (mandatory first read) → semantic catalog (`reference/catalog.md`) →
at most one card → that card's cited sources → stop.

- Never load sibling cards to answer one question.
- Never load the whole registry; only a task-specific resolution record if supplied.
- A card must let the reader answer without its siblings; if it cannot, that is an
  uncovered question and is reported, not hidden by adding cards silently.

## 3. Map-worthiness (a candidate gets a parcel only with ≥3 of these)

1. Referred to as a distinct thing in task language.
2. Owns meaningful state, contract, schema, or load-bearing behavior.
3. Can change independently of neighboring concepts.
4. Has useful, distinct Hits / Does not hit boundaries.
5. Spans several locations or has naming collisions that make path navigation unreliable.
6. A cold reader could ask "what is X?" or "what changes if I touch X?"

Exclusions: never coordinate files/pages/headings merely for structure; never
coordinate aspirations or duplicated names before live/leftover/ghost status is
verified; processes qualify only when they run and fit Input → Movement → Output.

## 4. Granularity rule

The map is the smallest set of coordinates that passes a declared set of cold-reader
questions. A maximum card budget may be imposed, but uncovered questions must be
reported, never absorbed silently. Later expansion appends parcels.

## 5. Lifecycle gates

- **Survey** may be run cold but yields only provisional claims — no permanent
  coordinates, evidence and uncertainty shown.
- **Ratify** requires human review of district boundaries, naming collisions,
  identity matches, and load-bearing Hits/Does-not-hit claims against cited evidence.
  The reviewer need not be the author but must be able to inspect the cited sources.
- **Steward** preserves ratified coordinates through ordinary moves/renames by updating
  locators and recording aliases; splits, merges, ghost promotion, ownership transfer,
  or any widening of a closed boundary returns to a human gate.

## 6. Evolution contract

- Registry lives under `_meta/` or `registry/`; generated indexes rebuild from it and
  are never hand-edited.
- Ordinary file move / folder rename / heading rename: **coordinate unchanged**, locator
  updated, old locator kept as an alias. Old references resolve via alias — never
  silently rewritten.
- Retired coordinates become tombstones: never deleted-and-reused for another noun.
- Splits/merges create NEW append-only coordinates with explicit lineage
  (`split_from` / `merged_from` / `replaced_by`).
- Broken locators are recorded broken/uncertain and reported; no recovery, no guessed
  replacement sources.
- Ambiguous identity freezes as `ambiguous_review` for a human decision.

## 7. Statuses and safe defaults

Known facts are statuses, not unknowns (`issued; active`, `stale_locator_404`,
`known_nonconforming`, `missing_at_expected_path`). Genuinely open items become named
provisional fields with deny-by-default safe defaults ("say nothing stronger than the
evidence"). Provisional fields never block issuance when their default is safe — but
they are never silently cleared either.

## 8. Evidence discipline

- Every card carries `as_of`. Date-bound plans require re-verification after their
  target date; owner attestation is admissible survey evidence but converts to
  source-citable artifacts before ratification.
- Observation of implementation (theme code, rendered pages) never proves publication,
  authenticity, transaction completion, or compliance.
- Financial values and credentials are excluded from packets by construction.

## 9. First-order change routing (Steward rules)

1. Offer-identity changes gate on the owning card first, then downstream claim and
   page-contract reviews.
2. Claim/policy changes sweep every surface repeating the claim across variants;
   membership does not change.
3. Locator/route/suffix/composition-only changes update the touched card without
   rewriting upstream authority, provided identity is verified.
4. Loss of an observed fact (route, marker, form) updates the recorded status and
   triggers review — it does not silently retire or renumber anything.
