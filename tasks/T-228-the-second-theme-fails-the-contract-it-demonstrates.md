---
id: T-228
title: Bring lattice.css up to the theme contract, and put a theme in a gate's subject
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables: []
---

# T-228 — Bring lattice.css up to the theme contract, and put a theme in a gate's subject

## 1. Specify

**Outcome**
`python tools/deck/theme.py validate themes/lattice.css` exits 0, and a tracked theme is inside some check's subject. Today it exits 1 with **fifteen tokens not declared** - the whole affordance and press band, most of the inter-slide transition, `--motion-density`, both pager tokens and the three pop tokens - every one of which arrived after the file did, because `check_all.py` runs `theme.py check <deck>` and never `theme.py validate <theme>`.

**Closes** `PR-37` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the fifteen declarations in `themes/lattice.css`
- In: **the missing step**, which the register calls the larger half: `check_all.py` already discovers every checker and every deck, and discovering every *theme* is what would have caught this the day DS-240 landed
- Out: what the tokens' values should be for a second look - that is a design question and this is a conformance one
- Out: `themes/quarto.css`, which passes

**Inputs**
- `PR-37` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) section 5

**Acceptance criteria**
- [ ] `theme.py validate` exits 0 on every tracked theme
- [ ] a theme that drops a required token **fails a gate**, proved by seeding one rather than asserted
- [ ] `python tools/check_all.py` green with the new step classified

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

**The register calls the declarations the smaller half and it is right.** Fifteen tokens is an
afternoon; a gate that never looked at a theme is why there were fifteen. So the second step is the
one that has to be built properly, and *properly* here means **discovered**: a hand-kept list of
themes goes stale at the same moment a hand-kept anything does, which is when someone adds the
thing it was supposed to cover.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce, and read what each of the fifteen governs before writing a value | the failure as stated, and the split between tempo, shape and identifier |
| 2 | Declare the fifteen in `themes/lattice.css`, in its own section order | `theme.py validate` exits 0 on both themes |
| 3 | `check_all.py` — a `PER_THEME` table and a **discovered** theme list, run before the per-deck gates | a theme that is added is gated the day it lands |
| 4 | Assert the discovery's one distinction in the self-test: it reaches the themes, and not `themes/faces/` | a glob somebody checks |
| 5 | Seed a theme missing a required token and prove the gate fails on it, then leave the seed behind as a fixture rather than as a paragraph | criterion 2, proved rather than asserted |
| 6 | Close `PR-37`; both gates, run separately | register and task agreeing, green |

## 3. Implement

**Decisions & assumptions**

- **The four timing tokens are scaled to lattice's tempo; the other eleven are copied** —
  2026-08-29. §1 puts the *values* out of scope as a design question, and that settles whether they
  are **good**, not whether they may be arbitrary. lattice's own header names motion as one of four
  axes it moves — *200 ms rise, 35 ms stagger against quarto's 340 and 60* — so copying quarto's
  clock would have written a contradiction into the file whose whole job is to show a theme swap
  changing the design. The ratio is its own: **0.59**, applied and rounded the way the file already
  rounds. `--afford-dur` 200→**120ms**, `--press-dur` 100→**60ms**, `--arrow-pop-delay`
  120→**70ms**, `--dot-stagger` 8→**5ms** (thirty dots at 5 ms stay inside DS-141's cap). The rest
  are not tempo: `--slide-leave-fwd`/`-back` are **keyframe identifiers** `components.css` defines
  and a theme inventing its own would name nothing; `--slide-leave-shadow` is composed from this
  theme's own shadow dials, so lattice's flat shadow follows without restating a number;
  `--motion-density` is **100**, DS-238's shipped default and not a theme's question to reopen; and
  the shape values — `--slide-scale`, `--slide-shift`, `--pager-pinch`, `--pager-tilt`,
  `--dot-overshoot` — are feel rather than clock, so they are quarto's. A second look may move any
  of them; none of them is a claim this task is making.
- **`tracked()` takes a git pathspec, not a shell glob** — 2026-08-29, and it cost a step. Under
  git, `themes/*.css` matches **across** directories, so the discovery returned the three font
  faces in `themes/faces/`, which have no contract to validate against and would have failed on
  every token. The filter is explicit and the distinction is depth: **a theme is a `.css` directly
  in `themes/`, and anything deeper is a resource a theme uses.**
- **The self-test asserts the glob in both directions, and that is what caught the above** —
  2026-08-29. It was written before the run, on the principle that a glob nobody checks is a list
  nobody wrote, and it named the real cause immediately rather than surfacing three steps later as
  a font face failing fifteen tokens.
- **`theme.py` had no fixture for a *missing* token, which is the branch this defect lived in** —
  2026-08-29, and it is the finding worth more than the fifteen declarations. Both existing
  negative fixtures seed a **value** the validator can read and object to — a line height outside
  DS-034's band, a derived token rewritten as a literal. Nothing seeded an **absence**, so
  `not declared` was a verdict only ever produced by a real theme being wrong, never by a test.
  It is also the branch that decays on its own: **a token added to the contract is undeclared
  everywhere by construction**, which is exactly how fifteen accumulated. `drop_token` is the
  sibling of `set_token` and refuses a no-op for the same reason, with the worse trap named —
  *removing nothing* looks exactly like *removing something the validator did not mind*.
- **Proved by seeding, not asserted** — 2026-08-29. `themes/lattice.css` with `--afford-dur`
  removed, run through the gate's own command: **exit 1, `1 problem(s)`, `--afford-dur not
  declared`**. The durable half is the self-test fixture, which `main()` runs before every command,
  so `check_all.py` carries it on every future run.

**Outputs produced**
- [`themes/lattice.css`](../themes/lattice.css) — the fifteen declarations, in three sections with
  the reason each value was scaled or copied
- [`tools/check_all.py`](../tools/check_all.py) — `PER_THEME`, `themes_tracked()`, the themes run
  before the decks, and the self-test asserting the discovery both ways
- [`tools/deck/theme.py`](../tools/deck/theme.py) — `drop_token`, and the missing-token fixture
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-37` closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `theme.py validate` exits 0 on every tracked theme | pass | `themes/lattice.css - conforms`, `themes/quarto.css - conforms`. Both are now run by `check_all.py` rather than by hand, which is what makes *every tracked theme* a claim the gate re-derives |
| A theme that drops a required token **fails a gate**, proved by seeding one rather than asserted | pass | Seeded `lattice` without `--afford-dur`, run through the gate's own command: **exit 1**, `1 problem(s)`, `--afford-dur not declared`. The durable half is `theme.py`'s new `drop_token` fixture, which `main()` runs before every command — so the branch is watched on every future run, not only in this one |
| `python tools/check_all.py` green with the new step classified | pass | `theme.py` was already in `PER_DECK`, so the tool partition is unchanged at 0 unclassified and 0 stale; the two theme commands join the command partition. Outcome in the log row below |

**Child fix tasks raised**
- none

**Nothing rendered here, so no look is owed** — the fifteen declarations are all affordance, press,
transition and figure-motion dials on a theme **no tracked deck is built against**; the four decks
carry `quarto`, which was already conforming and is untouched. `lattice` is a demonstration that a
swap works, and the question of whether its motion *reads* at 0.59 of quarto's clock is a second
look this task's §1 puts out of scope — it would need a deck built against it first.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Both halves, and the register's hypothesis held: the declarations were the smaller half. **The four timing tokens were scaled to this theme's stated tempo rather than copied** - lattice names motion as one of the four axes it moves, so quarto's clock would have contradicted the file's own header - and the other eleven are shape, keyframe identifiers or DS-238's default. The gate **discovers** themes rather than listing them. Two findings the register did not name: `tracked()` takes a git pathspec, so `themes/*.css` reached the three font faces, caught by the self-test written before the run; and **`theme.py` had no negative fixture for a *missing* token at all**, which is the branch this defect lived in and the one that decays by itself, since a token added to the contract is undeclared everywhere by construction. Seeded proof: exit 1, `--afford-dur not declared`. Both gates green, run separately. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
