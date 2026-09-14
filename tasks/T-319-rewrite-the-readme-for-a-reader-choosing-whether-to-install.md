---
id: T-319
title: Rewrite the README for a reader choosing whether to install
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-300, T-056, T-060, T-320]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: high
effort: s
created: 2026-09-14
updated: 2026-09-15
deliverables: [README.md, .github/readme/deck-chart.png, .github/readme/deck-print-contents.png, .github/readme/deck-colophon.png, tools/docs/figures.py]
---

# T-319 — Rewrite the README for a reader choosing whether to install

## 1. Specify

**Outcome**
`README.md` is the GitHub front page for a stranger deciding whether to install: what htmldeck is,
what a deck looks like, how to install, what it does, how to use it, and where the examples are.
It is shorter than the 0.7.0 page and carries screenshots of a shipped deck.

**Scope**
- In: `README.md`; screenshots of shipped example decks under `.github/readme/`; the repository
  description (the GitHub *About* text).
- Out: every other document. How the project is maintained (phases, audits, tasks, lessons,
  release chronology) and any other project by name. The same removal across the rest of the tree
  is [T-320](T-320-remove-what-the-repository-says-about-other-projects.md).

**Inputs**
- The owner's request, 2026-09-14: facts first, then brief reasoning; screenshot; install; feature
  highlights; usage; examples; no other projects; no maintenance method; more attractive, not more
  verbose.
- `docs/PUBLISHING.md` §5 (humanizer mode and the owner's exception) and §6 (figures survive
  byte-identical; `tools/docs/figures.py` proves it).
- `examples/README.md` for deck facts; `skills/htmldeck/SKILL.md` for the two questions.

**Acceptance criteria**
- [x] Sections: pitch, screenshot, install, features, usage, examples, licence. No section on
      maintenance method, backlog or release history. No other project named.
- [x] Every image is a capture of a shipped deck, cropped to the stage or the printed page.
- [x] The humanizer ran over the draft, under `docs/PUBLISHING.md` §5's exception.
- [x] `python tools/docs/figures.py` and `python tools/docs/refcheck.py` are green.
- [x] The owner reviewed the draft.

**Open questions**
- Does "remove other projects" reach beyond the README? — the owner, 2026-09-15: no; the rest of the
  tree is T-320.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Research how popular repositories structure a README front page | Section order and techniques, used in step 3 |
| 2 | Capture slides with `tools/deck/render.py shots` and a printed page with Chrome `--print-to-pdf`, crop, scale | `.github/readme/*.png` |
| 3 | Draft the README | `README.md` |
| 4 | Humanizer pass, `docs/PUBLISHING.md` §5 | `README.md` |
| 5 | Run `figures.py` and `refcheck.py` | Green, or the draft corrected |
| 6 | Owner review | Accepted, or revised |

## 3. Implement

**Decisions & assumptions**
- Images go under `.github/readme/`, not `docs/`: they serve the repository page and are not part of the plugin payload. Reversible. — 2026-09-14
- The top image is the portfolio review's slide 6 (a waterfall chart with a disclosure control and a source link); the pair under the features is the reference deck's printed contents page and its colophon. Chosen by the owner 2026-09-15, replacing a network-diagram slide and a timeline slide. Reversible. — 2026-09-15
- The README keeps one compared block, `check.py` on the reference deck, because it shows the gate's account to a reader and `figures.py`'s self-test fails a README with no compared block. Reversible. — 2026-09-15
- `EXCLUDED_FENCES` lost `git clone https://` and `taskmd check`, whose fences left the page. Reversible. — 2026-09-15
- `figures.py`'s self-test required the live README to carry a `refcheck.py` floor block and a built-deck size, so a page without maintenance output failed it. `fixture_tail()` now derives both at test time and appends them to the self-test's copy of the page; the live page is still audited as written. The owner agreed 2026-09-15. Reversible. — 2026-09-15
- Repository description, humanizer pasted-text mode. Draft and final: *A Claude Code plugin for presentations that don't look generated. You get one HTML file that opens with a double-click and works offline.* What still sounds generated: nothing flagged. Claims changed from the 0.7.0 text: the stale `165-rule` count and the critique clause were dropped, nothing added. Set with `gh repo edit` 2026-09-15 on the owner's approval. Reversible. — 2026-09-15

**Outputs produced**
- `README.md`: 359 lines to 142 at the first draft.
- `.github/readme/deck-chart.png`, `deck-print-contents.png`, `deck-colophon.png`
- `tools/docs/figures.py`: `fixture_tail()`, and the exclusion table trimmed.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Sections, no maintenance method, no other project | pass | `taskmd`, adopter reports, phases, audit and release history removed |
| Images are captures of a shipped deck | pass | `render.py shots`; the print page from Chrome `--print-to-pdf`, rendered with PyMuPDF |
| Humanizer pass | pass | Installed 2.11.2; patterns 15, 16, 18 re-verified by name |
| Gates green | pass | `figures.py` 0 stale figures; `refcheck.py` 0 broken |
| Owner review | pass | Text accepted 2026-09-15; images changed at the owner's direction |

**Child fix tasks raised**
- [T-320](T-320-remove-what-the-repository-says-about-other-projects.md)

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | → in_progress | Created from the owner's request during B29, and batched into B29 after T-318. |
| 2026-09-15 | → review | Owner reviewed the draft; images replaced as directed; self-test fixture added. |
| 2026-09-15 | → done | Owner: "Looks all good". No lesson beyond the existing rule that a self-test must not assert repo state. |
