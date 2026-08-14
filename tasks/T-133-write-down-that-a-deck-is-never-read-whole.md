---
id: T-133
title: Write down that a deck is never read whole
type: admin
status: done
phase: review
shipped_in: unreleased
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
finding: CE-13
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - CLAUDE.md
---

# T-133 — Write down that a deck is never read whole

## 1. Specify

**Outcome**
The working rules say what everyone has so far done by habit: a deck's HTML is queried by the tools
or by targeted search, and looking at a deck means rendering it. **The finding is `CE-13`**, stated
in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.1; it is not restated here.

**Why a one-line rule is ranked above larger savings**
The three example decks are **810,746 bytes, ~202,686 estimated tokens**. The rule saves nothing on
almost every session and saves an entire session on the one that opens a deck to answer a question a
tool already answers. That shape — nothing, nothing, nothing, catastrophe — is exactly what a written
rule is for and exactly what a habit is not.

**Scope**
- In: one rule in [`../CLAUDE.md`](../CLAUDE.md), beside rule 6, which already says looking at a
  rendered deck is not the same as validating it.
- In: naming what to use instead — [`../tools/deck/check.py`](../tools/deck/check.py),
  [`../tools/deck/printgeom.py`](../tools/deck/printgeom.py) and the rest of
  [`../tools/deck/`](../tools/deck) — as a pointer, not a list to maintain.
- Out: any tool change. Everything needed already exists; nothing had written down that it is the
  route.
- Out: a mechanical guard. Nothing can stop a file being read, and a rule that cannot be enforced is
  still worth stating when the failure is this expensive.
- Out: growing `CLAUDE.md` overall — it is tier 1, and `CE-01` and `CE-11` are about its size. This
  adds a line to a file two sibling tasks are shortening, which is deliberate and worth one sentence
  at implement.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §2.4 and §6.1 — the measurement and `CE-13`
- [`../CLAUDE.md`](../CLAUDE.md) *The rules that must survive* rule 6, and *Verifying*

**Acceptance criteria**
- [ ] The rule is stated where a reader meets it before deck work, in one or two sentences
- [ ] It names the route to use instead, without becoming a list of tools that goes stale
- [ ] It distinguishes *reading the HTML* from *looking at the rendered deck*, which rule 6 requires
      and which this must not appear to weaken
- [ ] `CLAUDE.md`'s line count is recorded before and after, since it is tier 1

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Count [`../CLAUDE.md`](../CLAUDE.md) before the edit, and re-measure the three decks rather than copying the figure out of the audit | The before-count, and a checked 810,746 |
| 2 | Find out whether the rule can take a number of its own — that is, whether anything cites these rules by number | The answer, which decides step 3 |
| 3 | Write it into rule 6 rather than as rule 8, keeping both halves in one rule: *look* means render, and it never means read the file | The rule |
| 4 | Name the route as a directory, not a list of tools | A pointer that cannot go stale |
| 5 | Re-count, and record both numbers where a tier-1 file's growth is read | The §4 row, and the audit's rank table |

## 3. Implement

**Decisions & assumptions**
- **It extends rule 6 instead of becoming rule 8, because the numbers are cited** — 2026-08-13. A
  sweep of the tracked record found **about 130 citations of the form `rule n`**, across task files,
  research documents, `docs/`, and the printed output of four tools — `check.py`, `check_all.py`,
  `printgeom.py`, `printpages.py`. Inserting a rule after 6 renumbers 7 and silently falsifies every
  citation of it; appending as 8 keeps the numbers but puts the rule two entries away from the one it
  belongs beside. Extending 6 costs neither. **The same reasoning is already written down for
  `TASK-WORKFLOW.md`'s own headings in its §6.1**, which is why it is not repeated in `CLAUDE.md`
  (**L-13**) — that file gains the rule and nothing else.
- **The route is named as a directory** — 2026-08-13. `tools/deck/` rather than a list: the scope
  asked for a pointer that does not go stale, and the audit's own finding is that lists of tools are
  what go stale. A reader who needs the specific tool runs `check_all.py --list`, which derives it.
- **810,746 was re-measured, not copied** — 2026-08-13. 268,563 + 265,804 + 276,379 across the three
  shipped `.html` decks, and it agrees with the audit exactly.
- **The tension in the scope is real and the trade was taken.** `CLAUDE.md` is tier 1 and two open
  tasks exist to shorten it; this adds **4 lines and 322 bytes, 207 → 211 and 15,630 → 15,952**. The
  cost is paid every turn of every session; the saving is one whole session, once. A first draft also
  carried a *do not renumber these rules* clause, which was cut for exactly this reason — it is a
  second copy of a rule `TASK-WORKFLOW.md` §6.1 already owns.

**Outputs produced**
- [`../CLAUDE.md`](../CLAUDE.md) — rule 6, both halves

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Stated where a reader meets it before deck work, in one or two sentences | met | Rule 6 of *The rules that must survive*, which is the list every session reads before touching a deck. Two sentences |
| Names the route without becoming a list that goes stale | met | `tools/deck/`, a directory — the audit's own finding is that tool lists go stale, and `check_all.py --list` derives the members |
| Distinguishes reading the HTML from looking at the rendered deck, and does not weaken rule 6 | met | The rule leads with *look means render it and open it, which nothing here replaces*, then says what it does not mean. The original sentence is intact inside it |
| `CLAUDE.md`'s line count recorded before and after | met | **207 → 211 lines, 15,630 → 15,952 bytes.** Four lines and 322 bytes onto a tier-1 file, paid every turn, against one session saved once — the trade is argued in §3 rather than assumed |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | The rule is inside rule 6 rather than beside it, and **that was decided by measurement rather than by taste**: about 130 places cite these rules by number, including the printed output of four tools, so a new rule 7 would have falsified every citation of the old one. `CLAUDE.md` grew 207 → 211 lines. A *do not renumber* clause was drafted and cut — `TASK-WORKFLOW.md` §6.1 already owns that rule, and tier 1 is the worst place to keep a second copy. |
| 2026-08-13 | → in_progress | Five steps, and step 2 changed the shape of the work: *can this rule have a number of its own* had to be answered before anything was written. |
| 2026-08-13 | → planned | The measurement comes first here for the same reason it did in T-132 — a before-and-after criterion has no instrument once the edit is in. |
| 2026-08-13 | → specified | §1 arrived written, with the deliverable declared, the tension with `CE-01` and `CE-11` named in scope, and no open question. |
| 2026-08-13 | → proposed | Raised from [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s ranking at the owner's review, third of four. `CE-13`, and the one whose gain is **bimodal** — nothing on most sessions, a whole session's runway on the one that opens 200k estimated tokens of HTML to ask a question a tool already answers. It ranks above larger bands for that reason and not despite it. It also adds a line to the file `CE-01` and `CE-11` exist to shorten, which is a real tension and is named in scope rather than discovered at review. |
