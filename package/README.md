# Comp 11 — Cartographer

A drop-in cartographer package: a small, source-citing semantic map that gives a cold
human or AI agent stable coordinates for the durable nouns of a workspace, so they can
answer real change questions by traveling **catalog → one card → cited source**, then
stopping.

- Worked territory: UlteemateAI (Ulteemate.com business workspace).
- Ratified slice: Product offer → Proof and claim boundary → Storefront product-page
  contract (district `ULT.OFR`, parcels `-001/-002/-003`).
- Evidence status: the three coordinates are issued and active (`SPEC.md` §§26–28), and
  the predeclared cold-reader benchmark passed all eight thresholds on 2026-08-23
  (`../pilot/RESULTS.md`, audited in `../pilot-AUDIT.md`).

## Layout

| Path | Surface | Question it answers |
|---|---|---|
| `identity.md` | What Cartographer is and is not | "Why does this exist and where are its edges?" |
| `rules.md` | Operating rules and lifecycle | "How does a coordinate get issued, survive change, and die?" |
| `examples.md` | Worked reader walks | "What does using it actually look like?" |
| `reference/catalog.md` | Z0 semantic catalog | "Which durable nouns exist in this district?" |
| `reference/cards/*.md` | One card per coordinate | "What is this noun, what hits/does-not-hit when I touch it?" |
| `reference/registry/registry.yaml` | Machine-readable registry | "What is the exact identity, state, and current locator set?" |
| `reference/registry/resolution-records/` | Worked steward artifacts | "How do moves, renames, collisions, and stale locators resolve?" |

## Reader journey (the whole product)

1. Start at the territory's own `workspace.md` (Cartographer never replaces it).
2. Open `reference/catalog.md`.
3. Pick **at most one** card.
4. Follow that card's cited source locators.
5. Stop. No sibling cards, no registry sweeps.

## Boundaries (anti-duplication acceptance, SPEC §18)

- Removing Cartographer loses no structural-recovery data; it performs no recovery.
- It adds no folder tree that `workspace.md` doesn't already route.
- Persisted records scale with map-worthy nouns, not with files/headings/lines.
- Every card states first-order **Hits** and **Does not hit** boundaries.
- A broken locator is reported broken/uncertain — never silently repaired or guessed.

## Statuses used

`issued; active` · `provisional` (named fields with safe defaults) · known negatives
recorded as statuses, not unknowns (e.g., `stale_locator_404`,
`missing_at_expected_path`) · `tombstone` (retired, never reassigned).

## Provenance note

All territory facts in this package derive from the sanitized, financially redacted
ratification packets and the frozen benchmark snapshot; no credentials, account data,
or monetary values appear. Locators are date-bounded (`as_of`) mutable citations.
