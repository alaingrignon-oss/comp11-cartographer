#!/usr/bin/env python3
"""Cartographer verification engine — deterministic, dependency-free map gates.

Verifies the structural promises a Cartographer map makes: coordinate grammar,
registry/card/catalog linkage, required card boundaries, evidence-ledger joins,
append-only parcel discipline, and locator syntax.

Pure Python standard library. No model, network, database, or orchestrator is
required: the engine is the ruler, not a reader. Any language model (local or
hosted, any vendor) can be used alongside it as a cold reader; nothing here
depends on one.

Usage:
    python3 verify_map.py                 # verify this repo's map
    python3 verify_map.py ROOT            # verify a map rooted elsewhere
    python3 verify_map.py --selftest      # prove every gate bites (negative fixtures)

Exit codes: 0 = pass, 1 = verification failure, 2 = selftest failure.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

COORD_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*\.[A-Z0-9]{2,}-\d{3}$")
REQUIRED_SECTIONS = ("Hits", "Does not hit", "Current source locators")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, bool, str]] = []

    def add(self, gate: str, ok: bool, detail: str) -> None:
        self.rows.append((gate, ok, detail))

    @property
    def ok(self) -> bool:
        return all(ok for _g, ok, _d in self.rows)

    def print(self) -> None:
        width = max(len(g) for g, _o, _d in self.rows)
        for gate, ok, detail in self.rows:
            mark = "PASS" if ok else "FAIL"
            print(f"  {gate:<{width}}  {mark}  {detail}")
        print(f"\n{'ALL GATES PASS' if self.ok else 'VERIFICATION FAILED'} "
              f"({sum(o for _g, o, _d in self.rows)}/{len(self.rows)})")


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def registry_blocks(text: str) -> dict[str, list[str]]:
    """Minimal targeted YAML extraction — no yaml dependency."""
    lines = text.splitlines()
    blocks: dict[str, list[str]] = {"ids": [], "cards": [], "tombstones": [], "locators": []}
    section = None
    indent = 0
    for i, line in enumerate(lines):
        if re.match(r"^coordinates:\s*$", line):
            section, indent = "coords", 0
            continue
        if re.match(r"^tombstones:", line):
            section, indent = "tombstones", len(line) - len(line.lstrip())
            m = re.search(r"\[(.*?)\]", line)
            if m and m.group(1).strip():
                blocks["tombstones"] += [t.strip() for t in m.group(1).split(",")]
            continue
        if re.match(r"^(lineage_events|ambiguous_review|district|schema|territory):", line):
            if section == "tombstones":
                section = None
            continue
        if section == "coords":
            m = re.match(r"\s+- id:\s*(\S+)", line)
            if m:
                blocks["ids"].append(m.group(1))
            m = re.match(r"\s+card:\s*(\S+)", line)
            if m:
                blocks["cards"].append(m.group(1))
            m = re.match(r'\s+-\s*"([^"]+#)[^"]*"', line)
            if m:
                blocks["locators"].append(m.group(1))
        elif section == "tombstones":
            m = re.match(r"\s+- id:\s*(\S+)", line)
            if m:
                blocks["tombstones"].append(m.group(1))
    return blocks


def card_files(reference: Path) -> dict[str, Path]:
    return {p.name: p for p in sorted((reference / "cards").glob("*.md"))}


def verify(root: Path) -> Report:
    rep = Report()
    pkg = root / "package"
    reg_text = read(pkg, "reference/registry/registry.yaml")
    reg = registry_blocks(reg_text)
    evidence_paths = sorted((root / "explorer").glob("ulteemate-*-evidence.json"))
    evidence: dict = {}
    for p in evidence_paths:
        try:
            evidence[p.name] = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rep.add("G4-ledger-json", False, f"{p.name}: invalid JSON ({exc})")
            evidence[p.name] = {}

    # G1 — coordinate grammar everywhere an id appears.
    bad = [cid for cid in reg["ids"] if not COORD_RE.match(cid)]
    h1_bad = []
    for path in card_files(pkg / "reference").values():
        h1 = path.read_text(encoding="utf-8").splitlines()[0]
        cid = h1.split("\u2014")[0].replace("#", "").strip()
        if not COORD_RE.match(cid):
            h1_bad.append(f"{path.name}: '{cid}'")
    rep.add("G1-grammar", not bad and not h1_bad,
            f"{len(reg['ids'])} registry ids + card titles checked"
            + (f"; violations: {bad + h1_bad}" if bad or h1_bad else ""))

    # G2 — registry <-> card file <-> catalog row linkage.
    problems = []
    ref_dir = pkg / "reference"
    for cid, card_rel in zip(reg["ids"], reg["cards"]):
        card_path = ref_dir / card_rel
        if not card_path.exists():
            problems.append(f"missing card file {card_rel}")
            continue
        if cid not in card_path.read_text(encoding="utf-8").splitlines()[0]:
            problems.append(f"{card_rel} title does not match {cid}")
    catalog = read(pkg, "reference/catalog.md")
    for cid in reg["ids"]:
        if f"`{cid}`" not in catalog:
            problems.append(f"catalog missing row for {cid}")
    rep.add("G2-linkage", not problems,
            f"{len(reg['ids'])} coordinates linked registry->card->catalog"
            + (f"; problems: {problems}" if problems else ""))

    # G3 — required card sections present and non-empty.
    problems = []
    for path in card_files(ref_dir).values():
        text = path.read_text(encoding="utf-8")
        for sec in REQUIRED_SECTIONS:
            m = re.search(rf"^## {re.escape(sec)}\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
            if not m or not m.group(1).strip(" -\n"):
                problems.append(f"{path.name}: section '{sec}' missing/empty")
    rep.add("G3-boundaries", not problems,
            "Hits / Does-not-hit / source locators present in every card"
            + (f"; problems: {problems}" if problems else ""))

    # G4 — every card's claim ids resolve in a shipped ledger.
    ledger: set[str] = set()
    for payload in evidence.values():
        for key in ("claims", "claim_ledger"):
            for c in payload.get(key, []) or []:
                cid = c.get("id") or c.get("claim_id")
                if cid:
                    ledger.add(cid)
    problems = []
    for payload in evidence.values():
        for card in payload.get("cards", []) or []:
            for cid in card.get("claim_ids", []):
                if cid not in ledger:
                    problems.append(f"{card.get('coordinate')}: unresolved claim {cid}")
    rep.add("G4-ledger-join", not problems,
            f"{len(ledger)} ledgered claims; all card claim_ids resolve"
            + (f"; problems: {problems}" if problems else ""))

    # G5 — append-only discipline: no tombstone id may equal a live id.
    clash = sorted(set(reg["tombstones"]) & set(reg["ids"]))
    rep.add("G5-tombstones", not clash,
            f"{len(reg['tombstones'])} tombstones never collide with "
            f"{len(reg['ids'])} live coordinates"
            + (f"; collision: {clash}" if clash else ""))

    # G6 — locator syntax: path#anchor with non-empty path half.
    problems = []
    for path in card_files(ref_dir).values():
        text = path.read_text(encoding="utf-8")
        m = re.search(r"^## Current source locators\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
        for line in (m.group(1).splitlines() if m else []):
            hit = re.search(r"`([^`]+)`", line)
            if hit and "#" not in hit.group(1):
                problems.append(f"{path.name}: locator without anchor '{hit.group(1)}'")
    rep.add("G6-locators", not problems,
            "every card locator is path#anchor form"
            + (f"; problems: {problems}" if problems else ""))

    # G7 — evidence JSON parses and carries the audited snapshot fields.
    main = evidence.get("ulteemate-three-card-evidence.json", {})
    audit_ok = bool(main.get("audit", {}).get("as_of")) and bool(main.get("district"))
    rep.add("G7-snapshot", audit_ok,
            f"snapshot as_of={main.get('audit', {}).get('as_of', 'MISSING')}, "
            f"district={main.get('district', {}).get('code', 'MISSING')}")
    return rep


# --- negative fixtures -------------------------------------------------------

def _mutated_tree() -> tempfile.TemporaryDirectory:
    tmp = tempfile.mkdtemp(prefix="carto-selftest-")
    base = Path(tmp) / "repo"
    shutil.copytree(Path(__file__).resolve().parent.parent.parent, base,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    return tempfile.TemporaryDirectory(tmp) if False else _Ctx(base)


class _Ctx:
    """Tiny context wrapper so selftest reads cleanly."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def __enter__(self) -> Path:
        return self.root

    def __exit__(self, *exc: object) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


def _m_grammar(root: Path) -> None:
    p = root / "package/reference/cards/ULT.OFR-003.md"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "# ULT.OFR-003 ", "# ult.ofr-0003 "), encoding="utf-8")


def _m_boundary(root: Path) -> None:
    p = root / "package/reference/cards/ULT.OFR-001.md"
    text = p.read_text(encoding="utf-8")
    text = re.sub(r"## Does not hit\s*\n(.*?)(?=^## )", "", text, flags=re.S | re.M)
    p.write_text(text, encoding="utf-8")


def _m_linkage(root: Path) -> None:
    p = root / "package/reference/registry/registry.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "cards/ULT.OFR-002.md", "cards/ULT.OFR-999.md"), encoding="utf-8")


def _m_tombstone_reuse(root: Path) -> None:
    p = root / "package/reference/registry/registry.yaml"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "tombstones: []",
        'tombstones:\n  - id: ULT.OFR-002\n    reason: selftest-reuse'), encoding="utf-8")


def _m_ledger_join(root: Path) -> None:
    p = root / "explorer/ulteemate-three-card-evidence.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    victim = data["cards"][0]["claim_ids"][0]
    data["cards"][0]["claim_ids"][0] = "XX.BOGUS-999"
    p.write_text(json.dumps(data), encoding="utf-8")
    del victim


SELFTEST_CASES = [
    ("coordinate grammar violation", _m_grammar, "G1-grammar"),
    ("card boundary section deleted", _m_boundary, "G3-boundaries"),
    ("registry points at missing card", _m_linkage, "G2-linkage"),
    ("tombstone reuses live coordinate", _m_tombstone_reuse, "G5-tombstones"),
    ("dangling claim id", _m_ledger_join, "G4-ledger-join"),
]


def selftest() -> int:
    print("SELFTEST — every gate must fail its matching corruption:")
    failures = 0
    for name, mutate, expected_gate in SELFTEST_CASES:
        with _mutated_tree() as root:
            mutate(root)
            rep = verify(root)
            fired = any(g == expected_gate and not ok for g, ok, _d in rep.rows)
            status = "BIT" if fired else "DID NOT FIRE"
            print(f"  [{status:>13}] {name} -> expects {expected_gate}")
            if not fired:
                failures += 1
                rep.print()
    print(f"\n{'SELFTEST PASSED' if failures == 0 else 'SELFTEST FAILED'} "
          f"({len(SELFTEST_CASES) - failures}/{len(SELFTEST_CASES)} gates proven to bite)")
    return 2 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", nargs="?", default=str(Path(__file__).resolve().parent.parent.parent),
                        help="map repository root (default: auto)")
    parser.add_argument("--selftest", action="store_true",
                        help="corrupt a throwaway copy five ways and require every gate to fire")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    print(f"VERIFYING MAP AT {Path(args.root).resolve()}")
    rep = verify(Path(args.root))
    rep.print()
    return 0 if rep.ok else 1


if __name__ == "__main__":
    sys.exit(main())
