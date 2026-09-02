---
id: T-269
title: Unwrap a provenance row, read a rich Sources field, and convert bold across a line break
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-269 — Unwrap a provenance row, read a rich Sources field, and convert bold across a line break

## 1. Specify

**Outcome**
Three build-path tools handle input the adopter's deck actually contained. Today the reading view undoes the sources **box** and never the **item**, so `white-space:nowrap` survives into a document that must fold to 320 px and one long row holds the page open — while `DS-075` reports `overflowing: 0` because the probe scans `#docBody *` and the wide element is outside it; `spec.py` splits a `Sources` field on commas and semicolons and treats every fragment as a slug, so a field naming its section breaks `SPEC-2`, `SPEC-3` and `SPEC-4` at once; and a quick view leaves `**bold**` unconverted when the emphasis spans a line break.

**From the adopter report** [`003`](../docs/adopter-reports/claimai/003-reading-view-never-unwraps-a-provenance-row.md), [`004`](../docs/adopter-reports/claimai/004-spec-py-cannot-read-a-sources-field-that-carries-a-section.md), [`007`](../docs/adopter-reports/claimai/007-quickview-leaves-bold-unconverted-across-a-line-break.md).

**Scope**
- In: `.doc .sources-item{white-space:normal}` beside the `.doc .sources-box` rule it belongs with — **a deck should not have to repair the reading view**, and this one did
- In: splitting the `Sources` field on `;` only and taking the leading token, so both forms read; and `artifacts.md` stating the field's grammar, because today the only statement of it is a regex
- In: normalising a paragraph before the inline pass — **and a gate**: a scan for unconverted `**`, `__` or a leading `#` in rendered quick-view content, run where `spec.py` runs
- In: widening the `DS-075` probe's scan, or naming the widest element whatever the count says
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the records above, [`003`](../docs/adopter-reports/claimai/003-reading-view-never-unwraps-a-provenance-row.md), [`004`](../docs/adopter-reports/claimai/004-spec-py-cannot-read-a-sources-field-that-carries-a-section.md), [`007`](../docs/adopter-reports/claimai/007-quickview-leaves-bold-unconverted-across-a-line-break.md) — each carries its evidence, its version and its own proposed fix
- each record carries its own reproduction; `003`'s is the one that cost most, because the failure named a number with nothing beside it

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce each of the three, from the reproduction its own record carries | three failing observations, not three descriptions |
| 2 | `003` — the CSS rule, and the probe's scan beside it | `.doc .sources-item`, and a DS-075 count taken over the subtree the number measures |
| 3 | `004` — measure the tracked specifications before touching `slugs()` | the separator the shipped decks actually use, which decides whether the proposed remedy survives |
| 4 | `004` — the split, and the grammar stated where a builder reads it | `spec.py`, and `artifacts.md` |
| 5 | `007` — find the site, which the record's own diagnosis does not name | the list-item continuation, not the paragraph |
| 6 | `007` — the renderer, then the gate the record asks for | `inline` called once per run, and a leak scan run where `spec.py` runs |
| 7 | Seed each fix and watch its check fire in both directions (**L-125**) | self-test fixtures, kept |
## 3. Implement

**Decisions & assumptions**
- **`004`'s proposed remedy is refused** — split on `;` alone, as report `004` proposes, reads
  `D5-management-decision-matrix, D2-predictive-analytics-assessment` as **one** slug. All three
  tracked specifications separate with commas and never a semicolon, and `artifacts.md` states the
  comma, so the proposal fails every deck this repository ships. Measured before writing anything.
  What landed is decided by the entry's own shape: `;` always separates, and inside a part the comma
  separates only until something marks that part as carrying prose — ` — `, ` – ` or ` §`. Both
  forms read — 2026-08-29
- **`007`'s record names the wrong site** — it proposes normalising the paragraph before the inline
  pass, and `flush_para` already joins the paragraph and converts once, which is why the same
  sentence as a paragraph always converted. The failing site is the **list item**: its first line was
  converted on arrival and each wrapped continuation converted separately. The record's source
  passage is indented under a list marker, which is why a paragraph-shaped diagnosis fitted the
  symptom. Fixed at the item — 2026-08-29
- **The leak gate scans every carried rendering, not only the compared ones** — a leak is a property
  of the rendering and needs no source file, and the views `--source` did not name are exactly the
  ones nothing else in that command reads — 2026-08-29
- **The leak gate scans text runs, not the body** — the first draft's docstring claimed the patterns
  could not fire on an attribute, and the seeded fixture said otherwise: `data-t="a**b**c"` matched.
  Tags are split out first, and the claim is now a split rather than a sentence — 2026-08-29
- **`003`'s probe is widened rather than its message reworded** — the record offered either. The
  count was taken over `#docBody *` while the number reported was `scrollWidth` off `#doc`, so the
  two could contradict each other; a count over a smaller subtree than its own measurement is worse
  than no count. Both halves of the record are closed by the one change — 2026-08-29

**Outputs produced**
- `shell/components.css` — `.doc .sources-item{white-space:normal}`, beside the box rule
- `tools/deck/audit.py` — the DS-075 probe counts over the subtree `scrollWidth` measures
- `tools/deck/spec.py` — `RICH_ENTRY` and the rewritten `slugs()`
- `skills/htmldeck/references/artifacts.md` — the `Sources` grammar, with three worked examples
- `tools/deck/quickview.py` — `settle`/`open_run` in the renderer, `leaked()` and `LEAKS`, the scan
  in `check()`, and seven self-test fixtures across both directions
- `docs/adopter-reports/claimai/003`, `004`, `007` — closed, each with what the measurement said
## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every record named above is closed with its remedy measured, or explicitly deferred | pass | Three closed. **`004`'s remedy was refused by measurement** and replaced; `007`'s was refused as a diagnosis and the real site fixed. Both recorded on the records themselves |
| each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | `007`: the seeded body — the exact markup the old renderer produced — fires the gate, the fixed body does not, and four false-alarm shapes stay silent. `004`: eight fields, tracked and rich. `003`: the CSS is a look, recorded as owed |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both run at the end of B10, separately and with the tree frozen. Recorded in the batch's log row below |

**Child fix tasks raised**
- none

**No look owed, and that is a measurement rather than an omission.** `003`'s CSS was the one change
here that could alter what a reader sees, so it was measured rather than assumed: the reading view of
each tracked deck rendered at 320 CSS px, before and after. **`measure-first` wraps 19 of its 25
provenance rows either way** - it uses the `sources--list` variant, which has carried
`white-space:normal` since before this task - and the other three wrap none, their widest row being
264 px inside a 320 px column. `scrollWidth` is 320 on all four in both trees. The rule is still the
right fix, because the deck that reported it is not one of these four and had to repair the reading
view itself; it simply changes nothing here. [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) says a task
that changes nothing a reader sees writes no row, and this is that case.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-29 | proposed → done | Worked in **B10** of the remediation order. All three records closed; **two of the three proposed remedies were refused by measurement** and replaced — `004`'s separator would have broken every tracked specification, and `007` named the paragraph path, which was already correct. The gate `007` asked for is in `quickview.py check` and reads **20 quick views, 0 leaking** across the tracked decks. **No look owed**, measured rather than assumed: the reading view of all four tracked decks is byte-identical in behaviour before and after the CSS rule, because none of them is the deck that reported it. |
