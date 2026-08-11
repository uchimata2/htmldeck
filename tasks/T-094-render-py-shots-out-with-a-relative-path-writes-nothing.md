---
id: T-094
title: render.py shots --out with a relative path writes nothing and says FAILED
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-019, T-074]
work_package: v0.1
owner: maintainer
business_value: high
effort: xs
created: 2026-08-11
updated: 2026-08-11
deliverables:
  - tools/deck/render.py
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
| 1 | `make_probe` resolves the directory through `out_dir` and **is the only thing that does**; `measure` and `cmd_shots` take theirs from the probe it returns | `render.py` |
| 2 | Give the failure message the path it asked Chrome for | `render.py` |
| 3 | Fixture for the relative case, over the real function and with no browser | `render.py` self-test |
| 4 | Both example decks rendered through a relative `--out` | evidence in §3 |

**Why step 1 is shaped that way.** Three call sites wrote `out = out or out_dir(deck)`, which reads
as resolution and is not: the `or` takes the override verbatim and only the *default* goes through
the function where `abspath` lives. Adding `abspath` at each site fixes the bug and leaves three
places to keep in step. Taking the directory from the probe's own path leaves one, and it is the one
a fixture can reach without launching a browser.

## 3. Implement

**Decisions & assumptions**

- **One resolution, in `make_probe`, and everything downstream takes its directory from the probe it
  returns** — 2026-08-11. `measure` and `cmd_shots` now read `os.path.dirname(probe)` instead of
  resolving a second time. Adding `abspath` at three call sites would have fixed the bug and left
  three places to keep in step; this leaves one, and it is the one a fixture can reach without
  launching a browser.
- **A directory at the destination is not a shot** — 2026-08-11, found while forcing a failure to
  read the new message. `os.path.exists` is true of a directory, so a destination that was a folder
  reported as a successful `0 KB` capture. The test is `isfile` and a non-zero size.

**Outputs produced**
- [`tools/deck/render.py`](../tools/deck/render.py) — `out_dir` resolves and says why, `make_probe`
  is the single resolution, `measure` and `cmd_shots` take theirs from it, the failure line names
  the path, and `self_test` has a relative-path fixture.

**Evidence**

```
python tools/deck/render.py shots examples/reference-deck.html 4,10 --out .assets-cache/deck/normal
  slide-05.png  151 KB
  slide-11.png  132 KB

C:\Work\AgentPlugins\htmldeck\.assets-cache\deck\normal
```

The same command printed `FAILED` twice before, and the directory it named was the relative string
it was given. `measure --out .assets-cache/deck/meas` writes `measurements.json` to the resolved
place; an absolute `--out` is byte-for-byte what it was.

**The fixture fails against the shape it replaced**, which is the only thing that makes it evidence
(**L-04**). Running the old `out = out or out_dir(deck)` beside the new one on the same relative
argument:

```
  fixed  make_probe -> C:\...\htmldeck-t094-rwate2w6\out\shots\probe.html   absolute: True
  old    make_probe -> out\shots\old.html                                   absolute: False
```

And the failure line, forced by putting a directory where the image goes:

```
  slide-01.png  FAILED - no image at C:\Work\AgentPlugins\htmldeck\.assets-cache\deck\failmsg\slide-01.png
```

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A relative `--out` writes the shots, and the printed directory is where they are | met | Two shots at 151 KB and 132 KB, and the trailing line prints the resolved directory rather than the argument. One of them was opened and looked at. |
| An absolute `--out` is unchanged | met | `abspath` of an absolute path is itself; a shot written through one is 101 KB as before, and every internal caller already passed absolute paths. |
| `measure --out <relative>` writes `measurements.json` to the same resolved place | met | Present at the resolved path; the three resolutions per run collapsed to the one in `make_probe`. |
| A missing shot reports what was asked for, not only that it failed | met | And the test tightened from `exists` to `isfile` plus a size, because a directory at the destination had been reporting as a successful `0 KB` capture. |
| A fixture for the relative case (**L-04**) | met | Over `make_probe` itself, with no browser, and shown failing against the old shape. Every path this tool had ever been tested with was absolute, which is why a defect in the one branch that is not survived a whole task about the same flag. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (shipped) | **Shipped in `0.2.1`.** **One of the three fixes this release is for**, and the only one nobody reported. |
| 2026-08-11 | → done | **Fixed by removing two of the three resolutions rather than correcting all three.** `make_probe` is the only place `--out` becomes a directory now, and `measure` and `cmd_shots` read theirs back off the probe — which is also what makes the fixture possible without a browser, and it is shown failing against the shape it replaced. One thing was found while forcing a failure to read the new message: `os.path.exists` is true of a directory, so a folder at the destination had been reporting as a successful `0 KB` capture; the test is `isfile` plus a size. Both example decks gate green and the four render-backed suites pass. Owed to the release: this is a `v0.1` patch and `v0.1.6` is still uncut, so it joins T-090 and T-091 there. |
| 2026-08-11 | → planned | Three steps and a shape. The three call sites all wrote `out = out or out_dir(deck)`, which reads as resolution and is not — the `or` takes the override verbatim, so only the default ever reached `abspath`. Resolving at each site would fix the bug and leave three places to keep in step. |
| 2026-08-11 | → proposed | Created from [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md), found while rendering the decks to look at them. `v0.1` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — a defect in the published plugin, in a command [`build.md`](../skills/htmldeck/references/build.md) §3 tells an author to run. Nobody reported it, which is the precedent `v0.1.5` set rather than an argument against: a defect found by running the project's own instructions is still a defect an adopter can hit. |
