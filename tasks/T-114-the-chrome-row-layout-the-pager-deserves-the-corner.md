---
id: T-114
title: The chrome row layout — give the pager the corner, and decide what happens to Read and Motion
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-035, T-036, T-112]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - docs/sketches/chrome-row-candidates.svg
  - shell/shell.html
  - shell/components.css
  - docs/COMPONENT-CONTRACT.md
---

# T-114 — The chrome row layout — give the pager the corner, and decide what happens to Read and Motion

## 1. Specify

**Outcome**
The pager reads as the primary control of the deck, because it is. Today it does not, and the reason
is ordering and weight rather than styling of the buttons themselves.

**The mechanism**
[`shell/shell.html`](../shell/shell.html) puts the controls in this order:

```
[ ruler ....................... ] [count] [prev] [next] [Read] [Motion on]
```

The two chevrons sit **between** a counter and two wide text buttons, and they are not in the corner
— *Motion on* is. Two labelled text buttons outweigh two glyphs at any styling, so the reporter's
*"next to the Read and Motion Buttons it seems very subtle"* is a description of the source order.

**The constraint that makes this more than a taste question**
**DS-218**: motion that loops or runs over 5 s ships with a **persistent, keyboard-operable** control
that stops it. DS-140's `Current` is infinite, so **every deck with a flow diagram owes one** — and
[T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md) classifies
`Current` as affordance motion, which means density 0 does not switch it off either. *Motion* is
therefore a compliance control in those decks, not chrome, and a control behind a click is not
persistent. **DS-164** rules out the other easy answer: three unlabelled lines is the unlabelled
control that rule exists to forbid.

So *Read* may move anywhere; *Motion* may only move behind a click in a deck that has nothing looping.

**The governing principle, set by the owner 2026-08-12 after seeing the first sketch**

> *"The pager and the navigation belong together. It makes no sense to put the reader and the motion
> trigger into this box, but the pager."*

**The box is for navigation.** The ruler, the counter and the pager are one thing — three renderings
of *where am I and how do I move* — and they share a container. *Read* and *Motion* are neither, and
they leave it. That single rule decides more than the first three candidates did between them: it
explains why the pager looked subtle without appealing to weight at all. The pager was not
under-styled, it was **in the wrong company**.

**DS-138, and the owner has now chosen the side of it that costs something.** The rule reads
*popovers drop below the element, never above — so the control sits high enough that its panel fits
below it on the stage*, and it names this exact case in its own reasoning: *"a control near the foot
of a 1080-unit stage cannot host a panel more than a row or two deep, and no styling of the panel
repairs it."* The chrome sits inside `.stage`, at its foot. **Option Y opens its menu upward by
design.** That is not an oversight to route around; it is the arrangement DS-138 exists to prevent,
chosen deliberately.

**So Y is only buildable if DS-138 is settled first**, one of two ways:

1. **Carve the exemption.** Argue that DS-138 governs *tier-two content the reader is reading* and
   that a two-item control menu is not that. This is the stronger argument and the one to try. If it
   wins, **the exemption is written into DS-138 with its boundary stated** — an exemption living only
   in this task is one the next control will not find.
2. **Amend DS-138.** Broader, and it weakens a rule that is doing real work elsewhere.

**Neither reaches the multi-source mark, which is content and stays bound.** That boundary is the
test of whether option 1 is a principle or an excuse.

**Option X avoids the question entirely** by opening nothing.

**The owner chose Y on 2026-08-12**, for flexibility and future room: a `More` control takes a third
and a fourth item without redesigning the row, where X's second section grows by getting wider until
it is competing with the pager again. **So the DS-138 work is no longer conditional — it is step one
of this task, and no chrome code is written before it lands.**

**The second, non-obvious payoff**
[`shell/deck.js`](../shell/deck.js) sizes the ruler from what the controls leave it:

```
capacity = floor((availDu - LABEL_MIN_DU) / TICK_PITCH_DU)      // 260 du, 52 du
availDu  = chrome width - controls width - gap                  // measured, not assumed
```

The comment on `rulerAvailableDu()` records that the controls cost **32% of the row**, and that this
number is what T-035's paper estimate got wrong. **Narrower controls buy ruler ticks.** That matters
now rather than later: the owner has said the next deck will not be limited to 12 slides, and the
ruler degrades to dense mode when the slide count passes capacity. The task must **measure** the
capacity each candidate buys, not assert it.

**The two live candidates**

Both put the nav box at `[ruler ......... count · prev · next]` with **the pager filled**, and differ
only in what happens to the two controls that left.

| | What sits outside the nav box | Costs |
| :--- | :--- | :--- |
| **Y — the More button is the section — CHOSEN** | A single standalone `More` control, **outside** the nav box rather than inside a section; its two items pop up **above** it | Narrowest controls, so the most ruler capacity, and it takes a third item without a redesign. **Needs DS-138 settled first**, and needs *Motion* promoted out of the menu whenever the deck loops, which is a conditional control a gate has to decide. |
| **X — a second section** *(not taken)* | A separate, quieter section to the right holding *Read* and *Motion*, both subtle | Opens nothing, so DS-138 never applies and DS-218 is satisfied for free. Buys the least ruler capacity, and grows by getting wider. |

**Superseded, kept for the record:** the first sketch offered *reorder only*, *labelled menu inside
the row*, and *pager as a detached cluster*. The owner rejected all three on 2026-08-12 — **not on
their arrangement but on their premise.** Every one of them kept *Read* and *Motion* inside the
navigation container and argued about ordering and weight within it. The principle above says the
container was the problem.

**Scope**
- In: **the navigation-only container**, whichever candidate wins. The ruler, the counter and the
  pager share it; nothing else may enter it. Written into
  [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) as a rule, not left as an arrangement — a
  container defined by what it is for is the only version of this that survives the next control
  somebody wants to add.
- In: **the sketch**, showing X and Y at one scale against what ships today. Delivered before
  implementation; the owner rules; then it is built. *Revision 2 — the first three candidates were
  rejected on their premise.*
- In: whichever candidate is chosen, built, with its contract rows.
- In: the measured ruler capacity each candidate yields, since that is a decision input and
  `chrome_row.py` already measures the row.
- In: keyboard order and focus ring for the chosen layout — the pager becoming primary must not make
  it later in the tab order than what it now outranks.
- In: DS-218 satisfied in both candidates, demonstrated on a deck that loops.
- In: **if Y wins, DS-138 settled first** — the exemption argued and written into the rule with its
  boundary, or the rule amended. Before any code.
- Out: **what the pager buttons do on hover and press** — the 3° rotate and the pinch are affordance
  motion and belong to [T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md).
  **That work waits on this one**: building the pager's hover behaviour before its shape is settled
  is building it twice.
- Out: the ruler's own behaviour and its dense mode — [T-035](T-035-the-ruler-navigator.md).
- Out: a second contents page — [T-036](T-036-the-second-contents-page-for-long-decks.md).

**Inputs**
- [`shell/shell.html`](../shell/shell.html) — the chrome row as it stands.
- [`shell/deck.js`](../shell/deck.js) — `rulerLayout()`, `rulerAvailableDu()`, and the 32% comment.
- [`tools/deck/chrome_row.py`](../tools/deck/chrome_row.py) — already measures the rendered row and
  fails when the shipped bound and the code disagree; it is the instrument for the capacity figure.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — **DS-218**, **DS-164**, **DS-163**,
  **DS-138**, **DS-168**, **DS-131**.

**Acceptance criteria**
- [ ] `docs/sketches/chrome-row-candidates.svg` shows X and Y against today's row at one scale, and
      the owner has ruled on it.
- [ ] The navigation container has a contract row saying what may be inside it and what may not.
- [ ] The measured ruler capacity of each candidate is recorded before the ruling, not after.
- [ ] The chosen layout is built, with contract rows for anything new.
- [ ] The pager is filled, and is the last control inside the navigation container.
- [ ] On a deck containing looping motion, a persistent keyboard-operable stop control is present —
      verified by keyboard alone, with no mouse.
- [ ] Tab order follows visual prominence.
- [ ] If Y: DS-138 carries the exemption and its boundary, and the multi-source mark is demonstrably
      still bound by it.
- [ ] `chrome_row.py` green; `check.py` green; `contrast.py` green on any new weight.
- [ ] Opened and looked at, offline, on a deck long enough to exercise the ruler's capacity bound.

**Open questions**
- **Does DS-138 bind a chrome control menu?** Live, and now unconditional — the owner chose Y. Answered
  before building, not during. A `no` needs the exemption written into DS-138 itself with its boundary
  stated, because an exemption that lives only in this task is one the next control will not find. The
  boundary's test: the multi-source mark is content and must stay bound.
- *Settled 2026-08-12:* X or Y — **Y**.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the current controls width and the ruler capacity it leaves | the baseline number |
| 2 | Measure the capacity X and Y would each leave | two numbers |
| 3 | Draw X and Y at stage proportions, against today's row | the sketch, revision 2 |
| 4 | ~~Owner rules~~ — **done 2026-08-12: Y** | decision, logged |
| 5 | **Settle DS-138 before any code** | the exemption and its boundary, in the rule |
| 6 | Write the navigation container's contract row | contract |
| 7 | Build the chosen layout | shell |
| 8 | Keyboard-only pass on a looping deck | DS-218 verdict |
| 9 | Render on a long deck and look at it offline | verdict |

## 3. Implement

**Decisions & assumptions**
- 2026-08-12 — owner: **the navigation container holds navigation only.** The ruler, the counter and
  the pager belong together; *Read* and *Motion* leave the box. This supersedes the first three
  candidates, which all argued about arrangement inside a container whose membership was the actual
  problem.
- 2026-08-12 — owner: the pager is **filled** in both surviving candidates. Not a styling detail —
  it is what makes the pager read as the deck's primary control once it is no longer competing with
  two labelled text buttons.
- 2026-08-12 — owner: in Y, the menu **opens upward**, knowingly against DS-138. Recorded as a
  deliberate choice with a cost, not as an oversight.

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. Scoped as three sketched candidates rather than as the menu, at the owner's objection. DS-218 bounds the space before it starts, and the ruler-capacity coupling is recorded because it is a decision input nobody would look for. |
| 2026-08-12 | (no change) | Drawing the sketch found DS-138 against candidate B: the chrome row is at the foot of the stage, so its menu can only open upward, which is the arrangement DS-138 names in its own reasoning. B cannot be built as drawn. Recorded in §1 with the three ways out, and as an open question the owner answers only if they pick B. |
| 2026-08-12 | (no change) | **Owner rejected all three candidates on their premise, not their arrangement** — every one kept *Read* and *Motion* inside the navigation container. Replaced by the navigation-only principle and two new candidates, X and Y. Y takes the DS-138 collision on purpose, so the question that was conditional on B is now conditional on Y and has to be settled before code rather than argued after. Sketch to be redrawn. |
| 2026-08-12 | (no change) | **Owner chose Y**, from the second sketch, on flexibility: a `More` control absorbs a third and fourth item without a redesign, where X's section grows by widening until it competes with the pager again. The DS-138 question is therefore no longer conditional — it is step one and gates every line of chrome code in this task. |
