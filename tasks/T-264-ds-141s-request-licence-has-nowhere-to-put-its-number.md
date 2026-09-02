---
id: T-264
title: Give a licensed long motion somewhere to state its duration
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-264 — Give a licensed long motion somewhere to state its duration

## 1. Specify

**Outcome**
An author who is granted `DS-141`'s `request` licence can write the duration they asked for. Today three rules close every route: `DS-013` refuses a theme token the contract does not name, `DS-010` refuses the literal in the slides region, and the only declared dial near the value is Pulse-once's, which [T-198](T-198-give-affordance-motion-its-own-band-faster-than-content-motion.md) already recorded borrowing as a defect. **The licence exists and cannot be used** — the adopter shipped the third route and recorded the deviation.

**From the adopter report** [`005`](../docs/adopter-reports/claimai/005-a-deck-cannot-express-an-author-requested-duration.md).

**Scope**
- In: a per-deck motion band the theme contract names — one duration and one delay token reserved for `--motion-long` rules, unset by default. **This is the better of the two candidates**: it keeps the value where a generator can find it, which is the whole argument `DS-013` rests on
- In: **the asymmetry the record found second**: a custom property holding the same value is exempt from `DS-010` and a literal duration is not. The loophole is open for a delay and shut for a duration, and neither is a decision anyone took
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`005`](../docs/adopter-reports/claimai/005-a-deck-cannot-express-an-author-requested-duration.md) — each carries its evidence, its version and its own proposed fix
- [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md), which created `--motion-long` and its four reason values, `request` among them

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce all three closed routes as fixtures on this repository's own deck, before writing a fourth | The literal fails `DS-010` on the same declaration the record prints; the invented token fails `DS-013` with the same message. Both verdicts are the record's, to the word |
| 2 | Decide what *unset by default* has to mean, since `DS-013` requires every named token to be declared | A fourth kind, `optional`. Requiring it of both themes would put a dial in two themes nothing reads — `PR-77`'s defect — and adding it to the five tracked decks would rebuild them outside B12 |
| 3 | Add the band to the theme contract, and the kind that lets it be absent | §2's kind row; §3.6's three tokens; `theme.py`'s `KINDS`, `validate` and the `DS-013` row's two counts; `shell.py`'s `undeclared_tokens` |
| 4 | Measure the second finding before deciding it. How many custom-property declarations would `DS-010` newly scan, and how many would offend? | **18 scanned, 0 offending** across all five tracked decks. The hole was open and unused, which is what made closing it cheap |
| 5 | Close it: scan a custom property like any other declaration and let §5's table decide | The blanket skip removed from `theme.py`'s `literals()`; the `DS-010` row says so and carries the measurement |
| 6 | Prove the fourth route, in both directions | `band` passes `DS-013`, `DS-010` and `DS-141`; the same rule with no `--motion-long` fails `DS-141` |
| 7 | Put the band where an author meets it | `MOTION-GUIDE.md`'s motion checklist and the skill's `build.md`, both beside the `--motion-long` instruction that sends them there |

## 3. Implement

**Decisions & assumptions**
- **The band, not the exemption** — the owner's ruling, [`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3, and the record's own preference. It keeps the value where a generator can find it, which is the argument DS-013 rests on.
- **Three tokens, not two.** 2026-08-29. The record proposes a duration and a delay. §3.6's own sentence — *every named motion carries a duration and an easing* — makes the easing the third, and without it the record's actual request (1000 ms **with an ease-in-out curve**) is still unwritable: DS-010 polices curves outside the region as well as lengths.
- **A fourth kind, `optional`, rather than three more required tokens.** 2026-08-29. *Unset by default* is the record's phrase and DS-013 requires every named token to be declared, so one of the two had to give. Requiring them would put three dials in both shipped themes that nothing reads — the defect `PR-77` is already tracking in the colour band — and would make all five tracked decks fail DS-013 until they were rebuilt, which is B12's work and not this task's. The kind is narrow on purpose: **`optional` is for a value only a deck that does the thing can supply**, never for a token a theme could not be bothered with.
- **The asymmetry is closed by scanning custom properties, not by exempting durations.** 2026-08-29. DS-010's reason is *a value a theme cannot reach*, and that does not care which property holds it; the skip was justified by a comment saying the defect belonged to another rule, and no rule owned it. **Measured before committing to it**: 18 custom-property declarations newly scanned across the five tracked decks, **0** newly offending. §5's exemption table still decides, so composition scopes are unaffected — which is why the adopter's own `--no-delay:120ms` inside `#slides` stays legal, now for a stated reason rather than by an accident of the scanner.
- **No look is owed.** No deck changed; three checks and a contract did.

**Outputs produced**
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — §2's `optional` kind, §3.6's licensed long band
- [`tools/deck/theme.py`](../tools/deck/theme.py) — `KINDS`, `validate`, the `DS-013` row's counts, and `literals()`
- [`tools/deck/shell.py`](../tools/deck/shell.py) — `undeclared_tokens` no longer reports an optional token as missing
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-141` and `DS-010` rows
- [`docs/MOTION-GUIDE.md`](../docs/MOTION-GUIDE.md), [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) — where an author is told to declare the licence
- [`docs/adopter-reports/claimai/005-a-deck-cannot-express-an-author-requested-duration.md`](../docs/adopter-reports/claimai/005-a-deck-cannot-express-an-author-requested-duration.md) — closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Record [`005`](../docs/adopter-reports/claimai/005-a-deck-cannot-express-an-author-requested-duration.md) closed with its remedy measured | pass | Closed. Both findings taken; the first by the candidate the owner ruled for, with an easing token the record does not name and this contract's own sentence requires |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | Four fixtures on the reference deck. `literal` **FAILs DS-010** on the record's own declaration; `untoken` **FAILs DS-013** with the record's own message; `band` passes DS-013, DS-010 and DS-141; `unlicensed` — the same rule with no `--motion-long` — **FAILs DS-141**. The custom-property half measured at 18 scanned, 0 offending |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Both run at the end of B5, on a tree nothing was editing |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-29 | → done | Batch **B5**. The licensed long band exists and is `optional`, which needed a fourth token kind; the custom-property loophole is closed after measuring what closing it costs. All three routes the record says are shut were reproduced as fixtures first, so the fourth is proved against the same verdicts rather than against a description of them. |
