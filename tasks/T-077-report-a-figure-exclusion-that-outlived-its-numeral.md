---
id: T-077
title: Report a figure exclusion that outlived the numeral it was written for
type: fix
status: done
phase: review
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
- ~~**Fail the run, or report it?**~~ **Settled 2026-08-10: fail, as recommended.** The rival —
  report it the way a volatile block is reported — loses on the same ground the recommendation
  states, and the four dead entries found within a minute of the check existing are the argument: a
  green run with four false statements in it is what had been happening.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the open question | The decision, in §3 |
| 2 | The check, plus a seeded stale entry that shows the message | `tools/docs/figures.py` |
| 3 | Run against the live README | The green run |

## 3. Implement

**Decisions & assumptions**
- **Fail the run** — 2026-08-10, as recommended, with reporting-only as the rival. Both the decision
  and its reason sit next to the arithmetic in `report()`, not only here.
- **Seed the fixture by taking the numeral off the page, not by adding a fabricated table entry** —
  2026-08-10. An invented entry tests the loop; what has to be tested is a *live* declaration going
  stale when the page moves underneath it, which is what happened. The fixture removes the first
  declared numeral from a copy of the README and requires the message to name it, and it fails loudly
  if the live README already carries a stale entry, because a green run underneath one would mean
  nothing (**L-55**).
- **The four dead entries were deleted, not rephrased** — 2026-08-10. `1.1`, `0.1`, `0.2` and `106`
  were all declared in `EXCLUDED_PROSE` and none is on the page. An exclusion is re-earned by its
  numeral coming back, and the way it asks is a red run; a rewritten reason for an absent subject is
  the same defect with better prose. **One of five entries survived.**

**What the check found the minute it existed**

| Declared | Reason it carried | On the page? |
| :--- | :--- | :---: |
| `31` | *113 − 82, the remainder in the same sentence* | yes |
| `1.1` | *a section number in `EVALUATION.md 1.1`* | no |
| `0.1` | *a release name* | no |
| `0.2` | *a release name* | no |
| `106` | *a rule ID (DS-106) without its prefix* | no |

All six `EXCLUDED_FENCES` entries are live, so the rot is on the prose side, where the page is edited
by hand and the table is not.

**And it caught a figure this session had just broken.** The run went red on `212` — the README's
size for `examples/sort-window/sort-window.html`, which
[T-071](T-071-the-intermediate-specifications-carry-their-references.md) had changed to 220 KB two
commits earlier without re-running this tool. That is the tool doing exactly its job, on a defect
introduced by the same session that was extending it, and it is the reason the README's commands are
the durable list rather than any prose about them.

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `stale_exclusions`, a `STALE` row and count
  in the report, the failure arithmetic, fixture 6, and `EXCLUDED_PROSE` reduced to its one live entry.
- [`README.md`](../README.md) — 212 KB → 220 KB, and the drifted `refcheck.py` block repasted.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| An exclusion whose numeral or fence is not on the page is named in the run's output | met | `STALE  EXCLUDED_PROSE declares '0.1' and the page no longer carries it - a release name`, plus a `STALE` line in the exclusions account so a clean run states the number it checked. |
| Seeding one shows the message, not merely the exit status | met | Fixture 6 removes a live numeral from a copy and requires the key back from `stale_exclusions`; a second assertion fails the self-test if the live README is already stale. |
| The live README passes with no stale entry reported | met | `0 stale figure(s)`, `STALE 0`, `declared 7`. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | The check found **four** dead entries on the live README, not the one it was raised for — four of five prose exclusions, every one a written reason for a numeral that had left the page. Deleted rather than rephrased. It also went red on `212`, a figure T-071 had invalidated two commits earlier in this same session without re-running the tool; corrected, and worth leaving in the record as the clearest possible statement of why this direction of the check was missing. |
| 2026-08-10 | → in_progress | Written as a standalone `stale_exclusions` rather than a fourth element of `audit`'s tuple, because three call sites unpack that tuple by name and a fourth would have made this change touch them all for nothing. |
| 2026-08-10 | → proposed | Raised on the owner's decision after `figures.py` was found red on `master` for a stale exclusion, not for a stale figure. The tool watches one direction — *is every numeral on the page accounted for?* — and not the other, *is every account still about a numeral on the page?*. That asymmetry is **L-54**'s, arriving in a second file. |
