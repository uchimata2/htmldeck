---
id: T-076
title: A verdict producer that exits the process instead of reporting a row
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-075]
work_package: v0.2
owner: the project owner
business_value: medium
effort: s
created: 2026-08-10
updated: 2026-08-10
deliverables:
  - tools/deck/contrast.py
---

# T-076 — A verdict producer that exits the process instead of reporting a row

## 1. Specify

**Outcome**
No stage of the gate can end the run by deciding its input is not worth reporting on. A deck the gate
cannot judge produces a failing row that names why, like every other finding.

**Why this exists**
Found while bringing every verdict producer inside the absent-subject fixture
([T-075](T-075-ds-064-probes-for-the-reference-decks-own-class-names.md)).
[`tools/deck/contrast.py:102`](../tools/deck/contrast.py) is:

```
if not light:
    sys.exit("no :root colour tokens found - is this a deck?")
```

**`contrast.verdicts` is not a pure producer, and the exit takes the whole gate with it.** Every other
stage returns `(rule, what, ok)` rows and lets [`check.py`](../tools/deck/check.py) assemble the
account; this one ends the process. A deck with a broken or missing theme therefore gets no account at
all — not a failing row, not a partition, not the 27 excusals — just a sentence and a non-zero status.
That is the opposite of what the coverage account exists to guarantee, and it is invisible on any deck
that has a theme, which is every deck anyone has run it on.

It also puts one producer permanently outside the fixture's reach on the input that fixture is built
from. T-075 worked around it by handing `contrast.verdicts` a theme with nothing to measure — which is
a legitimate absent subject and is now declared — but the empty document, the input every other
producer is held to, still cannot be passed to it.

**Scope**
- In: `contrast.verdicts` returns a row rather than exiting when the document declares no colour
  tokens. DS-013 is the rule that already says the tokens must be declared.
- In: the absent-subject fixture passes it the same empty document as the others, and its declarations
  are re-derived from that rather than from the hand-built theme T-075 gave it.
- In: **a sweep of every other stage for a `sys.exit` reachable from a `verdicts` function.** One was
  found by accident; the question of how many there are has not been asked.
- Out: `sys.exit` in a `self_test` or in `main`, which is where a tool refusing to run belongs.
- Out: what `check.py` should do with a deck that has no theme, beyond reporting it. The account
  already has a shape for that.

**Inputs**
- `tools/deck/contrast.py`, `tools/deck/audit.py` (`ABSENCE_IS_A_FAIL`, `self_test`)

**Acceptance criteria**
- [ ] `contrast.verdicts("")` returns rows and does not exit
- [ ] A deck with no `:root` colour tokens gets a full account with a failing row, shown end to end
- [ ] The fixture passes it the empty document, and its declarations are unchanged in meaning
- [ ] Every `verdicts` function in `tools/deck/` is checked for a reachable `sys.exit`, with the
      result recorded whether or not it found anything
- [ ] The reference deck's account is unchanged, diffed

**Open questions**
- ~~**Which rule does the row cite?**~~ **Settled 2026-08-10, and the recommendation was wrong.** It
  proposed returning the four rows as *undecided*; that would overturn a decision already recorded in
  `ABSENCE_IS_A_FAIL`, in writing, by T-051 and T-075 — *"the count was made a failure deliberately,
  because `0 of 0` passing is how a missing theme reads as a clean one."* No new row and no
  reclassification: all four keep failing, and the only change is that the process no longer ends
  before they can be returned. See §3.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the open question, since it decides whether this adds a row or converts four | The decision, in §3 |
| 2 | Replace the exit; run the fixture on the empty document and re-derive the declarations | `contrast.py`, `audit.py` |
| 3 | Sweep every `verdicts` function for a reachable `sys.exit` and record the result either way | The sweep, in §3 |
| 4 | Diff the reference deck's account; run the seeded-defect deck | Both runs |

## 3. Implement

**Decisions & assumptions**
- **The four rows keep failing; nothing is reclassified** — 2026-08-10, against §1's recommendation.
  `ABSENCE_IS_A_FAIL` already carries the argument and it is better than the one this task arrived
  with: a `0 of 0` pass is indistinguishable from a clean theme, which is why DS-027 owns the absence
  and 1.4.3 / 1.4.11 are declared *entailed by DS-027*. Checked before changing anything, and the
  declarations are unchanged in form as well as in meaning.
- **The refusal moves to `main`, it does not disappear** — 2026-08-10. Pointing this tool at a file
  by hand and being told it is not a deck is the useful answer; `check.py` asking the same question of
  the same document needs a row. Same condition, two callers, and the difference is who is asking.
  `main`'s message now names where the row appears instead.
- **`read_tokens` is the fix site, not `verdicts`** — the exit was one call down, in a helper. That is
  why a scan of producer bodies finds nothing, and it is what made the sweep below worth doing
  properly rather than with a grep.

**The sweep — every verdict producer, one call level down**

Twelve producers under `tools/deck/`, enumerated from source by `audit.verdict_producers()` rather
than by hand, each scanned for a `sys.exit` in its own body and in every function it calls.

| Producer | Reaches a `sys.exit` | Verdict |
| :--- | :--- | :--- |
| `contrast.verdicts` | was, via `read_tokens` | **fixed** |
| `theme.verdicts` | yes, via `load` | left alone |
| `component.verdicts` | yes, via `load` | left alone |
| the other nine | no | — |

**The two survivors are a different thing and the distinction is the finding.** Both exits are in a
loader reading the **contract document** — `CONTRACT: %s appears twice`, `parsed only %d parts …
the format moved under the parser`. That is the tool's own configuration being broken, not the deck
under judgement, and there is no honest row to emit about a deck when the ruleset that would judge it
cannot be read. **The boundary is whose input is malformed**: the document being judged gets a row,
the tool's own inputs get a refusal. `contrast` was on the wrong side of that line; these two are on
the right one.

**Outputs produced**
- [`tools/deck/contrast.py`](../tools/deck/contrast.py) — `read_tokens` returns instead of exiting;
  `main` refuses, and says where the row appears instead.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the fixture hands it `""`, the subject every other
  producer takes.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `contrast.verdicts("")` returns rows and does not exit | met | Four rows, all `False`, identical to what the hand-built theme produced. |
| A deck with no colour tokens gets a full account with a failing row, end to end | met | The reference deck with its theme region emptied: **113 rules owned, 81 checked, 18 failures** including DS-027, 1.4.3, 1.4.11 and DS-013. Before this change the same file produced one sentence and a non-zero status. |
| The fixture passes it the empty document, its declarations unchanged in meaning | met | Unchanged in form too — no entry moved between `ABSENCE_IS_A_PASS` and `ABSENCE_IS_A_FAIL`, which is the stronger result and the reason the open question closed against its own recommendation. |
| Every `verdicts` function checked for a reachable `sys.exit`, result recorded either way | met | The table above. It found two, and the interesting part is that both are correct. |
| The reference deck's account is unchanged, diffed | met | `check.py --json` before and after, compared by hash: **byte-for-byte identical.** |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | **The open question closed against its own recommendation**, which is the note worth keeping: §1 proposed returning the four rows undecided, and `ABSENCE_IS_A_FAIL` already held a written decision saying the opposite and giving a better reason. Reading the declarations before changing them turned a reclassification into a one-line fix, and left the reference deck's account byte-identical. The sweep found two more producers reaching a `sys.exit` and both are correct — the line is whose input is malformed, the deck's or the tool's, and it is now written down. |
| 2026-08-10 | → proposed | Found while T-075 brought every verdict producer inside the absent-subject fixture: `contrast.verdicts` is the one that cannot be handed the empty document, because it calls `sys.exit` rather than returning a row. **`v0.2` rather than `v0.1`, and the reason is that no adopter has hit it** — it fires only on a deck with no colour tokens at all, which the shell makes impossible to produce by accident. It is a defect in the gate's contract with itself rather than in what the gate reports, and T-075 has already declared the input it can take. |
