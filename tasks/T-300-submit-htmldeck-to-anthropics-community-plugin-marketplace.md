---
id: T-300
title: Submit htmldeck to Anthropic's community plugin marketplace
type: admin
status: in_progress
phase: implement
parent: null
blocked_by: [T-271, T-282, T-287, T-290, T-294, T-296, T-298, T-301, T-303, T-304, T-305, T-307, T-308, T-309, T-311, T-318, T-319, T-320]
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-12
updated: 2026-09-15
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
- **`CLAUDE.md` stays at the repository root, and the plugin manifest fails `--strict` because of it.**
  `claude plugin validate . --strict` exits 0, but on a directory holding
  `.claude-plugin/marketplace.json` it validates that manifest and nothing else. `claude plugin
  validate .claude-plugin/plugin.json --strict` exits 1 on one warning: *CLAUDE.md at the plugin root
  is not loaded as project context*. A probe plugin in a temporary directory raised it with a root
  `CLAUDE.md` and not with the same file inside a `.claude` directory, so moving the file would clear
  it. The move was not
  made: `git grep` found `CLAUDE.md` named in 220 tracked files, 642 times, 125 of them Markdown
  links, and the file is this repository's tier 1. The warning is also right about adopters, since
  the file is for working on htmldeck and not for using it. **Reversible**: if the review rejects the
  submission on it, the move is the fix, as its own task.
- **"Scored" is struck from the catalog text.** The draft offered a scored critique, and
  [`critique.md`](../skills/htmldeck/references/critique.md) §6 says no score reaches the report.
  What a design-audit finding carries, per its §3.2, is the rule it violates and the slide it is on,
  and the final text says that instead.
- **"Asks two questions" is scoped to building.** [`SKILL.md`](../skills/htmldeck/SKILL.md) says the
  two questions do not apply when a deck is reviewed.
- **The submission link is recorded as measured.** The community repository's README now points at
  `https://clau.de/plugin-directory-submission`, which answered `302` to
  `https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-official-marketplace` on
  2026-09-15. §1's route to the Console form for an individual author is not changed by it.

**Outputs produced**
- **Every figure in §1 and §2, re-measured 2026-09-15.** The catalog was fetched with
  `gh api -H "Accept: application/vnd.github.raw" repos/anthropics/claude-plugins-community/contents/.claude-plugin/marketplace.json`.

  | Figure | 2026-09-12 | 2026-09-15 |
  | :--- | :--- | :--- |
  | `claude plugin validate . --strict` | exit 0 | exit 0, marketplace manifest only |
  | `claude plugin validate .claude-plugin/plugin.json --strict` | not run | exit 1, the `CLAUDE.md` warning above |
  | Catalog entries | 2,282 | 2,282 |
  | `htmldeck` taken | no | no |
  | Entries setting a homepage | 2,280 | 2,280 |
  | Median description, and share over 200 characters | 274, 64% | 274, 64% |
  | Neighbours matching *slide*, *presentation*, *deck* or *pptx* | 29 | 28 |
  | Neighbours claiming *offline* | `semanticsearch` only | `semanticsearch` only |
  | Neighbours saying *critique* | `arcdeck` | `arcdeck`, a critique-revise-judge loop producing PowerPoint |
  | Neighbours saying *self-contained* | `keynot`, `slidecast` | `keynot`, `slidecast`, `bloom` |
  | Tools making outbound requests | `tools/assets/measure.py` | `tools/assets/measure.py`, the only `urllib.request` import under `tools/` |

- **The two long fields, humanized** with `humanizer` 2.11.2 in pasted-text mode, under the owner's
  exception in [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §5.
  - **Draft description:** *Single-file HTML presentations that don't look generated. Build a slide
    deck as one .html file that opens offline with zero external references, carrying real diagrams,
    progressive disclosure and considered typography. Or point it at an existing deck for a scored
    critique. Asks two questions and nothing else.*
  - **Patterns found:** an `-ing` tail (3), a subjectless clipped close (9, 13), a contrast with
    bullet lists in the third use case (9). The three-feature list was kept: it is three real
    features from the manifest, not padding (10).
  - **Claims changed:** removed *scored* (false, above), *and nothing else*, and *instead of bullet
    lists* (never verified). Added *blunt*, from `.claude/rules/decks.md`'s *Voice*.
  - **Final, for the form:**

    ```text
    Plugin description:
    Single-file HTML presentations that don't look generated. htmldeck builds a slide deck as one .html file that works offline, with real diagrams, progressive disclosure and careful typography. It asks two questions, then builds. Point it at an existing deck and it writes a blunt critique naming the slide and the rule behind each finding.

    Example use cases:
    - Turn an outline or a brief into a presentation you can send as one file and open with no network.
    - Review a deck you already have: a blunt critique that names the slide and the design rule behind each finding.
    - Explain a technical argument with diagrams that reveal one step at a time.
    ```

- **Every other field** is §1's two tables as written: the path blank, Claude Code only, `MIT`, the
  privacy-policy URL blank with `measure.py`'s fetches accounted for.

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
| 2026-09-15 | proposed → in_progress | Every blocker closed, so §1 and §2 stood as written and the work went to implement. Every figure re-measured, the two long fields humanized, and one new finding: the plugin manifest fails `--strict` on the root `CLAUDE.md`, kept there for the reason in §3. **Every value is ready, and the record waits for the owner to send the form.** |
