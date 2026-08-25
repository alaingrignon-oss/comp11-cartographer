# ULT.OFR-003 — Storefront product-page contract

**One sentence:** Storefront product-page contract is the purchase-facing expression rule
under which each Card 1 live offer has a canonical product page that consumes Card 2's
closed claim gate, exposes product selection and cart-add affordances, and stops before
inferring transaction, provenance, policy-publication, accessibility, admin, or
source-revision facts.

- **as_of:** 2026-08-20 · **status:** issued; active
- **Evidence grade:** A for public route/canonical/suffix/theme-marker/markup/form observations; B for public/local one-object/four-variant topology; C for historical intent and known nonconforming copy; D for transactional/administrative/provenance/source-revision state
- **Aliases:** PDP contract; product-page contract; purchase surface; storefront expression; four-route PDP family; product-template assignment

## Shape

1. **Identity and route:** one observed canonical product route per Card 1 live offer;
   ghosts receive no purchasable expression. Current public locators: Bundle →
   `/products/ulteemate-2-0-bundle`; Solo → `/products/ulteemate-drive-system-2-0`;
   Legacy Bundle → `/products/ulteemate-legacy-bundle`; Spare Spikes / Spike Pack →
   `/products/ulteemate-2-0-spike-pack`.
2. **Product information:** title, media, selection controls, availability expression,
   quantity, add-to-cart affordance.
3. **Offer facts:** names, membership, contents come only from Card 1 — never stale theme copy.
4. **Claims and policies:** all benefit/proof/FAQ/testimonial/shipping/return/guarantee
   language must pass Card 2's closed gate. Known negative: current live copy is
   `known_nonconforming` with Card 2 (immediate/first-use certainty and stronger outcome
   framing observed). Live presence does not authorize the stronger wording.
5. **Variant family:** four dedicated semantic suffixes (`eca-pdp-bundle`, `eca-pdp-solo`,
   `eca-pdp-legacy`, `eca-pdp-spikes`), shared core, optional sections vary by offer;
   Spare Spikes intentionally smaller. One shared public theme marker:
   `Live Ulteemate 2 — 2026-07-25`.
6. **Purchase expression:** product-data markup and two `/cart/add` forms observed on all
   four routes (`public_purchase_expression: observed`). Cart transaction completion and
   checkout completion remain `unverified` — no form was ever submitted.
7. **Deployment record:** observation date 2026-08-20; exact live source revision
   `unverified`. Known negatives: older Legacy route returns `404`
   (`stale_locator_404`); expected supporting-policy route `/pages/shipping-returns`
   returns `404` (`missing_at_expected_path`). Review/testimonial markers render but
   provenance is unverified; media/accessibility QA unverified.

## Hits

Product title and offer name; collection link, route, canonical locator, stale locator
status; media and product selectors; availability/quantity/add-to-cart expression; offer
contents as consumed facts; benefits/features; how-to; FAQ; policy snippets/links; proof,
review, testimonial presentation; founder story; related offers; suffix assignment;
page-level publication observation.

## Does not hit

Offer membership or contents as source truth; efficacy substantiation; testimonial
consent/provenance; external review-system records; unrelated theme-code mechanics;
cart/checkout completion; payment/tax/inventory/fulfillment/customer state;
CAD/product design; campaign execution; recovery artifacts; financial values; credentials.

## Current source locators

- `Website/storefront-readback/current-routes-and-deployment.md#Collection observation`, `#Product-route observation`, `#Negative observations`, `#Limits`
- `Website/storefront-readback/purchase-expression.md#Verified on 2026-08-20`, `#Not verified`, `#Safe rule`
- `Website/BRIEF.md#Product Page — Ulteemate 2.0 Bundle` — historical build intent only (pre-launch plan)
