# You asked for a map. We built a GPS and a heads-up display.

*(Comp 11 Cartographer entry)*

## The problem it solves

Ulteemate.com has information we cannot afford to get wrong:

- What products are really for sale today
- What we are allowed to promise customers
- What our buy pages must show

The files about this stuff move. Names change. People forget. So we gave each big idea
its **own address that never changes**, like `ULT.OFR-001`, and wrote one short card per
idea that says: what it is, what to check when you change it, and what to leave alone.

When a file moves or gets a new name, the address still works — there's a saved note
connecting the old spot to the new one. That's the **GPS part**: ask "where is this?",
get taken there in two steps, then stop. No wandering the whole building.

## See it live

**https://alaingrignon-oss.github.io/comp11-cartographer/**

You'll see colored blocks. A bigger block means we know more about that idea. Tap a
block and it opens up into every single fact inside it. That's the **heads-up display**.

## What's in the box

| Thing | What it is |
|------|------------|
| `package/reference/catalog.md` | The front door: the list of big ideas |
| `package/reference/cards/` | One card per idea, written for someone who knows nothing yet |
| `package/reference/registry/registry.yaml` | The address book (a computer can read it too) |
| `package/examples.md` | Four true stories of people using it — including one where we said "no" |
| `package/MAPPING-GUIDE.md` | Six steps to use this on **your own** workspace |
| `package/engine/verify_map.py` | A robot checker: makes sure the map's promises are still true |
| `package/engine/run_walk.py` | A tester: asks any AI (or person) questions and saves their answers |
| `explorer/app.py` | A bigger dashboard you can run on your own computer |
| `docs/` | The live webpage |

## How to use it

1. Open the catalog. Find your question in plain words.
2. Open **one** card. Read what changes and what doesn't.
3. Not sure? Open the one source link on the card and check.
4. **Stop.** Two steps is all it should ever take.

## Does it actually work?

We made up the test rules *before* running anything, then tried 36 times — with the map
and without.

- With the map: **18 out of 18 correct**, reading about **half** as much stuff.
- Without it: readers worked much harder and still missed the "leave this alone" lists.
- We moved a file and renamed its heading on purpose. Map users found it right away.
  Everyone else hit a dead end.
- Our own robot checker once failed all three cards (hidden numbers had erased the
  product list). We accepted the failing grade, fixed the problem, and only then handed
  out the addresses. We keep that failure on display — see the receipts.

Full results live in `docs/receipts.md`.

## Use it on your own workspace

Same six steps, start to finish, in **[`package/MAPPING-GUIDE.md`](package/MAPPING-GUIDE.md)**:
copy the folder → list your big ideas → have a person approve the addresses → run the
robot checker → ask cold questions and keep the answers → when things move, update the
note, never the address. Everything runs offline with nothing fancier than Python.

## Honest edges

Right now the map covers three ideas — the ones where getting it wrong costs money or
trust. Everything else says openly: "not covered, go here instead." A few details are
marked "we don't know yet" rather than guessed.

## Who it's for

A brand-new teammate **or** a fresh AI session with no memory of this project. Both
should be able to walk in cold and leave with the right answer.

Built with the ICM Architect skill, system-map form.
