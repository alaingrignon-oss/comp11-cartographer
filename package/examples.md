# Cartographer — worked examples

Three real walks from the benchmark pilot (2026-08-23; 36 tasks, transcripts preserved
in `../pilot/runs/`). Each shows the whole value chain: coordinate → card → source →
answer with boundaries.

## Example 1 — Two-hop offer question (Q1: "which products are live, which must never be presented as live?")

- **Journey:** catalog → `ULT.OFR-001` Product offer → two cited sources
  (`post-launch-gtm_draft.md#The situation (verified July 5)`,
  `survey-decision-extracts.md#Live offer reconciliation`).
- **Outcome (both reps):** exactly four live offers named — 2.0 Bundle, 2.0 Solo,
  Legacy Bundle, Spare Spikes/Spike Pack as one refill offer — and both ghosts
  (Trainer; Boller/Super Bundle) explicitly future-only. The Original/Legacy collision
  was flagged as one slot, not a fifth product.
- **Cost:** 2 snapshot files opened after the card. Baseline readers answering the same
  question opened 3–8 files each.
- **Boundary stated:** Hits = claim/packaging review, title/contents/purchase-expression
  review; Does-not-hit = theme mechanics, CAD, campaign execution, financials,
  credentials, recovery state.

## Example 2 — Drift: file moved and heading renamed (Q8)

Fixture: the claim-rules section moved from
`company-product-description.md#Customer-Facing Copy Rules (V2)` to
`reference/product-truth.md#Customer Claim Boundary` between snapshot v1 and v2.

- **Cartographer walk:** the card carries the updated locator plus a locator alias;
  the task's resolution record states the rule (coordinate unchanged; old references
  resolve via alias, never silently rewritten). Reader verified on disk: new heading
  present, body verbatim, provenance note in place. Answer: same noun reached without
  changing the coordinate. Both reps resolved directly through the updated locator.
- **Baseline walk (same fixture):** the stale `path#heading` pointer dead-ended in both
  reps — heading absent from the cited file, no tombstone at the old location. Recovery
  required content search: a full 240-line read plus greps (rep 1), or a glob sweep of
  all 15 files (rep 2). Stated conclusion: bare path#heading does not survive move +
  rename; repair requires re-pointing.
- **Threshold served:** drift advantage (strict) — met in both repetitions.

## Example 3 — Ambiguity and stale locators (Q9, safety-critical)

Question: if a coordinate is retired/split/replaced, does the reader get an explicit
lineage-or-uncertainty result instead of being sent to a different noun?

- **Resolution record behavior:** "Original Ulteemate Bundle" resolves as an explicit
  collision inside ONE offer slot with `original_legacy_relation: provisional` left
  open for human decision — not silently aliased away. The dead Legacy route is
  recorded `stale_locator_404` with the current route given explicitly — no redirect
  inferred, no fifth offer invented.
- **Standing rules demonstrated:** tombstones never reused; splits/merges create new
  append-only coordinates with lineage fields; broken locators reported broken;
  ambiguity freezes as `ambiguous_review`.
- **Result:** zero silent misresolutions across all 36 pilot transcripts (identity
  safety threshold).

## Example 4 — A declined territory (the refusal walk)

A cartographer that maps everything maps nothing. This walk shows the tool saying no,
per the map-worthiness signals (`rules.md` §14) and the responsibility boundary
(`identity.md`).

- **Request:** "Map the Horizon theme templates — `index.json`,
  `product.eca-pdp-bundle.json`, `page.shipping-returns.json` — so we know what the
  storefront shows."
- **Refusal:** declined as primary territory. Theme files are regenerated implementation
  material whose only durable meaning is *as evidence of purchase expression* — they fail
  the map-worthiness test (they do not own state or contracts independently; their
  "what changes if I touch it" answer is fully absorbed by an existing coordinate). They
  already appear where they belong: cited inside `ULT.OFR-003` as observed expression,
  and listed in its Does-not-hit boundary as mechanics, never as offer truth.
- **Also declined, same rules:** `product-design/` (a separate nested ICM workspace with
  its own boundary), generated/build artifacts and binaries (no durable noun), recovery
  machinery (structural tooling owns it), and this cartographer's own methodology (a map
  that maps itself is recursion, not navigation).
- **What the reader gets instead:** routed back to `workspace.md` for anything outside
  the ratified slice — an explicit "uncovered by design" answer (`catalog.md` coverage
  note) rather than a plausible-looking card. In the pilot this discipline was scored:
  zero invented dependencies across 36 transcripts.

## What the benchmark showed (summary)

| Threshold | Result |
|---|---|
| Accuracy ≥90% pooled / 100% safety-critical | PASS — 18/18; 8/8 |
| Unchanged-source parity vs path#anchor baseline | PASS — 14/14 vs 10/14 (Q1–Q7) |
| Context reduction ≥20% (median) | PASS — 44.9% by bytes; ~60–69% by files opened |
| Two-hop discipline ≥90% | PASS — 18/18 |
| Change boundary ≥90%, none invented | PASS |
| Drift advantage on Q8 (strict) | PASS — both reps |
| Identity safety: zero silent misresolutions | PASS |
| Truth safety: zero violations | PASS |

Full scoring, per-task grounds, deviations, and the independent audit:
`../pilot/RESULTS.md` and `../pilot-AUDIT.md`.

## Implementation lessons baked into this package

1. Cards, catalog, and registry ship as real files (pilot readers wasted a failed
   lookup on inline-only materials).
2. Every card keeps its own current locators plus aliases — the steward updates these;
   coordinates stay put.
3. Provisional fields and known negatives ride along visibly; nothing is hidden to
   make a card look complete.
