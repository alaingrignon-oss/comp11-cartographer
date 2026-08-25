from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import altair as alt
import pandas as pd
import streamlit as st

EVIDENCE_FILENAME = "ulteemate-three-card-evidence.json"
ACCENT = "#31597e"
EMPTY_CELL = "#e3e7ee"
APP_DIR = Path(__file__).parent
SOURCE_NOTE_URI = (APP_DIR / "_meta" / "source-link-note.md").resolve().as_uri()

GRADE_FACET_LABELS = {
    "core_boundary": "core boundary",
    "internal_stale_or_draft_evidence": "internal/draft",
    "external_or_deployed_state": "external/deployed",
}

WORK_MODES = {
    "Offer & product decisions": ["ULT.OFR-001"],
    "Copy, proof & policy review": ["ULT.OFR-002", "ULT.OFR-003"],
    "Storefront / PDP planning & QA": ["ULT.OFR-001", "ULT.OFR-002", "ULT.OFR-003"],
    "Source navigation & wayfinding": ["ULT.OFR-001", "ULT.OFR-002", "ULT.OFR-003"],
    "Change-impact review": ["ULT.OFR-001", "ULT.OFR-002", "ULT.OFR-003"],
}

GRAMMAR_STRIP = """ULT . OFR - 001
 │     │     └ parcel 001 — Product offer (append-only, never renumbered)
 │     └ district OFR — Offer truth and purchase expression (permanent)
 └ territory — Ulteemate.com"""

STORY_BULLETS: dict[tuple[str, ...], str] = {
    ("ULT.OFR-001", "ULT.OFR-002", "ULT.OFR-003"): (
        "Chain-wide: PDP planning, wayfinding, and change-impact review move all three together."
    ),
    ("ULT.OFR-001",): "Offer decisions start — and stop — at the offer itself.",
    ("ULT.OFR-002", "ULT.OFR-003"): "Claim review always carries the page contract with it.",
}


@st.cache_data(show_spinner=False)
def load_payload() -> Any:
    path = Path(__file__).with_name(EVIDENCE_FILENAME)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _pick(source: Any, *names: str, default: Any = None) -> Any:
    if not isinstance(source, dict):
        return default
    for name in names:
        value = source.get(name)
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return default


def _items(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, dict):
        return ", ".join(f"{key}={_text(val)}" for key, val in value.items())
    if isinstance(value, (list, tuple)):
        return ", ".join(_text(item) for item in value)
    return str(value)


def extract_cards(payload: Any) -> list[dict]:
    candidates: list[list[dict]] = []
    if isinstance(payload, list):
        candidates.append([item for item in payload if isinstance(item, dict)])
    elif isinstance(payload, dict):
        for key in ("cards", "landmarks", "coordinates", "nodes", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                candidates.append([item for item in value if isinstance(item, dict)])
        for value in payload.values():
            if isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
                candidates.append(list(value))
    for candidate in candidates:
        if candidate:
            return candidate
    return []


def extract_meta(payload: Any) -> dict[str, str]:
    as_of = ""
    note = ""
    if isinstance(payload, dict):
        as_of = _text(_pick(payload, "as_of", "asOf", "snapshot_date", "generated_at", "updated", "date", default=""))
        note = _text(_pick(payload, "note", "disclaimer", "scope_note", "description", default=""))
        nested = payload.get("meta")
        if isinstance(nested, dict):
            if not as_of:
                as_of = _text(_pick(nested, "as_of", "asOf", "snapshot_date", "generated_at", "updated", "date", default=""))
            if not note:
                note = _text(_pick(nested, "note", "disclaimer", "description", default=""))
    return {"as_of": as_of, "note": note}


def card_id(card: dict) -> str:
    return _text(_pick(card, "id", "card_id", "key", "coordinate", default="unknown"))


def card_title(card: dict) -> str:
    return _text(_pick(card, "title", "name", "label", default=""))


def card_landmark(card: dict) -> str:
    return _text(_pick(card, "landmark", "anchor", default=""))


def card_status(card: dict) -> str:
    return _text(_pick(card, "status", "state", default="unspecified"))


def card_shape(card: dict) -> str:
    return _text(_pick(card, "shape", "form", "geometry", default=""))


def card_coordinate(card: dict) -> str:
    return _text(_pick(card, "coordinate", "coords", "position", default=""))


def card_sentence(card: dict) -> str:
    return _text(_pick(card, "one_sentence", "summary", "gist", "description", default=""))


def card_surfaces(card: dict) -> list[str]:
    return [_text(surface) for surface in _items(_pick(card, "surfaces", "surface", default=[]))]


def card_aliases(card: dict) -> list[str]:
    return [_text(alias) for alias in _items(_pick(card, "aliases", "useful_aliases", "aka", "alternate_names", default=[]))]


def card_connections(card: dict) -> list[Any]:
    return list(_items(_pick(card, "connections", "connected_to", "links", "related", "edges", default=[])))


def card_hits(card: dict) -> list[str]:
    nested = _pick(card, "hits_does_not_hit", default={})
    raw = _pick(card, "hits", "hit", "covers")
    if raw is None:
        raw = _pick(nested, "hits", "hit", "covers")
    return [_text(hit) for hit in _items(raw)]


def card_misses(card: dict) -> list[str]:
    nested = _pick(card, "hits_does_not_hit", default={})
    raw = _pick(card, "does_not_hit", "doesnt_hit", "does_not", "non_hits")
    if raw is None:
        raw = _pick(nested, "does_not_hit", "doesnt_hit", "does_not", "non_hits")
    return [_text(miss) for miss in _items(raw)]


def card_sources_raw(card: dict) -> list[Any]:
    return list(_items(_pick(card, "sources", "citations", "source_locators", "references", "see", default=[])))


def card_evidence(card: dict) -> tuple[str, str, list[str]]:
    raw = _pick(card, "evidence_grade", "evidence", "grade", "confidence", default=None)
    if raw is None:
        return "unspecified", "", []
    if isinstance(raw, dict):
        label = _text(_pick(raw, "grade", "level", "rating", "score", "label", default=""))
        rationale = _text(_pick(raw, "rationale", "reason", "why", "because", "basis", "note", "notes", "comment", default=""))
        reserved = {
            "grade", "level", "rating", "score", "label",
            "rationale", "reason", "why", "because", "basis", "note", "notes", "comment",
        }
        extras = [
            f"{key}: {_text(value)}"
            for key, value in raw.items()
            if key not in reserved and value is not None and not isinstance(value, (dict, list))
        ]
        if not label:
            grades = [str(value).strip() for value in raw.values()]
            if grades and all(grade in {"A", "B", "C", "D"} for grade in grades):
                label = "/".join(grades)
        return label or "unspecified", rationale, extras
    return _text(raw) or "unspecified", "", []


def card_as_of(card: dict) -> str:
    return _text(_pick(card, "as_of", "snapshot_date", default=""))


def card_provisional_fields(card: dict) -> list[str]:
    raw = _pick(card, "provisional_fields", default={})
    if not isinstance(raw, dict):
        return []
    return [_text(key) for key in raw if _text(key)]


def resolve_locator(locator: str) -> str | None:
    path_part = locator.split("#", 1)[0].strip()
    if not path_part:
        return None
    resolved = (APP_DIR / path_part).resolve()
    if resolved.exists() and resolved.is_relative_to(APP_DIR.resolve()):
        return resolved.as_uri()
    return None


def locator_link(locator: str) -> str:
    resolved = resolve_locator(locator)
    if resolved is None:
        return f"[{locator} · simulated link]({SOURCE_NOTE_URI})"
    return f"[{locator}]({resolved})"


def natural_list(names: list[str]) -> str:
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


def grade_summary(record: dict) -> tuple[str, bool]:
    raw = _pick(record["raw"], "evidence_grade", "evidence", "grade", "confidence", default=None)
    if isinstance(raw, dict):
        parts = [
            f"{GRADE_FACET_LABELS.get(key, key.replace('_', ' '))} graded {_text(value)}" if index == 0
            else f"{GRADE_FACET_LABELS.get(key, key.replace('_', ' '))} {_text(value)}"
            for index, (key, value) in enumerate(raw.items())
        ]
        return f'{record["grade"]} ({", ".join(parts)})', False
    if ";" in record["grade"] or " " in record["grade"]:
        return record["grade"], True
    return f"Grade {record['grade']}", False


def describe_connection(connection: Any, by_id: dict[str, dict]) -> tuple[str, str, str, str]:
    if isinstance(connection, dict):
        target_id = _text(_pick(connection, "to", "target", "target_id", "connects_to", "card", "node", "id", default=""))
        relation = _text(_pick(connection, "relation", "type", "relationship", "kind", "label", default=""))
        note = _text(_pick(connection, "note", "why", "because", "explanation", "reason", "description", "purpose", default=""))
    else:
        target_id = _text(connection)
        relation = ""
        note = ""
    label = target_id
    target = by_id.get(target_id)
    if target is not None:
        name = card_landmark(target) or card_title(target)
        label = f"{target_id} · {name}" if name else target_id
    elif resolve_locator(target_id) is not None:
        label = locator_link(target_id)
    return target_id, label, relation, note


def build_records(cards: list[dict]) -> list[dict]:
    records: list[dict] = []
    for card in cards:
        grade, rationale, extras = card_evidence(card)
        title = card_title(card)
        status = card_status(card)
        sentence = card_sentence(card)
        surfaces = card_surfaces(card)
        aliases = card_aliases(card)
        records.append(
            {
                "raw": card,
                "id": card_id(card),
                "title": title or card_id(card),
                "landmark": card_landmark(card),
                "status": status,
                "shape": card_shape(card),
                "coordinate": card_coordinate(card),
                "sentence": sentence,
                "as_of": card_as_of(card),
                "grade": grade,
                "rationale": rationale,
                "extras": extras,
                "provisional_fields": card_provisional_fields(card),
                "surfaces": surfaces,
                "aliases": aliases,
                "connections": card_connections(card),
                "hits": card_hits(card),
                "misses": card_misses(card),
                "sources": [_text(entry) for entry in card_sources_raw(card)],
                "haystack": " ".join(
                    _text(part)
                    for part in [card_id(card), title, card_landmark(card), status, sentence, grade, rationale, *aliases, *surfaces]
                ).lower(),
            }
        )
    records.sort(key=lambda record: record["id"])
    return records


def status_chip(status: str) -> str:
    lowered = status.lower()
    if any(word in lowered for word in ("settle", "stable", "confirm", "locked")):
        return f":green[{status}]"
    if any(word in lowered for word in ("provision", "draft", "pending", "review", "wip")):
        return f":orange[{status}]"
    if any(word in lowered for word in ("negative", "contested", "reject", "retire", "deprecated")):
        return f":red[{status}]"
    return f":gray[{status}]"


def focus_label(record: dict) -> str:
    name = record["landmark"] or record["title"]
    if name and name != record["id"]:
        return f'{record["id"]} — {name}'
    return record["id"]


def short_id(card_id_value: str) -> str:
    return card_id_value.split(".")[-1] or card_id_value


def connection_locators(connection: Any) -> list[str]:
    if not isinstance(connection, dict):
        return []
    return [_text(locator) for locator in _items(connection.get("locators")) if _text(locator)]


def exact_set_label(ids_tuple: tuple[str, ...], scope_count: int) -> str:
    shorts = [short_id(cid) for cid in ids_tuple]
    if len(shorts) == 1:
        return f"{shorts[0]} alone"
    if len(shorts) == scope_count:
        tail = "+".join(part.split("-", 1)[-1] for part in shorts[1:])
        return f"All three · {shorts[0]}+{tail}"
    return "+".join(shorts)


def render_detail(record: dict, by_id: dict[str, dict]) -> None:
    name = record["landmark"] or record["title"]
    with st.container(border=True):
        st.markdown(f"### {record['id']} · {name}")
        if record["sentence"]:
            st.markdown(f"**What this is**\n\n**{name}** — {record['sentence']}")

        if record["status"] != "unspecified" or record["as_of"] or record["grade"]:
            lead = f"As of {record['as_of']}, " if record["as_of"] else ""
            endorsement = (
                " — issued on source-backed review with named fields still provisional"
                if record["provisional_fields"] or "provisional" in record["status"]
                else ""
            )
            grade_text, grade_standalone = grade_summary(record)
            if grade_standalone:
                evidence_run = (
                    f"Evidence runs {grade_text}. Evidence is strongest where the map cites current "
                    "documents, weakest where state lives outside the packet."
                )
            else:
                evidence_run = (
                    f"Evidence runs {grade_text}: strongest where the map cites current documents, "
                    "weakest where state lives outside the packet."
                )
            st.markdown(
                "**Where it stands**\n\n"
                f"{lead}{record['id']} {name} stands at status “{record['status']}”{endorsement}. "
                f"{evidence_run}"
            )
        with st.expander("Status & evidence detail"):
            chips = [f"Status {status_chip(record['status'])}"]
            if record["shape"]:
                chips.append(f"Shape **{record['shape']}**")
            if record["coordinate"]:
                chips.append(f"Coordinate **{record['coordinate']}**")
            chips.append(f"Evidence grade **{record['grade']}**")
            st.markdown("  ·  ".join(chips))
            if record["rationale"]:
                st.markdown(f"*{record['rationale']}*")
            for extra in record["extras"]:
                st.markdown(f"- {extra}")
            if record["provisional_fields"]:
                listed = ", ".join(f"`{field}`" for field in record["provisional_fields"])
                st.markdown(f"Provisional fields: {listed}")

        if record["surfaces"]:
            surface_noun = "surface" if len(record["surfaces"]) == 1 else "surfaces"
            example = natural_list(record["surfaces"][:2])
            st.markdown(
                f"**What it touches**\n\nA change here reaches {len(record['surfaces'])} "
                f"{surface_noun} — for example {example}."
            )
            with st.expander("All surfaces"):
                for surface in record["surfaces"]:
                    st.markdown(f"- {surface}")

        if record["aliases"]:
            with st.expander("Aliases"):
                for alias in record["aliases"]:
                    st.markdown(f"- {alias}")

        if record["hits"] or record["misses"]:
            sentences = []
            if record["hits"]:
                area_noun = "area" if len(record["hits"]) == 1 else "areas"
                first_hits = "; ".join(record["hits"][:2])
                sentences.append(
                    f"Expect impact on {len(record['hits'])} {area_noun} ({first_hits})."
                )
            if record["misses"]:
                miss_noun = "neighbour" if len(record["misses"]) == 1 else "neighbours"
                sentences.append(
                    f"Equally important, it does NOT touch {len(record['misses'])} {miss_noun} — "
                    f"including {record['misses'][0]} — even when names sound related."
                )
            st.markdown("**What moves if you change it**\n\n" + " ".join(sentences))
            if record["hits"] and record["misses"]:
                hit_col, miss_col = st.columns(2)
                with hit_col:
                    st.markdown("**Hits**")
                    for hit in record["hits"]:
                        st.markdown(f"- {hit}")
                with miss_col:
                    st.markdown("**Does not hit**")
                    for miss in record["misses"]:
                        st.markdown(f"- {miss}")
            elif record["hits"]:
                st.markdown("**Hits**")
                for hit in record["hits"]:
                    st.markdown(f"- {hit}")
            else:
                st.markdown("**Does not hit**")
                for miss in record["misses"]:
                    st.markdown(f"- {miss}")

        described = [describe_connection(connection, by_id) for connection in record["connections"]]
        if described:
            all_reasoned = all(relation or note for _tid, _label, relation, note in described)
            neighbour_noun = "neighbour" if len(described) == 1 else "neighbours"
            targets = ", ".join(label for _tid, label, _relation, _note in described)
            closing = ", each for a stated reason" if all_reasoned else ""
            st.markdown(
                f"**How it connects**\n\n{record['id']} links to {len(described)} "
                f"{neighbour_noun}: {targets}{closing}."
            )
            with st.expander("Connections detail"):
                st.caption(
                    "Each arrow below is a stored connection. Follow it only for the stated relation; the destination's "
                    "own Hits and Does not hit boundaries always remain in force."
                )
                for (target_id, target_label, relation, note), connection in zip(described, record["connections"]):
                    head = f"- **{record['id']} → {target_label}**"
                    if relation:
                        head += f" · relation `{relation}`"
                    st.markdown(head)
                    if note:
                        st.markdown(f"> {note}")
                    for locator in connection_locators(connection):
                        st.markdown(f"  - Locator {locator_link(locator)}")
                    target = by_id.get(target_id)
                    if target is not None and target is not record["raw"]:
                        tail = f"Destination status: {card_status(target)}"
                        destination_sentence = card_sentence(target)
                        if destination_sentence:
                            tail += f" — {destination_sentence}"
                        st.caption(tail)

        if record["sources"]:
            cited_noun = "cited location" if len(record["sources"]) == 1 else "cited locations"
            st.markdown(
                f"**Where the evidence lives**\n\nEvery claim traces to {len(record['sources'])} "
                f"{cited_noun} you can open directly."
            )
            for source in record["sources"]:
                st.markdown(f"- {locator_link(source)}")


def reset_filters() -> None:
    for key in ("cg_search", "cg_status", "cg_grade", "cg_mode"):
        st.session_state.pop(key, None)


st.set_page_config(page_title="Cartographer — three-card map", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    '<style>[data-testid="stMarkdownContainer"] li { margin-bottom: 0.1rem; } '
    '[data-testid="stMarkdownContainer"] li > p { margin-bottom: 0.15rem; }</style>',
    unsafe_allow_html=True,
)

payload = load_payload()
meta = extract_meta(payload)
records = build_records(extract_cards(payload))

st.title("Cartographer · three-card map")
st.markdown(
    "Offline explorer for the curated three-coordinate Cartographer evidence map: browse landmarks, "
    "trace connections, and read exact relevance overlaps."
)
snapshot_bits = f"Evidence snapshot: **{meta['as_of']}**" if meta["as_of"] else "Evidence snapshot date: not recorded in the source file"
st.caption(
    f"{snapshot_bits}. Every status, grade, hit, miss, and citation below is rendered exactly as recorded in "
    f"`{EVIDENCE_FILENAME}`; nothing is upgraded from provisional or known-negative into a positive claim."
)
if meta["note"]:
    st.info(meta["note"])

if not records:
    st.error("No card records were found in the evidence file.")
    st.stop()

by_id = {record["id"]: record["raw"] for record in records}

with st.container(border=True):
    st.markdown("#### Read this first")
    st.markdown("**What you are looking at**")
    st.markdown(
        "You are looking at a map, not the territory. Three durable concepts in Ulteemate's offer world "
        "each have a permanent coordinate:"
    )
    st.code(GRAMMAR_STRIP, language=None)
    st.markdown(
        "Neighbours: ULT.OFR-002 Proof and claim boundary · ULT.OFR-003 Storefront product-page contract. "
        "Codes are addresses; the landmark names are what you read."
    )
    st.markdown("**How to walk this map**")
    st.markdown(
        "1. Find your task language in the catalog (or filter by work mode).\n"
        "2. Open exactly one card.\n"
        "3. Check Hits / Does not hit before touching anything.\n"
        "4. Need authority? Follow one cited source locator. If the card and the file disagree, "
        "the file wins and the card is wrong."
    )
    st.markdown(
        "Then stop. Two hops is the whole design budget: catalog → card → source. Nobody photocopies "
        "the library into a backpack."
    )
    st.markdown("**What a card tells you**")
    st.markdown(
        "Status and evidence grade (how well-sourced it is) · shape (what the noun owns) · aliases and "
        "surfaces · connections with stated relations · Hits and Does not hit · exact source locators."
    )
    st.markdown("**What this map is not**")
    st.markdown(
        "Not a tour — enter anywhere; there is no required order. Not an auditor — no list of everything "
        "wrong. Not a diagnostician — never why it failed. Not a photocopy — cards cite source, they do "
        "not replace it. Not usage analytics — the coverage chart is curated judgement, not measured "
        "behaviour. Not recovery — a broken locator is reported as broken, never silently repaired or guessed."
    )

scope_ids = {cid for ids in WORK_MODES.values() for cid in ids}
landmark_by_id = {record["id"]: record["landmark"] or record["title"] for record in records}
chain_bits = [f"**{cid}** {landmark_by_id.get(cid, '')}".strip() for cid in sorted(scope_ids)]
st.markdown(" → ".join(chain_bits))
st.caption(f"{len(records)} coordinates in scope.")

with st.sidebar:
    st.subheader("Filters")
    st.button("Reset filters", on_click=reset_filters)
    search = st.text_input("Search", key="cg_search", placeholder="id, landmark, alias, surface…")
    status_options = sorted({record["status"] for record in records})
    picked_statuses = st.multiselect("Status", status_options, key="cg_status")
    grade_options = sorted({record["grade"] for record in records if record["grade"]})
    picked_grades = st.multiselect("Evidence grade", grade_options, key="cg_grade")
    picked_modes = st.multiselect("Work mode", list(WORK_MODES), key="cg_mode")
    st.caption("Work modes are curated; see Work-mode coverage below.")

mode_allowance: set[str] | None = None
if picked_modes:
    mode_allowance = set()
    for mode_name in picked_modes:
        mode_allowance.update(WORK_MODES[mode_name])

needle = search.strip().lower()
visible: list[dict] = []
for record in records:
    if needle and needle not in record["haystack"]:
        continue
    if picked_statuses and record["status"] not in picked_statuses:
        continue
    if picked_grades and record["grade"] not in picked_grades:
        continue
    if mode_allowance is not None and record["id"] not in mode_allowance:
        continue
    visible.append(record)

visible_ids = {record["id"] for record in visible}
catalog_rows = []
for record in records:
    supporting_modes = sum(1 for ids in WORK_MODES.values() if record["id"] in ids)
    catalog_rows.append(
        {
            "ID": record["id"],
            "Landmark": record["landmark"] or record["title"],
            "Status": record["status"],
            "Evidence": record["grade"],
            "Surfaces": len(record["surfaces"]),
            "Links": len(record["connections"]),
            "Modes": supporting_modes,
            "Matches filters": "yes" if record["id"] in visible_ids else "no",
        }
    )

st.divider()
st.subheader("Coordinate catalog")
st.dataframe(pd.DataFrame(catalog_rows), hide_index=True)
st.caption(f"{len(visible)} of {len(records)} coordinates match the current filters.")

if visible:
    previous_focus = st.session_state.get("cg_focus_id")
    focus_options = [record["id"] for record in visible]
    default_index = focus_options.index(previous_focus) if previous_focus in focus_options else 0
    labels_by_id = {record["id"]: focus_label(record) for record in records}
    selected_id = st.selectbox(
        "Focused coordinate",
        focus_options,
        index=default_index,
        format_func=lambda oid: labels_by_id.get(oid, oid),
        help="Pick a coordinate to open its full detail panel.",
    )
    st.session_state["cg_focus_id"] = selected_id
    selected_record = next(record for record in records if record["id"] == selected_id)
    render_detail(selected_record, by_id)
else:
    st.warning("No coordinates match the current filters. Loosen the search, narrow the work mode, or reset.")

st.divider()
st.subheader("Which coordinates move together")
st.caption("(UpSet-style exact-set view of the curated mapping)")
st.markdown(
    "Each column is one way work combines across the offer chain. Read any column top to bottom: the bar "
    "counts how many curated work modes share that exact set of coordinates; the dots below name them."
)
st.caption(
    "Curated relevance interpretation: the shipped mapping from work modes to coordinates, grouped into exact-set "
    "intersections. This section is NOT historical usage data, telemetry, or a benchmark result."
)
st.caption("Bar height counts curated work modes — not visits, priority, or volume.")

all_scope = sorted(scope_ids)
scope_labels = {
    record["id"]: f"{short_id(record['id'])} · {record['landmark']}" if record["landmark"] else short_id(record["id"])
    for record in records
}
grouped_modes: dict[tuple[str, ...], list[str]] = {}
for mode_name, ids in WORK_MODES.items():
    grouped_modes.setdefault(tuple(sorted(ids)), []).append(mode_name)
ordered_groups = sorted(grouped_modes.items(), key=lambda item: (-len(item[1]), item[0]))

column_order = [exact_set_label(ids_tuple, len(all_scope)) for ids_tuple, _modes in ordered_groups]

bar_rows: list[dict] = []
dot_rows: list[dict] = []
label_rows: list[dict] = []
for ids_tuple, modes_in_group in ordered_groups:
    label = exact_set_label(ids_tuple, len(all_scope))
    bar_rows.append(
        {
            "Exact set": label,
            "Mode count": len(modes_in_group),
            "Included work modes": ", ".join(modes_in_group),
        }
    )
    for cid in all_scope:
        dot_rows.append(
            {
                "Exact set": label,
                "Coordinate": scope_labels[cid],
                "Member": cid in ids_tuple,
            }
        )
    label_rows.append({"Exact set": label, "Coordinate": "", "Column label": label})

coordinate_sort = [scope_labels[cid] for cid in all_scope] + [""]

bar_frame = pd.DataFrame(bar_rows)
bar_bars = alt.Chart(bar_frame).mark_bar(color=ACCENT).encode(
    x=alt.X("Exact set:N", sort=column_order, axis=None),
    y=alt.Y(
        "Mode count:Q",
        title="Curated work modes",
        axis=alt.Axis(tickMinStep=1, orient="right"),
    ),
    tooltip=[
        alt.Tooltip("Exact set:N", title="Exact set"),
        alt.Tooltip("Mode count:Q", title="Curated work modes"),
        alt.Tooltip("Included work modes:N", title="Modes"),
    ],
)
bar_counts = alt.Chart(bar_frame).mark_text(align="center", dy=-6, color="#3c4654").encode(
    x=alt.X("Exact set:N", sort=column_order, axis=None),
    y=alt.Y("Mode count:Q"),
    text=alt.Text("Mode count:Q"),
)
bar_chart = (bar_bars + bar_counts).properties(width=620, height=140)

cell_frame = pd.DataFrame(dot_rows)
dot_axis = alt.Axis(orient="right", title=None, labelLimit=320, labelExpr="datum.value !== ''")
dot_layer = alt.Chart(cell_frame).mark_circle(size=340).encode(
    x=alt.X("Exact set:N", sort=column_order, axis=None),
    y=alt.Y("Coordinate:N", sort=coordinate_sort, axis=dot_axis),
    color=alt.condition("datum.Member", alt.value(ACCENT), alt.value(EMPTY_CELL)),
)
link_layer = alt.Chart(cell_frame[cell_frame["Member"]]).mark_line(color=ACCENT, strokeWidth=3, opacity=0.8).encode(
    x=alt.X("Exact set:N", sort=column_order, axis=None),
    y=alt.Y("Coordinate:N", sort=coordinate_sort),
    detail="Exact set:N",
)
label_strip = alt.Chart(pd.DataFrame(label_rows)).mark_text(
    align="center", baseline="top", dy=10, fontSize=12, color="#3c4654"
).encode(
    x=alt.X("Exact set:N", sort=column_order, axis=None),
    y=alt.Y("Coordinate:N", sort=coordinate_sort),
    text=alt.Text("Column label:N"),
)
matrix_chart = (link_layer + dot_layer + label_strip).properties(
    width=620, height=max(120, 36 * len(coordinate_sort))
)

st.altair_chart(alt.vconcat(bar_chart, matrix_chart).configure_concat(spacing=10))
st.caption("Filled, linked dots mark the coordinates contained in each exact intersection; pale dots are excluded.")

with st.expander("How to read this section"):
    st.markdown(
        "Each bar counts how many curated work modes land on the same exact set of coordinates. The dot matrix "
        "mirrors that view: one column per exact set, one row per coordinate, with a connecting line tracing "
        "membership. Because the mapping is curated judgement rather than measured behaviour, treat these overlaps "
        "as navigation aids, not statistics."
    )

for ids_tuple, _modes in ordered_groups:
    bullet = STORY_BULLETS.get(ids_tuple)
    if bullet:
        st.markdown(f"- {bullet}")
st.caption(
    "No curated mode touches Cards 2 or 3 alone — in this slice, claim and purchase-expression work is never separate."
)
st.caption(
    "Every coordinate appears in 4 of the 5 curated work modes — the exact combinations, not the coverage, are the story."
)

membership_rows = []
for mode_name, ids in WORK_MODES.items():
    row: dict[str, str] = {
        "Work mode": mode_name,
        "Exact set": " + ".join(short_id(cid) for cid in sorted(ids)),
    }
    for cid in all_scope:
        row[short_id(cid)] = "included" if cid in ids else "—"
    membership_rows.append(row)
st.dataframe(pd.DataFrame(membership_rows), hide_index=True)
st.caption("Exact memberships, transcribed from the curated WORK_MODES mapping defined in this app.")

st.divider()
st.caption(f"Rendered fully offline from `{EVIDENCE_FILENAME}` · no network calls, secrets, or external services.")
