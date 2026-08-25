# Map YOUR workspace with this kit — six steps

This package is a product AND a factory. The worked map (`reference/`, Ulteemate offer
records) is the product. The same folder is also everything you need to cartograph your
own ICM workspace. No special tooling required: text files, a text editor, Python 3
standard library for the engine.

**You will build:** one catalog, one card per map-worthy noun, one machine-readable
registry — such that a cold reader (human or AI model) can answer real change questions
by traveling catalog → one card → cited source, then stopping.

---

## Step 0 — Copy the kit

```bash
cp -r package/ your-workspace-map/
```

Keep the shape: `identity.md`, `rules.md`, `examples.md`, `reference/catalog.md`,
`reference/cards/`, `reference/registry/`. Delete the three worked cards and the
worked resolution records once you have your own (they stay useful as style guides).

## Step 1 — Survey (provisional; NO permanent coordinates yet)

Walk the territory and inventory **durable nouns and processes** — not files. A noun
earns a future card when it satisfies at least three of these signals (`rules.md`):

1. People refer to it as a distinct thing in task language.
2. It owns state, a contract, a schema, or load-bearing behavior.
3. It changes independently of its neighbors.
4. You can state useful **Hits** and **Does-not-hit** boundaries for it.
5. It spans locations, or its name collides, so plain paths mislead.
6. A cold reader could ask "what is X?" or "what changes if I touch X?"

Propose **semantic districts** that cut across the folder tree (like `ULT.OFR`,
"Offer truth"), never mirror the directory hierarchy. Write draft cards marked
`provisional`. Assign **no parcel numbers yet** — numbering happens once, at
ratification, and is forever append-only.

## Step 2 — Ratify (human gate)

A human who can inspect the cited sources reviews:

- district boundaries and naming collisions,
- every load-bearing Hits / Does-not-hit claim,
- evidence for each claim, graded **A** (current source-citable artifact) through
  **D** (external/unavailable state).

Then issue coordinates in the registry using the grammar
`<territory>.<DISTRICT>-NNN` (e.g. `AC.RUN-014`): parcels start at `-001` per
district, append-only, never renumbered or reused. Record each card's locators as
`path#heading` — mutable citations under stable identities. Retire nothing silently:
tombstones and lineage fields exist for that.

## Step 3 — Verify

```bash
python3 your-workspace-map/engine/verify_map.py PATH/TO/YOUR-REPO
python3 your-workspace-map/engine/verify_map.py PATH/TO/YOUR-REPO --selftest
```

Gates G1–G6 are territory-agnostic (grammar, linkage, boundaries, ledger joins,
tombstone safety, locator syntax). G7 checks that shipped evidence ledgers carry an
audited `as_of`. The selftest corrupts a throwaway copy five ways and requires every
gate to fire — proof the checker bites on YOUR map, not just the demo.

## Step 4 — Prove it with cold walks

Predeclare 3–9 questions a cold reader should answer (write the scoring key BEFORE
running anyone). Cut a packet: `workspace.md`-equivalent + catalog + one card + the
cited sources. Then use the harness with any reader — ollama, LM Studio, opencode,
a colleague:

```bash
python3 your-workspace-map/engine/run_walk.py \
  --packet PACKET_DIR --question "..." --reader "ollama run llama3.2" --label q1-r1
```

Compare armed vs unarmed readers if you want measured value, and keep receipts —
including failures. Failures are where rules get fixed.

## Step 5 — Steward

The map now evolves under three rules:

- **Moves and renames:** update the locator, keep the coordinate, append a locator
  alias (worked example: `reference/registry/resolution-records/q8-move-plus-heading-rename.md`).
- **Collisions and stale locators:** record them as statuses (`stale_locator_404`,
  `missing_at_expected_path`) — never silently redirect (see `q9-collision-and-stale-locator.md`).
- **After every change:** rerun the engine. Red gate = fix the map, not the gate.

If you host a viewer, wire a rebuild-on-push workflow so the display can never drift
from the registry (this repo ships one: `.github/workflows/rebuild-site.yml`).

---

## Rules of the road

- One card per question; two hops maximum; stop.
- Never renumber, compact, or reuse coordinates.
- Uncovered questions are reported as uncovered — never faked.
- Say plainly who the later reader is (a person, a cold model, or both).
- If asked to map something non-durable (generated artifacts, nested workspaces,
  methodology itself), refuse explicitly — see `examples.md`, Example 4.
