# Verification engine — deterministic gates for any Cartographer map

`verify_map.py` is the ruler, not a reader. It mechanically checks the promises a
Cartographer map makes, so no reader — human or model — has to take them on faith.

## Run it

```bash
python3 package/engine/verify_map.py             # verify the map (7 gates)
python3 package/engine/verify_map.py --selftest  # corrupt a throwaway copy 5 ways;
                                                 # every gate must fail its corruption
python3 package/engine/run_walk.py --packet PACKET_DIR --question "..." \
    --reader "ollama run llama3.2" --label q1-r1   # any CLI reader
python3 package/engine/run_walk.py --packet PACKET_DIR --question "..." \
    --label q1-human                               # or manual-paste mode: no model needed
```

Pure Python standard library. No model call, no network, no database, no orchestrator,
no vendor. Runs identically on a laptop with no internet.

`run_walk.py` is the reader-agnostic harness: it freezes the exact prompt bytes, hashes
the packet manifest into a receipt, executes any command as the reader (or prints paste
instructions), and files the transcript — so walks are reproducible and comparable
across models. Scoring stays external by design: apply the key you declared *before*
running.

| Gate | Promise it enforces |
|---|---|
| G1 grammar | Every coordinate matches `<territory>.<DISTRICT>-NNN`; ids are never malformed |
| G2 linkage | Registry → card file → catalog row all agree for each coordinate |
| G3 boundaries | Every card states non-empty **Hits** and **Does not hit** plus source locators |
| G4 ledger join | Every claim a card cites resolves to an entry in a shipped evidence ledger |
| G5 tombstones | A retired coordinate is never reassigned to a new noun |
| G6 locators | Every citation is `path#anchor` form — checkable, never vague |
| G7 snapshot | The evidence ledger carries its audited `as_of` date and district |

The selftest is the difference between a checker and a security blanket: each gate is
proven to bite by feeding it a deliberately corrupted copy of the map (bad grammar, a
deleted boundary section, a dangling card reference, tombstone reuse, a dangling claim)
and requiring the exact gate to fire. Passing alone can be theater; pass *plus*
fail-on-demand is evidence.

## Why this is model-agnostic

The engine never invokes a model, so it works with any stack. Cold-reader walks that
exercise the map are likewise model-agnostic by construction — a walk is just:

1. **Input:** one question prompt + a matched packet directory (catalog + one card +
   cited sources).
2. **Reader:** anything that can read files and answer — `ollama run`, LM Studio,
   llamafile, OpenCode, Claude, Codex, a colleague. No AriOS or executor lock-in; the
   orchestrator used during development was incidental, not required.
3. **Output:** a transcript recording files opened, answer given, and stop point.
4. **Scoring:** a predeclared mechanical key (all-elements-present checklist) applied to
   the transcript — the same spirit as this engine's gates.

Any local model becomes a testable cold reader with zero extra infrastructure.

## Why this generalizes beyond maps

The engine implements a reusable pattern for making local-model work trustworthy on any
task, not just cartography:

> **predeclared questions → matched packets → mechanical scoring → published receipts**

Swap the subject and the same four steps measure whether context material actually
improves a model's answers (accuracy, context cost, drift behavior) instead of hoping:

- *Predeclared questions* fix what will be asked before anyone answers — no moving goalposts.
- *Matched packets* give armed and unarmed readers byte-identical inputs, isolating the tool's effect.
- *Mechanical scoring* keeps judgment out of grading; a script re-derives every verdict.
- *Published receipts* keep failures visible, so the method self-corrects.

The Cartographer is instance #1 of that pattern: its benchmark ran 36 tasks across two
arms and two repetitions against exactly such a key, and this engine turns the map's own
structural claims into re-runnable checks. Bring your domain — codebase reviews, policy
QA, document pipelines — and the pattern ports unchanged.
