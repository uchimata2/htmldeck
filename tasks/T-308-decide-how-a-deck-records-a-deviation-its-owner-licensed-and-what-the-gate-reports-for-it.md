---
id: T-308
title: Decide how a deck records a deviation its owner licensed, and what the gate reports for it
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-299, T-225, T-264, T-265]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: high
effort: m
created: 2026-09-13
updated: 2026-09-14
deliverables: [tools/deck/check.py, skills/htmldeck/references/build.md]
---

# T-308 — Decide how a deck records a deviation its owner licensed, and what the gate reports for it

## 1. Specify

**Outcome**
A deck whose owner licensed a departure from a rule can say so in the deck, and `check.py` reports
that failure as licensed instead of red on every run. Today there is one per-deck licence, `DS-141`'s
theme token from [T-264](T-264-ds-141s-request-licence-has-nowhere-to-put-its-number.md), and only
that rule reads it. `check.py`'s excusal mechanism excuses a **rule** from automated checking for the
whole project, not a **deck** from one rule.

**Two adopters have met this, and one of them built a wrapper for it.** the second adopter's four
permanently-failing rules led [T-225](T-225-triage-the-second-adopters-report.md) to rule that a deck
of that shape should fail at most one rule, *by an explicit decision rather than by exhaustion*, and
there is still no place to record the decision. the third adopter ended with three owner-ruled failures,
`DS-110`, `DS-100` and `DS-005`, red on every run and held by a forty-line wrapper.

**From the adopter report** `17`.

**Not a defect, and why that matters for the scope.** The three rules fire correctly on that deck, so
the gate does what it says. What is missing is vocabulary. That also separates `17` from the second adopter's
`023`, which was a rule firing outside its scope and was answered by narrowing `DS-100`.

**Scope**
- In: where a licence lives — in the deck, beside its specification, or both
- In: what a licence must carry — the rule, the reason, who licensed it, and when
- In: what the gate prints and exits with for a licensed failure, an unlicensed one, and a licence
  whose rule now passes
- In: whether some rules may never be licensed
- In: if the decision is to build it, the mechanism, proved on a seeded deck
- Out: the individual rule changes [T-265](T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md)
  and T-270 carry

**Inputs**
- the record above, and its forty-line wrapper as the shape an adopter reached for unaided
- `DS-141`'s licence token, the one precedent in this tree

**Acceptance criteria**
- [ ] the decision is recorded here with the rejected alternatives and their reasons
- [ ] if the decision is to build: a seeded deck licensing one rule shows the gate reporting it licensed,
      and the same deck with the licence removed shows it failing (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- Whether a deck may license a `hard` rule at all — the project owner. Recommended: yes, with the rule,
  the reason and the date required in the deck and printed on every run. An author who can never reach
  zero stops reading the gate, which is T-225's ruling, and a licence the gate prints stays visible
  where a wrapper hides it.
  **Answered by the owner 2026-09-13: yes, as recommended.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Run the unchanged gate on a seeded deck, with and without a licence line | the before direction, §3 |
| 2 | Decide where a licence lives, what it carries, what the gate prints and exits with, and which rules can take one | §3 |
| 3 | Build it in `check.py`: read the licences, apply them to the rows, print them on every run, and self-test each outcome | `tools/deck/check.py` |
| 4 | Document it where a builder meets the gate | `skills/htmldeck/references/build.md` |
| 5 | Prove it on the seeded decks: licensed, unlicensed, stale and incomplete, and a `sync` that keeps the line | §3 |
| 6 | Lint, then the full gate | — |

## 3. Implement

**Decisions & assumptions**
- Build it: a decision that stops at vocabulary leaves every adopter writing the wrapper, and the
  owner's answer in §1 already settled the hardest part. Reversible. — 2026-09-14
- A licence lives in the deck, as a line in its head comment, which is `shell.py`'s `NOTE` region.
  Beside the specification is rejected: the gate does not read it, and it is lost when the deck is
  sent alone. Both places is rejected as two homes for one fact (**L-13**). A project wrapper or a
  command-line list is rejected as the record's own cost, a mechanism that travels with one
  project's scripts. A `<meta>` in the head is rejected on measurement: it is DS-122's precedent,
  and `shell.py sync --write` deletes it ([T-311](T-311-keep-a-decks-chart-engine-declaration-through-a-shell-sync.md)).
  An HTML comment anywhere, the record's proposal, is rejected because only the head comment
  survives a sync. Reversible. — 2026-09-14
- A licence carries four fields, all required: the rule, the reason, who licensed it, and the date
  as `YYYY-MM-DD`. Reversible. — 2026-09-14
- A licensed failure leaves the failure list, and the run exits 0 when nothing else fails. The
  licence prints on every run with its reason, who and when, `--quiet` included, and `--json` carries
  it as `licensed`. An unlicensed failure fails as before. Reversible. — 2026-09-14
- A licence is itself a failure when its rule passes on the deck, as a stale excusal is, so the list
  cannot outlive the deviations it names. So is a licence that omits a field, is declared twice,
  names no owned rule, or sits outside the head comment. Reversible. — 2026-09-14
- Every owned rule can take a licence, `hard` rules included, by the owner's answer. No rule is
  exempt: the licence prints on every run, which is the owner's condition, and a list of exempt rules
  would be a second severity scale beside the ruleset's own. A coverage fault is not a rule and
  cannot be licensed. Reversible. — 2026-09-14
- `DS-141`'s `--motion-long` token stays as it is. It is part of that rule's statement, and a licence
  is for a rule that fails. Reversible. — 2026-09-14
- A deck with no licence prints what it printed before, so no pasted gate output moves. Reversible.
  — 2026-09-14

Every deck below is a copy of the reference deck outside the repository. "Seeded" means slide 2's
headline is a question, which fails `DS-100`.

| Case | Tool | Result |
| :--- | :--- | :--- |
| seeded, no licence | unchanged | `1 failure(s): DS-100`, exit 1 |
| seeded, a `<meta>` licence after the viewport line | unchanged | `1 failure(s): DS-100`, exit 1 |
| a `<meta>` licence, then `shell.py sync --write` | — | licence lines 1 → 0 |
| DS-122's chart-engine `<meta>`, then `shell.py sync --write` | — | declaration lines 1 → 0, raised as T-311 |
| seeded, a head-comment licence | fixed, `--quiet` | `0 failing, 1 licensed`, and the licence printed with its reason, who and when; exit 0 |
| seeded, no licence | fixed | `1 failure(s): DS-100`, exit 1 |
| no question, the licence kept | fixed | `LICENCE DS-100`: the rule does not fail on this deck; exit 1 |
| seeded, a licence with no `by` | fixed | `DS-100` and `LICENCE DS-100`: omits by; exit 1 |
| seeded, the licence as a `<meta>` after the viewport line | fixed | `DS-100` and `LICENCE`: outside the head comment; exit 1 |
| the head-comment licence, then `shell.py sync --write` | fixed | licence lines 1 → 1; `0 failing, 1 licensed`, exit 0 |

**Outputs produced**
- `tools/deck/check.py`: `head_note`, `licences_in` and `apply_licences`; the licensed failures
  printed on every run and carried in `--json`; a self-test case for each outcome
- `skills/htmldeck/references/build.md`: how a deck's owner writes a licence
- [T-311](T-311-keep-a-decks-chart-engine-declaration-through-a-shell-sync.md), raised

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| the decision is recorded here with the rejected alternatives and their reasons | **pass** | §3 |
| a seeded deck licensing one rule reports it licensed, and fails with the licence removed | **pass** | §3's table, which also runs the stale, incomplete and misplaced licences, and a licensed deck after a sync |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree, since the diff reaches `tools/deck/` |

**Child fix tasks raised**
- [T-311](T-311-keep-a-decks-chart-engine-declaration-through-a-shell-sync.md): the chart-engine
  declaration does not survive a sync

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | Built and proved on seeded decks in both directions. The first design put the licence in a `<meta>`, and a sync deleted it, so it moved to the head comment, and the same loss in DS-122's declaration is raised as T-311. No look is owed: no deck in the repository changed. |
| 2026-09-14 | -> in_progress | Step 1 ran on the unchanged gate before any edit. |
| 2026-09-14 | -> planned | Six steps. The decision in step 2 builds on the owner's answer in §1. |
| 2026-09-14 | -> specified | §1's one open question was answered by the owner on 2026-09-13. |
| 2026-09-13 | -> proposed | Raised by T-299 from the third adopter's record `17`. `PH3` and `decision`: the rules fire correctly, so no published behaviour is wrong, and the open question is the owner's. |
| 2026-09-13 | (no change) | The owner answered the open question: a deck may license a `hard` rule, with the rule, the reason and the date stated in the deck and printed on every run. Still `proposed`. |
