---
id: T-033
title: Reconcile DS-131 with the chrome budget it now contradicts
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-027, T-028, T-025]
work_package: WP2
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-07
updated: 2026-08-12
deliverables: []
---

# T-033 — Reconcile DS-131 with the chrome budget it now contradicts

## 1. Specify

**Outcome**
[`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) stops requiring an element that two other rules
in it require removing. Either DS-131 no longer lists clickable dots, or DS-216/DS-217 say when
dots are the right answer — one of the two, decided by the owner and written down.

**The conflict, stated exactly**

| Rule | Says | Label |
| :--- | :--- | :--- |
| DS-131 | *"Keyboard ←/→/space/Home/End; prev/next arrows; **clickable dots**; click-to-jump; touch/swipe; wheel."* | `default` · `render` |
| DS-216 | One encoding of position, never three. A dot per slide is one of the three it names. | `default` · `render` |
| DS-217 | *"per-slide dots stop scaling somewhere around ten slides. **Prefer a compact indicator plus click-to-jump over one target per slide.**"* | `default` · `render` |

**DS-131 lists the thing DS-217 says to prefer against.** This was latent while nothing enforced
DS-216 or DS-217. [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) made it
concrete: obeying DS-216 and DS-217 meant deleting the twelve dots, so
[`examples/reference-deck.html`](../examples/reference-deck.html) — the deck the ruleset ships as
its own worked example — **now departs from DS-131 as written**. All three rules are `default`, so
a reasoned departure is legitimate; a ruleset whose flagship example silently contradicts one of
its own rules is not.

[`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) *Three encodings of one fact* already
names DS-131 as one of the three individually-sanctioned rules that together specified a bad whole.
It diagnosed the composition failure and did not resolve it — DS-216 and DS-217 were added *beside*
DS-131 rather than reconciled *with* it.

**Why this is a task and not an edit**
T-028's scope put rule changes out, and routed any finding to
[T-025](T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md) — which is `done`,
so that route no longer exists. This is the finding, carrying its own file.

**Scope**
- In: deciding which of the two sides moves, and editing `DESIGN-SYSTEM.md` to match.
- In: whatever `DESIGN-RATIONALE.md` owes the decision.
- Out: changing the reference deck again. It satisfies DS-216 and DS-217 as measured; if the owner
  rules for dots, that becomes its own task with its own gate run.
- Out: gating DS-131. Whether it earns a check is a separate question from whether it is consistent.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §6 — DS-131, DS-133, DS-134, DS-216, DS-217
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) — *Three encodings of one fact*
- [`T-028`](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) §3.2 and §4 — what
  removing the dots actually cost and what replaced them
- [`T-027`](T-027-specify-the-slide-deliverable-and-the-outline-contract.md) — where DS-216 and
  DS-217 came from, and the owner's *"extremely noisy"*

**Acceptance criteria**
- [ ] DS-131, DS-216 and DS-217 can all be satisfied by one deck at once, and it is stated how
- [ ] The reference deck's chrome either conforms to the reconciled rules or its departure is
      recorded in `DESIGN-SYSTEM.md` with a reason
- [ ] `DESIGN-RATIONALE.md` says why the reconciliation went the way it did
- [ ] `python tools/deck/audit.py examples/reference-deck.html` still reports zero mechanical
      failures, and `python tools/deck/deliverable_variants.py` still catches 7 of 7

**Open questions**
- ~~**Does click-to-jump require one target per slide, or is per-stage enough?**~~ **Answered
  2026-08-07 by the owner: per-stage.** So it is **DS-131 that moves**, not DS-216/DS-217: the rule
  is reworded to require click-to-jump to a **bounded set of named targets**, and *"clickable dots"*
  stops being a named requirement — it becomes one permitted implementation of a bounded set, which
  DS-217's *"somewhere around ten slides"* already bounds. [`examples/reference-deck.html`](../examples/reference-deck.html)
  therefore **conforms** once the rewording lands, rather than needing a recorded departure, which
  is the cheaper of the two branches in the second acceptance criterion below.
  **What the answer does not settle, and the rewording must not paper over:** a deck whose stages
  are uneven, or long enough that a stage is not a useful jump target, still has no answer. Name
  that limit in the rule rather than leaving the next deck to discover it — an on-demand slide
  index is the obvious shape, it is a component
  [T-016](T-016-the-interaction-and-motion-layer.md) would own, and it is out of scope here.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Put the three rule texts side by side and mark the exact clause that conflicts | the conflict, in one table |
| 2 | Take the owner's ruling on per-slide versus per-stage jump targets | the decision |
| 3 | Edit `DESIGN-SYSTEM.md` so one deck can satisfy all three | the reconciled rules |
| 4 | Record the reasoning in `DESIGN-RATIONALE.md` | the rationale |
| 5 | Re-run the gate and the variants to confirm nothing moved underneath | the verdicts |

## 3. Implement

**Decisions & assumptions**
- **DS-131 was reworded, DS-216 and DS-217 were not touched** — 2026-08-08, executing the owner's
  ruling. The rule now requires *click-to-jump to a bounded set of named targets*; *"clickable
  dots"* is gone as a named requirement and appears as one permitted implementation. Every other
  member of the navigation set — keyboard, prev/next arrows, touch/swipe, wheel — is unchanged.
- **The reason the reconciliation runs this way is that DS-131 named a widget where the other two
  named a requirement** — 2026-08-08. That is the generalisable part and it went into
  [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md): a rule that specifies the element rather
  than the need is the one that collides with the next composition rule, because composition rules
  are written about elements. **Candidate for a lesson of its own; not minted here** — the ruleset
  already carries **L-37** for the answer-versus-rule half, and inventing an `L-nn` was not in scope.
- **The limit the ruling did not cover is named in the rule text, not left to the rationale** —
  2026-08-08. Uneven or long stages make a per-stage jump barely a jump; the rule says so and names
  the on-demand slide index as the answer, so a deck meeting that shape has a stated route rather
  than a discovery. Building the index remains [T-016](T-016-the-interaction-and-motion-layer.md)'s.
- **Nothing implements a DS-131 check, and this task did not add one** — 2026-08-08, `grep DS-131
  tools/ skills/` returns nothing. That matters here only as a negative: the rewording could not
  desync a gate from the rule, because no gate reads it. The rule keeps its `render` label, which
  is the L-36 class of defect and explicitly out of §1's scope.

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.1 — DS-131 reworded.
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) — *Which side moved — DS-131 against
  DS-216 and DS-217*, after *Three encodings of one fact*, which had diagnosed this and stopped.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| DS-131, DS-216 and DS-217 can all be satisfied by one deck at once, and it is stated how | pass | One primary encoding, a second only if it encodes a different fact (DS-216), inside a ~12-item / ~90 du budget (DS-217), with jump targets that are a bounded named set rather than one per slide (DS-131). The reference deck is the worked instance: a stage ribbon of **7 named targets** carrying stage, a counter carrying slide, and no third encoding. |
| The reference deck's chrome either conforms to the reconciled rules or its departure is recorded in `DESIGN-SYSTEM.md` with a reason | pass — conforms, nothing recorded | The cheap branch, as the owner's answer predicted. Verified in [`examples/reference-deck.html`](../examples/reference-deck.html): keyboard ←/→/space/PageUp/PageDown/Home/End, `#prev`/`#next` arrows, `wheel` with a 700 ms lock, `touchstart`/`touchend` swipe, and ribbon click-to-jump over 7 stages — inside DS-217's "around ten". Stage lengths are 1·1·2·2·3·2·1 over 12 slides, so the rule's uneven/long-stage limit is not reached and no slide index is owed. **The deck was not edited**, which §1 put out of scope. |
| `DESIGN-RATIONALE.md` says why the reconciliation went the way it did | pass | New section states which side moved and why — DS-131 was the only one of the three specifying an implementation — plus why the stage names were the cheaper target set (7 labelled and already drawn against 12 unlabelled and not), and why the uneven-stage limit is in the rule rather than left latent. |
| `audit.py` still reports zero mechanical failures, and `deliverable_variants.py` still catches 7 of 7 | pass | `audit.py examples/reference-deck.html` → **0 mechanical failures**, 48 gated rule results. `deliverable_variants.py` → **7 of 7**; `contract_variants.py` → **7 of 7**. Expected to be unchanged and was: this task edited two documents and no deck, and no tool reads DS-131. |

**Child fix tasks raised**
- none

**Noted, not raised**
- The gate's rule-result count reads **48** in this run against the **43** last recorded in a
  session handoff. Nothing here touched the deck or the tools, so the difference is in what was
  counted rather than in what passed — recorded so the next session compares like with like rather
  than reading it as movement.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-08 | → done | Steps 3–5 executed; steps 1–2 were already discharged by the conflict table in §1 and the owner's ruling. **DS-131 reworded to *a bounded set of named targets*, DS-216 and DS-217 untouched**, and the reference deck conforms without being edited — the cheap branch the answer predicted, confirmed against the deck rather than assumed: 7 stage targets, stage lengths 1·1·2·2·3·2·1, every other member of the navigation set present. The uneven/long-stage limit the ruling did not cover is **in the rule's own text**, naming the on-demand slide index as the answer and leaving it to [T-016](T-016-the-interaction-and-motion-layer.md) to build. Gates re-run and unchanged, as expected of a documents-only change: `audit.py` 0 mechanical failures, both variant suites 7 of 7. **One thing found and deliberately not taken**: DS-131 is labelled `render` and no tool reads it, which is L-36's class and §1's explicit out-of-scope. |
| 2026-08-07 | (no change) | **Answered by the owner: per-stage, so DS-131 is the side that moves.** Click-to-jump requires a **bounded set of named targets**; dots become one permitted implementation rather than a requirement, and DS-216/DS-217 stand unchanged. Two consequences for the plan. **Step 2 is no longer a decision, it is drafting** — the ruling exists and what remains is wording that three rules can be read together. **The second acceptance criterion resolves to its cheap branch**: [`examples/reference-deck.html`](../examples/reference-deck.html) conforms once the rewording lands, so no departure has to be recorded and the deck is not touched — which was already out of scope. The limit the answer does *not* cover — an uneven or long deck where a stage is not a useful target — belongs in the rule's own text, not in a later surprise. |
| 2026-08-07 | → proposed | Raised while closing [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md), which surfaced the conflict by obeying DS-216 and DS-217 for the first time. Not folded into T-028: its scope explicitly put rule changes out, and the reference deck now passes every gated rule — this is a defect in the ruleset's internal consistency, not in the deck. Raised as its own file rather than appended to T-025 because that task is `done`. |
