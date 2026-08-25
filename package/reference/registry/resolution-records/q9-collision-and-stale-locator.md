# Registry resolution record — Q9 (ambiguity, stale locator, retirement rules)

Task-specific record. Two lookups plus the standing registry rules.

## Lookup 1 — ambiguous name: "Original Ulteemate Bundle"

- **Result:** explicit collision, not a silent redirect. The name maps to live offer
  `Ulteemate Legacy Bundle` inside coordinate `ULT.OFR-001` as ONE offer slot; the exact
  alias/rename/lineage relation is recorded `original_legacy_relation: provisional` and
  stays open for a human decision. The reader is told the relation is unresolved rather
  than being sent to a different noun as if it were settled.
- **Status:** issued; active with explicit provisional field.

## Lookup 2 — stale locator: older Legacy product route

- **Result:** `/products/ulteemate-tee-golf-drive-improvement-system` returns `404`.
  Recorded status: `legacy_old_route: stale_locator_404`. Current locator given
  explicitly: `/products/ulteemate-legacy-bundle`. No redirect is inferred, no fifth
  offer is created, and the Original/Legacy lineage question is not silently answered.

## Standing rules (from the ratified registry contract)

- Retired coordinates become tombstones and are never reused for a different noun.
- Splits and merges create NEW append-only coordinates with explicit lineage
  (`split_from` / `merged_from` / `replaced_by`); they never silently reuse an identity.
- A broken locator becomes broken/uncertain and is reported; Cartographer performs no
  recovery and guesses no replacement source.
- Ambiguous identity freezes for human review (`ambiguous_review`) before any change.

Rule source: `owner-reconciliation/coordinate-stress-test-extracts.md#2. Surviving design`
and `#3. Critical clarification: districts are cadastral zones`.
