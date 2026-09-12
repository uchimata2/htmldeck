---
id: T-300
title: Submit htmldeck to Anthropic's community plugin marketplace
type: admin
status: proposed
phase: specify
parent: null
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-12
updated: 2026-09-12
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
| Supported platforms | **Claude Code only** | The field's own instruction is to test each surface first. Cowork has never been run against this plugin, and it ships `tools/` and `shell/`, which is exactly what differs between surfaces. Add Cowork after someone has built a deck there. |
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
- Out: the submission itself. The form is behind a sign-in and is the owner's to send
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

**Open questions**
- Is the catalog description covered text under `docs/PUBLISHING.md`'s *what a stranger reads before
  installing* test? It is read in a directory listing before anything is installed, which argues yes,
  and yes means it goes through the humanizer before submission — the owner answers.

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
The nearest catalog neighbours are presentation and markdown-slide plugins, so the differentiator to
lead with is the one they do not have: a deck that renders with the network disabled, and a critique
pass that scores an existing deck rather than only generating a new one.

**Category.** The form's next screen stores one. `development` holds 104 entries and `productivity`
18, against 2,125 with none set at all. Filling it is a cheap differentiator either way; `design` has
a single entry and is arguably the honest home for this plugin.

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
