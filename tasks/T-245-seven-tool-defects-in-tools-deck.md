---
id: T-245
title: Fix seven defects in the deck tools, each with its own seeded proof
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables: []
---

# T-245 — Fix seven defects in the deck tools, each with its own seeded proof

## 1. Specify

**Outcome**
Seven tools behave as their own documents say. Today `theme.py swap`'s refusal path crashes instead of reporting and had never run; the diagram-placement gate measures one diagram per slide where a shipped deck has two; `shell.py` states its region count three ways and prints one of them; the browser search names five Windows paths, four Linux binaries and no macOS install; `rulerstrip.py` and `longdeck.py` build an exit code and throw it away; `quickview.py` escapes a title in three places and not in two; and `deck.js` dereferences `toDoc` and `motionBtn` unguarded.

**Closes** `PR-38`, `PR-42`, `PR-55`, `PR-56`, `PR-58`, `PR-59`, `PR-78` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the seven sites the register names, one per finding
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-38`, `PR-42`, `PR-55`, `PR-56`, `PR-58`, `PR-59`, `PR-78`
- each finding's own evidence column, which carries the command that reproduces it

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce each of the seven from its own evidence column | seven failing observations |
| 2 | `PR-38` — format the pairs, then **sweep the file for the same shape**, which the row asks for | one line, and a sweep that came back empty |
| 3 | `PR-55` — derive the count from `SLOTS` everywhere a reader meets it | one number, four sites |
| 4 | `PR-56` — decide which of the row's two fixes, then take it | the macOS bundles, because only that keeps *clone and run* whole |
| 5 | `PR-58` — return `0` on success, then wrap both entry points | five failure codes the shell can see |
| 6 | `PR-59` — decide which title form is the tool's currency, then move every boundary to it | the raw title, escaped at the markup edge and unescaped coming back |
| 7 | `PR-42` — iterate the figures, and count what the filters decline | ten diagrams where there were nine, and a declined count |
| 8 | `PR-78` — guard the two ids the way the other three already are | a deck whose chrome tail is short still starts |
| 9 | Sync the four tracked decks, re-derive the seeded fixture, re-run both gates | a tree where a green covers what is in it |
## 3. Implement

**Decisions & assumptions**
- **`PR-42` moved a rule, and the rule question went to the owner.** Fixing the selector made
  `figgrid.py` see ten diagrams on portfolio-review where it saw nine, and the tenth — the
  right-hand figure of a two-column slide, **correctly placed in its own column** — failed DS-236 by
  **+962.3 du**. So the rule as written could not be satisfied by a correct figure, and its
  population had never been complete: T-184's 21 were counted through the same blind probe. The
  order's §4 does not cover a rule question, so it stopped the batch and was put to the owner with
  four options. **Ruled the same day: a diagram answers to the text column it sits in.** DS-236's
  row is amended, marked reversible, and portfolio-review reads **0 of 10** — 2026-08-29
- **The column is found by geometry, never by class name.** `.col` is the deck's own vocabulary and
  the shell defines nothing of the sort, so a probe matching it would be reading one deck's markup
  and calling it a rule. The column is the outermost ancestor still materially narrower than
  `.body`; a one-column slide has none and falls back to the slide's text edge, which is why the
  other three decks are unchanged at 8, 7 and 6 with every reference still 96.0 du — 2026-08-29
- **`PR-38`'s wider hypothesis was swept and came back empty.** The row suspected the same shape
  behind other refusal paths in the file. The three other joins over checker output in `tools/deck/`
  hold strings, and `theme.py`'s own second use already unpacked the pair. One instance — 2026-08-29
- **`PR-56` is not verified on macOS**, because there is no macOS here. The search now names the
  right places; that is a search corrected, not an install confirmed — 2026-08-29
- **`PR-58` changed `longdeck.py` too**, on the row's uniformity argument rather than on a defect —
  2026-08-29
- **`PR-78` guarded `toStage` as well as the two the row names.** Its twin sits one line below
  `toDoc` and is the same dereference on the same slot; guarding one would have left the identical
  crash reachable by removing the other button. `setMotion` still sets `root.dataset.motion` when
  the button is absent, because motion is a property of the deck and only the label is a property of
  the control — 2026-08-29
- **`PR-78`'s wider hypothesis is left open.** Whether the chrome tail is really bounded to two
  forms — and so whether `shell.html`'s comment or `shell.py check` should give way — is a second
  rule question, and one ruling in a batch is what the order's §4 allows. The script now agrees with
  the shell's own description of the region, which is the half that was a defect — 2026-08-29

**Outputs produced**
- `tools/deck/theme.py` — `swap`'s refusal formats `validate()`'s pairs
- `tools/deck/figgrid.py` — the probe iterates, counts what it declines, and measures each diagram
  against its own column; `Figures`, `_declined()`, and the wording that follows the amended rule
- `docs/DESIGN-SYSTEM.md` — DS-236 amended under DS-000, reversible
- `tools/deck/shell.py` — the region count derived from `len(SLOTS)` at four sites
- `tools/deck/render.py` — `BROWSERS` gains the macOS bundles
- `tools/deck/rulerstrip.py`, `tools/deck/longdeck.py` — the exit code reaches the shell
- `tools/deck/quickview.py` — `unesc()`, and the title's one boundary
- `shell/deck.js` — `toDoc`, `toStage` and `motionBtn` guarded
- the four tracked decks, synced; `examples/reference-deck-seeded-defects.html`, re-derived
## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy measured, or explicitly deferred with the reason on its row | pass | Seven closed. `PR-42` needed a rule ruling to close; `PR-78`'s wider half is explicitly left open on its row and is a separate rule question |
| each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Seven rows rewritten, each carrying its own measurement |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both at the end of B10, tree frozen, run one after the other |

**Measurements that decided something**
- `PR-42`: 9 → **10** diagrams on portfolio-review; **0 of 10** off after the amendment; 8, 7 and 6
  on the other decks with 6, 5 and 7 icons declined — counts that were invisible in both numbers
- `PR-55`: `shell.py parts` printed *eleven* above twelve rows; now **12** above 12, `len(SLOTS)` 12
- `PR-58`: `rulerstrip.main([])` with no Chrome returns **3**, which the shell now sees
- `PR-78`, both directions in real Chrome: `HEAD` with the `Read` button removed gives
  `data-preflight` **fail**, **0 of 13** current; the fixed shell gives **none**, **1 of 13**, and
  so does the fixture with the motion button removed

**No look owed.** Six of the seven are tools, which render nothing. The seventh, `PR-78`, guards
three dereferences that are no-ops on a deck carrying all five of the chrome tail's ids - which every
tracked deck does - and its proof is a fixture built by *removing* a button, never a shipped deck.
The four decks were re-synced, so their bytes moved; what they render did not, and `check.py` decides
that on every run. An empty queue after a batch of checker work is the correct answer, not a gap.

**Child fix tasks raised**
- none
## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-08-29 | proposed → done | Worked in **B10** of the remediation order. Seven findings closed. **`PR-42` stopped the batch on a rule question** — the fixed probe found a correctly placed figure that DS-236 as written could not pass — which went to the owner and was ruled the same day: a diagram answers to the text column it sits in. DS-236 amended under DS-000 and reversible. **`PR-78`'s wider hypothesis is left open** as a second rule question. |
