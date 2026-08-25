#!/usr/bin/env python3
"""Build the static GitHub Pages site for the Comp 11 Cartographer submission.

Reads explorer/ulteemate-three-card-evidence.json and package/ surfaces,
emits docs/index.html — fully self-contained (data embedded, no network, no CDN).
Re-run after any evidence change: python3 build_site.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent
EVIDENCE = ROOT / "explorer" / "ulteemate-three-card-evidence.json"
CARD3_EVIDENCE = ROOT / "explorer" / "ulteemate-card3-evidence.json"
OUT = ROOT / "docs" / "index.html"
TEMPLATE = ROOT / "site" / "template.html"

CATEGORY_ORDER = [
    "claims", "hits", "does_not_hit", "sources",
    "surfaces", "aliases", "open_fields",
]
CATEGORY_META = {
    "claims": {"label": "Checked facts", "color": "#31597e"},
    "hits": {"label": "Change these too", "color": "#2f7d4f"},
    "does_not_hit": {"label": "Leave these alone", "color": "#a8443c"},
    "sources": {"label": "Where we checked", "color": "#5b6d8f"},
    "surfaces": {"label": "Where it shows up", "color": "#4a7ba6"},
    "aliases": {"label": "Other names it goes by", "color": "#7a8a99"},
    "open_fields": {"label": "Not settled yet", "color": "#c07f2e"},
}


def leaf_items(card: dict, claims_by_id: dict) -> dict[str, list[str]]:
    """Every leaf item is a real recorded fact; area = its text length."""
    open_fields = list(card.get("provisional_fields", {}).keys())
    kn = card.get("known_negative_states") or []
    open_fields += [f"known negative: {k}" for k in kn]
    open_fields += [u.get("field", u) if isinstance(u, dict) else str(u)
                    for u in card.get("non_blocking_uncertainties", [])]
    return {
        "claims": [claims_by_id[cid]["claim"] for cid in card.get("claim_ids", []) if cid in claims_by_id],
        "hits": list(card.get("hits_does_not_hit", {}).get("hits", [])),
        "does_not_hit": list(card.get("hits_does_not_hit", {}).get("does_not_hit", [])),
        "sources": list(card.get("see", [])),
        "surfaces": list(card.get("surfaces", [])),
        "aliases": list(card.get("useful_aliases", [])),
        "open_fields": open_fields,
    }


def normalize_connections(card: dict) -> list[dict]:
    out = []
    for conn in card.get("connected_to", []):
        if isinstance(conn, dict):
            out.append({
                "target": str(conn.get("target", "")),
                "relation": str(conn.get("relation", "")),
                "locators": [str(x) for x in conn.get("locators", [])],
            })
        else:
            out.append({"target": str(conn), "relation": "", "locators": []})
    return out


def main() -> None:
    data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    claims_by_id = {c["id"]: c for c in data.get("claims", [])}
    if CARD3_EVIDENCE.exists():
        card3 = json.loads(CARD3_EVIDENCE.read_text(encoding="utf-8"))
        for entry in card3.get("claim_ledger", []):
            cid = entry.get("claim_id")
            if cid:
                claims_by_id[cid] = {
                    "id": cid,
                    "claim": f"{entry.get('claim', '')} [grade {entry.get('grade', '?')}]",
                }

    cards_out = []
    for card in data["cards"]:
        items = leaf_items(card, claims_by_id)
        volume = sum(len(t) for values in items.values() for t in values)
        grade = card["evidence_grade"]
        if isinstance(grade, dict):
            grade = ", ".join(f"{k.replace('_', ' ')} {v}" for k, v in grade.items())
        cards_out.append({
            "id": card["coordinate"],
            "landmark": card["landmark"],
            "sentence": card.get("one_sentence", ""),
            "status": card.get("status", ""),
            "grade": grade,
            "as_of": card.get("as_of", ""),
            "connected_to": normalize_connections(card),
            "items": items,
            "counts": {k: len(v) for k, v in items.items()},
            "volume": volume,
        })

    payload = {
        "district": {
            "code": data["district"]["code"],
            "name": data["district"]["display_name"],
        },
        "asOf": data["audit"].get("as_of", ""),
        "cards": cards_out,
        "categories": CATEGORY_META,
    }

    template = TEMPLATE.read_text(encoding="utf-8")
    html = template.replace("__DATA_JSON__", json.dumps(payload, ensure_ascii=False))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
