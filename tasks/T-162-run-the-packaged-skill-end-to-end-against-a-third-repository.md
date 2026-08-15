---
id: T-162
title: Run the packaged skill end to end against a third repository
type: deliverable
status: done
phase: review
parent: T-137
blocked_by: []
related: [T-130, T-136, T-137, T-153]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-15
updated: 2026-08-15
deliverables: []
---

# T-162 — Run the packaged skill end to end against a third repository

## 1. Specify

**Outcome**
The `ecoctx` skill runs **all sixteen steps** against a repository that is neither the one the method
was invented in nor the one the skill ships from, and produces the two documents. The subject is
`taskmd`, chosen by the owner on 2026-08-15.

**Why this is the product test and not a loose end**
[T-137](T-137-package-the-context-economy-method-as-a-skill.md) closed with one criterion unmet, and
it is this one. **The method's rule that part 1 names no file of any one repository was a discipline
until the skill was published; it is now the thing that makes the skill installable at all.** A search
proved the *text* carries no such name — 238 distinctive names, zero hits — and that is a weaker claim
than it looks. **A search proves nothing is named. A run proves nothing is assumed.** The gap between
those two is where a portable method turns out to have one repository's habits in it, and no static
check reaches it.

**What the partial run already found, and why it is not enough**
T-137 exercised steps 1–4 against `taskmd` and got real figures: tier 1 at **6,619 bytes**, the board
at **36,393** on the read path, and a green test run printing **344 bytes** for 261 tests. Those are
measurements, and they are the half of the method that has never failed. **The half that fails is
steps 7–9**, where a technique is screened, a mechanism is named and a band is written, and none of
that was touched. Eleven of thirteen bands missed in the one graded run; a method whose measured half
has been exercised twice and whose estimated half has been exercised once is not tested.

**Scope**
- In: steps 1–11 in full, against `taskmd`, producing a ranked register and a report **in that
  repository**, not here.
- In: the search record step 5 owes, across all three axes, with saturation declared per axis and the
  empty rounds listed. **Expect the catalogue to be a delta against the existing one** rather than a
  fresh survey, and say which it was.
- In: **a written answer to *did anything have to be explained that the skill should have said*.** That
  is the output this task exists for, and it is a change to the skill rather than to `taskmd`.
- Out: implementing any finding it raises. That is `taskmd`'s decision and its own work.
- Out: phase 2. It runs after the raised work is done, and there will be none for months.
- Out: any finding about `ecoctx` itself. A skill auditing the repository it ships from is a
  different task and would not test portability at all.

**Inputs**
- The `ecoctx` skill, in its own repository, at the commit T-137 closed on.
- [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §3 — the partial run's figures, so
  steps 1–4 are re-measured rather than re-derived, and the dates are compared.

**Acceptance criteria**
- [ ] All sixteen steps are accounted for: run, or **not run with a stated reason**. A step in
      neither fails this task, which is the skill's own partition rule applied to the skill
- [x] Both documents exist in `taskmd`, and the portable half names no file of `taskmd` either
- [x] Every finding carries all eleven fields, `Controller` included — **it has never been reported on
      by a real run**, because it was added on the last day of the first one
- [x] The search record covers three axes with saturation declared per axis and the empty rounds listed
- [ ] **Every place the skill had to be explained, worked around or ignored is written down** as a
      change to the skill, separately from anything about `taskmd`
- [ ] `findings.py` runs green against the result, configured for whatever `taskmd` uses, **with no
      change to the tool** — or the change it needed is the finding
- [ ] The run's own cost is stated: what was loaded, and how much

**Open questions**
- ~~**Does the owner want findings raised as work items in `taskmd`, or only reported?**~~ **Answered
  2026-08-15 — report only.** The run produces the two documents and stops; nothing is placed on
  `taskmd`'s board by this task. **The owner owning both projects makes the objection weaker, not
  absent** — the method's upstream rule is that a handed-over item carries the sender's guess about
  someone else's priorities, and a first real run that ignores its own rule because the two owners
  happen to be the same person teaches the skill the wrong habit at the exact moment it is being
  tested for portability.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- **The run was carried out in `taskmd` by its own session, 2026-08-15, report only** — the open
  question above, answered before it started. This section assesses what it produced; it is not a
  re-run, and nothing here re-derives a figure the run measured.
- **Entries without a field table were not held to the eleven fields** — 2026-08-15. E-14, E-15,
  E-17, E-18, E-19 and *Write volume — surface D* are labelled *result, not a finding*, *family with
  no finding, reported as one*, or *rejected under F3's guard rail* in the source. Only the 14
  entries that do carry a field table were checked.
- **The packaged skill has no source in this repository, and does not need one** — 2026-08-15,
  confirmed by a full-depth search: `skills/` holds `htmldeck` alone, and the five files naming
  `ecoctx` are records about it. **It is its own public repository, `uchimata2/ecoctx`**, which
  tracks its work as GitHub issues under taskmd's issues binding. So the fifth criterion's output has
  a durable home — it is just not here, which is why this task cannot close it.

**Outputs produced**
- `taskmd`, branch `audit/ecoctx-phase1`, commit `304e52f` (2026-08-15 17:10) — two documents under
  `docs/audits/`: the portable half at **29,286 characters** (11 findings, technique catalogue,
  search record) and the project's own report at **25,758** (ranked list, load path, upstream
  section, 7-row byproduct register).
- **That branch has no upstream and is not pushed.** This project's note commit `e0a0f57` (17:46)
  sits on top of it — the one recorded in the handoff before either document had been read.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| All sixteen steps accounted for | partial | Steps 1–11 are each traceable to a section, and steps 12–16 are named collectively as phase 2, *blocked on the repairs*. **No partition names all sixteen** — the word appears in neither document. Substance yes, form no. |
| Both documents exist in `taskmd`; portable half names no file of it | **pass** | Both are in the tree at `304e52f`. A search of the portable half for `taskmd`, `METHOD.md`, `tasks/README`, `T-1__`, `SKILL.md`, `pytest` and `context T-` returns **two hits, both on lines 4–5, and both the cross-reference to the sibling document**. This is the criterion the task exists for. |
| Every finding carries all eleven fields, `Controller` included | **pass** | 14 of 14 findings with a field table carry `Controller`, verified by count — 11 in the portable half, 3 here. The tables run Surface, Family, Finding, Change, Gain, Effort, Risk, Applies to, Controller, Source under an id-and-title heading. **One caveat: `E-06` exists in neither document**, though the two declare one shared numbering space; ids run E-01–E-05 and E-07–E-20, and nothing explains the hole. |
| Search record, three axes, saturation per axis, empty rounds listed | **pass** | A/B/C at 7, 9 and 5 rounds, each with its stopping round quoted. Axis C is recorded as **not fully empty** rather than rounded up, which is the honest form of the claim. |
| Every place the skill had to be explained is written down as a change to the skill | **fail** | **Absent from both documents.** The byproduct register's 7 rows are about `taskmd`, the harness and the user; none is a change to `ecoctx`. §1 calls this *the output this task exists for*. |
| `findings.py` runs green against the result, with no change to the tool | **fail — not run** | Named nowhere in either document. The skill ships its own `tools/findings.py`, which takes `--root` and `--config`; pointed at `taskmd` it exits 1 with `report not found at AUDIT.md - set "report" in .ecoctx.json`. **The tool supports the criterion — `taskmd` was simply never configured for it.** No change to the tool is needed, so the escape clause does not apply. *(This project's older [`tools/docs/findings.py`](../tools/docs/findings.py) is a different, repo-bound tool and is not what the criterion means.)* |
| The run's own cost is stated | partial | *The load path as measured* states what the session was handed, **by observation**, at ~56,600 characters ≈ 14,200 tokens across named items with a controller each. What the audit **itself** then consumed — the skill, the three search axes, the documents read — is not stated. |

**Child fix tasks raised**
- **None here. The remainder went to `ecoctx`, which is where it can be worked** — six issues on
  [`uchimata2/ecoctx`](https://github.com/uchimata2/ecoctx/issues), 2026-08-15, all `status:proposed`
  / `phase:specify`:
  [#1](https://github.com/uchimata2/ecoctx/issues/1) the skill-change writeup (criterion 5),
  [#2](https://github.com/uchimata2/ecoctx/issues/2) `findings.py` needs the subject configured and
  the skill never says so (criterion 6),
  [#3](https://github.com/uchimata2/ecoctx/issues/3) emit the sixteen-step partition (criterion 1),
  [#4](https://github.com/uchimata2/ecoctx/issues/4) define what the run's own cost means
  (criterion 7),
  [#5](https://github.com/uchimata2/ecoctx/issues/5) assert the shared numbering space is contiguous
  (the `E-06` hole),
  [#6](https://github.com/uchimata2/ecoctx/issues/6) its `.taskmd/` and `.handoff/` configs are
  untracked.
- **This closes the skill-building work in this repository.** `ecoctx` is its own public repository
  with its own tracker; a seventh task here would be the register T-164 retired, in another shape.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → proposed | **T-137's one unmet criterion, raised as its own task because it is the product test rather than a remainder.** A search proved the skill's text names no file of the repository it came from; a run is what proves nothing is *assumed*, and no static check reaches the gap between those two. Steps 1–4 already ran against `taskmd` during T-137 and produced figures, so what is untested is precisely the half that fails: screening, naming a mechanism, and writing a band, where eleven of thirteen missed in the one graded run. `l` rather than `m` because a full sixteen-step audit is the same size as the audit that produced the method, and T-137 was scoped as packaging. **`Controller` has never been reported on by a real run** — it was added on the last day of the first one — which makes this the first test of an eleventh field as well. Publication is gated on it. |
| 2026-08-15 | specify → review | **The run happened elsewhere and its results have been assessed against the seven criteria: three pass, two partial, two fail.** The portability criterion — the one the task exists for — passes cleanly: the portable half names no file of `taskmd` beyond the cross-reference to its sibling, and a run proves that where the earlier search could not. `Controller` is reported on by a real run for the first time, 14 of 14. **The two failures are both about this side of the boundary, not about `taskmd`.** The skill-change writeup is absent, and its home is `uchimata2/ecoctx`'s issue tracker rather than anything here. `findings.py` was never run: the skill's own tool takes `--root` and `--config` and would have worked, but `taskmd` was never given the `.ecoctx.json` it asks for. Also open: `E-06` is missing from a numbering space both documents declare shared. Phase advanced to `review` because the deliverable exists and is being assessed; status stays `proposed` because two criteria are unmet. |
| 2026-08-15 | → done | **Closed with two criteria unmet, the way T-137 closed with one — the unmet part is raised where it can be worked, and here it is not this repository.** The owner ruled the skill-building process closed here on 2026-08-15. The six remaining items are `uchimata2/ecoctx` issues [#1](https://github.com/uchimata2/ecoctx/issues/1)–[#6](https://github.com/uchimata2/ecoctx/issues/6), each carrying its own evidence rather than a pointer to this file, so they stand without it. **What this task set out to prove, it proved**: a run, not a search, is what shows nothing is assumed, and the portable half came through naming no file of its subject. **What it could not prove is that the skill teaches its own run** — criterion 5 asked the run to say what it had to be told, and the run said nothing, which is not the same as nothing being wrong. That question is `ecoctx` #1 and it is the one at risk of decay, because the session that hit the friction is gone. |
