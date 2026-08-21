---
id: T-209
title: Six more probes measure a page whose entrance animation never ran, and none of them says so
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-185, T-206]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-21
updated: 2026-08-21
shipped_in: unreleased
deliverables: [tools/deck/render.py, tools/deck/audit.py]
---

# T-209 — Six more probes measure a page whose entrance animation never ran, and none of them says so

## 1. Specify

**Outcome**
Every probe that measures geometry either measures a settled page, or states in its own text why an
unsettled one is the right subject for it. Today six of them do neither, by omission rather than by
a decision anyone took.

**How it was found**
Closing [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md) on 2026-08-21. That
task fixed `render.PROBE`, which is the probe `measure` and `shots` share. Every other consumer
builds its own and passes it through `make_probe(..., extra=…)`, so the fix reaches none of them:

| Probe | Built in | Pins motion |
| :--- | :--- | :--- |
| `PROBE` | [`tools/deck/audit.py`](../tools/deck/audit.py) `:1832` | no |
| `REDUCED_PROBE` | [`tools/deck/audit.py`](../tools/deck/audit.py) `:1889` | no |
| `PROBE` | [`tools/deck/chrome_row.py`](../tools/deck/chrome_row.py) `:256` | no |
| probe source | [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py) `:370` | no |
| `PROBE` | [`tools/deck/figgrid.py`](../tools/deck/figgrid.py) `:95` | no |
| `SHEET_PROBE` | [`tools/deck/printgeom.py`](../tools/deck/printgeom.py) `:263`, [`tools/deck/printpages.py`](../tools/deck/printpages.py) `:101` | no |

**The subject is present, which is what makes this worth a task.** In the portfolio-review deck the
figure wrapper and the headline both carry the entrance class — `class="body figwrap rise"` — and
`figgrid` measures `.body svg.fig` and `.headline` by name. T-206 measured the offset that class
produces at exactly **18.00 du**, the full `--rise-dist`, on a page read at frame zero.

**What is NOT established, and must not be assumed.** Whether each probe's particular comparison
actually reads an axis the entrance moves. `.rise` is `translateY`, so a check that compares `left`
offsets is untouched by it while one comparing `top` or `height` is not — and `figgrid`'s visible
comparison is a left offset, which may well be immune. **Six probes lacking the pin is six subjects
to measure, not six defects.** Filing it as six defects would be the same error T-206 corrected in
its own §1: writing down the lead as the finding.

**Why it is not folded into T-206.** That task's scope is *"making DS-063's verdict a function of
the deck's bytes"* and explicitly nothing wider. A fix that swept six more probes on the same day
would have made its ten-run evidence a statement about a much larger change than the one it argued
for.

**Scope**
- In: determining, per probe, whether any quantity it compares is moved by an entrance animation.
- In: pinning motion in the probes where it is, and recording the reason in the ones where it is
  not.
- Out: `MOTION_PROBE`. Measuring motion is its declared subject and it has its own name for exactly
  this reason (T-185).
- Out: re-opening DS-063 or any tolerance. T-206 settled that row.

**Inputs**
- [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md) §3 — the measurement, the
  18.00 du offset, and the argument for an unconditional pin over a per-caller flag.
- [`docs/lessons/L-128.md`](../docs/lessons/L-128.md) — why two readings agreeing said nothing, and
  the general rule about a guarantee a caller can decline.
- **L-26** and [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) — a CSS animation's
  clock under `--virtual-time-budget` is frame production, not time.

**Acceptance criteria**
- [ ] For each of the six, a stated verdict: *pinned*, or *unpinned with the reason it is correct
      here*. No probe is left unexamined.
- [ ] Where a probe is pinned, its rule's verdict is shown before and after, so a changed number is
      visible rather than absorbed.
- [ ] The seeded-variant suites covering these rules still behave as specified.
- [ ] A guard, in the shape T-206 used: browser-free, structural, and failing if a pin is removed.

**Open questions**
- ~~Whether the print probes are already settled by the print stylesheet.~~ **Answered in §2, and
  the guess was right about the stylesheet and wrong about why it does not matter.** The print block
  does settle `.rise` ([`shell/components.css`](../shell/components.css) `:1091`) — but
  `SHEET_PROBE` never renders under print media, and it reads **counts** rather than geometry, which
  is a stronger reason and a different one.
- ~~Whether the pin belongs in `make_probe` rather than copied into six probe sources.~~
  **Decided in §2: in `make_probe`, and structurally rather than by a flag.**
## 2. Plan

**The fault is one expression, and the census in §1 is short.** `make_probe` composes the page as
`(PROBE if not extra else extra)` — [`tools/deck/render.py`](../tools/deck/render.py) `:239`. `extra`
**replaces** the shared probe rather than joining it, so every caller passing one loses the pin
T-206 installed at `render.py` `:149`. The count is therefore a property of *who passes `extra`*, and
asking `make_probe`'s callers directly rather than listing probes finds **eight** unpinned sources
where §1 listed six:

| # | Probe source | Built in | Pins motion | In §1's table |
| :-- | :--- | :--- | :---: | :---: |
| 1 | `PROBE` | [`audit.py`](../tools/deck/audit.py) `:1196` | no | yes |
| 2 | `REDUCED_PROBE` | [`audit.py`](../tools/deck/audit.py) `:1846` | no | yes |
| 3 | `PROBE` | [`chrome_row.py`](../tools/deck/chrome_row.py) `:49` | no | yes |
| 4 | probe source | [`contents_bound.py`](../tools/deck/contents_bound.py) `:128` | no | yes |
| 5 | `PROBE` | [`figgrid.py`](../tools/deck/figgrid.py) `:52` | no | yes |
| 6 | `SHEET_PROBE` | [`printgeom.py`](../tools/deck/printgeom.py) `:237` | no | yes |
| 7 | `SHEET_PROBE` | [`printpages.py`](../tools/deck/printpages.py) `:81` | no | counted with 6 |
| 8 | `PROBE` | [`contract.py`](../tools/deck/contract.py) `:82` | no | **no** |

*§1 listed the two `SHEET_PROBE`s as one row because they share a name; they are two definitions in
two files and each needs its own verdict. **`contract.py` was missed outright** — it was found by
asking who calls `make_probe` instead of who defines a probe, which is the census the fault's shape
actually implies.* Two further sources already pin and are **not** subjects:
[`rulerstrip.py`](../tools/deck/rulerstrip.py) `:130` and [`markhits.py`](../tools/deck/markhits.py)
`:94`, the second born pinned under T-204. [`static_variants.py`](../tools/deck/static_variants.py)
`:337` passes `audit.PROBE` and inherits row 1's verdict rather than being a ninth subject.

**Two rows are already answerable without a browser, and both are *unpinned, and correct*.**

- **Rows 6 and 7 — `SHEET_PROBE` reads no geometry.** It reports
  `querySelectorAll('.cbox').length` and `.contents-foot`.length. A count is immune to `translateY`
  and to `scale`: a moved element is still in the DOM and still counted. The print stylesheet is a
  red herring here — the probe is read at 1280×800 through `render.read_result`, which is screen
  media, so the print block never applies to it at all.
- **Row 2 — `REDUCED_PROBE` is settled by the deck, not by the probe.** It runs Chrome with
  `--force-prefers-reduced-motion` ([`audit.py`](../tools/deck/audit.py) `:1892`) and the deck's own
  rule at [`shell/components.css`](../shell/components.css) `:744` sets
  `.rise,.pulse,.opening{animation:none;opacity:1;transform:none}`. **The emulation is asserted
  rather than assumed** — `:1878` reads `matchMedia` back and `:1904` fails the run when it does not
  match — which is what makes this a reason instead of a hope. **Its bound must be written down:**
  the reason holds exactly as far as that block's selector list, so an animation added outside it
  settles nothing here. DS-143 is the rule that keeps the list complete.

**Which axis each remaining probe reads is the measurement, and §1's caution stands.** `.rise` is
`translateY(var(--rise-dist))` (`components.css` `:607`, `:713`), so a comparison of `left` offsets
is untouched by it and one of `top` or `height` is not — `figgrid`'s visible comparison is a left
offset and may well be immune. `.pulse` is `scale`, and with `1` iteration and `both` fill it holds
`scale(1)` at frame zero, so it moves nothing there. `.opening` is
`translateY(calc(-1 * var(--open-rise))) scaleY(var(--open-squash))` (`:286`) and **is not reset by
the print block**, which resets only `.rise` — relevant to anything measured in print, and to
nothing here.

**The pin goes into `make_probe`, and structurally.** T-206's argument was an unconditional pin over
a per-caller flag; applied one level up it says `make_probe` composes the pin **ahead of** `extra`
rather than instead of it. The exception is `MOTION_PROBE`, identified by **being** that constant
rather than by a boolean the caller passes — **L-128**'s rule is that a guarantee a caller can
decline is not a guarantee, and a `pin=False` parameter is exactly that. The pin's text is the two
declarations already duplicated in three places (`render.py` `:149`, `rulerstrip.py` `:130`,
`markhits.py` `:94`); it becomes one named constant and those three stop being copies.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Extract the pin from `render.PROBE` into a named constant, and have `make_probe` inject it ahead of `extra` for every caller except `MOTION_PROBE`, identified by identity | `render.py` — one pin, one exception, no flag |
| 2 | Record the **before** verdict of every rule owned by rows 1, 3, 4, 5 and 8, on the portfolio-review deck, before step 1's change is made | a verdict table's first column |
| 3 | Apply step 1 and record the **after** verdict of the same rules | the same table, second column |
| 4 | For each of the eight, write the verdict: *pinned*, or *unpinned with the reason* — rows 2, 6 and 7 are drafted above and need only their bounds stated | §3's decisions |
| 5 | Re-run the seeded-variant suites covering these rules | pass, or a named difference |
| 6 | Add the guard in T-206's shape: browser-free and structural, failing if `make_probe` stops pinning or if a probe source reintroduces its own copy | a self-test row |
| 7 | Run `python tools/tasks/lint.py`, then `python tools/check_all.py` — never together | both green |

**Risk, stated before the work.** Step 1 changes a shared function every browser-reading tool
depends on. Step 2 exists because of that: a rule whose verdict moves is the point of the task, and
a rule whose verdict moves *unexpectedly* is a defect the before/after table is the only thing
positioned to catch.

## 3. Implement

**Decisions & assumptions**
- **The pin went into `make_probe` and the exception stopped being `MOTION_PROBE`.** §2 assumed one
  exempt probe, identified by identity. That was wrong, and the seeded-variant suite is what said
  so: pinned unconditionally, it fell from **8 of 8 and 2 of 2** rendered variants caught to **7 of 8
  and 1 of 2**. A deck hiding its stop control inside a shut menu passed **DS-218**, and a deck
  leaving a slide blank under reduced motion passed **DS-143**. — 2026-08-21
- **The cause is that the pin erases the property those rules read.** `audit.PROBE` decides DS-140,
  DS-142 and DS-218 from `getComputedStyle(el).animationIterationCount === 'infinite'`, and
  `animation:none!important` makes it never infinite. **The rules did not fail, they lost their
  subject** — the eighth time this repository has met that defect class (**L-57**). `REDUCED_PROBE`
  is the same shape one axis along: its subject is what the *deck* does under
  `prefers-reduced-motion`, so pinning from outside makes every deck compliant. — 2026-08-21
- **So the exception is a declaration the probe carries, not a flag the caller passes.**
  `MEASURES_MOTION` is a marker in the probe's own source; `make_probe` reads it back. This keeps
  **L-128** — nobody can decline the pin from the call site — while letting a probe state that
  motion is its subject. It is the idiom DS-217's `data-scale` and DS-230's `data-disc` already use:
  the artifact makes the claim, the tool verifies rather than infers. — 2026-08-21
- **Three probes declare it and only one was obvious.** `MOTION_PROBE` announces itself in its name
  (T-185); `audit.PROBE` and `audit.REDUCED_PROBE` did not, and each declaration records the rule
  that forced it and the seeded variant that proved it. — 2026-08-21
- **`rulerstrip.py` and `markhits.py` stopped carrying their own copies.** Both had the pin inline —
  `markhits` deliberately, born pinned under T-204. There is one pin now and the self-test refuses a
  second, read off the package directory rather than a list beside it (**L-57**). — 2026-08-21

**Outputs produced**
- [`tools/deck/render.py`](../tools/deck/render.py) — `MOTION_PIN`, `MEASURES_MOTION`, the
  composition in `make_probe`, and the guard.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — two declarations, each carrying its reason.
- [`tools/deck/rulerstrip.py`](../tools/deck/rulerstrip.py),
  [`tools/deck/markhits.py`](../tools/deck/markhits.py) — copies removed.

**The eight, each with its verdict**

| # | Probe source | Verdict | Evidence |
| :-- | :--- | :--- | :--- |
| 1 | `audit.PROBE` | **unpinned, with the reason** | It reads `animationIterationCount` for DS-140, DS-142 and DS-218. Pinned, the DS-218 seeded variant goes CAUGHT → MISSED. Its geometry rows were measured both ways on the portfolio deck and are **identical**, so pinning buys nothing here and costs three rules. |
| 2 | `audit.REDUCED_PROBE` | **unpinned, with the reason** | Its subject is the deck's own `prefers-reduced-motion` behaviour. Pinned, the DS-143 seeded variant goes CAUGHT → MISSED. It is also already settled *by the deck*: [`shell/components.css`](../shell/components.css) `:744` sets `.rise,.pulse,.opening{animation:none}` and the emulation is asserted rather than assumed — `audit.py` `:1878` reads `matchMedia` back and `:1904` fails the run when it does not match. |
| 3 | `chrome_row.PROBE` | **pinned** | Verdicts identical before and after: 0 changed lines. |
| 4 | `contents_bound` probe source | **pinned** | Verdicts identical before and after: 0 changed lines. |
| 5 | `figgrid.PROBE` | **pinned** | Verdicts identical before and after: 0 changed lines. §1 guessed its visible comparison is a left offset and so immune to a `translateY`; the measurement agrees. |
| 6 | `printgeom.SHEET_PROBE` | **pinned, and it was already immune** | It reports `querySelectorAll('.cbox').length` — a **count**, which no transform moves. The print-stylesheet hypothesis in §1 was true and irrelevant: this probe is read at 1280×800 through `render.read_result`, which is screen media. |
| 7 | `printpages.SHEET_PROBE` | **pinned, and it was already immune** | The same probe shape in a second file. Both tools green. |
| 8 | `contract.PROBE` | **pinned** | The source §1 missed entirely. DS-063 reads **0.00 du** before and after — the value did not move, and it is now a fact about the deck rather than about two equally-unsettled reads agreeing (**L-128**). |

**Not subjects:** [`rulerstrip.py`](../tools/deck/rulerstrip.py) and
[`markhits.py`](../tools/deck/markhits.py) already pinned and now inherit;
[`static_variants.py`](../tools/deck/static_variants.py) passes `audit.PROBE` and takes row 1's
verdict.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| For each of the six, a stated verdict: *pinned*, or *unpinned with the reason it is correct here*. No probe left unexamined | **met**, and for **eight** | §1's census was short. Asking who calls `make_probe` rather than who defines a probe found `contract.py`, missed outright, and split the two `SHEET_PROBE`s counted as one. Six pinned, two unpinned with the reason. |
| Where a probe is pinned, its rule's verdict is shown before and after | **met** | Five tools run on the portfolio deck before the change and again after: `audit`, `contract`, `figgrid`, `chrome_row`, `contents_bound`. **0 changed lines in all five**, all exit 0. §1's caution was right — eight probes lacking the pin was eight subjects to measure, and none of them was a defect. |
| The seeded-variant suites covering these rules still behave as specified | **met**, and this is the criterion that earned its place | **27 of 27 static, 8 of 8 rendered, 2 of 2 reduced-motion.** The first attempt scored 7 of 8 and 1 of 2, which is how the unconditional pin was caught erasing DS-218's and DS-143's subject. Baseline taken by reverting the three files to `HEAD` and re-running, so the regression was measured rather than inferred. |
| A guard, in T-206's shape: browser-free, structural, failing if a pin is removed | **met** | T-206's guard asserted `"data-motion" in PROBE` — true of one probe and blind to the eight that replace it. The assertion is now on **what `make_probe` writes**: three fixture probes, one plain, one with a foreign `extra`, one declaring `MEASURES_MOTION`. Plus a directory scan refusing a second copy of the pin anywhere in the package. **All three seeded and proved red**: the injection removed, the declaration removed, and a copy reintroduced in `markhits.py`. Restored and verified byte-identical. |
| *(closing checklist step 3)* | **n/a** | This task produced no rendered artifact. It changed how probes are built; the decks they read are unchanged and their verdicts are identical. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised by [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md), which fixed the same fault in `render.PROBE` and found the other six by asking what else builds a probe. The subject is present — the deck's figures and headlines carry `.rise`, worth 18.00 du at frame zero — but whether each probe reads an axis that class moves is unmeasured, so this is six subjects rather than six defects. `PH3`: no adopter is affected, the exposure is this repository's confidence in its own instruments. |
| 2026-08-21 | proposed → planned | §2 written. **Both open questions settled, and the census corrected from six to eight.** The fault is `make_probe` composing `(PROBE if not extra else extra)`, so asking who passes `extra` — rather than who defines a probe — found `contract.py` `:82`, missed outright, and split the two `SHEET_PROBE`s that §1 counted as one. Two rows are answerable without a browser and both are *unpinned, and correct*: `SHEET_PROBE` reads counts rather than geometry, and `REDUCED_PROBE` is settled by the deck under `--force-prefers-reduced-motion`, with the emulation asserted rather than assumed. The print-stylesheet hypothesis was true and irrelevant — that probe never renders under print media. The pin goes into `make_probe` with `MOTION_PROBE` excepted by identity rather than by a flag, on **L-128**. |
| 2026-08-21 | planned → done | The pin is `make_probe`'s and the exception is a declaration the probe carries. **§2's design was wrong and the seeded-variant suite is what said so**: pinned unconditionally it fell from 8/8 and 2/2 rendered variants caught to 7/8 and 1/2, because `animation:none` erases the `animationIterationCount` that DS-140, DS-142 and DS-218 read, and because `REDUCED_PROBE`'s subject is what the deck does under reduced motion. **The rules did not fail, they lost their subject** — the eighth time this repository has met that class (**L-57**). With `MEASURES_MOTION` declared by the three probes that measure motion, the suite is back to 27/27, 8/8 and 2/2. **Six pinned, two unpinned with the reason, and not one verdict moved**: five tools run before and after, 0 changed lines each. §1's caution held exactly — eight subjects, no defects. |
