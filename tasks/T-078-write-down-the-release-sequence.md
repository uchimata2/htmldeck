---
id: T-078
title: Write down the release sequence, which lives only in four task logs
type: admin
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-008, T-056]
work_package: v0.2
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-10
updated: 2026-08-10
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
- **Retitle `PUBLISHING.md`, or add a file?** Recommended: retitle. A second document about
  publishing is how the humanizing rule ended up cited from three places, and the existing one is
  already the file everyone opens for this. The rival is a `RELEASING.md`, which keeps the rule
  document short but splits one subject across two files.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the open question | The decision, in §3 |
| 2 | Write the sequence, checked against `v0.1.4`'s commits rather than from memory | The document |
| 3 | Point `CLAUDE.md` at it | `CLAUDE.md` |

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
| 2026-08-10 | → proposed | Raised while shipping `v0.1.4`, which was performed from precedent because nothing states the sequence. `v0.2` rather than `v0.1`: no adopter is affected and the releases have all shipped correctly, but each one has re-derived the same seven steps and the fourth of them is the one a gate cannot cover. |
