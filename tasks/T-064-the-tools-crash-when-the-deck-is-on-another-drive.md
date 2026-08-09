---
id: T-064
title: The tools crash when the deck is on a different drive from the plugin
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-008, T-061]
work_package: v0.1
owner: the project owner
business_value: critical
effort: xs
created: 2026-08-10
updated: 2026-08-10
deliverables:
  - tools/deck/paths.py
---

# T-064 — The tools crash when the deck is on a different drive from the plugin

## 1. Specify

**Outcome**
A deck anywhere on the machine can be checked. Today a deck on a drive other than the plugin's makes
the tools raise `ValueError` and exit, and the plugin is published, so this reaches users.

**The report**
From another project, 2026-08-10. Both `shell.py check` and `check.py` die on a deck under `N:` while
the plugin sits under `C:`:

```
ValueError: path is on mount 'N:', start on mount 'C:'
```

That project lives on `N:` by decision and had to copy the deck to `C:` to get any result at all.

**Reproduced here** — the mechanism is `os.path.relpath(deck, ROOT)` where `ROOT` is the *plugin's own
directory*, and `relpath` cannot express a path across Windows drives:

```
os.path.relpath(r"N:\proj\deck.html", r"C:\...\plugins\htmldeck")  ->  ValueError
```

**Every one of these calls is display-only.** They format a path for a heading:
`print("deck:    %s" % os.path.relpath(deck, ROOT))`. Nothing downstream consumes the result. So a
tool that has finished its work correctly dies while printing its own output, which is the worst
version of this bug rather than the mildest — the analysis was sound and is thrown away.

**Scope**
- In: every `os.path.relpath(..., ROOT)` in `tools/`. Grep found them in `audit.py`, `check.py`,
  `chrome_row.py`, `content.py`, `content_variants.py`, `contents_bound.py`, `contract.py`,
  `contract_variants.py`, `critique.py`, `deliverable_variants.py`, `print_variants.py`,
  `printpages.py`, `render.py`, `ruleset.py`, `shell.py`.
- In: a helper that degrades to the absolute path when a relative one is impossible, used everywhere.
- In: a fixture that **fails without the fix** (**L-04**), asserting the helper on cross-drive input.
- Out: making the tools resolve decks relative to the *project* rather than the plugin. That is a
  larger change about what `ROOT` means, and this defect does not need it.
- Out: `refcheck.py`, whose `relpath` calls are against the project root it `chdir`s into.

**Acceptance criteria**
- [ ] A cross-drive deck path prints a heading and completes, rather than raising
- [ ] The helper is used at every site the grep above found, not only the two the report named
- [ ] A fixture covers cross-drive input and fails without the fix
- [ ] `check.py` and `shell.py` still print an unchanged heading for a same-drive deck
- [ ] A patch release ships, because the published plugin has this defect

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add `display_path(path, start)` to the shared module, returning the absolute path when `relpath` cannot express one | The helper |
| 2 | Fixture: cross-drive input, and same-drive input that must be unchanged | The failing run, then passing |
| 3 | Replace every `relpath(..., ROOT)` display call | The edited tools |
| 4 | Verify a same-drive run prints exactly what it printed before | The diff of two runs |
| 5 | Patch release | The tag |

## 3. Implement

**Decisions & assumptions**

- **A courtesy may never fail — 2026-08-10.** `display_path` returns the relative path when that is
  expressible and the absolute one when it is not. Shortening a heading is a nicety; losing a whole
  run over it is not a trade anyone would take if asked.

- **Its own module rather than `render.py` — 2026-08-10.** `render.py` is the shared base for ten of
  these tools, but it carries the Chrome machinery, and `ruleset.py` is one of the commands the
  README describes as needing *"nothing but Python"*. A three-line path helper must not drag a
  browser driver into it. *Rejected: inlining the two-line fallback at each site*, which is fifteen
  copies of one fact.

- **Fifteen sites, not the two the report named — 2026-08-10.** The reporter hit `shell.py` and
  `check.py` because those are what the pipeline runs. `audit.py`, `critique.py`, `contract.py`,
  `content.py`, `printpages.py`, `render.py`, `ruleset.py`, `theme.py` and six more had it too.

- **`tools/assets/`, `tools/examples/` and `tools/portability/` were left — 2026-08-10.** Their
  `relpath` calls take paths the tool itself constructs **inside the repository** (`OUT`, `DST` under
  `examples/` and `.assets-cache/`), so they are same-drive by construction and cannot receive a
  user's deck. Recorded rather than silently skipped, because the scope said *every* call.

**Outputs produced**
- `tools/deck/paths.py`
- fifteen tools under `tools/deck/`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A cross-drive path prints a heading and completes | **met** | `display_path(r"N:\proj\deck.html", r"C:\plugin")` returns `N:/proj/deck.html`; the bare `relpath` raises |
| The helper is used at every site the grep found | **met** | Fifteen tools; `grep "os.path.relpath([^,]*, *ROOT)" tools/deck/` returns nothing |
| A fixture covers cross-drive input and fails without the fix | **met** | `paths.self_test()` asserts `relpath` **does** raise first, so the fixture cannot pass vacuously on a platform where it would not |
| Same-drive output unchanged | **met** | Every gate re-run: reference deck `0 failure(s)`, sort-window `0 failure(s)`, headings identical |
| A patch release ships | **met** | `v0.1.2` |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | **Fixed at fifteen sites, not the two that were reported.** The helper degrades to the absolute path when a relative one cannot be expressed, which is the whole fix: every crashing call was formatting a heading. Its self-test asserts that `relpath` **raises** before asserting the fallback, so on a single-drive machine the fixture reports that it could not verify rather than passing vacuously. The three tool directories left alone take repository-internal paths and cannot receive a user's deck, which is recorded in §3 rather than skipped quietly. |
| 2026-08-10 | → proposed | Reported from another project on `N:` and **reproduced here**. **`v0.1` rather than `v0.2`:** the plugin is published, and for anyone whose work is not on the plugin's drive it does not run at all — the same class as [T-061](T-061-the-scaffold-check-passed-a-manifest-the-installer-rejects.md), where the shipped artefact did not work and the fix was one line. Worth recording that every crashing call is **display-only**: the tool completes its analysis and then dies formatting the heading, so the fix cannot change a single verdict. |
