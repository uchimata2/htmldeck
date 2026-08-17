---
id: T-172
title: The shell sync falsified four published deck figures and nothing could see it
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-128, T-129, T-154]
work_package: PH3
shipped_in: 0.3.0
owner: the project owner
business_value: high
effort: xs
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - README.md
  - examples/README.md
  - docs/BRIEF.md
---

# T-172 — The shell sync falsified four published deck figures and nothing could see it

## 1. Specify

**Outcome**
`python tools/check_all.py` reaches green. The three documents that state the shipped decks' sizes
state the sizes those decks actually have, and the one numeral that no command is bound to either
gains a binding or is excused by name.

**What is wrong.** [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md)'s step 5 synced the
shell into all three decks — commit `745f6b8` — and both shipped decks grew. Nothing re-derived the
pages that quote their size, so five figures are now wrong or unwatched:

| Document | States | Actual |
| :--- | :--- | :--- |
| [`examples/README.md`](../examples/README.md) | `262 KB in one file`, `268 563 bytes` — the reference deck | 263 KB, 269 083 bytes |
| [`examples/README.md`](../examples/README.md) | `265 804 bytes` — `sort-window` | 266 324 bytes |
| [`docs/BRIEF.md`](../docs/BRIEF.md) | `262 KB` — the reference deck | 263 KB |
| [`README.md`](../README.md) | `262 KB in one file` — the reference deck | 263 KB, and **bound to nothing**: `figures.py` reports it as `UNDECLARED prose numeral 262` |

**Why it matters, and why it is not just four numbers.** Three of the four are on pages a stranger
reads before installing anything, which is the covered set
[`docs/PUBLISHING.md`](../docs/PUBLISHING.md) defines. The fourth is the finding: the root
`README.md` states the same measurement as the two bound pages and **no gate holds it to anything**,
so it can be right today and drift silently tomorrow — the exact hole
[T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md)
closed for `examples/README.md` and did not close here.

**Why nothing saw it.** `check_all.py` refused the undeclared `examples/measure-first/` deck and
exited **before running a single checker**, so the whole suite has been dark since `745f6b8`. The
`DECKS` entry that landed 2026-08-16 is what made these five visible; it did not cause them.

**Scope**
- In: correct the four stated figures against the manifest `figures.py` prints.
- In: decide the root `README.md` numeral — bind it to the artifact manifest as `examples/README.md`
  binds its own, or excuse it by name with the reason. Binding is the recommendation: an unbound
  figure on the front door is what T-129 was raised about.
- Out: `examples/measure-first/`'s own entry on `examples/README.md` and the figures that come with
  it. That is [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) step 7 and stays there.
- Out: any change to the decks themselves. The decks are correct; the prose about them is not.

**Inputs**
- `python tools/docs/figures.py` — prints both the findings and the artifact manifest they are
  compared against.
- [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) —
  the same defect on the same page, with the binding mechanism it introduced.

**Acceptance criteria**
- [ ] `python tools/docs/figures.py` exits 0
- [ ] `python tools/check_all.py` exits 0
- [ ] Every corrected figure was read off the manifest, not off a previous document
- [ ] The root `README.md` numeral is either compared or excused by name, and the record says which
      and why

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the four values off `figures.py`'s artifact manifest, never off another document | the manifest is derived from the files; a document is what went wrong |
| 2 | Correct them in `examples/README.md` (three), `docs/BRIEF.md` and `README.md` | four figures, four edits |
| 3 | Re-run and settle the root `README.md` numeral — bind it, or excuse it by name | the second half of the finding |
| 4 | `figures.py` green, then `check_all.py` green | publishing step 1 |

## 3. Implement

**Decisions & assumptions**
- **Every corrected value was read off the manifest** — 2026-08-16.
  `examples/reference-deck.html  263 KB, 269083 bytes` and
  `examples/sort-window/sort-window.html  260 KB, 266324 bytes`, as `python tools/docs/figures.py`
  prints them. `sort-window`'s rounded `260 KB` was already right and was left alone; only its exact
  byte count had moved.
- **The root `README.md` numeral needed neither of the two things §1 proposed, and §1 was wrong
  about it.** It is not unbound. `deck_facts()` binds a prose numeral by **matching it against the
  deck's actual properties**, so `262` reported `UNDECLARED` because no property has that value —
  the stale value is what unbound it. At `263` it binds and the report lists it:
  `263 'examples/reference-deck.html', printed by the deck files themselves`. Nothing was added and
  nothing excused.
- **The `refcheck.py` block on `README.md` was left alone, deliberately.** The same run reports
  `1 floor block(s) grew above what is pasted, which is reported rather than failed`. That block is
  in `figures.py`'s `FLOOR` by name, with the reason: *every count is of documents in this
  repository, so it is stale in the very commit that corrects it — re-derived three times in one
  session and wrong again each time* (T-067 §4). Refreshing it is the behaviour the declaration
  exists to stop. The two figures in it that carry its evidence, `0 broken` and `0 dead`, are
  compared exactly and are correct.

**Outputs produced**
- [`examples/README.md`](../examples/README.md) — the reference deck's `KB` and `bytes`,
  `sort-window`'s `bytes`.
- [`docs/BRIEF.md`](../docs/BRIEF.md) — the reference deck's `KB` in *Definition of done*.
- [`README.md`](../README.md) — the reference deck's `KB` on the front door.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `python tools/docs/figures.py` exits 0 | met | `0 stale figure(s)`. The `UNDECLARED` prose numeral went with the four `STALE` ones — one cause, five reports |
| `python tools/check_all.py` exits 0 | met | **26 ran, 0 failed, 0 unclassified, 0 stale.** The first clean full-gate run this repository has had |
| Every corrected figure was read off the manifest, not off a previous document | met | Four values, all from `figures.py`'s artifact manifest. `sort-window`'s `260 KB` was already correct at the rounding and was not touched |
| The root `README.md` numeral is either compared or excused by name, and the record says which and why | met — **compared**, and it always was | §3 records the correction: `deck_facts()` binds by matching the value, so a stale figure reports `UNDECLARED` rather than `STALE`. §1 read that as *bound to nothing* and it was not |

**One finding, and it is about the report rather than the page.** The same drift, on the same
property of the same file, produced two different verdicts depending on where it was written:
`STALE … claims 262 KB of examples/reference-deck.html, which is 263` in a block that links the deck,
and a bare `UNDECLARED prose numeral 262` in prose. The first names the right answer; the second
names nothing, and it is what led this task's own specification to plan a binding that already
existed. Left as an observation for the owner rather than raised: it is a message, both verdicts fail
the run, and neither lets a wrong figure through.

**Nothing here renders.** Four numerals on three pages; no deck changed and no browser was launched.
`TASK-WORKFLOW.md` §7 step 3 is not owed.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → done | Pulled forward on the owner's instruction, immediately after the batch it was raised out of. **Four numerals, four edits, and `check_all.py` is green for the first time — 26 checkers ran, none failed.** The specification was wrong in one place and the record says so: the root `README.md` figure was never unbound, and `UNDECLARED` is what a value-matched binding says when the value is wrong. Nothing was added to bind it and nothing excused. The `refcheck.py` paste on the same page stays as it is — it is a declared floor, and refreshing it is the churn the declaration exists to stop. |
| 2026-08-16 | → proposed | Raised out of the unattended batch's first item. Landing T-128's authorised `DECKS` entry let `check_all.py` past the undeclared deck for the first time since `745f6b8`; all three decks pass their per-deck gates and the run then fails at `figures.py` with five figures. Raised rather than fixed inside the batch, because the authorisation bounded that item to one line and the rest of T-128's step 7 touches the same page. |
