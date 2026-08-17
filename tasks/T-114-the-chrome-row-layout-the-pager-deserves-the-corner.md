---
id: T-114
title: The chrome row layout — give the pager the corner, and decide what happens to Read and Motion
type: deliverable
status: planned
phase: implement
parent: null
blocked_by: []
related: [T-035, T-036, T-112]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-12
updated: 2026-08-18
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
it is competing with the pager again. ~~**So the DS-138 work is no longer conditional — it is step one
of this task, and no chrome code is written before it lands.**~~

> **Step one was paid on 2026-08-17 by
> [T-119](T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md), and it took option 1
> above.** DS-138 now reads *every panel opens fully inside the stage* as the general obligation, and
> binds the **below** direction to a tier-two disclosure panel only, with chrome explicitly outside
> it. The audit reached this rule from the other end — a scope test asking whether a rule's wording
> reaches as far as its reason — and cited this task's blocked menu as the instance. **So Y is
> buildable, the exemption lives in the rule rather than in this task, and no argument is owed before
> the code.**
>
> **But the boundary landed one step wider than option 1 promised.** Option 1's own test was that
> *the multi-source mark is content and stays bound*. DS-138 is now bound to a **tier-two disclosure
> panel**, and **DS-105 puts the multi-source mark outside tier two by name** — its own component,
> deliberately not a `.disc`, outside DS-230's closed vocabulary. Read literally, the narrowing frees
> the mark as well, which is the thing option 1 said it must not do.
>
> **Settled 2026-08-18, before any chrome code: it does free it, and the repair is to name the mark
> beside tier two in the direction clause.** Three findings decide it.
>
> 1. **No second route binds it.** DS-105 lists the disclosure rules the mark obeys regardless —
>    DS-164, DS-163, DS-227, DS-137 — and **DS-138 is not among them.** That list is about *what may
>    be open*; direction was never in it, because until 2026-08-17 DS-138 bound every popover and no
>    list had to name it.
> 2. **The freeing is not hypothetical — it falsified two shipped citations.**
>    [`shell/components.css`](../shell/components.css)'s `.sources-box` rule carries the comment
>    *opens below the mark (DS-138)* beside the `top:calc(100% + …)` that implements it, and
>    [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.2's behaviour table reads *shut at
>    load, opens below the mark — a disclosure (DS-138)*. Both name a clause that, since the
>    narrowing, no longer reaches their subject.
> 3. **The alternative is true for the wrong reason.** *Bound by the general obligation alone* does
>    hold today: DS-105 fixes the mark **upper-right**, so a downward panel fits inside the stage and
>    an upward one leaves it. But the general obligation is about **fitting**, not about opening away
>    from the reading line — so it makes the direction an accident of where the mark sits, says
>    nothing if the mark ever moves, and leaves both citations above false, since neither is about
>    fitting.
>
> **Naming the mark costs nothing in behaviour**: the shell already opens below, the contract already
> says below, and DS-105's fixed row is where below always fits. The amendment restates what ships
> and restores two citations, which makes it the cheapest way to keep option 1's promise. It is plan
> step 5, and it lands before the first line of chrome code.

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
- *Settled 2026-08-17 by [T-119](T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md):*
  **Does DS-138 bind a chrome control menu? — no.** The rule now binds the *below* direction to a
  tier-two disclosure panel and states the general obligation separately, so chrome is bound to open
  fully inside the stage and to nothing about direction. The exemption is in the rule, which is where
  this question required it to be.
- *Settled 2026-08-18 by this task:* **Does the narrowing also free the multi-source mark? — yes, so
  DS-138's direction clause takes the mark beside tier two.** DS-105's list of disclosure rules the
  mark obeys regardless does not include DS-138, so nothing else binds it; two shipped citations
  already name DS-138 for the mark's direction and the narrowing falsified both. The amendment
  restates behaviour that already ships, so it costs nothing. Reasoning in §1 above; the edit is plan
  step 5.
- *Settled 2026-08-12:* X or Y — **Y**.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | ~~Measure the current controls width and the ruler capacity it leaves~~ — **done 2026-08-18**, `chrome_row.py` on the reference deck in real Chrome, offline: row **1726.0 du**, controls block **505.6**, gap **43.1**, so **548.8 du taken — 32% of the row** — **1177.2 left** and **17 targets as built** | the baseline number |
| 2 | Measure the capacity **Y** leaves, **after step 7** — see the sequencing note below | Y's number, against 17 |
| 3 | ~~Draw X and Y at stage proportions, against today's row~~ — **done**, [`docs/sketches/chrome-row-candidates.svg`](../docs/sketches/chrome-row-candidates.svg), revision 2 | the sketch |
| 4 | ~~Owner rules~~ — **done 2026-08-12: Y** | decision, logged |
| 5 | ~~**Settle DS-138 before any code**~~ **done 2026-08-17 by T-119**; the remaining clause was **decided 2026-08-18** (§1). What is left is the edit itself: name the multi-source mark beside tier two in DS-138's direction clause | DS-138 amended, and the two citations that already name it resolve again |
| 6 | Write the navigation container's contract row — what may sit inside it and what may not | contract |
| 7 | Build Y: a `.navbox` holding the ruler, the counter and the filled pager; a standalone `More` **outside** it whose menu opens upward; `rulerAvailableDu()` measuring the navbox rather than the whole chrome row | shell, css, js |
| 7a | **Motion leaves the menu whenever the deck loops.** DS-218 wants a persistent stop control and one behind a click is not persistent, so the placement is conditional — decided at **build** time, because a control JavaScript relocates at load is one a static gate cannot decide | the conditional control, and the rule that decides it |
| 8 | Re-derive every published figure the new row moves. **DS-217 quotes 546 du and 17 targets by name**; `tools/docs/figures.py` finds the others | figures corrected |
| 9 | Keyboard-only pass on a looping deck | DS-218 verdict |
| 10 | Render on a long deck and look at it offline | verdict |

**Sequencing note, and it costs an acceptance criterion.** Step 2 was written to run *before* the
ruling, and criterion 3 says so. It cannot: the capacity a layout leaves is a property of the
rendered row, `chrome_row.py` measures a real deck in real Chrome, and Y's row does not exist until
step 7 builds it. Deriving it on paper instead is the exact move the comment on `rulerAvailableDu()`
records as having gone wrong once already. **The owner ruled on 2026-08-12 without the number**, and
said what they ruled on — flexibility and future room, not width — so the measurement never was the
input criterion 3 assumed. **Criterion 3 therefore closes `not met`, with this as the reason.** The
measurement is still taken at step 2, because it is a real input to DS-217's bound and to whether the
ruler still clears the slide counts this project now targets; it is simply evidence about the built
row rather than a decision input. *Rewording the criterion to match would be the dishonest close
`TASK-WORKFLOW.md` §2 names.*

**Step 7's blast radius, found while planning it and larger than the step implies.** The chrome row
is not this task's to edit locally — it lives in [`shell/`](../shell/), and
[`shell/README.md`](../shell/README.md) states that **`shell.py check` compares byte for byte**, so
any edit to `shell.html`, `components.css` or `deck.js` fails **every deck already built**, through no
fault of its author. So step 7 is not one edit but a sequence, and it must run in one uninterrupted
pass with the tree frozen:

1. edit the three shell files;
2. `shell.py sync` each shipped deck — **except
   `examples/reference-deck-seeded-defects.html`, which is generated and is regenerated instead**
   ([`docs/lessons/L-77.md`](../docs/lessons/L-77.md));
3. `shell.py tokens` for any token the new components declare, since a sync cannot carry a theme
   declaration and the deck fails DS-013 afterwards on a token the author never saw;
4. re-run the gates, then `tools/docs/figures.py` — **a shell change moves every deck's byte size**,
   and those sizes are quoted across the documentation.

**Step 7a needs a mechanism that does not exist yet.** `shell.html` carries `{{SLOT}}`s where a deck
differs, and *Motion*'s conditional placement is exactly such a difference — so a build-time decision
means `shell.py` learns it, not just the markup.

> **Settled 2026-08-18 by the owner: a slot, not a `shell.py new` flag.** The decision keeps the
> difference in the markup contract, where [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md)
> can hold it; a flag would make the caller declare something the deck's own content already says.
>
> **The slot cannot be bounded to *Motion* itself, and that is the design.** `SLOTS` in
> [`tools/deck/shell.py`](../tools/deck/shell.py) is a tuple of *(slot, opening delimiter, closing
> delimiter, what it is)*, and `cut()` replaces what lies **between two literal delimiters** — the
> delimiters are literals rather than patterns deliberately, so a deck whose anchor has drifted fails
> instead of being re-anchored around. *Motion* has no varying **content**; it has a varying
> **parent** — inside `.more-menu` where the deck has nothing looping, a sibling of `.more` where it
> does. **No slot bounded to one element can express a move between two parents**, so the slot is the
> smallest region containing both positions: the chrome row's tail, from the end of the navigation
> container to the close of the `<nav>`. One slot, named for the region rather than for the control
> that moves inside it.
>
> **What decides the form is the deck's own content**, not the caller: any motion that loops or runs
> past 5 s puts *Motion* outside the menu (DS-218), and `shell.py new` writes the menu form as the
> default because a fresh deck has no motion yet. **The gate decides correctness rather than the
> builder** — `#motion` inside `.more-menu` in a deck that loops is a static fact about the built
> markup, which is exactly why step 7a insisted on build-time placement in the first place.

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

- 2026-08-18 — owner: ***Motion*'s conditional placement is a slot**, not a `shell.py new` flag —
  the difference belongs in the markup contract rather than in the caller's hands. The slot spans
  the **chrome row's tail** rather than *Motion* itself, because `cut()` swaps what sits between two
  literal delimiters and *Motion* varies by parent, not by content; the region holding both parents
  is the smallest one a slot can express. Design in §2 above.
- 2026-08-18 — **DS-138's direction clause now names the multi-source provenance box beside tier
  two** (plan step 5, and the last thing gating chrome code). The argument is §1; what the rule
  gained is the clause plus a dated note recording why the narrowing needed it. It constrains
  nothing new — `.sources-box` already opens below and DS-105 fixes the mark upper-right — so the
  two citations that name DS-138 for that direction resolve again rather than being edited.

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-138 extended, 2026-08-18. Plan step 5
  closed.
- The baseline measurement, plan step 1: `chrome_row.py`, real Chrome, offline, reference deck —
  row 1726.0 du, controls block 505.6, gap 43.1, **548.8 du taken (32%)**, 1177.2 left,
  **17 targets as built**, 13 ticks drawn, dense mode off.

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
| 2026-08-18 | → specified | The one clause T-119's narrowing left live is settled, before any code: **DS-138's direction clause takes the multi-source mark beside tier two.** The narrowing did free the mark — DS-105's list of the disclosure rules the mark obeys regardless omits DS-138, so nothing else reached it — and the freeing was not hypothetical, because it falsified two shipped citations that name DS-138 for the mark's direction, in `shell/components.css` and `COMPONENT-CONTRACT.md` §3.2. The competing reading, *bound by the general obligation alone*, is true only as an accident of DS-105's fixed upper-right row and leaves both citations false, since neither is about fitting. Naming the mark restates behaviour that already ships, so the repair costs nothing. §1 carries the argument; plan step 5 is now an edit rather than a question. |
| 2026-08-18 | → planned | The baseline is **measured rather than quoted**: `chrome_row.py`, real Chrome, offline, puts the controls and their gap at **548.8 du — 32% of the row** — leaving 1177.2 and **17 targets as built**. **DS-217 quotes 546 for that same figure**, so a published number is 2.8 du adrift *before* this task moves it; step 8 re-derives it and everything `figures.py` finds with it. Step 2 moved after step 7, and **criterion 3 is booked `not met` now rather than at review**: the capacity a layout leaves is a property of a rendered row, Y's does not exist until it is built, and the owner ruled on 2026-08-12 on flexibility having said so — the number was never the input the criterion assumed. Step 7a added: DS-218's conditional promotion of *Motion* is a **build-time** placement, because a control JavaScript relocates at load is one a static gate cannot decide. |
| 2026-08-18 | (no change) | **Plan step 5 landed** — DS-138 names the multi-source box, so nothing now gates chrome code. **Stopped deliberately before step 7**, at a boundary where no shell file is touched and no shipped deck is out of sync. Reading `shell/README.md` to plan the build found the step's real size: **`shell.py check` is byte for byte**, so editing the three shell files fails every deck already built until each is `sync`ed — the generated seeded-defects deck regenerated instead (**L-77**) — with `tokens` after it, the gates after that, and `figures.py` last, because a shell change moves every deck's byte size. That is one uninterrupted pass with the tree frozen, not an edit. **Step 7a is also short a mechanism**: `Motion`'s conditional placement is a build-time difference, and `shell.py` has no slot or flag for it, so which of the two it becomes has to be settled before the row's markup is written. Both recorded in §2 rather than discovered mid-build. |
| 2026-08-18 | (no change) | **Owner settled step 7a's mechanism: a slot.** Designing it against `shell.py`'s `SLOTS` found the constraint that decides its shape — `cut()` replaces what lies between two *literal* delimiters, and *Motion* varies by **parent** rather than by content, so no slot bounded to the control can express it. The slot is therefore the **chrome row's tail**, the smallest region containing both of *Motion*'s positions, named for the region rather than for the control. `shell.py new` writes the menu form as the default and the gate decides correctness, which is what build-time placement was for. Nothing in `shell/` touched: the edit is step 7's frozen-tree pass, and this is the design it runs from. |
