---
id: T-017
title: Define the portability contract — what "opens anywhere and works" actually permits
type: research
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-002, T-005, T-013, T-016]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/research/R6-portability-contract.md]
---

# T-017 — Define the portability contract — what "opens anywhere and works" actually permits

## 1. Specify

**Outcome**
A tested statement of exactly which web platform features a single self-contained HTML file can use
when it is **double-clicked** rather than served — and therefore which interaction, animation and
3D techniques the build mode is allowed to emit.

**Why this one**
Portability is now the binding constraint, and it is not the same thing as restraint. The hazard is
specific: **`file://` is a restricted origin.** ES modules, `fetch`, XHR, some worker
registrations and several WebGL and `<canvas>` texture paths fail on a double-clicked file while
working perfectly over HTTP — which means they also work perfectly in every local preview, and the
breakage only appears on the recipient's machine. "Rich JavaScript" and "no installation" collide
exactly here. Every other task in WP3 builds on the answer, so it belongs in research, before them.

**Scope**
- In: an empirically tested feature matrix for `file://` — module scripts vs classic scripts,
  inline vs external, `fetch` and XHR, data and blob URIs, workers, WebGL context creation and
  texture sources, Web Audio, fullscreen, clipboard, `localStorage`, CSS 3D and filters,
  `<canvas>` tainting rules.
- In: naming the **target browser** and version floor, and what "no glitch" means as a testable
  statement.
- In: how far mobile degrades, given it is explicitly secondary — degrade gracefully or not care.
- In: the vendoring question — inlining a 3D or animation library into the file, and the size cost
  measured rather than guessed. Feeds T-013.
- In: the optional printable mode — what it costs to support, given it is no longer a gate.
- Out: choosing the libraries. This says what is *possible*; T-013 and T-016 choose.

**Method**
Test, do not read. Documentation and memory both describe the HTTP behaviour of these features;
the `file://` behaviour differs per browser and changes between versions. Build a probe deck, open
it by double-click on a clean profile, and record what actually happens.

**Acceptance criteria**
- [ ] Feature matrix produced from **actual double-click testing**, not documentation, with browser
      and version recorded against every row
- [ ] Target browser and version floor named, with the reason
- [ ] "Glitch-free" defined as something a check can test — see T-005
- [ ] Every failure mode paired with the workaround that keeps the feature usable, or an explicit
      "do not use"
- [ ] Verified with the network disabled, on a profile with no extensions
- [ ] Mobile degradation position stated, not left implicit
- [ ] The probe deck kept as the self-test, per the brief's "verify the checker on a known case"

**Decided 2026-08-06 — recent Chrome/Edge.** One engine, and the one to test against. Firefox and
Safari degrade gracefully but do not set the bar, and mobile is secondary. Probe the others only
far enough to know what breaks, not to support them.

**Open questions**
- Is a single-file deck still the requirement if it costs a large inlined 3D library, or is a
  folder-plus-file acceptable for the heaviest decks? — owner
- What is the version floor? "Recent" needs a number before a check can test it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Build the probe deck covering every feature in scope | probe file |
| 2 | Double-click test across candidate browsers, network off | raw results |
| 3 | Record workarounds and dead ends | feature matrix |
| 4 | Measure the cost of inlining a 3D/animation library | size measurements |
| 5 | Write the contract | `docs/research/R6-portability-contract.md` |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created after the owner replaced the minimal-JavaScript constraint with a portability constraint, making the `file://` envelope the thing WP3 depends on. |
