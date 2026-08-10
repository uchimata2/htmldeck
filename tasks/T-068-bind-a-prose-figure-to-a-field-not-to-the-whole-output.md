---
id: T-068
title: Bind a prose figure to the field that produces it, not to the whole output
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-060]
work_package: v0.2
owner: the project owner
business_value: medium
effort: s
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-068 — Bind a prose figure to the field that produces it, not to the whole output

## 1. Specify

**Outcome**
`figures.py` reports a prose numeral as `compared` only when it matches **the figure it claims to
be**, rather than when it occurs anywhere in the union of the bound commands' output.

**Why this one**
Raised by [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md)'s
review as the gap that task deliberately did not close. The check confirms a numeral **occurs**
somewhere in the corpus. So if the README's *"the judgement half is 25 `hard` rules"* were edited to
say **81**, the run stays green: `81` is in the gate's account as `checked 81`. The number would be
correct, present in the corpus, and describing the wrong thing.

**This is a weaker version of the false pass T-060 already fixed once.** Three prose figures were
matching rule IDs — `163` against `DS-163`, `113` against `DS-113`, `221` against `DS-221` — and were
reported as `compared`. Tightening the word boundary fixed those, and it fixed the *symptom*: the
binding is still numeral-to-corpus rather than numeral-to-field, so a different coincidence produces
the same false pass. **A check that reports a coincidence as a comparison is the failure this
repository treats hardest** (**L-36**, **L-44**).

**Scope**
- In: the prose pass in [`tools/docs/figures.py`](../tools/docs/figures.py) — how a numeral is bound
  to a figure.
- In: whatever the README has to say for that binding to be possible. If a sentence cannot name
  which figure it quotes, that is a finding about the sentence.
- Out: the fenced-block pass, which is bound by adjacency and is not affected.
- Out: the `volatile` split, settled in T-060 and not reopened here.
- Out: spelled-out numbers, excluded as a class in T-060 with the closing condition stated there.

**Inputs**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `audit`'s prose pass and `EXCLUDED_PROSE`.
- [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md) §4 — the gap as
  the review stated it, and the coincidence that motivated it.
- [`docs/LESSONS.md`](../docs/LESSONS.md) **L-44** — a check that ran, found nothing to look at and
  said `pass`; **L-54** on deriving a fixture's inputs from the thing being modelled.

**Acceptance criteria**
- [ ] A prose numeral moved to a sentence describing a different figure **fails the run**,
      demonstrated on a staled copy — the `25` → `81` case above is the fixture
- [ ] The binding is derived from the document or the command output, not from a hand-kept table of
      which sentence quotes which field (**L-54**)
- [ ] Any sentence that cannot be bound is reported as undeclared rather than passing quietly, so
      the partition still holds
- [ ] No numeral currently reported as `compared` regresses to `excluded` to make the check pass —
      the count of genuinely compared prose figures does not go down

**Open questions**
- **Does the README have to change for this to be possible?** A sentence like *"the judgement half
  is 25 `hard` rules"* names its figure in words a person reads but not in anything a parser can
  bind to. The candidates are a marker in the prose, deriving the binding from the nearest matching
  label in the command's output, or accepting that some sentences stay undeclared. Whoever works
  this decides it; the criteria admit any of the three.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- none yet

**Outputs produced**
- none yet

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → proposed | Raised by [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md)'s review, which closed with this gap named rather than buried. **v0.2**: the figures on the published page are correct today and T-060's check keeps the stale-figure class red, so nothing shipped is wrong — this closes a *false pass* that needs a second coincidence to bite. `medium` rather than `high` for that reason, and because T-060 already removed the instance that was actually firing. |
