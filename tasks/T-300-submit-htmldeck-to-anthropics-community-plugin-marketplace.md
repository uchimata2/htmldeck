---
id: T-300
title: Submit htmldeck to Anthropic's community plugin marketplace
type: admin
status: proposed
phase: specify
parent: null
blocked_by: [T-271, T-282, T-287, T-290, T-294, T-296, T-298, T-301, T-303, T-304, T-305, T-307, T-308, T-309, T-311, T-318]
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-12
updated: 2026-09-14
deliverables: []
---

# T-300 — Submit htmldeck to Anthropic's community plugin marketplace

## 1. Specify

**Outcome**
htmldeck is submitted to `anthropics/claude-plugins-community`, the marketplace a user adds as
`@claude-community`, with the form's values chosen deliberately rather than left at their defaults.
Everything in §1 below was measured on 2026-09-12 while the sibling project `taskmd` was submitted;
it is restated here rather than cited, because a pointer into another repository is not resolvable
from this one.

**The official marketplace is the wrong target, and its own README says otherwise.**
`claude-plugins-official` is curated at Anthropic's discretion. Their documentation states there is
**no application process** and that the submission form does not add plugins to it. The marketplace
repository's README reads *third-party partners can submit plugins for inclusion in the marketplace*,
which is what produced the wrong answer the first time. Trust the documentation.

**The route.** Two forms exist. The claude.ai one requires a Team or Enterprise organization with
directory-management access. An individual author uses the Console form at
`https://platform.claude.com/plugins/submit`. It is behind a sign-in, so a session cannot submit; the
work here is to have every value ready and correct.

**What the form asks, in two screens.**

*Screen 1 — plugin information*

| Field | Value for htmldeck | Why |
| :--- | :--- | :--- |
| Link to plugin | `https://github.com/uchimata2/htmldeck` | |
| Path within repository | **leave blank** | `.claude-plugin/marketplace.json` declares `"source": "./"`, so the plugin *is* the repository root. taskmd needed a value here because its manifest sits under `plugin/`; this repository is the other case, and copying that answer would break the submission. |
| Plugin homepage | `https://github.com/uchimata2/htmldeck` | 2,280 of the 2,282 catalog entries set it. |
| Plugin name | `htmldeck` | Must equal `name` in `.claude-plugin/plugin.json`. It is the skill namespace and **immutable once published** — renaming it later breaks every install with `plugin-not-found`. Verified free against all 2,282 entries on 2026-09-12. |
| Plugin description | see below | |
| Example use cases | see below | |

*Screen 2 — submission details*

| Field | Value | Why |
| :--- | :--- | :--- |
| Supported platforms | **Claude Code only** | The field's own instruction is to test each surface first. Cowork has never been run against this plugin. Add Cowork after someone has built a deck there. |
| License type | `MIT` | `LICENSE` and `plugin.json` agree. |
| Privacy policy URL | leave blank, **but read the note below first** | |
| Email address | prefilled | |

**The privacy-policy field needs a check this project cannot skip.** `"source": "./"` means an
install copies the whole repository, `tools/` included, and **`tools/assets/measure.py` makes
outbound requests** — `fonts.googleapis.com` for font CSS and `cdn.jsdelivr.net` for `.woff2` files.
`tools/deck/render.py` imports `urllib.parse` only and reaches nothing. No personal data is
collected either way, so blank is still the right answer, but do not answer this field by claiming
the plugin makes no network calls. One of its tools does, by design, and a safety screen that
notices before you do is worse than saying so.

**Scope**
- In: the form's values, and any manifest change they expose
- In: confirming `claude plugin validate . --strict` still exits 0 at the time of submission
- In: **re-measuring every figure in this record when the work starts.** They date from 2026-09-12,
  and the owner scheduled other tasks to land first, any of which can move `plugin.json`, the
  validator's result or the catalog
- Out: the submission itself. The form is behind a sign-in and is the owner's to send
- Out: **review and close before the owner confirms the form was sent.** Implement ends with every
  value ready, and the record waits there
- Out: adding Cowork as a supported surface. That is a test first, then a resubmission

**Inputs**
- `.claude-plugin/plugin.json` — `name`, `version`, `description`, `author`, `keywords`
- `.claude-plugin/marketplace.json` — the `"source": "./"` that settles the path field
- `docs/PUBLISHING.md` — the covered-set rule, if the description is treated as human-facing text

**Acceptance criteria**
- [ ] `claude plugin validate . --strict` exits 0, captured as output rather than asserted
- [ ] The path field is left blank, and the record says why
- [ ] The description is written for the catalog's norms, not copied from the manifest unchanged
- [ ] Supported platforms names only a surface that has actually been tested
- [ ] The privacy-policy answer accounts for `tools/assets/measure.py`'s outbound fetches
- [ ] `htmldeck` is re-checked as free in the catalog at submission time, not trusted from 2026-09-12
- [ ] At close, `shipped_in` follows `tasks/TASK-WORKFLOW.md` for a task that ships no version.
  `python tools/tasks/lint.py` counts closed records without one; it printed
  ``0 closed with no `shipped_in` `` on 2026-09-12

**Open questions**
- Is the catalog description covered text under `docs/PUBLISHING.md`'s *what a stranger reads before
  installing* test? It is read in a directory listing before anything is installed, which argues yes,
  and yes means it goes through the humanizer before submission — the owner answers.
  **Answered by the owner 2026-09-14: yes.** The description goes through the humanizer before
  submission.
- Which tasks must close before this one starts? The owner scheduled other work first. Any that
  must land before submission belong in `blocked_by`, not in prose — the owner answers.
  **Answered by the owner 2026-09-14: every open task except `T-057`**, the 3D line 1.0.0 does not
  wait for. They are in `blocked_by`, and 1.0.0 is released with this submission once they close.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Run `claude plugin validate . --strict` and capture the output | evidence, not an assertion |
| 2 | Answer the open question above, then draft the description and use cases | the two long fields |
| 3 | Fill both screens from the tables in §1 | a completed form |
| 4 | Owner submits; record what was sent | this record's §3 |

**Description — a draft, not the answer.** The catalog's median description is **274 characters** and
64% run over 200; `plugin.json`'s current 218 is serviceable but does not carry the words someone
would search. The gap to close is *deck*, *slides*, *presentation*, *offline*, *critique*, *diagram*.
**The neighbours, measured 2026-09-12.** 29 catalog entries match *slide*, *presentation*, *deck* or
*pptx* in their name or description. **Self-contained is already claimed**: `keynot` describes a
self-contained HTML slide deck in a single file with no runtime dependencies, which is close to this
plugin's opening sentence, and `slidecast` also says self-contained. Most of the rest produce `.pptx`
(`genpptx`, `pptx-deck-plugin`, `hackflow-ppt`, `arcdeck`) or PDF (`pdf-forge`). **None of them
claims offline**: the one catalog match for the word in that set is `semanticsearch`, a search tool.
*Critique* appears in one description, `arcdeck`'s; read it before calling the critique mode unique.

**Category.** The catalog stores one, but the Console form asks for none on either screen, checked
when the sibling project `taskmd` was submitted on 2026-09-12. It is not a field you can fill.

## 3. Implement

**Decisions & assumptions**
- <not started>

**Outputs produced**
- <not started>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-12 | → proposed | Created from the sibling project `taskmd`'s submission the same day, with every figure re-measured against this repository rather than carried over. **Two answers differ from taskmd's and would be wrong if copied**: the path field is blank here because `source` is `./`, and the privacy-policy reasoning has to account for `tools/assets/measure.py` fetching fonts over the network. |
| 2026-09-13 | no change | **Folded in what a separate prompt would otherwise have carried**, on the owner's instruction that everything this task needs lives in the record: the stop before review, re-measuring before the work starts, the `shipped_in` rule at close, and the question of which tasks land first. **Two claims corrected**: the form has no category field, and the Cowork row asserted a difference between surfaces that nobody measured. The neighbours paragraph is now measured against the catalog rather than described. |
| 2026-09-14 | no change | The owner answered both open questions: the catalog description is humanized, and every open task except `T-057` closes first, so `blocked_by` names them. |
| 2026-09-14 | no change | `T-318` joined B29 ahead of this task by the owner's ruling, and `blocked_by` names it. |
