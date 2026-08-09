---
id: T-047
title: Give the rationale's conflicts their own ID namespace, and fix the mis-citation it has already caused
type: fix
status: proposed
phase: specify
parent: T-042
blocked_by: []
related: [T-004, T-005, T-014, T-025, T-045]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - docs/DESIGN-RATIONALE.md
  - tools/deck/check.py
---

# T-047 — Give the rationale's conflicts their own ID namespace, and fix the mis-citation it has already caused

## 1. Specify

**Outcome**
`X-nn` names one thing. The sixteen source conflicts in `DESIGN-RATIONALE.md` §2 move to their own
prefix; `X-01`–`X-12` stay the anti-patterns; and the one citation that already crossed the two is
corrected.

**Why this one**
`DESIGN-SYSTEM.md` §6 defines twelve anti-patterns `X-01`–`X-12`, cited from five documents and from
the evaluation rubric's dimension lists. `DESIGN-RATIONALE.md` §2 uses `X-1`–`X-11` for the conflicts
found by reading the sources against each other. **They differ by a leading zero and they appear in
the same sentences.** It has already cost a mis-citation, in the gate's own closing paragraph — the
sentence that tells a reader what a clean run does *not* mean:

```
tools/deck/check.py:303
"…so a clean DS-106 is never 'reads as human-written' (DS-107, X-10)."
```

The intended reference is the **conflict** X-10 — *a word-list check versus "text can pass all five
categories and still sound like AI"*. `X-10` in the ruleset is **the dual-axis chart**. A reader
following the citation lands on a rule about two y-axes.

**Which side moves, and why it is the rationale's.** The same reasoning
`DESIGN-RATIONALE.md` §3 already uses for DS-131: *the side that moves is the one that is cheaper to
move and whose identity is less load-bearing.* The anti-patterns are cited from `DESIGN-SYSTEM.md`,
`EVALUATION.md` §3–§4, `examples/README.md`, `check.py` and several task files, and
`DESIGN-SYSTEM.md` §6 exists so *"the critique pass and the standard cannot drift apart"* — renaming
them would break the thing that sentence is protecting. The conflicts are cited from one document
plus a handful of task logs.

**Recommended prefix: `C-nn`, zero-padded to two digits** — `C-01`–`C-11`, matching the
`DS-nnn` / `A-nn` / `X-nn` / `L-nn` / `F-nn` convention already in use, and not colliding with any
of them.

**Scope**
- In: renaming `X-1`–`X-11` in `DESIGN-RATIONALE.md` §2 and every citation of them, in `docs/` and
  in `tasks/`.
- In: `check.py:303`, which is the mis-citation and is the reason this is not cosmetic.
- In: a one-line note in `DESIGN-RATIONALE.md` §2 recording that these were `X-n` until 2026-08-09,
  so a reader meeting an `X-n` in an old task log can resolve it. **IDs here are not permanent the
  way `DS-nnn` are** — nothing consumes them at runtime — but a rename with no forwarding note
  makes every historical citation unresolvable, which is the defect this task is fixing in a new
  form.
- Out: `F-01`–`F-13`, the conflicts the build found. They already have their own prefix and collide
  with nothing.
- Out: the anti-patterns themselves. No `X-nn` changes meaning, number or text.
- Out: adding an ID to anything that does not have one.

**Inputs**
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2 — the sixteen conflicts
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §6 — the twelve anti-patterns
- [`tools/deck/check.py`](../tools/deck/check.py) line 303
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-6

**Acceptance criteria**
- [ ] No `X-n` (single digit) remains anywhere outside the forwarding note
- [ ] Every renamed conflict is cited by its new ID in every document that cited it, `tasks/`
      included — found by search, not by memory
- [ ] `check.py:303` cites the conflict correctly, and the sentence still says what it meant
- [ ] `X-01`–`X-12` are unchanged in number, text and meaning
- [ ] `python tools/tasks/task.py check` and `python tools/deck/check.py examples/reference-deck.html`
      both pass afterwards

**Open questions**
- none — the prefix is a recommendation the implementer may improve on, provided it collides with
  no existing namespace.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), finding F-6. **Two ID namespaces separated by a leading zero, cited in the same sentences, and the collision has already fired**: `check.py:303` cites `X-10` meaning the word-list conflict, while `X-10` in the ruleset is the dual-axis chart. The rationale's conflicts move because the anti-patterns are cited from five documents and exist to stop the critique pass and the standard drifting apart — the same *which side moves* reasoning §3 used for DS-131. Sequence this either side of [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md), never alongside it; both edit `DESIGN-RATIONALE.md` §2 and §5. |
