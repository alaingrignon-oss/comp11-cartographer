# Receipts — selected raw evidence from the cold-reader pilot

The predeclared benchmark (`BENCHMARK.md` thresholds fixed before any run) executed
2026-08-23 as a matched-packet pilot: 9 questions × 2 arms (with map / without) × 2
repetitions = **36 preserved task transcripts**. Headline: cartographer arm 18/18 HIT
(100%; safety-critical 8/8), parity 14/14 vs 10/14, median context bytes −44.9%,
median files opened 2 vs ~5–6.5, two-hop discipline 18/18, zero identity-safety or
truth-safety violations across all 36 transcripts. Independently audited
(`pilot-AUDIT.md`: "stands with listed corrections; no threshold impact").

Below: three receipts, quoted from the raw transcripts.

## 1. Necessity — the failure that justifies the map (baseline Q4)

Question: *a proof point changes — what must be reviewed, and what does not?*

The baseline reader (no map) worked honestly and hard — and still missed the boundary.
Its own transcript records:

> FILES OPENED: … directory listings of `Website/`, `Artifacts/`, `owner-reconciliation/`,
> `reference/`, `Marketing/`, `Website/storefront-readback/`, `Website/horizon-observations/`;
> `copy-and-proof.md`; `local-policy-extract.md`; `product-truth.md`;
> `company-product-description.md`; `storefront-claims.md`; `BRIEF.md`; `audience.md`;
> both storefront-readback files; `post-launch-gtm_draft.md`; both reconciliation extracts;
> the spike-QR instructions; grep sweeps for `guarantee|money-back|ninety|proof`…
>
> WRONG TURNS: tried to read four artifacts that do not exist in this snapshot; tried to
> reach `Website/Horizon/templates/*.json` — there is no `Horizon/` directory anywhere;
> followed a stale pointer to a heading that had moved.

It answered with a Hits list but never stated the map's required does-not-hit set — offer
membership, monetary/threshold values, theme mechanics, deployment/SaaS state, CAD,
campaign execution, credentials were never excluded. Both repetitions missed. Scored MISS.

The cartographer-arm reader answered the same question by opening **the card plus its four
cited locators** — and stated the complete boundary verbatim:

> DOES NOT HIT: Offer membership or contents as facts (ULT.OFR-001 territory); monetary
> values or the free-shipping threshold value; theme layout/code mechanics; live deployment
> or SaaS configuration; CAD/product design; campaign execution; credentials; independent
> validation itself.

Same question, same snapshot: ~18 opens + greps + a wrong boundary vs. one card + four
resolving locators + the exact boundary.

## 2. Drift advantage — move a file, rename its heading (Q8)

A source file moved and its heading was renamed after ratification. Which reader still
reaches the noun?

Baseline (stale `path#heading` citation):

> company-product-description.md — resolve provided pointer #Customer-Facing Copy Rules
> (V2): FAILED — full read (240 lines) shows no such heading anywhere. … Grep across the
> assigned dir … reference/product-truth.md — new home of the moved section.
>
> ANSWER: No — not via the unchanged coordinate. A bare file#heading citation breaks when
> the file moves and the heading is renamed … requires re-pointing. [The registry design]
> is documented as rules, not demonstrated.

Cartographer arm (same drift, armed with card + alias history + resolution record):

> reference/product-truth.md — checked the CURRENT locator #Customer Claim Boundary …
> heading present, body verbatim, plus an explicit provenance note (line 3).
>
> ANSWER: Yes. The reader reaches the same noun without touching the coordinate.
> ULT.OFR-002 is stable; only the mutable locator changed. A reader following the old
> reference resolves it through the recorded alias … verified on disk.

Both reps: strict cartographer advantage. The unaided readers had to *rediscover* the
move; the map's readers resolved it in two hops with on-disk proof.

## 3. Discipline — stop when told to stop

Across all 36 transcripts: every cartographer-arm walk went catalog → at most one card →
cited sources and stopped; sibling cards were never opened; registry use was limited to
supplied resolution records; zero silent re-resolution to a different noun anywhere in
either arm.

## 4. Self-correction — when the map's own gate said no

The strongest evidence a method works is a documented case where it refused its own
authors. During ratification (2026-08-20), the first independent evidence audit **blocked
all three cards**:

> The first evidence-bounded audit incorrectly blocked all three cards because mechanical
> financial redaction removed whole product rows. — SPEC.md §26

The redaction step had deleted so much of the offer sources that the four-member live
catalog could not be verified — including dropping the `Product Lineup` heading itself.
The audit's `do not ratify` verdict was correct *given the evidence it was shown*. The fix
was not to argue with the gate but to re-cut the safe packet preserving product names,
contents, and statuses while still excluding every monetary value and credential; on
re-review all three coordinates issued with explicit provisional fields.

Lesson recorded in the map's own rules: **a missing artifact is not a missing fact** —
redaction is evidence loss and must be repaired as evidence, never waved through. The
historical `do not ratify` verdict stands unedited in the record (`SPEC.md` §26); only the
later superseding decision (§28) is authoritative today.

---

*Full transcripts and scoring grounds are retained in the authoring workspace; the
predeclared key, scope, results, and independent audit summary travel with the map's
canonical evidence ledger (`explorer/ulteemate-three-card-evidence.json`).*
