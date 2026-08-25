# Comp 11 Cartographer — ICM Workspace Semantic Map

A lightweight, reusable semantic map for ICM workspaces: stable coordinates
(`<territory>.<district>-<parcel>`, e.g. `ULT.OFR-001`), append-only parcels,
and mutable source locators — so humans and agents can wayfind a workspace
without duplicating its file tree.

**Live map viewer:** https://alaingrignon-oss.github.io/comp11-cartographer/
(static coverage treemap rendered from the evidence ledgers — no backend, no network)

## Use it on your OWN workspace

This package is both product and factory: the worked Ulteemate map demonstrates it,
the same folder is everything you need to map your own ICM workspace. Start here:
**[`package/MAPPING-GUIDE.md`](package/MAPPING-GUIDE.md)** — six steps from copying
the kit to stewarding your ratified slice, using only text files and the stdlib
engine (`survey → ratify → verify → cold-walk → steward`). The verifier's gates and
the walk harness are territory-agnostic by design.

## What's inside

| Path | What it is |
|------|------------|
| `package/README.md` | Start here — what the map is and how to read it |
| `package/engine/verify_map.py` | Deterministic verification: 7 structural gates + self-proving negative fixtures (`--selftest`) |
| `package/engine/README.md` | Why the engine is model-agnostic and how its pattern generalizes to any local-model task |
| `package/identity.md` | Territory/district identity rules |
| `package/rules.md` | Coordinate grammar: cadastral districts, append-only parcels |
| `package/examples.md` | Worked examples of reading and resolving coordinates |
| `package/reference/catalog.md` | The semantic catalog for the worked territory |
| `package/reference/cards/` | The three issued cards (`ULT.OFR-001..003`) |
| `package/reference/registry/` | Machine-readable registry + worked resolution records (move+rename, collision+stale-locator) |
| `explorer/app.py` | Interactive Streamlit explorer for the worked map (local) |
| `docs/index.html` | Hosted coverage treemap + card drill-down (GitHub Pages; rebuild with `python3 build_site.py`) |
| `docs/receipts.md` | Quoted pilot receipts: the baseline failure, the drift head-to-head, discipline totals |

## How to walk this (cold model or human)

1. Open `package/reference/catalog.md` — the front door. Pick **one** coordinate.
2. Read that one card in `package/reference/cards/`. It names what the noun is,
   what else moves if you change it, and what does **not** move.
3. Follow the card's cited source locator if you need the underlying file.
4. **Stop.** Never load more than catalog + one card. The map points; the shelves
   stay closed.

The later reader may be a model — nothing here assumes memory you don't have.

## Worked territory

**UlteemateAI** — the public Ulteemate.com business workspace, sliced along
its offer truth: product offer (`ULT.OFR-001`) → proof and claim boundary
(`ULT.OFR-002`) → storefront product-page contract (`ULT.OFR-003`).

## Run the explorer

```bash
pip install streamlit
streamlit run explorer/app.py
```

No other dependencies. The explorer reads `ulteemate-three-card-evidence.json`
from its own directory; every card claim links back to its cited source.
