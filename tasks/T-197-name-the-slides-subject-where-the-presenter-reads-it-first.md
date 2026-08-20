---
id: T-197
title: Name the slide's subject in the eyebrow, where a presenter reads it before speaking
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-114]
work_package: PH3
shipped_in: 0.5.0
owner: the project owner
business_value: high
effort: m
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-197 - Name the slide's subject in the eyebrow, where a presenter reads it before speaking

## 1. Specify

**Outcome**
A presenter glancing at the top of a slide learns what it is about. Today, on a well-built deck,
they cannot.

**The owner's finding, 2026-08-20**
On slides 6 and 7 of the adopter deck - a RACI chart and an AI policy, two entirely different
subjects - neither the headline, the eyebrow, the section label in the navigation row, the standfirst
nor the bottom line names the subject. The presenter has to read the whole slide to find a keyword
telling them what is now on screen. The owner asks for the factual name of the content at the top of
every slide: no indirect reference, no message, just the name.

**Where I disagree, and what I propose instead**
The owner's wording is *replacing the text of the current pages*. If that means the headline, it
collides head-on with **DS-090 - the headline is a claim, not a topic** - a `hard` rule, and one of
the three propositions §3 of the design system opens with. That rule is the reason these decks do not
read as generated, and a topic label in the headline slot is precisely the house style it was written
against. I recommend keeping DS-090 untouched.

**The eyebrow is the right slot, and it is currently carrying nothing.** `.eyebrow` holds a `.tick`
and a stage name - on the adopter deck, `13 - DECISION`. Both facts are already on the screen: the
navigation row prints `13 / 16` and the word `DECISION` at the same moment. So the eyebrow states,
in the most prominent position a slide has after the headline, two things the reader can already see
twice. Put the subject there and the slide gains the presenter's fact and loses a redundancy - which
is a separate observation from the same review pass, not a bonus argued into this one.

**No contradiction with the rest of the ruleset.** DS-091 bounds the headline and the fragments, not
the eyebrow. Nothing in the design system states a rule about eyebrow content at all - measured, the
string does not appear in `DESIGN-SYSTEM.md`. So this is a new rule in an empty slot rather than an
amendment to a full one.

**Scope**
- In: a rule for what `.eyebrow` carries, with DS-000's stated reason.
- In: whether the stage name stays beside the subject or gives way to it. My recommendation is that
  it gives way: the navigation row is the stage's home and it is always visible.
- In: whether the subject is authored or derived. Deriving it from the slide title would make it a
  second copy of the headline, which is the thing it must not be, so I expect authored - and then
  the slide specification needs a field for it.
- In: how the gate can judge it. A factual name is a reading, so this is likely `judge` rather than
  `auto`, with an `auto` half that only asserts the slot is filled and is not the headline restated.
- Out: DS-090. This task must not weaken it, and an outcome that does is the wrong outcome.

**Inputs**
- [`../docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) DS-090, DS-091, DS-202, DS-207.
- [`../docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) 3.2 - `.eyebrow`, `.tick`.

**Acceptance criteria**
- [ ] A rule exists saying what the eyebrow names, and DS-090 is unchanged.
- [ ] The three shipped decks are re-cut to it and **looked at**, per `CLAUDE.md` rule 6.
- [ ] Slides 6 and 7 of the adopter deck, or their equivalents in a shipped deck, are shown before
      and after, and a reader who has not seen the deck can say what each is about from the top
      strip alone.

**Open questions**
- Does the stage name stay in the eyebrow? Owner's call. My recommendation is no.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure how the shipped decks use the slot | 23 of 36 slides were position+stage |
| 2 | Write DS-241 and gate its mechanical half | `audit.eyebrow_verdicts` |
| 3 | Re-cut the two older decks and look | 24 eyebrows |

## 3. Implement

**Decisions & assumptions**
- **DS-090 is untouched**, as recommended at filing. The subject goes in the eyebrow, which was carrying the position and the stage - both already printed by the navigation row at the same moment.
- **The stage gives way rather than sharing the slot** - the owner's call, taken as recommended. The navigation row is the stage's home and is always visible.
- **Authored, not derived.** Deriving the subject from the slide's title would make it a second copy of the headline, which is the one thing it must not be.
- **The rule was missing rather than broken**, and the measurement is the evidence: `measure-first`, the newest deck, was already right and is what the rule was read off; the other two were not.

**Outputs produced**
- `docs/DESIGN-SYSTEM.md` DS-241
- `tools/deck/audit.py`
- `tools/deck/check.py`
- `examples/reference-deck.html`
- `examples/sort-window/sort-window.html`
- `examples/measure-first/measure-first.html`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A rule exists and DS-090 is unchanged | **pass** | DS-241, `hard` and `auto`; DS-090's row is byte-identical |
| The three shipped decks are re-cut and looked at | **pass** | 24 eyebrows; slide 5 of the reference deck rendered and read - `THE TWO PROPOSALS` over `Both options are real`, with `05 / 13` and `THE CHOICE` in the ruler |
| A reader can say what a slide is about from the top strip alone | **pass** | on the rendered slide, yes. The judgement half of the rule stays the critique pass's and is not claimed here |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | Measured first: 23 of 36 slides. |
| 2026-08-20 | -> done | Three criteria met. |
