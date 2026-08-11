---
id: T-047
title: Give the rationale's conflicts their own ID namespace, and fix the mis-citation it has already caused
type: fix
status: done
phase: review
parent: T-042
blocked_by: []
related: [T-004, T-005, T-014, T-025, T-045]
work_package: none
shipped_in: 0.1.0
owner: the project owner
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - docs/DESIGN-RATIONALE.md
  - tools/deck/check.py
  - docs/DESIGN-SYSTEM.md
  - docs/research/R1-rules-candidate.md
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
| 1 | Find every `X-n` in the repository and **classify each by which namespace it means**, not by which file it is in | Five files carry conflicts; three carry anti-patterns; `X-10` and `X-11` exist in both |
| 2 | Rename `X-1`…`X-11` → `C-01`…`C-11` in the files that carry conflicts, by one pattern applied to a named list rather than a global replace | 53 citations renamed, no anti-pattern touched |
| 3 | Fix the mis-citation in `check.py`'s closing paragraph | `(DS-107, C-10)` — the word-list conflict, not the dual-axis chart |
| 4 | Forwarding note in `DESIGN-RATIONALE.md` §2, so an `X-n` in an older document still resolves | The rename does not orphan the history it renames |
| 5 | Forwarding note in `R1`, saying why the rename reached a dated research note at all | The record says what changed and what did not |
| 6 | State the convention where the surviving namespace lives, so the collision cannot recur | One line in `DESIGN-SYSTEM.md` §6: `X-nn` means these twelve and nothing else |
| 7 | Re-run both gates and re-scan for survivors | Clean, and the only `X-n` left is inside the two forwarding notes |

## 3. Implement

**Decisions & assumptions**
- **`C-nn`, zero-padded**, as §1 recommended. It collides with no existing namespace and matches
  `DS-nnn` / `A-nn` / `X-nn` / `L-nn` / `F-nn`. — 2026-08-09
- **The rename reached `docs/research/R1-rules-candidate.md`, and that needed deciding rather than
  assuming.** A research note is a dated record and is normally left as written. But R1's `X-1`…
  `X-11` are **the same eleven objects** `DESIGN-RATIONALE.md` §2 resolves — not a historical
  mention of them — so leaving R1 on the old name would have produced two names for one thing,
  which is the defect this task exists to remove, in mirror image. Renamed, with a note saying so
  and confirming nothing else in the note changed. — 2026-08-09
- **Classified before replacing, because `X-10` and `X-11` are valid in both namespaces.** A global
  substitution would have renamed the dual-axis chart and the rainbow encoding. Every occurrence
  was read: `R3` §"anti-patterns", `EVALUATION.md` §3's dimension lists and
  `DESIGN-RATIONALE.md:393` mean the **anti-patterns** and were left alone;
  `R4:271` (*"which R1 records as contradiction X-10"*) and `T-005:176` mean the **conflict** and
  moved. — 2026-08-09
- **One line added to `DESIGN-SYSTEM.md` §6, slightly beyond §1's scope.** §1 asked for a forwarding
  note in the rationale, which tells a reader where the old IDs went; it does not stop the namespace
  being reused. The line in §6 says `X-nn` means those twelve and nothing else, which is the part
  that prevents a third namespace. No anti-pattern's number, text or meaning changed. — 2026-08-09

**Outputs produced**
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) — 14 renames and the forwarding note
- [`docs/research/R1-rules-candidate.md`](../docs/research/R1-rules-candidate.md) — 27 renames and
  a note on why a research note was touched
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §6 — the convention, stated once
- [`tools/deck/check.py`](../tools/deck/check.py) — the mis-citation
- [`docs/research/R4-prior-art.md`](../docs/research/R4-prior-art.md),
  [T-005](T-005-build-check-the-gate-the-deck-must-pass.md),
  [T-014](T-014-synthesise-research-into-the-design-system-reference.md) — 11 renames between them

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| No `X-n` (single digit) remains anywhere outside the forwarding note | **met** | A repository-wide scan for `X-[1-9]` not followed by a digit returns two hits, both the literal `` `X-1`…`X-11` `` inside the two forwarding notes |
| Every renamed conflict is cited by its new ID in every document that cited it, `tasks/` included — found by search, not by memory | **met** | 53 renames across six files, from a scan rather than a list: `DESIGN-RATIONALE.md` 14, `R1` 27, `T-014` 7, `T-005` 3, `R4` 1, `check.py` 1 |
| `check.py:303` cites the conflict correctly, and the sentence still says what it meant | **met** | `…so a clean DS-106 is never "reads as human-written" (DS-107, C-10).` C-10 is the word-list conflict; the sentence is otherwise unchanged |
| `X-01`–`X-12` are unchanged in number, text and meaning | **met** | 12 rows in `DESIGN-SYSTEM.md` §6, untouched. Their citations in `EVALUATION.md` §3 (S3, S4, S5), `R3` and `DESIGN-RATIONALE.md:393` were classified as anti-patterns and deliberately left |
| `task.py check` and `check.py` both pass afterwards | **met** | `OK - 51 tasks, … 687 document pointer(s) checked, 0 broken` and `0 failure(s): none` |

**The half of the fix §1 did not ask for.** A forwarding note tells a reader where the old IDs went;
it does not stop the surviving namespace being reused for a third thing. `DESIGN-SYSTEM.md` §6 now
says in one line that `X-nn` means those twelve and nothing else — which is the part that makes this
a fix rather than a tidy-up.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **53 renames, and the work was the classification rather than the substitution.** `X-10` and `X-11` are valid IDs in *both* namespaces, so a global replace would have silently renamed the dual-axis chart and the rainbow encoding — every occurrence was read and assigned before anything changed. Two decisions are worth carrying forward. **The rename reached `R1`, a dated research note**, which is normally left as written: its `X-1`…`X-11` are not a historical *mention* of the conflicts but the same eleven objects `DESIGN-RATIONALE.md` §2 resolves, so leaving them would have produced two names for one thing — this defect in mirror image. Both documents carry a note saying what was renamed, when, and that nothing else moved. **And one line went beyond the stated scope**, into `DESIGN-SYSTEM.md` §6: a forwarding note tells a reader where the old IDs went, but only a statement in the surviving namespace stops it being reused for a third thing. That line is what makes this a fix rather than a tidy-up, and it is placed where §6 already explains itself — *"so the critique pass and the standard cannot drift apart"* is the same argument one level down. |
| 2026-08-09 | → planned | §1 accepted as written, including its recommended prefix — `C-nn` collides with nothing and matches the five namespaces already in use, so there was nothing to improve on. Seven steps, with classification as step 1 rather than as part of the replace, because the two namespaces overlap at exactly the two IDs the finding is about. Worked separately from [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) as the log below requires; both edit `DESIGN-RATIONALE.md`. |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), finding F-6. **Two ID namespaces separated by a leading zero, cited in the same sentences, and the collision has already fired**: `check.py:303` cites `X-10` meaning the word-list conflict, while `X-10` in the ruleset is the dual-axis chart. The rationale's conflicts move because the anti-patterns are cited from five documents and exist to stop the critique pass and the standard drifting apart — the same *which side moves* reasoning §3 used for DS-131. Sequence this either side of [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md), never alongside it; both edit `DESIGN-RATIONALE.md` §2 and §5. |
