---
id: T-102
title: data-stage is an index into STAGES, the contract does not say so, and component.py passes a name
type: fix
status: done
phase: review
shipped_in: 0.2.2
parent: null
blocked_by: []
related: [T-035, T-090, T-101]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - docs/COMPONENT-CONTRACT.md
  - tools/deck/component.py
---

# T-102 — data-stage is an index into STAGES, the contract does not say so, and component.py passes a name

## 1. Specify

**Where this came from.** The adopting project, re-authoring its deck on v0.2.1. It is `Report 4` in
that project's own defect report, written 2026-08-12.

**What happens.** A deck built strictly from `COMPONENT-CONTRACT.md` §3.2, carrying
`data-stage="Problem"` on its slides, **loses its ruler and its arrow keys**. The deck opens, renders
and reads correctly. Only navigation is gone.

`check.py` reports:

```
DS-166 arrow advances with everything closed: False
DS-113 sprite icons never used: 4 of 5
```

Neither names the cause. `shell.py check` says `OK`. **`component.py check` passes all five `DS-229`
rows**, because the attribute is present and the contract constrains nothing about its value.

## The cause

`shell/deck.js` reads the attribute as an array subscript — `STAGE_ICON[st]` — so the value must be
the **index** of the stage in `STAGES`, not the stage's name. `examples/reference-deck.html` does this
correctly, with `data-stage="0"` and `data-stage="1"`, and **is the only place it is written down.**

## Why this is a defect rather than a documentation wish

§3.2's row lists `data-stage` among `.slide`'s attributes with an empty constraint. §2 already carries
the notation for a closed value set — `attr:a/b/c`, which `data-disc` uses for DS-230's four kinds —
so the contract **can** express this and does not.

The result is that a generator following the contract exactly produces a deck that opens, renders,
passes four gates and cannot be navigated. The one artefact that would have told the author is the
example deck, which puts the reference deck back in the position of being the real specification.

**Still present at `master`:** §3.2's row is `` `.slide` | `section` | `.stage` | `1+` |
`data-name` `data-stage` `aria-label` | author `` — no value notation on any of the three.

**Scope**
- In: saying in `COMPONENT-CONTRACT.md` §3.2 what the value is — the zero-based index into the deck's
  own `STAGES` declaration.
- In: `component.py` deciding it, which is the half that matters. The value parses as an integer and
  is in range for the deck's own `STAGES` array, and both are in the file being checked.
- Out: changing `deck.js` to accept names. The index is a reasonable design; it is undocumented, which
  is a different problem.

**Acceptance criteria**
- [ ] §3.2 states the value of `data-stage`, in the notation §2 already defines
- [ ] `component.py` fails a deck whose `data-stage` is not an in-range index, and names the attribute
- [ ] The failure message points at the attribute rather than at navigation or icons

**Open questions**
- none.

## 2. Plan

**Phase: `PH1`.** A deck built strictly from the published contract comes out unnavigable, which is
a defect in the published plugin. Derived here; the task arrived with `work_package: none`.

| # | Step | Where |
| :--- | :--- | :--- |
| 1 | Say what the value is, in the Attributes notation | `COMPONENT-CONTRACT.md` §2, §3.2 |
| 2 | Read the deck's own `STAGES` length | `component.py` |
| 3 | Decide the attribute against it, naming the attribute in the message | `component.py` |
| 4 | Three failing cases and one passing one, in the self-test | `component.py` |

**The notation is the open question the spec left, and it is settled here.** §2 defines `attr:text`
and `attr:a/b/c`, and neither can express *an index into an array this document cannot see*: the
length is a per-deck fact. So §2 gains one form, `attr:#NAME`, and `.slide` reads
`data-stage:#STAGES`. **This is a deviation from the acceptance criterion**, which asked for the
notation §2 *already* defines — recorded rather than worked around, because the alternative was
`data-stage:0/1/2/3/4/5/6`, a closed set that encodes the reference deck's stage count as a contract
truth. That is the same defect one level up.

## 3. Implement

**§3.2 now says it twice — once for the gate and once for a reader.** The row carries
`data-stage:#STAGES`; the prose above the table says the value is the stage's *position*, that
`deck.js` subscripts `STAGES` and `STAGE_ICON` with it, and that `data-stage="Problem"` gives a deck
that opens, renders and reads correctly with no ruler and no arrow keys.

**`script_arrays(html)` reads the deck.** `var NAME = [...]` for each uppercase name, counted by its
quoted entries. The deck is the only place these lengths exist — the shell writes `STAGES` per deck —
so the check that decides the attribute has to read the file it is checking, not the contract.

**The failure names the attribute, not what it breaks.** Both of the deck's own symptoms were two
steps downstream: `DS-166 arrow advances with everything closed: False` and `DS-113 sprite icons
never used: 4 of 5`. What the gate says now is `.slide: data-stage is a zero-based index into STAGES
(0-7) and 2 element(s) leave it: Problem`.

**No sixth verdict row.** `verdicts()` returns five rows always, and an attribute problem is already
the first row's subject, so this rides in `structure()` where the other attribute specs live.

## 4. Review

| Criterion | Verdict | Evidence |
| :--- | :--- | :--- |
| §3.2 states the value of `data-stage`, in the notation §2 defines | **met, with a deviation** | §2 gained `attr:#NAME`; §3.2's row reads `data-stage:#STAGES`. The deviation and its reason are in §2 above |
| `component.py` fails a deck whose `data-stage` is not an in-range index, and names the attribute | **met** | The reference deck with `data-stage="2"` → `"Problem"`: row 1 FAIL, `.slide: data-stage is a zero-based index into STAGES (0-7) and 2 element(s) leave it: Problem` |
| The failure message points at the attribute rather than at navigation or icons | **met** | The message above names `.slide`, `data-stage` and the legal range, and says nothing about the ruler |

**Three wrong values are covered, not one.** A stage name, an index one past the end, and an empty
attribute fail differently, and the self-test asserts all three plus a deck declaring no `STAGES` at
all. Both example decks pass unchanged: 84 authored parts, five rows, no problems.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Filed from the adopting project's defect report, `Report 4`. The adopter reproduced the symptom, read `audit.py`'s own DS-166 implementation, and only then compared the reference deck's opening `<section>` with its own — the difference was in the first attribute either file carries. Re-verified against §3.2 on `master` before filing. |
| 2026-08-12 | → done | Phase derived as `PH1`. §2 gained one notation, `attr:#NAME`, because neither existing form can express a deck-relative range — a deviation from the acceptance criterion, recorded in §2 with the alternative it rejects. |
| 2026-08-12 | (no change) | Shipped in `0.2.2`, 2026-08-12. Named in the release's *what stops conforming* row: a deck carrying a stage name in `data-stage` newly fails. |
