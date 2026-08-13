---
id: T-133
title: Write down that a deck is never read whole
type: admin
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
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
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised from [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s ranking at the owner's review, third of four. `CE-13`, and the one whose gain is **bimodal** — nothing on most sessions, a whole session's runway on the one that opens 200k estimated tokens of HTML to ask a question a tool already answers. It ranks above larger bands for that reason and not despite it. It also adds a line to the file `CE-01` and `CE-11` exist to shorten, which is a real tension and is named in scope rather than discovered at review. |
