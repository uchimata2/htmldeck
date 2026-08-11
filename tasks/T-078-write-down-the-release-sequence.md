---
id: T-078
title: Write down the release sequence, which lives only in four task logs
type: admin
status: done
phase: review
parent: null
blocked_by: []
related: [T-008, T-056]
work_package: PH2
shipped_in: 0.1.5
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - docs/PUBLISHING.md
---

# T-078 — Write down the release sequence, which lives only in four task logs

## 1. Specify

**Outcome**
One place says what shipping a release consists of, in order. Today the answer is reconstructed from
whichever task last did it.

**Why this exists**
Noticed while shipping `v0.1.4` on 2026-08-10. Nothing in the repository states the sequence; it was
re-derived from the previous release's commits and the shape of the last GitHub release note.
[`docs/PUBLISHING.md`](../docs/PUBLISHING.md) owns the **humanizing rule** and says so in its own
title, so it covers one step of about seven and is silent on the rest.

The steps, as actually performed, so the task starts from a record rather than from memory:

1. Every gate green, including the suites the routine set omits — this release found two of them red.
2. Bump `version` in `.claude-plugin/plugin.json`, and the version stated in `CLAUDE.md` and
   `README.md`.
3. Run the humanizer over the human-facing set (`PUBLISHING.md` §2), then `tools/docs/figures.py` to
   prove no pasted figure moved, and re-paste the `volatile` block from `--values`.
4. Check the prose *around* the figures, which no gate reads: this release had a spelled-out
   fixture count and a defect tally that had both gone false (**L-05**).
5. Commit, tag `vX.Y.Z`, push both.
6. `gh release create` with a note written to the same humanizing rule, since a release page is read
   before installing and is therefore covered by §2's test.
7. Record the shipping version in each task's log and in `docs/BRIEF.md`.

**Scope**
- In: the sequence above, verified against what the last release actually did, in one document.
- In: **which document.** `PUBLISHING.md`'s title scopes it to the humanizing rule, so either it is
  retitled to own publishing generally, or the sequence gets its own file.
- In: whether step 1's gate list is written here or derived. This session ran suites the handoff's
  list omitted and found two red, so an enumeration has already failed once.
- Out: automating any of it. The question is where the steps are written, not who runs them.
- Out: the humanizing rule itself, which `PUBLISHING.md` already owns and which this must point at
  rather than restate (**L-13**).

**Inputs**
- `docs/PUBLISHING.md`, `CLAUDE.md` *Publishing constraints*
- [T-008](T-008-package-document-and-publish.md) and [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md),
  whose logs hold the first release's version of this

**Acceptance criteria**
- [ ] The sequence is in one document, in order, with each step naming what proves it was done
- [ ] The gate list is derived, or its enumeration is declared with what would close the excusal
- [ ] Nothing in it restates the humanizing rule; it points at `PUBLISHING.md` §2 and §6
- [ ] `CLAUDE.md` points at it, since that is where someone looks for the project's rules

**Open questions**
- ~~**Retitle `PUBLISHING.md`, or add a file?**~~ **Settled 2026-08-10: retitle, as recommended.**
  The rival, a `RELEASING.md`, keeps the rule document short and splits one subject across two files,
  which is the failure the recommendation names.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the open question | The decision, in §3 |
| 2 | Write the sequence, checked against `v0.1.4`'s commits rather than from memory | The document |
| 3 | Point `CLAUDE.md` at it | `CLAUDE.md` |

## 3. Implement

**Decisions & assumptions**
- **Retitle to `# Publishing`, and the sequence becomes §8** — 2026-08-10, as recommended. **§1–§7
  keep their numbers**: `PUBLISHING.md §2`, `§3` and `§6` are cited from T-008 and T-060, and
  renumbering falsifies all eight citations silently, which is `TASK-WORKFLOW.md` §6.1's own case.
  So the part read first sits at the end, and the preamble carries a pointer to it — the cost of
  citation stability, paid deliberately and written down as such.
- **The gate list is declared, not derived** — 2026-08-10, taking the second half of criterion 2.
  Deriving it needs a tool that runs every checker under `tools/` and reports what it skipped with a
  reason, and building that is out of scope by §1. What is written instead is the list, the fact that
  it has already failed, and the condition that closes the excusal — the same partition
  `figures.py` applies to fences.

**And writing it down was not a formality: three of the eleven were red.** The section was written by
running every command it names, which is the only honest way to write a list of gates, and it found:

| Command | State on 2026-08-10 | Since |
| :--- | :--- | :--- |
| `shell.py check examples/sort-window/…` | red — shared shell stale | T-069, the same day |
| `check.py examples/sort-window/… --sources` | red — DS-064 at 15.0 px | before `d80e0c3` |
| `contents_bound.py` | **refused to start** — fixture counts 12 boxes, the deck builds 13 | T-069's commit, measured by checking the deck out either side of it |

The first was fixed in [T-071](T-071-the-intermediate-specifications-carry-their-references.md); the
other two are [T-083](T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md)
and [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md). **Every one was
outside the five commands the README prints**, which is precisely the enumeration this task was
asked to justify or replace.

**Outputs produced**
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) — retitled, a pointer in the preamble, and §8: the
  seven steps with what proves each, the declared gate list, and what closes its excusal.
- [`CLAUDE.md`](../CLAUDE.md) — *Publishing constraints* opens by pointing at §8.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The sequence is in one document, in order, with each step naming what proves it | met | §8's table. Step 4 names *nothing* as its proof, deliberately — it is the step no gate covers, and saying so is the point of listing it. |
| The gate list is derived, or its enumeration is declared with what would close the excusal | met, declared | Eleven commands, the three that were red, and the closing condition: one command that runs every checker under `tools/` and reports what it skipped with a reason. |
| Nothing restates the humanizing rule; it points at §2 and §6 | met | Step 3 and step 6 both point; neither repeats the test or the exception. |
| `CLAUDE.md` points at it | met | First line of *Publishing constraints*, before the four bullets, because the sequence is what someone arrives looking for. |

**Child fix tasks raised**
- [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md) — `contents_bound.py`
  has refused to start since T-069 changed the reference deck.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | The sequence is `PUBLISHING.md` §8 and the document is retitled. **The task justified itself while being done**: running the eleven commands it was about to write down found three red, all outside the five the README prints, and one of them refusing to start. A list of gates written without running them would have been a list of gates that had not been run — which is the same defect as the release sequence living in four task logs, one altitude up. §1–§7 keep their numbers so eight citations from T-008 and T-060 stay true, and the cost of that is a preamble pointer to the part read first. |
| 2026-08-10 | → proposed | Raised while shipping `v0.1.4`, which was performed from precedent because nothing states the sequence. `PH2` rather than `PH1`: no adopter is affected and the releases have all shipped correctly, but each one has re-derived the same seven steps and the fourth of them is the one a gate cannot cover. |
