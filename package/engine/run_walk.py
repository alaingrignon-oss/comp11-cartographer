#!/usr/bin/env python3
"""Cartographer cold-walk harness — run the same walk on ANY reader, model or human.

A "walk" is the atomic unit of evidence for a map: one predeclared question, one
matched packet (catalog + card + cited sources), one transcript. This script makes
the reader interchangeable:

    # any CLI model — ollama, LM Studio server scripts, llamafile, opencode, etc.
    python3 run_walk.py --packet PACKET_DIR --question "..." \
        --reader "ollama run llama3.2" --label q1-ollama-r1

    # no model at all — print a prompt to paste into any chat UI, or hand to a human
    python3 run_walk.py --packet PACKET_DIR --question "..." --label q1-human-r1

    # plumbing self-test without any model (echoes the prompt back)
    python3 run_walk.py --packet PACKET_DIR --question "..." --reader "cat" --label smoke

Pure standard library. No orchestrator, no vendor SDK, no network. Scoring is
deliberately OUT of scope here: grade transcripts against a key you declared BEFORE
running (see README.md — predeclared questions, mechanical scoring).

Output per walk (under --out dir, default ./walks):
    <label>/PROMPT.md         exact bytes the reader received (or must receive)
    <label>/RAW_OUTPUT.md     reader stdout/stderr in exec mode
    <label>/TRANSCRIPT.md     transcript skeleton (manual mode) to be filled in
    <label>/receipt.meta.json label, mode, reader command, hashes, timing, exit code

Exit codes: 0 = walk completed, 2 = usage/environment error, 124 = reader timeout.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

PROMPT_TEMPLATE = """# Cartographer cold-reader task — {label}

You are a cold reader: you have no prior memory of this territory and no time to
explore it all. Your budget is two hops: catalog -> at most ONE card -> cited sources,
then stop.

## Question

{question}

## Materials

All files you may read are under the packet root:

    {packet_root}

Nothing outside that directory exists for you. Do not assume sibling cards, registries,
or parent folders.

## Required answer format (use these exact headings)

FILES OPENED:
WRONG TURNS:
FIRST CORRECT SOURCE:
ANSWER:
HITS:
DOES NOT HIT:
UNRESOLVED:

Rules: cite every claim as `path#heading`; if a locator fails, record it as a wrong turn
instead of guessing; never present an unverified state as fact; stop after answering.
"""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest(packet_root: Path) -> list[dict]:
    entries = []
    for p in sorted(packet_root.rglob("*")):
        if p.is_file():
            data = p.read_bytes()
            entries.append({"path": str(p.relative_to(packet_root)),
                            "bytes": len(data), "sha256": sha256_bytes(data)})
    return entries


def write_prompt(out_dir: Path, label: str, question: str, packet_root: Path) -> Path:
    out_dir = out_dir / label
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = out_dir / "PROMPT.md"
    prompt_path.write_text(
        PROMPT_TEMPLATE.format(label=label, question=question.strip(),
                               packet_root=packet_root.resolve()),
        encoding="utf-8")
    return prompt_path


def write_meta(out_dir: Path, label: str, *, mode: str, question: str,
               packet_root: Path, reader: str | None, prompt_path: Path,
               exit_code: int | None, duration_s: float | None) -> None:
    meta = {
        "label": label,
        "mode": mode,
        "utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "question_sha256": sha256_bytes(question.strip().encode("utf-8")),
        "packet_root": str(packet_root.resolve()),
        "packet_manifest_sha256": sha256_bytes(
            json.dumps(manifest(packet_root), sort_keys=True).encode("utf-8")),
        "reader_command": reader,
        "prompt_file": str(prompt_path),
        "exit_code": exit_code,
        "duration_seconds": duration_s,
        "scoring": "external; apply your predeclared key to the transcript",
    }
    (out_dir / label / "receipt.meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8")


def run_exec(reader: str, prompt_path: Path, timeout: int) -> tuple[int, str, float]:
    argv = shlex.split(reader)
    if not argv:
        raise ValueError("--reader command is empty")
    # substitute {prompt} if the template names it; otherwise append as last arg
    argv = [prompt_path.as_posix() if "{prompt}" in a else a for a in argv]
    if not any(prompt_path.as_posix() == a for a in argv):
        argv.append(prompt_path.as_posix())
    started = dt.datetime.now()
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    duration = (dt.datetime.now() - started).total_seconds()
    blob = [f"$ {' '.join(shlex.quote(a).replace('{prompt}', str(prompt_path)) for a in argv)}",
            "--- stdout ---", proc.stdout or "(empty)",
            "--- stderr ---", proc.stderr or "(none)",
            f"--- exit {proc.returncode} after {duration:.1f}s ---"]
    return proc.returncode, "\n".join(blob), duration


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--packet", required=True, type=Path,
                    help="matched packet directory the reader may read from")
    ap.add_argument("--question", required=True,
                    help="the single predeclared question for this walk")
    ap.add_argument("--label", required=True, help="unique walk id, e.g. q1-ollama-r1")
    ap.add_argument("--reader", default=None,
                    help="reader command template; '{prompt}' substitutes the prompt "
                         "file path (appended if absent). Omit for manual-paste mode.")
    ap.add_argument("--timeout", type=int, default=900, help="exec-mode timeout seconds")
    ap.add_argument("--out", type=Path, default=Path("walks"), help="output root")
    args = ap.parse_args(argv)

    if not args.packet.is_dir():
        print(f"error: packet directory not found: {args.packet}", file=sys.stderr)
        return 2
    prompt_path = write_prompt(args.out, args.label, args.question, args.packet)

    if args.reader is None:
        skeleton = (f"# Transcript skeleton — {args.label}\n\n"
                    "Paste PROMPT.md into any chat model (or give it to a person).\n"
                    "Save their full answer below verbatim, then score externally.\n\n"
                    "--- begin transcript ---\n")
        (args.out / args.label / "TRANSCRIPT.md").write_text(skeleton, encoding="utf-8")
        write_meta(args.out, args.label, mode="manual", question=args.question,
                   packet_root=args.packet, reader=None, prompt_path=prompt_path,
                   exit_code=None, duration_s=None)
        print(f"MANUAL MODE — walk artifacts in {(args.out / args.label).resolve()}\n"
              f"  1. send a reader {prompt_path}\n"
              f"  2. save the reply into {(args.out / args.label / 'TRANSCRIPT.md')}\n"
              f"  3. score against your predeclared key")
        return 0

    try:
        code, output, duration = run_exec(args.reader, prompt_path, args.timeout)
    except FileNotFoundError as exc:
        print(f"error: reader command not found ({exc})", file=sys.stderr)
        return 2
    except subprocess.TimeoutExpired:
        print(f"error: reader timed out after {args.timeout}s", file=sys.stderr)
        write_meta(args.out, args.label, mode="exec", question=args.question,
                   packet_root=args.packet, reader=args.reader, prompt_path=prompt_path,
                   exit_code=124, duration_s=float(args.timeout))
        return 124
    (args.out / args.label / "RAW_OUTPUT.md").write_text(output, encoding="utf-8")
    write_meta(args.out, args.label, mode="exec", question=args.question,
               packet_root=args.packet, reader=args.reader, prompt_path=prompt_path,
               exit_code=code, duration_s=duration)
    print(f"EXEC MODE — exit {code} in {duration:.1f}s; "
          f"transcript at {(args.out / args.label / 'RAW_OUTPUT.md').resolve()}")
    return 0 if code == 0 else code


if __name__ == "__main__":
    sys.exit(main())
