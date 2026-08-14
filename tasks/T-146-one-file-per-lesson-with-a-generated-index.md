---
id: T-146
title: One file per lesson, with a generated index
type: deliverable
status: done
phase: review
parent: T-130
blocked_by: []
related: [T-130, T-145, T-147]
work_package: PH3
finding: CE-06
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: l
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - tools/docs/lessons.py
  - docs/LESSONS.md
  - tools/check_all.py
---

# T-146 — One file per lesson, with a generated index

## 1. Specify

**Outcome**
A lesson is fetched one at a time instead of by loading every lesson this project has learned.
**The finding is `CE-06`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**Re-measured 2026-08-14: 167,043 bytes over 2,439 lines, 89 entries** in three categories —
*Evidence and verification*, *Tooling*, *Writing*. Mean entry 1,859 bytes, median 1,846, smallest
360, largest 3,963: **a flat distribution with no outlier carrying the weight**, which is what makes
this a by-unit case rather than the by-kind case T-145 was.

**The interface is wider than the document and nothing validates it.** `L-nn` is cited **983 times
across 165 files** outside the lessons themselves — task records, project docs, research notes and
tool source. A dated reading, taken 2026-08-14 before the split; it was 1,015 across 166 by the end
of the same task, because working on lessons cites lessons. All 89 ids resolve
today and all 89 are cited at least once, so the record is currently honest. **It is honest by
accident:** `refcheck.py` resolves markdown links, prose `.md` paths and `<document> §n` references,
and `L-nn` is none of those. `taskmd check` sees front-matter and links. **A citation of a lesson
that does not exist is caught by no gate in this repository**, and a lesson deleted or renumbered
falsifies up to 872 pointers silently. That was measured while specifying, not assumed.

**The pattern already exists in this repository**, in the tracker: one file per unit, an index
generated from them, and a checker that fails when the index and the files disagree. That is the
comparison to argue against, not a new invention.

**`CE-06`'s 81× is not the gain, and must not be quoted as one.** It is the ratio of the whole
document to one entry, which is the cost only of a session that reads the file whole. **Nothing here
does that and nothing instructs it**: `../CLAUDE.md` places `LESSONS.md` outside tier 1 and says in
as many words that it may grow without limit, and a session fetching `L-73` greps for the heading and
reads the line range. Measured, that fetch is **two tool calls and about 1,859 bytes**; after this
change it is **one call and the same bytes**. `CE-02` understated its finding by twenty times
(§6.2, rule 2) and this one overstates it by about eighty — the rule is the same rule, and it cuts
both ways.

**So the case rests on three gains the finding did not claim**, in ascending order of size:

1. **One tool round-trip per fetch**, which is what the honest version of `CE-06`'s number is worth.
2. **A question that cannot be asked today.** *Have we learned anything about X* is answered by grep,
   which matches words rather than subjects, or by reading 167 KB. A generated index of 89 one-line
   hooks answers it for about 9 KB — **this is a new capability, not a saving**, and it is the same
   shape as `tasks/README.md` and the memory index this project already relies on.
3. **872 citations become checkable.** A lesson stored at its own id is a path, and a path is the
   one thing every gate here already resolves. The storage change is what turns an unvalidated
   interface into a validated one, and it is worth more than the bytes.

**And it removes an accident of the CE-13 class.** One `Read` of `LESSONS.md` with no range is
167,043 bytes, ~42,000 estimated tokens — a session. `CE-13` met the identical risk on decks and was
answered with **one line of rule at `xs`**, deliberately, rather than a restructure
([T-133](T-133-write-down-that-a-deck-is-never-read-whole.md)). **That precedent is the strongest
argument against this task and it is answered rather than ignored**: the rule was the whole remedy
there because a deck has no other reason to be split, and gains 1–3 above do not exist for an
810 KB HTML file. Here the restructure is bought by the validation gain and the rule comes free with
it. **If gains 2 and 3 were removed, the honest close would be `cancelled` plus one line of rule.**

**Scope**
- In: the storage shape, the generated index, and the checker that keeps them honest.
- In: every `L-nn` citation continuing to resolve, which `refcheck.py` decides.
- Out: rewriting a lesson's text. A restructure that also edits is two changes nobody can review.
- Out: deciding this project's general splitting policy alone — see below.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting
- `R8` §8 — `CE-06` in full
- **L-74** in [`../docs/LESSONS.md`](../docs/LESSONS.md) — when a fact cannot be derived, make the
  stored copy fail loudly in both directions. It is the rule a generated index lives or dies by

**What specifying must settle**
- ~~**The shared policy question**, with [T-145](T-145-move-brief-mds-release-phases-to-its-own-document.md)
  and [T-147](T-147-one-workflow-file-per-lifecycle-phase.md): does this project split large documents
  by unit, with a generated index? **The first of the three specified settles it**; the other two
  adopt it or argue explicitly.~~ **Settled 2026-08-14 by T-145 as `L-89`**, and this task is the
  limb that says yes: *split to one file per unit only when the unit is addressed by its own id and
  is wanted one at a time.* `L-nn` is an address and lessons are cited singly, so the shape is
  decided and what is left to specify is below. **Adopt it or argue against it — do not re-decide
  it.**
- ~~Whether the gain is real for an agent that already greps a single file cheaply, or whether the
  cost is paid mostly by whole-file reads nobody performs.~~ **Measured above: the whole-file gain is
  not real and the finding's number rests on it.** The task stands on the index, the checker and the
  round-trip instead, and says so rather than quoting a ratio it cannot support.
- **What generates the index, what checks it, and where that runs in the gate chain** — settled
  below.

**The shape, settled**

- **`L-nn.md` under `docs/lessons/`, the bare id as the filename, no slug.** The id *is* the address; a slug
  makes a session glob for the file and hands back the one round-trip this change buys. It diverges
  from `tasks/`, where files are slugged, and the reason is that a task is found through the board
  while a lesson arrives as a citation with its address already in hand.
- **`docs/LESSONS.md` stays, and becomes the generated index.** 130 files name that path and the
  name is the known address; keeping it costs nothing and repoints nothing. It mirrors
  `tasks/README.md` exactly — preamble by hand, the table between generated markers — and the three
  category headings survive as the index's grouping.
- **The checker is the deliverable, not the split.** Both directions, which is **L-74**: an index
  entry with no file fails, a file with no index entry fails, and **a cited `L-nn` with no file
  fails** — the last being the 872-citation gap that exists today.
- **One new tool, wired into `check_all.py`'s `WIDE` table.** That file's four tables name every
  tracked `tools/**/*.py` exactly once and go red on a tool that is wired nowhere, so registering it
  is not optional and not extra.

**Acceptance criteria**
- [ ] 89 files under `docs/lessons/`, one per id, and the concatenated entry text is **byte-identical**
      to what was removed — asserted, not reviewed
- [ ] `docs/LESSONS.md` is the generated index: every id, its title, its category, in id order, with
      the hand-written preamble kept
- [ ] All **872** `L-nn` citations still resolve, and a seeded citation of a lesson that does not
      exist **fails the gate** — the defect that is invisible today
- [ ] A seeded stale index and a seeded orphan file each fail the gate, in their own direction
- [ ] The new tool is named in exactly one of `check_all.py`'s tables
- [ ] `python tools/check_all.py` green; `python tools/tasks/lint.py` ends with its one known advisory

**Open questions**
- ~~**Is it worth doing at all?**~~ **Answered: yes, and not for the reason the finding gave.** The
  whole-file ratio does not survive measurement; the index, the checker and the closed validation gap
  do. Had those not been there, `cancelled` plus one line of rule was the honest close and is
  recorded above so the judgement can be checked rather than trusted.

## 2. Plan

**The split is a slice, not a retype** — T-145's method, for the same reason: 167 KB cannot enter a
session, and the only honest proof that 89 files hold what one file held is an assertion that the
bytes match. Everything mechanical happens in one script run; everything judged happens before it.

**The checker is written before the split, and seeded first.** A gate written after the content it
guards is a gate tuned to pass what is already there (**L-86**, and **L-78**/**L-85** on self-tests).
Its three directions are seeded on a synthetic fixture, never on the tracked files.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write the tool: `index` regenerates, `check` asserts all three directions | `lessons.py`, under `tools/docs/` |
| 2 | Give it a self-test that seeds a dangling citation, a stale index and an orphan file on a synthetic fixture, and fails if any goes unreported | The gate proved before it is trusted |
| 3 | Split by slicing on the `### L-nn` boundaries; assert the concatenation identical to the removed text | 89 files under `docs/lessons/` |
| 4 | Regenerate `docs/LESSONS.md` as preamble plus generated table, keeping the three categories | The index, at the address 130 files already use |
| 5 | Register the tool in `check_all.py`'s `WIDE` table | The manifest partition holds |
| 6 | Run the gates; re-measure the fetch and the index | Figures for §4, taken after |

**What this must not do.** Renumber, reword or reorder a lesson — the preamble's own rule is *add at
the end of a section, never renumber*, and 872 citations depend on it. The three category headings
are metadata after the split rather than positions, and the index is where they survive.

## 3. Implement

**Decisions & assumptions**
- **The checker was written and seeded before the split — 2026-08-14.** Its first run, against a
  tree with no `docs/lessons/` in it, reported all 89 ids dangling. That is the gate proving it can
  fail before there is anything for it to pass, which is the order **L-86** and **L-04** ask for and
  the order a gate written afterwards cannot be given.
- **A lesson keeps its body byte for byte; only the heading marker changes — 2026-08-14.** `###`
  becomes `#` because a standalone document leads with `#`, and a `category:` front-matter line
  carries what the old `##` grouping carried by position. The round trip is asserted: undo those two
  and the 166,380 bytes come back identical.
- **Every relative reference moved one level, in text as well as in target — 2026-08-14.** The
  lessons went from `docs/` to `docs/lessons/`, so a target that began with one `../` now begins with
  two. **The link *label* was rewritten too**, and that is the part worth recording: a label showing
  the old one-level path beside a target carrying the new two-level one passes every gate here while
  telling the reader a path that is wrong from the new depth. The link works and the words beside it
  lie, and no checker reads a label.
- **The first attempt at that rewrite was wrong, and my own verification hid it — 2026-08-14.** Links
  and prose were rewritten in two passes, and the prose pass matched the targets the link pass had
  just written, deepening 47 of them twice. The summary I printed bucketed `../../../` under
  `startswith("../../")` and reported the run clean; `taskmd check` found it one command later. Redone
  from the committed file as a **single substitution over an alternation**, so no span can be
  rewritten twice. **L-62** is the rule and this is an instance of it: the instrument that produced
  the change cannot be the one that clears it.
- **`docs/LESSONS.md` keeps its path and becomes the index — 2026-08-14.** 165 files name it. The
  hand-written preamble stays above the generated markers, exactly as `tasks/README.md` does, so
  `index` rewrites only what it owns.
- **No illustrative path is written in a resolvable form, in the tool or in this record —
  2026-08-14.** `refcheck.py` resolves a repo-relative `.md` path written anywhere, including inside
  a fence or a docstring, and it caught three illustrative mentions in the tool, two self-test
  fixtures, and then **four more in this task file's own §3 and §4** — an example of the depth
  rewrite, an example of the misleading label, and the gate output quoted as evidence. It was right
  every time: they read as promises. All are written the way `TASK-WORKFLOW.md` §3 prescribes for a
  path that is not meant to resolve — the filename, and its directory said separately.
- **An unallocated `L-nn` cannot be written in prose either, and that is this tool's own rule —
  2026-08-14.** Quoting the seeded gate output verbatim put a citation of a lesson that does not
  exist into this record, and `lessons.py` reported it, correctly, on the release gate. **The
  narrow fix is the right one**: describe the seeded id rather than write it. An exemption for
  fences or for task files is the change T-098 refused for the duplicate-index advisory and for the
  same reason — a check that can be silenced where someone believes they are entitled to trip it is
  a check nobody trusts where it is right.
- **The tool went into `check_all.py`'s `WIDE` table, immediately after `lint.py` — 2026-08-14.** The
  four tables name every tracked tool exactly once and go red on one wired nowhere, so this was
  required rather than chosen; the position is chosen, and it is beside the other document gate.
- **The gate went red on the new tool before it was staged, and that is the gate working —
  2026-08-14.** `check_all.py` enumerates tools with `git ls-files`, so a `WIDE` entry naming a file
  git does not know about is reported `STALE`: *an entry names this and the file is not tracked*.
  Correct, and it is the clone-and-run rule enforced mechanically — a gate that ran a tool a fresh
  clone would not receive would be green on a repository nobody else can check. Staging cleared it.
  Recorded because the first reading of that line is *the tool is broken*, and it is not.

**Outputs produced**
- `docs/lessons/` — 89 files, `L-nn.md`, 169,361 bytes
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — the generated index, **12,258 bytes**
- [`../tools/docs/lessons.py`](../tools/docs/lessons.py) — `index` and `check`, three directions and
  a self-test that constructs each failure
- [`../tools/check_all.py`](../tools/check_all.py) — the new gate registered in `WIDE`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| 89 files under `docs/lessons/`, and the entry text byte-identical to what was removed | **met** | Asserted, not reviewed: undo the heading marker and the depth rewrite and the reconstruction equals the 166,380-byte source body exactly. The assertion is what caught the double-deepening described in §3 |
| `docs/LESSONS.md` is the generated index, with the hand-written preamble kept | **met** | 12,258 bytes — 89 rows in three categories, generated between markers, preamble above them as `tasks/README.md` does it |
| All citations resolve, and a seeded citation of a lesson that does not exist fails the gate | **met** | `1343 citation(s) across 256 file(s) resolved` — the lesson files are tracked now, so they are scanned too. A citation of an unallocated id was seeded into `CONTEXT-AUDIT.md` and reported as `DANGLING CITATION`, naming the one file it was in, exit 1. **This defect was invisible to every gate in the repository before today** — and the gate then caught the same id quoted back into this record, which is §3's last decision |
| A seeded stale index and a seeded orphan file each fail, in their own direction | **met** | Deleting one lesson's index row gave `ORPHAN LESSON`, naming the file and saying the index does not list it. The other direction and the title-mismatch case are asserted in the self-test on synthetic data (**L-85**) |
| The new tool is named in exactly one of `check_all.py`'s tables | **met** | `WIDE`, after `lint.py`. The manifest's partition is what proves it — a tool in none of the four fails the run |
| `check_all.py` green; `lint.py` ends with its one known advisory | **met, on the third run** | `lint.py`: three passed, `2169 document pointer(s), 0 broken`, one advisory naming `RELEASE-PHASES.md`. `check_all.py`: `0 failure(s), 0 unclassified, 0 stale` — **11 gates now, 38 tracked tools**. **The two red runs are the useful part and both were the gate being right**: the first reported the new tool `STALE` because git did not track it yet; the second was `lessons.py` catching an unallocated id quoted into this very record, with `figures.py` failing downstream of it because `refcheck` exited 1 and the README's documented `OK` lines were therefore absent. One cause, two reports, no defect in either tool |

**What the review does not claim.** Not a byte was saved: 167,043 in one file became 169,361 in 89
plus a 12,258-byte index. **What was bought is a fetch that is one call instead of two, a question
that could not be asked before, and 983 citations that a gate now resolves.** `CE-06`'s 81× assumed
a whole-file read that nothing here performs, and it is not claimed.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | **The finding's headline number did not survive specifying, and the task did.** `CE-06`'s 81× is the whole file over one entry, which is the cost only of a read nothing here performs — `../CLAUDE.md` puts `LESSONS.md` outside tier 1 and says it may grow without limit. What justified the work instead was found while measuring it: **983 citations across 165 files, resolved by no gate in this repository.** A lesson stored at its own id is a path, and a path is the one thing every gate here already checks. The bytes did not move; the validation did. |
| 2026-08-14 | → in_progress | Checker first, seeded before the content existed — its first run reported all 89 ids dangling, which is a gate proving it can fail. **The split's own rewrite went wrong and my summary of it read clean**: relative references were deepened in two passes and 47 were deepened twice, while the shape report bucketed `../../../` under `../../`. `taskmd check` found it one command later. Redone as a single substitution from the committed file (**L-62**). |
| 2026-08-14 | → planned | Six steps. The two that matter are *write the gate before the content* and *slice, then assert the bytes* — the second is what caught the first attempt's defect. |
| 2026-08-14 | → specified | **The open question was a measurement and it was taken rather than argued.** Re-measured 167,043 bytes, 89 entries, mean 1,859 — a flat distribution, which is what makes this the by-unit limb of `L-89` where T-145 was the by-kind one. `CE-13`'s precedent — the identical accident on decks, answered with one line of rule at `xs` — is the strongest case against, and it is answered in §1 rather than left out: without the index and the checker, `cancelled` plus one line was the honest close. |
| 2026-08-14 | (no change) | The shared policy question was struck out rather than answered here: T-145 settled it the same day as **L-89**, and this task cites it. Three tasks answering one question three ways is what the batch existed to prevent. |
| 2026-08-14 | → proposed | Raised at the owner's direction with the rest of the unraised findings; it was the sixth of T-130's seven candidates. **Scheduled to `plan` and no further** — the next session decides whether it is worth implementing. Its own band is the argument for stopping there: `l` on a document whose read cost is real but paid in greps rather than in whole-file loads. |
