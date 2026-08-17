---
id: T-159
title: Gate the text a reader follows and no checker reads
type: fix
status: done
phase: review
shipped_in: unreleased
parent: T-130
blocked_by: []
related: [T-130, T-146, T-147, T-149, T-153]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-14
updated: 2026-08-17
deliverables: [tools/docs/refcheck.py, tasks/TOOLING.md]
---

# T-159 — Gate the text a reader follows and no checker reads

## 1. Specify

**Outcome**
The class of defect that every gate here is blind to by construction becomes visible: text that a
reader acts on, sitting beside a pointer that resolves. **A link whose target is right and whose words
are wrong passes every check in this repository**, and so does a bare `§n` left behind by an
extraction.

**Why it exists**
Raised at [T-153](T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md)'s review,
2026-08-14, from [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.3. Phase 2 read the
byproduct register for a shape rather than row by row — which is `R8` §6.3's new instruction — and
**six of the eight defects found in passing turned out to be one class.** No single row could show
that; each looked like a small unrelated defect at the time it was recorded.

**The six, and what each one is.**

| Found by | The instance |
| :--- | :--- |
| T-146 | A link **label** showing a one-level path beside a target carrying the new two-level one. The link works; the words beside it are wrong from the new depth, and **no checker reads a label** |
| T-146 | A citation of an `L-nn` that was never allocated — invisible to every gate in the repository until `lessons.py` existed |
| T-147 | Three internal cross-references — *(§6.1)*, *(§3)*, *"the headings in this document"* — left pointing at the host after the text moved. **A bare `§n` is not bound to a document**, so `refcheck.py` counts it unbound and skips it, correctly by its own rule |
| T-149 | Three dangling `[[link]]`s in the memory store, **one a typo for an entry that exists**. Nothing checks these and nothing here can — the store is outside the tree |
| T-144 | A survey that named a document which had never stated the rule it was surveying |
| T-152 | A survey that **missed a copy sitting in the file the rule was being cut out of** |

**The mechanism they share.** Every one is a statement a reader follows, whose correctness is not a
property any pointer-resolver can test. `refcheck.py` proves a target exists; it cannot prove the
sentence beside the target is true. **The last two are the same failure at a different altitude** — a
survey is prose about what the repository contains, and it goes stale the moment the repository moves
(**L-96**).

**Scope**
- In: deciding **which of the six are mechanically decidable** and which are irreducibly a person's.
  A bare `§n` in a file that moved is arithmetic. A link label that lies is close to arithmetic — the
  label and the target are both in the same string. A survey that missed a copy is not.
- In: the decidable subset, gated on a trigger that already runs.
- In: **a written refusal for the rest**, naming why. `R8` §10's limits are the precedent and this
  project has refused gates before with reasons that outlived the refusal
  ([T-139](T-139-two-rows-in-brief-md-carry-a-cell-the-table-cannot-render.md) is one).
- Out: the memory store. It is outside the tree, `CLAUDE.md` forbids the repository to carry its
  paths, and T-149 already established nothing here can reach it.
- Out: widening `refcheck.py`'s adjacency rule. That rule is correct and T-147 confirmed it; the gap
  is not that it is wrong but that nothing else covers what it deliberately skips.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §10.3 — the eight, and the six that are one
  class
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §6.3 — *read the register for a shape*, which is the instruction that produced this task
- T-146 §3 and T-147 §3 — the two extractions where the class was first seen, one each
- **L-96** on a survey being evidence about the day it was taken, **L-62** on the instrument that
  produced a change not being the one that clears it

**Acceptance criteria**
- [ ] Each of the six is classified **decidable** or **a person's**, with the reason
- [ ] The decidable subset fails on seeded instances, in each direction, demonstrated rather than
      asserted (**L-86**)
- [ ] The self-test builds synthetic fixtures and does not assert the current state of a tracked file
      (**L-78**, **L-85**)
- [ ] Anything refused has its refusal written where the next person meets the question, not only here
- [ ] No existing gate's rule is widened to cover this — a new check or none (`refcheck.py`'s
      adjacency rule is correct and stays)
- [ ] `python tools/check_all.py` green, and any new tool named in exactly one of its four tables

**Open questions**
- **Is the link-label case worth a gate on its own?** It is the most mechanical of the six — label and
  target sit in one string — and it is also the only one that has bitten twice. Recommended: yes, and
  size the rest against it, because a check that decides one instance cleanly is worth more than one
  that half-decides four. — the implementer, at `plan`, after the classification in step 1.

## 2. Plan

**The classification was decided by measurement, not by argument, and the measurement decided the
shape as well as the verdict.** Two candidate rules were written as a throwaway probe over every
tracked `.md` — the second instrument, because the gates that missed this class are the wrong tool to
survey it with — and run before any of this was planned.

| Candidate rule | Candidates on the tree | Would fire | Verdict |
| :--- | ---: | ---: | :--- |
| **A** — a link **label** carrying a repo-relative `.md` path that disagrees with the link's target | 711 | **0** | build it |
| **B** — a **bare `§n`** that is not a heading in the document it sits in | 2,501 | **1,195** | refuse it |

**A is silent on a tree its owner believes is clean, which is what a gate owes before it is believed.**
Both path conventions in use here are accepted — a label written from the citing file's directory and
one written from the repository root — and that acceptance is why the 711 report nothing. T-146's own
instance still fires under it: a one-level label beside a two-level target resolves to neither.

**B fires on 48% of every bare mark in the repository, and that is the answer rather than a tuning
problem.** T-147's three instances are inside those 1,195, so the rule buys **3 true hits against
roughly 1,192 alarms**. Almost every one is a correct reference to *another* document that the
adjacency rule declined to bind — `R8 §3.1`, `EVALUATION §6.2 × §6.4`, a second mark in a sentence
whose first mark named the document. Widening adjacency is out of scope by §1 and would be wrong
anyway; resolving a bare mark against its host instead is the guess `TOOLING.md` §2 already reports
having tried, and it picks the wrong target here at scale.

**The open question is answered: yes, and it is the only one worth a gate.** Sizing the rest against
it is what produced the refusal above — a check that decides one instance cleanly beats one that
half-decides four.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Classify each of the six **decidable** or **a person's**, with the reason | §3's table |
| 2 | Add **check 4, `LYING LABEL`** to `refcheck.py` — a fourth *check*, leaving the §-adjacency rule of check 3 exactly as it is | `tools/docs/refcheck.py` |
| 3 | Extend its self-test with synthetic fixtures firing in **both** directions — a label that lies, and the two honest conventions staying quiet | same file |
| 4 | Write the refusal of B where the next person meets the question, with the two numbers in it | `tasks/TOOLING.md` §2 |
| 5 | `python tools/tasks/lint.py`, then `python tools/check_all.py` | both green |

**Why check 4 goes in `refcheck.py` rather than in a tool of its own.** A lying label is a reference
defect, which is that file's whole subject, and every input the rule needs is already assembled there
— the tracked-document walk, the `.gitignore` exclusion, the code-stripping that stops a quoted link
from being resolved, and the link regex itself. A separate tool would be a fourth copy of that
machinery carrying one rule, and would add a row to `check_all.py` for it. §1's criterion forbids
**widening an existing gate's rule** and names which rule it means; check 3's adjacency rule is not
touched, and *a new check* is what gets built.

## 3. Implement

**The classification — each of the six, with the reason**

| # | Found by | The instance | Verdict |
| :-- | :--- | :--- | :--- |
| 1 | T-146 | A link **label** naming one file beside a target that opens another | **Decidable — built.** Label and target are one string, and the comparison needs no knowledge outside it. `LYING LABEL`, check 4 |
| 2 | T-146 | A citation of an `L-nn` that was never allocated | **Decidable — already gated.** `lessons.py` check 3 was written for it after this was recorded, so the remedy landed before the classification did. Nothing to build; recorded so the row is not re-opened |
| 3 | T-147 | Three bare `§n` cross-references left pointing at the host after the text moved | **Refused, on a measurement.** 2,501 bare marks, 1,195 would fire — 3 true hits against ~1,192 alarms. `TOOLING.md` §2.1 carries the refusal and the numbers |
| 4 | T-149 | Three dangling `[[link]]`s in the memory store | **A person's, and unreachable.** Out of scope by §1: the store is outside the tree and `CLAUDE.md` forbids this repository to carry its paths |
| 5 | T-144 | A survey naming a document that had never stated the rule it surveyed | **Irreducibly a person's.** The claim is about what a document *says*, and no resolver reads meaning |
| 6 | T-152 | A survey that missed a copy in the file the rule was being cut out of | **Irreducibly a person's.** Same failure at a different altitude — a survey is prose about what the repository contains, and it goes stale the moment the repository moves (**L-96**) |

**One of six became a gate, one was already covered, one is refused with a number, and three are a
reader's.** That is the answer to §1's *Open question* — sizing the rest against the link label is
what produced the refusal, rather than a check that half-decides four.

**Decisions & assumptions**
- **Check 4 lives in `refcheck.py` rather than in a tool of its own** — the criterion forbids widening
  an existing gate's **rule** and names check 3's adjacency rule as the one it means; that rule is
  untouched, and *a new check* is what was asked for. A separate tool would have been a fourth copy of
  the document walk, the `.gitignore` handling and the code-stripping, carrying one rule, plus a row in
  `check_all.py`. — 2026-08-17
- **Both path conventions are accepted as honest** — a label written from the citing file's directory
  and one written from the repository root. Accepting only one turns a house style into 711 failures.
  The defect still fires, because a stale label resolves to neither. — 2026-08-17
- **The label is read from the raw text while `strip_code` still decides which links are read at all.**
  This repository writes the path inside a code span, so a label taken from the stripped text is blank
  — and a blank label can never lie. A check reading it that way would have reported a confident zero
  forever. It has its own self-test assertion for that reason. — 2026-08-17

**Outputs produced**
- [`../tools/docs/refcheck.py`](../tools/docs/refcheck.py) — check 4, `LYING LABEL`, plus seven
  self-test assertions: four honest shapes that must stay quiet, the defect shape that must fire, the
  code-span label that must still be read, and the fenced link that must not be.
- [`TOOLING.md`](TOOLING.md) §2.1 — what check 4 does, and the refusal of the bare-`§n` rule with the
  two numbers that decided it.

**Two things the work found that the plan did not forecast**

- **A self-test fixture opening with a parent-directory hop is a live dead pointer.**
  `points_into_repo` answers yes to a relative path unconditionally, so `no-such-dir/` cannot excuse
  one. Two fixtures did it and check 2 reported both — then reported the comment written to explain
  it, because check 2 reads code spans in prose on purpose. **Check 3 can quote a dead reference and
  check 2 cannot**, and that boundary is now written where the next fixture is drafted.
- **The two instruments agree on the count.** The throwaway probe and the shipped check both report
  711 path-shaped labels. The probe was written first and against a wrong reading of the convention —
  it reported 40-odd disagreements until the labels were read the way they are written — which is the
  only reason the honest cases are asserted in the self-test at all.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each of the six is classified **decidable** or **a person's**, with the reason | **met** | §3's table. One built, one already gated, one refused on a measurement, three a reader's |
| The decidable subset fails on seeded instances, in each direction, demonstrated rather than asserted (**L-86**) | **met** | A seeded document carrying one lying label and two honest ones was run through the **shipped entry point**: `FAIL - 1 problem(s)`, naming the lie and leaving both honest labels alone. Seed removed after the run. The unit-level assertions are additional, not the evidence — see the second finding below for why that distinction mattered here |
| The self-test builds synthetic fixtures and does not assert the current state of a tracked file (**L-78**, **L-85**) | **met** | All seven are string literals passed to the two new functions; none reads the tree. **Two of them were live dead pointers on the first attempt**, and so was the comment written to explain it — **L-34**, confirmed again |
| Anything refused has its refusal written where the next person meets the question, not only here | **met** | [`TOOLING.md`](TOOLING.md) §2.1, beside the adjacency rule the refusal turns on, with both numbers and the condition that would reverse it |
| No existing gate's rule is widened to cover this — a new check or none | **met** | Check 3's adjacency rule is untouched — its code, its regex and its self-test assertions are unchanged. Check 4 is new and shares only the document walk and the ignore handling |
| `python tools/check_all.py` green, and any new tool named in exactly one of its four tables | **met** | Green on the closing tree. **No new tool**, so the second clause has nothing to name: `refcheck.py` was already in exactly one table and check 4 did not move it |

**Where to look first if this is ever wrong.** The count printed on every run — *`n` link label(s)
name a path, 0 disagree* — is the check's own liveness signal. **If that first number ever drops to
near zero, the check has gone blind rather than the tree having gone clean**, because labels in the
hundreds do not disappear. That is the failure mode **L-114** records, and it is why the number is
printed at all rather than only the disagreements. It moved from 711 to 713 during this task's own
closing edits, which is why `TOOLING.md` §2.1 points at the run instead of quoting it.

**Nothing renders.** `TASK-WORKFLOW.md` §7 step 3 is satisfied vacuously — this task produced a
checker and two pieces of prose, and no deck, page or printed output. Said rather than skipped,
because a step passed in silence is indistinguishable from one not taken.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-17 | → done | Six classified, **one gated**. `refcheck.py` gains check 4, `LYING LABEL`; `TOOLING.md` §2.1 gains what it does and the refusal of the bare-`§n` rule with the 1,195-of-2,501 measurement behind it. Every criterion met, including the seeded demonstration through the shipped entry point rather than through the function — which is what would have caught the near-miss: the labels this check reads sit inside code spans, which the tool blanks before reading, so it was one line away from comparing 711 empty strings and printing *0 disagree* forever (**L-114**, new). Two self-test fixtures were live dead pointers on the first attempt and so was the comment explaining them — **L-34** confirmed again, no new lesson. Nothing renders, so §7 step 3 is vacuous and §4 says so. |
| 2026-08-17 | → in_progress | Implementation followed the plan without deviation. The only unforecast work was the code-span reading and two rounds of fixture collisions. |
| 2026-08-17 | → planned | Both candidate rules measured before the plan was written, with a throwaway probe rather than with the gates that missed the class. **A: 711 candidates, 0 firing. B: 2,501 bare marks, 1,195 firing.** The second number is the refusal — B buys T-147's 3 instances at the price of ~1,192 alarms over a tree believed clean, and no narrowing survives §1's *Out* on widening adjacency. The open question is answered yes for A. Check 4 goes into `refcheck.py`: the criterion forbids widening check 3's adjacency **rule**, which stays untouched, and asks for a new **check**, which this is — a tool of its own would be a fourth copy of the document walk, the ignore handling and the code-stripping for one rule. |
| 2026-08-17 | → specified | §1 stood as raised and was not rewritten. Deliverables declared, which `TOOLING.md` §3 owes at this transition: the checker, and the document where the refusal has to be readable. |
| 2026-08-14 | → proposed | Raised at the owner's acceptance on T-153's review. **Not a `CE-nn`** — the ranking closed at thirteen and phase 2 raises ordinary tasks, which is §1's Out scope in T-153. The evidence is that **six of eight byproducts are one class**, which no individual row could show and which only appeared once `R8` §6.3's *read the register for a shape* was applied. `m`, because the classification is most of the work and the gate may turn out to cover one instance rather than six. `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
