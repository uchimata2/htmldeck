---
id: T-150
title: Relocate the research prose in the two docstring outliers
type: deliverable
status: cancelled
phase: review
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
shipped_in: 0.2.4
owner: the project owner
business_value: low
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables: [docs/lessons/L-92.md]
---

# T-150 — Relocate the research prose in the two docstring outliers

**Cancelled 2026-08-14: there are no docstring outliers.** `CE-12`'s three figures are counts of
triple-quoted **string tokens**, not of docstrings, and in the files it names those strings are the
payloads the tools emit — probe HTML, probe JavaScript, print-variant CSS. Measured by AST role, the
"85%" file is the **least** docstring-heavy of the 38 files in `tools/`. §3 has the measurement, §4
the verdict, and the corrections to the audit are listed there. The lesson is **L-92**.

## 1. Specify

**Outcome**
Two files stop carrying a research record inside their docstrings, and carry a pointer to it instead.
**The finding is `CE-12`**, stated in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it
is not restated here.

**Docstrings are 30% of `tools/**/*.py` and that is this project's deliberate style, not a finding** —
the audit rejected the general sweep in writing (§5.1), on the method's own test. Two files sit far
outside it: `tools/portability/build_probes.py` at **85% docstring (52,408 of 61,484 bytes)** and
`tools/deck/print_variants.py` at **58%**. `tools/deck/audit.py` is 36% and the largest file in the
tree, so its 52,230 bytes of docstring is the biggest single block.

*Every figure in the paragraph above is wrong, and it is kept because it is what the task was raised
on. §3 has the corrected set.*

**The risk is the finding's own**: these are the files whose behaviour is least obvious, which is
plausibly why they carry the most explanation. A relocation that makes a probe's reasoning
unfindable costs more than it saves. **Deletion is not the change.**

**Scope**
- In: those files only, and only prose that is a research record rather than a rule for the next
  editor.
- In: the pointer left behind, which is the part that decides whether this was worth doing.
- Out: the general sweep over rationale prose. Rejected 2026-08-08 by the method's own test, and
  reopening it is not this task.
- Out: any behaviour change. Docstrings only.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting; §6.1 — `CE-12`;
  §5.1 — the rejection this task must not quietly reverse
- `R8` §4.1 — the test for whether prose is doing work

**What specifying must settle**

Three questions were listed, and **the first one answers the other two by dissolving them.**

1. **The test that separates a research record from a rule for the next editor.** `R8` §4.1 already
   states it — *does this decide anything future* — so specifying does not need a new test. What it
   needs, and what the finding never supplied, is **a test that the thing being counted is prose at
   all**. That is prior to §4.1 and is where this task went.
2. **Whether `audit.py` is in or out.** Out, with the other two. Not on the ratio-versus-volume
   tension the row names, which points both ways and would have to be argued — but because under the
   correct instrument `audit.py` is **11.6%** docstring against **16.3% for `tools/` as a whole**, so
   it is below the corpus figure rather than an outlier, and the tension has no subject.
3. **Where relocated prose lands, and what the pointer must say.** Moot. Nothing is relocated.

**Acceptance criteria**
- **AC1** — Every figure `CE-12` states is re-measured before any file is edited, with the instrument
  named and the unit it counts stated (§6.2 rule 1).
- **AC2** — The instrument is checked against a case whose answer is known by construction, before
  its output is read as a finding (§6.2 rule 5, **L-86**).
- **AC3** — Either the relocation is done, or the task is closed with the reason stated in the
  record and the audit's figures corrected in place with the old values kept (§6.2, *a correction to
  a row already written*).
- **AC4** — No tool behaviour changes, and the release gate is green.
- **AC5** — §5.1's rejection of the general sweep is neither reversed nor quietly widened.

**Open questions**
- **Is it worth doing at all?** The gain is `M` on a read path taken rarely — these files are edited
  seldom — against a risk the audit states plainly. This is the row most likely to be `cancelled` on
  its own merits rather than on size. *Answered, but not on these grounds: it is cancelled on its
  premise, not on its value.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-measure docstring share per file across `tools/**/*.py` by AST role, outside the repository | The corrected distribution, 38 files |
| 2 | If step 1 disagrees with the finding, find what the finding's instrument counted instead | The conflation named, with the arithmetic that identifies it |
| 3 | Check the instrument against a synthetic file whose answer is known by construction | Pass or fail, before any conclusion is drawn |
| 4 | Read what the counted strings in the three named files actually are | Their kind: prose, or payload |
| 5 | Decide: relocate, narrow, or cancel | The verdict in §4 |
| 6 | Correct every figure the audit states that this measurement falsifies, in place, old values kept | `CONTEXT-AUDIT.md` §5, §5.1, §6, §6.1, §8; `T-130`; `RELEASE-PHASES.md` |
| 7 | Write the portable half into the method, and the durable half as a lesson | `R8` §4.1; `L-92` |

## 3. Implement

**Decisions & assumptions**

- **The finding's instrument counted triple-quoted string tokens and reported them as docstrings** —
  2026-08-14. Three independent throwaway measures were taken over `tools/**/*.py`: docstrings by AST
  role (`ast.get_docstring` on module, class and function nodes), all triple-quoted `STRING` tokens,
  and comments. **The finding's three figures reproduce the triple-quoted token counts to within 21
  bytes and disagree with the docstring counts by up to 27×:**

  | File | `CE-12` says | Triple-quoted tokens | **Real docstrings** | Rank of 38 |
  | :--- | ---: | ---: | ---: | :--- |
  | `tools/portability/build_probes.py` | 85%, 52,408 B | 85.3%, 52,416 B | **3.2%, 1,949 B** | **38th — last** |
  | `tools/deck/print_variants.py` | 58% | 58.1% | **15.3%, 2,780 B** | 26th |
  | `tools/deck/audit.py` | 36%, 52,230 B | 36.8%, 52,251 B | **11.6%, 16,465 B** | 30th |
  | `tools/**/*.py` overall | 30% | 30.2% | **16.3%** | — |

  Four figures, four matches on the wrong unit. This is not a rounding disagreement or a stale
  denominator; it is a different quantity.

- **In these files the triple-quoted strings are payload, not prose** — 2026-08-14. `build_probes.py`
  holds four module-level constants, `PROBE_JS`, `PROBE_HTML`, `PROBE_3D_HTML` and
  `PRINT_PROBE_HTML`, opening at lines 143, 849, 890 and 1038 and running unbroken to `build()` at
  1263 — **1,120 of the file's 1,360 lines**: they *are* the probes, written out to disk by `build()`. `print_variants.py` holds `PAGINATED` and `REFLOW`, which are the CSS
  blocks the variants consist of. **Relocating them to `docs/research/` would not move an explanation
  out of a tool; it would remove the tool's output and break it.** The one reading of `CE-12` that its
  own numbers support is the one that must never be carried out.

- **The instrument was checked against a known case before its output was used** — 2026-08-14, AC2.
  A synthetic file with a 10-byte module docstring, a 5-byte function docstring and a 20-byte
  triple-quoted payload constant: expected 15 bytes of docstring, measured 15. The naive count calls
  that fixture 52% docstring against a true 15% — the same 3.5× overstatement, on a case whose answer
  is known by construction.

- **`audit.py`'s one true claim is kept.** At 16,465 bytes it *is* the largest single docstring block
  in the tree, ahead of `figures.py` at 13,527. The row's conclusion survives its arithmetic by
  coincidence and is worth nothing: 11.6% of the file, below the 16.3% corpus figure, in the largest
  file there is.

- **The genuine top of the corrected distribution is not a finding either** — `tools/tasks/query.py`
  at 57.8% and `tools/deck/paths.py` at 38.4%. Both are small files where one ordinary module
  docstring is a large share: 2,351 and 2,164 bytes. **A share is high there because the denominator
  is small, which is the distribution behaving normally.** There is no file in `tools/` where prose
  is both a large share and a large volume.

- **§5.1's rejection stands and is strengthened, not widened** — AC5. It rejected a sweep over prose
  at a claimed 30%. The real figure is 16.3%, so the sweep it rejected was half the size it thought,
  and the two outliers it carved out as survivors do not exist. Nothing in the rejection needed
  reversing; one figure inside it needed correcting.

- **Nothing in `tools/` was edited.** AC4 is met by there being no change to meet it against; the
  gate was run anyway, because a task that touches the record still has to leave it green.

**Outputs produced**

- [`../docs/lessons/L-92.md`](../docs/lessons/L-92.md) — *a share-of-file figure is a claim about a
  unit, and the instrument has to count that unit*.
- Corrections in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md), old values kept and marked,
  at §5 (the F3 family row), §5.1, §6 (the `CE-12` rank row), §6.1 (`CE-12` in full) and §8 (`BP-4`).
- A correction in [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) §3, which
  restated the same three figures.
- The portable half in
  [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §4.1 — the guard rail this finding got past.
- A method note in [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1.
- **No change to any file under `tools/`.**

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| AC1 — every figure re-measured, instrument and unit named | met | AST role, `tools/**/*.py`, 38 files. The table in §3 |
| AC2 — instrument checked against a known case first | met | 15 bytes expected, 15 measured; the naive count overstates the same fixture 3.5× |
| AC3 — relocate, or close with the reason recorded and the figures corrected | met | Closed. Five corrections in the audit, one in T-130, one in R8 |
| AC4 — no behaviour change, gate green | met | Nothing under `tools/` was touched. `python tools/check_all.py` green |
| AC5 — §5.1 neither reversed nor widened | met | Its rejection stands on a corrected figure; its carve-out is deleted because it has no subject |

**The verdict.** `cancelled`, under [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §3.1 — *a task withdrawn
because its premise proved false*. The premise is the existence of two files carrying a research
record in their docstrings. Neither exists. The relocation has no subject, and the one relocation the
finding's own numbers describe would delete two tools' payloads.

**This is not the answer the row expected to lose on.** The handoff and the task both flagged the
finding's stated risk — that these are the files whose behaviour is least obvious, so their
explanation is load-bearing — as the likely reason to withdraw. That argument was never reached: it
presumes the explanation is there, and it is 1,949 bytes.

**What the task cost, and what it bought.** The relocation was banded `s` and was never done. The
measurement that killed it took three throwaway scripts, and it corrects a document that four other
closures have been citing. **The row was rank 13 of 13 — the cheapest thing on the board to have got
wrong, and the last thing anyone would have re-measured.**

**Child fix tasks raised**
- none. The conflation is in one document's figures, corrected here; the guard rail against repeating
  it is in `R8` §4.1 and `L-92`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings; it ranked last of the thirteen and was never a candidate. **Scheduled to `plan` and no further.** The task exists partly to record a decision either way: the general sweep is already rejected in writing, and these two outliers are the only part of `F3` that survived that rejection. |
| 2026-08-14 | → specified | The `specify → plan` scope limit was lifted for the batch by the owner ([`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md) *The execution order*), so this runs the full lifecycle. Specifying found that the first of the three listed questions is prior to the other two: before asking whether prose decides anything, ask whether the counted bytes are prose. Acceptance criteria written before the measurement. |
| 2026-08-14 | → planned | Seven steps, the first three of which are measurement. Step 3 exists because §6.2 rule 5 requires it and because a scan that disagrees with a written finding by 27× is exactly the case where the scan is the likely defect. |
| 2026-08-14 | → in_progress | Step 1 disagreed with the finding on all four figures. Steps 2 and 3 identified the conflation and cleared the new instrument. Step 4 read what the strings are: probe payloads and CSS variant blocks. |
| 2026-08-14 | → cancelled | **The premise is false, so the task is withdrawn and the file kept** (§3.1). `phase: review` because all four sections were worked — the cancellation is the reviewed outcome, not an abandonment at `specify`. The corrections owed to the record are in §3 *Outputs produced*, and all of them are made. `L-92` is the rule that outlives it. |
| 2026-08-14 | (no change) | **Shipped in `0.2.4`.** The release carries this task's corrections and nothing else, and it is the first here that changes no file an adopter loads — the version moves because the published line takes the next patch number, which is `../CLAUDE.md`'s rule and not a claim that the plugin changed. |
