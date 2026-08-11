---
id: T-094
title: render.py shots --out with a relative path writes nothing and says FAILED
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-019, T-074]
work_package: v0.1
owner: maintainer
business_value: high
effort: xs
created: 2026-08-11
updated: 2026-08-11
deliverables: []
---

# T-094 — render.py shots --out with a relative path writes nothing and says FAILED

## 1. Specify

**Outcome**
`python tools/deck/render.py shots <deck> --out <dir>` writes the shots whether `<dir>` is relative
or absolute, and cannot report `FAILED` for a reason that is not about the deck.

**Why this one**
Observed 2026-08-11 while looking at the decks for
[T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md):

```
python tools/deck/render.py shots examples/reference-deck.html 4,10 --out .assets-cache/deck/normal
  slide-05.png  FAILED
  slide-11.png  FAILED

python tools/deck/render.py shots examples/reference-deck.html 4,10 --out C:\...\deck\normal
  slide-05.png  151 KB
  slide-11.png  132 KB
```

`out_dir(deck, override)` is where `os.path.abspath` lives, and `cmd_shots` takes the override
without going through it — so `--screenshot=` reaches Chrome as a relative path and Chrome resolves
it somewhere the caller does not look. `measure` has the same shape and writes
`measurements.json` through the same variable.

**This is [T-074](T-074-the-documented-render-command-does-not-exist.md)'s flag one layer down.**
That task made `--out` parse; this is the value it parses being used unresolved. The failure mode is
the one worth fixing rather than the size of the fix: **the run is green, the message names the file
rather than the cause, and the step it silently skips is the one that closes the visual gate.** An
author following [`build.md`](../skills/htmldeck/references/build.md) §3 verbatim gets `FAILED` twice
and no way to tell whether the deck or the tool is wrong.

**Scope**
- In: `--out` resolved once, in one place, for both `shots` and `measure`.
- In: `FAILED` never being printed for a path the tool chose. If the screenshot is missing after
  Chrome ran, say what was asked for and where.
- Out: `render.py`'s other arguments.

**Inputs**
- [`tools/deck/render.py`](../tools/deck/render.py) — `out_dir`, `cmd_shots`, `measure`, `main`.
- [T-074](T-074-the-documented-render-command-does-not-exist.md) — the same flag, the previous layer.

**Acceptance criteria**
- [ ] A relative `--out` writes the shots, and the printed directory is where they are
- [ ] An absolute `--out` is unchanged
- [ ] `measure --out <relative>` writes `measurements.json` to the same resolved place
- [ ] A missing shot reports what was asked for, not only that it failed
- [ ] A fixture for the relative case (**L-04**) — the defect is invisible to every absolute-path test

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Resolve `--out` once, where the default already resolves | `render.py` |
| 2 | Give the failure message the path it asked Chrome for | `render.py` |
| 3 | Fixture for the relative case; run both example decks | evidence |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → proposed | Created from [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md), found while rendering the decks to look at them. `v0.1` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — a defect in the published plugin, in a command [`build.md`](../skills/htmldeck/references/build.md) §3 tells an author to run. Nobody reported it, which is the precedent `v0.1.5` set rather than an argument against: a defect found by running the project's own instructions is still a defect an adopter can hit. |
