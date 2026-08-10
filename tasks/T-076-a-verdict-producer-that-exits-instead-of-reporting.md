---
id: T-076
title: A verdict producer that exits the process instead of reporting a row
type: fix
status: proposed
phase: specify
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
- **Which rule does the row cite?** DS-013 already requires every contracted token to be declared and
  is what fails today on a themeless document, so a second row citing it is a duplicate rather than a
  finding. Recommended: `contrast.verdicts` returns its four rows as undecided and lets DS-013 carry
  the failure, since it is the rule that states the requirement.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the open question, since it decides whether this adds a row or converts four | The decision, in §3 |
| 2 | Replace the exit; run the fixture on the empty document and re-derive the declarations | `contrast.py`, `audit.py` |
| 3 | Sweep every `verdicts` function for a reachable `sys.exit` and record the result either way | The sweep, in §3 |
| 4 | Diff the reference deck's account; run the seeded-defect deck | Both runs |

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
| 2026-08-10 | → proposed | Found while T-075 brought every verdict producer inside the absent-subject fixture: `contrast.verdicts` is the one that cannot be handed the empty document, because it calls `sys.exit` rather than returning a row. **`v0.2` rather than `v0.1`, and the reason is that no adopter has hit it** — it fires only on a deck with no colour tokens at all, which the shell makes impossible to produce by accident. It is a defect in the gate's contract with itself rather than in what the gate reports, and T-075 has already declared the input it can take. |
