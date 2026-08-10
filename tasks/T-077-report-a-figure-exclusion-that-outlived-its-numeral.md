---
id: T-077
title: Report a figure exclusion that outlived the numeral it was written for
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-060, T-073]
work_package: v0.2
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-10
updated: 2026-08-10
deliverables:
  - tools/docs/figures.py
---

# T-077 — Report a figure exclusion that outlived the numeral it was written for

## 1. Specify

**Outcome**
`figures.py` reports a declaration in `EXCLUDED_PROSE` or `EXCLUDED_FENCES` whose subject is no longer
on the page, the way [`audit.py`](../tools/deck/audit.py) already reports a stale `ABSENCE_IS_A_PASS`
entry.

**Why this exists**
Found on 2026-08-10 while resuming: `figures.py` was **failing on `master`** and had been since the
gate's coverage split moved from 81 checked / 32 named to 82 / 31.

- The README's sentence was corrected to *82 of 113 … the other 31*, which is right.
- `EXCLUDED_PROSE` still declared `"32"`, with the reason *"113 - 81, stated as the remainder in the
  same sentence"*.
- So `31` was reported `UNDECLARED` and the run went red, while the excusal for a numeral no longer on
  the page sat there saying nothing.

The excusal is the half nothing watched. An entry that outlives its subject is not merely untidy: it
is a written claim about a page that no longer says what the claim describes, and the *reason* text —
here, an arithmetic identity naming `81` — goes quietly false. `audit.py` has reported exactly this
shape since T-066 (`stale`, `stale_fail`), for the same reason, in a file that already had the
discipline. This one does not.

Four documents also carried the retired 81/32 split (`CLAUDE.md`, `BRIEF.md` — which said **80** —
`EVALUATION.md`, `pipeline.md`), all corrected by hand on 2026-08-10. `figures.py` covers the root
README only, so nothing saw them, and
[T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) corrected the same figure in the
same five places once already. **Binding a figure wherever it is stated, rather than only where it is
pasted, was folded into [T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) on
2026-08-10 by the owner** rather than raised separately: it is the same binding question one scope
out, and two tasks circling one gap is how the first gets closed as *mostly done*. This task is only
the exclusion tables.

**Scope**
- In: an entry in either exclusion table whose subject does not appear on the page is reported.
- In: whether it **fails** the run or is reported like a volatile drift. Recommended below.
- Out: widening `figures.py` beyond the root README.
- Out: the excusal reasons themselves, which are prose and cannot be checked.

**Inputs**
- `tools/docs/figures.py`, `README.md`

**Acceptance criteria**
- [ ] An exclusion whose numeral or fence is not on the page is named in the run's output
- [ ] Seeding one shows the message, not merely the exit status (**L-55**)
- [ ] The live README passes with no stale entry reported

**Open questions**
- **Fail the run, or report it?** Recommended: **fail**. A stale exclusion is a claim the page
  contradicts, which is the same kind of thing as a stale figure, and `audit.py` exits on its
  equivalent. The rival is reporting it like a volatile block, which would keep the run green while a
  false statement sits in the tool — the state this task exists because of.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the open question | The decision, in §3 |
| 2 | The check, plus a seeded stale entry that shows the message | `tools/docs/figures.py` |
| 3 | Run against the live README | The green run |

## 3. Implement

**Decisions & assumptions**
- <pending>

**Outputs produced**
- <pending>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <pending>

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → proposed | Raised on the owner's decision after `figures.py` was found red on `master` for a stale exclusion, not for a stale figure. The tool watches one direction — *is every numeral on the page accounted for?* — and not the other, *is every account still about a numeral on the page?*. That asymmetry is **L-54**'s, arriving in a second file. |
