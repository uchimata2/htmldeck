---
id: T-299
title: Triage the third adopter's report and decide each of its eighteen findings
type: analysis
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
shipped_in: 1.0.0
owner: the project owner
business_value: high
effort: m
created: 2026-09-08
updated: 2026-09-13
deliverables:
  - tasks/T-303-close-a-slidefacts-element-at-its-own-tag-find-every-control-and-make-readabilitys-ledger-add-up.md
  - tasks/T-304-bring-a-deck-authored-motion-inside-the-shells-motion-gate-the-motion-control-and-densitys-ranking.md
  - tasks/T-305-let-render-py-see-an-svg-paint-change-a-scripted-hover-and-a-figure-painting-over-its-neighbour.md
  - tasks/T-306-wire-an-icon-first-source-item-in-quickview-py-and-make-shell-py-sync-name-a-stale-chrome-tail.md
  - tasks/T-307-give-the-chrome-first-and-last-page-controls-and-a-ruler-whose-marks-a-reader-can-aim-at.md
  - tasks/T-308-decide-how-a-deck-records-a-deviation-its-owner-licensed-and-what-the-gate-reports-for-it.md
  - tasks/T-309-contract-an-inline-term-that-opens-a-definition-bubble.md
  - tasks/T-310-stop-the-shells-keydown-handler-throwing-on-a-document-target-and-taking-space-from-a-focused-control.md
---

# T-299 — Triage the third adopter's report and decide each of its eighteen findings

## 1. Specify

**Outcome**
Every finding in the adopter reports T-320 removed has a
decision against it — accepted and raised as a fix, accepted and deferred, or rejected with a
reason. Nothing in the set is left unjudged. This task produces the judgement; the fixes it accepts
become tasks of their own.

**Where it came from**

A second outside project used htmldeck to build its presentation: a thirty-three page argument deck
for a training capstone, built between 2026-09-01 and 2026-09-08 against a date that did not move,
and delivered. Seventeen findings were measured on `0.7.0` and one on `0.6.0`. Each was written the
day it was met, with the command that proves it, and the batch was held back so the project's own
deadline paid nothing for a context switch into this repository.

**The adopting project's repository is private, and the records were written to stand without it.**
Every piece of evidence is quoted inside the record. Paths such as `deck/the third adopter.html` and
`tools/deck.ps1` are that project's own and resolve nowhere here; nothing links out.

**What is different from [T-225](T-225-triage-the-second-adopters-report.md)**

- **Four records are `request` rather than `defect`** — places where the design system has no
  vocabulary for a decision the deck's owner made, not places where a rule misfires. `17` is the
  general case: three owner-ruled deviations leave the gate red on every run, so the adopter wrote a
  forty-line wrapper to hold the ruling. the second adopter's `011`, `023` and `024` each asked for one escape
  hatch; this one asks for the mechanism.
- **One defect arrives with its downstream consumer attached.** `13` truncates a slide's body at the
  first matching close tag; `14` is `readability.py` inheriting it through `slidefacts.facts` and
  reporting aggregates over two thirds of the copy, with a ledger that promises nothing goes missing
  quietly. Deciding `13` decides most of `14`.
- **Five records say no instrument can see an interaction** — `06`, `08`, `09`, `10`, and `12` from
  the other side. `016` and `017` of the second adopter set are the same complaint one release earlier, so
  the triage has a before and an after to compare.

**In scope.** Each of the eighteen: a verdict, and where accepted, a task. Re-deriving each one's
phase and type by this repository's rules rather than by what the filer called it — CLAUDE.md is
explicit that classification is this project's to make, and the report's `severity` is what it cost
the author who hit it.

**Out of scope.** Fixing anything here. Any change to the report's own files: an evidence record is
not edited after it arrives, and a verdict that disagrees with one says so in this task.

**Acceptance.** Eighteen verdicts, each with a reason. Every accepted finding names the task that
carries it. Every rejected one names why, in a sentence somebody who did not sit in this triage can
weigh.

## 2. Plan

1. Read the adopter reports T-320 removed whole —
   the covering note carries four themes and they cut across the individual records.
2. For each of the eighteen, in the index's order: reproduce or accept the record's own command,
   then rule.
3. Cross-check against the second adopter set before ruling on `11`, `16`, `17` and `18` — `011`, `023`,
   `024` and `025` touch the same rules, and `023` was already answered by narrowing `DS-100`, which
   is why `17` is not a re-run of it.
4. Cross-check `01` against what shipped in `0.7.0`: it is the one record measured on `0.6.0`.
5. Raise a task per accepted finding, phase and type re-derived here, and record in section 3 where
   each verdict differs from what arrived and why.

## 3. Implement

**Decisions & assumptions**

- **Nothing was ruled on the report's word.** All eighteen were checked against this tree on
  2026-09-13, on `master` at `dbc80b3`: six re-run, twelve confirmed at the line that produces the
  behaviour. **Seventeen hold as written, and `12` holds in part.** Every tool that writes output ran
  on a copy of a deck outside the repository. — 2026-09-13

| Record | Checked by | Result |
| :--- | :--- | :--- |
| `01` | `shell/shell.html` `:77`-`:78`, `shell/deck.js` `:618`-`:619` | only previous and next are wired, unchanged from `0.6.0`; Home and End are keyboard-only |
| `02` | `ArrowRight` dispatched on `document`, copy of the reference deck | `TypeError: e.target.matches is not a function`, slide unchanged |
| `03` | `item_pattern()` in `tools/deck/quickview.py`, both orderings | id-first matches, icon-first returns no match |
| `04` | `shell/components.css` `:661`-`:662` | `--m-on` is set on four shell classes only, with no inherited default |
| `05` | `tools/deck/density.py` `:394` | `--motion-kind` is searched only in the rule that starts the motion |
| `06` | `tools/deck/render.py` `:325`, `:350`-`:354` | a figure is compared with the stage, never with its own track |
| `07` | `shell/components.css` `:761`, `:765`-`:769`; `tools/deck/audit.py` `:2987` | the stop names shell classes only; `DS-218` counts, never toggles |
| `08` | `render.py state --hover ".ruler-ticks button"`, copy of the reference deck | the record's message, reproduced; `STATE_DEEP` holds no SVG paint property |
| `09` | the same run | the tick's `mouseenter` label write did not run; no event is dispatched anywhere in `render.py` |
| `10` | `slidefacts.py` on slide 2 of a copy of the reference deck | the disclosure is printed and the `sources-btn` button on the same slide is not |
| `11` | `shell/deck.js` `:209`-`:211`, `:233`-`:235` | hover and focus write the shared `#rulerLabel`, not a readout at the mark |
| `12` | `shell/deck.js` `:578`-`:611` | **in part**: Space advances with `preventDefault` and no exemption for a focused control; Enter has no case, and the listener is bubble-phase, not capture |
| `13` | `by_class` on a nested fixture | `['FIRST']` where `['FIRST SECOND THIRD']` was expected; the unnested control is correct |
| `14` | `tools/deck/readability.py` `:151`, `:162` | both sides of the ledger read through the truncated `slidefacts.facts` |
| `15` | `tools/deck/shell.py` `:1265`, `:198` | `sync` ends on region counts and never runs or names `tail` |
| `16` | `shell/deck.js` `:257`-`:259` | small ticks are `disabled` with `tabIndex = -1` past the bound, as `DS-217` states |
| `17` | `tools/deck/check.py`'s excusal mechanism; `DS-141`'s licence token | excusal is per rule for the project, and the one per-deck licence is read by `DS-141` alone |
| `18` | `docs/COMPONENT-CONTRACT.md`, `.disc` and the sources box | `.disc` is block-only and no inline disclosure is contracted |

- **`01` is still current.** It is the one record measured on `0.6.0`, and the pager on this tree is
  the pager it describes. — 2026-09-13

- **`12`'s Enter half is not in the source, and it is not rejected either.** The record describes a
  capture-phase listener cancelling both keys. The listener on this tree is bubble-phase and has no
  Enter case. A synthetic Enter press in triage was inconclusive, so
  [T-310](T-310-stop-the-shells-keydown-handler-throwing-on-a-document-target-and-taking-space-from-a-focused-control.md)
  measures it with a real key press and closes that half on the measurement. — 2026-09-13

- **The second adopter cross-check separates `17` from `023`, and ties it to `011`.** `023` was a rule
  firing outside its scope, answered by narrowing `DS-100`. `17`'s three rules fire correctly on the
  deck, so what is missing is a place for the owner's licence, not a narrower rule. `011`'s `DS-110`
  is one of those three and [T-265](T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md)
  still carries it. `18` takes its shape from the sources box, which
  [T-262](T-262-ds-092-counts-a-sources-box-as-prose.md) already subtracted from `DS-092`.
  `11` and `16` have no the second adopter counterpart. — 2026-09-13

- **Nothing was merged into an existing task, because no open task owns any of the eighteen.** Every
  neighbour is closed: [T-258](T-258-the-gate-passes-copy-its-own-reader-calls-difficult.md),
  [T-259](T-259-nothing-prints-what-a-slide-actually-contains.md) and
  [T-267](T-267-render-py-cannot-capture-a-decks-interactive-states.md) built `readability.py`,
  `slidefacts.py` and `render.py state` for `0.7.0`, and
  [T-268](T-268-three-chrome-and-timing-defects-in-deck-js.md) hardened the keydown handler. A defect
  found later in a shipped tool is new work, not an unfinished part of a closed task. — 2026-09-13

- **Eighteen records became eight tasks, grouped by the file a fix edits**, as T-225 grouped its
  twenty-seven. `04`, `05` and `07` are one task because the fix keys the motion gate on the ranking
  `density.py` writes, which makes `05` a precondition rather than a neighbour. `01`, `11` and `16`
  are one because `16`'s small ticks are aimable only once `11`'s readout exists. — 2026-09-13

- **Six classifications differ from what arrived.** `05` (`suggestion`), `06` (`gap`) and `15`
  (`friction`) are ruled defects and `PH1`, because each is a published tool reporting a state that is
  false. `17` (`request`) is a `decision` in `PH3`: the verifying pass read it as a defect, and that is
  rejected because no rule misfires. `01` (`suggestion`), `11` and `16` (`request`) are `PH3`
  deliverables: new chrome behaviour, not repair. `12` is accepted in part, above. — 2026-09-13

- **Nothing was rejected.** Every record is accepted and raised. None is deferred either: the owner's
  direction recorded in [T-302](T-302-give-the-3d-line-its-own-release-phase.md) is that 1.0.0 waits
  for an empty backlog outside `PH4`, and a deferral here would have no phase to wait in. **The owner
  confirmed the same day that the three `PH3` requests, T-307, T-308 and T-309, hold 1.0.0.** —
  2026-09-13

- **The eight are not added to [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md).** That
  document schedules the forty-nine tasks of 2026-08-29. These take the board's own ordering. —
  2026-09-13

**Outputs produced**

- Eight child tasks, `T-303` to `T-310`, listed in section 4.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Eighteen verdicts, each with a reason | **met** | The table below, with the reasons in section 3. All eighteen accepted and raised into eight tasks; none merged, deferred or rejected |
| Every accepted finding names the task that carries it | **met** | The table below, and every task names its records back |
| Every rejected finding names why | **met, and narrower than section 1 expected** | Nothing was rejected. `12`'s Enter half is the nearest thing to it, and section 3 says why it is left to be measured rather than dismissed |
| `01` checked against what shipped in `0.7.0` (plan step 4) | **met** | Section 3: the pager is unchanged |
| `11`, `16`, `17` and `18` checked against the second adopter set (plan step 3) | **met** | Section 3: `17` differs from `023` and shares `DS-110` with `011` |

**The triage**

| Record | Task | Decision | What it is | Phase, effort |
| :--- | :--- | :--- | :--- | :--- |
| `10`, `13`, `14` | [T-303](T-303-close-a-slidefacts-element-at-its-own-tag-find-every-control-and-make-readabilitys-ledger-add-up.md) | accepted, raised | Close an element at its balanced tag, find every control, and make readability's ledger add up | `PH1`, `m` |
| `04`, `05`, `07` | [T-304](T-304-bring-a-deck-authored-motion-inside-the-shells-motion-gate-the-motion-control-and-densitys-ranking.md) | accepted, raised | Key the motion gate and the Motion control off the ranking rather than class names, and rank what density finds | `PH1`, `m` |
| `06`, `08`, `09` | [T-305](T-305-let-render-py-see-an-svg-paint-change-a-scripted-hover-and-a-figure-painting-over-its-neighbour.md) | accepted, raised | SVG paint in `state`, a decided hover path, and a figure measured against its own track | `PH1`, `m` |
| `02`, `12` | [T-310](T-310-stop-the-shells-keydown-handler-throwing-on-a-document-target-and-taking-space-from-a-focused-control.md) | accepted, raised; `12` in part | Guard `matches`, leave Space to a focused control, and measure Enter | `PH1`, `s` |
| `03`, `15` | [T-306](T-306-wire-an-icon-first-source-item-in-quickview-py-and-make-shell-py-sync-name-a-stale-chrome-tail.md) | accepted, raised | An order-independent item pattern, and `sync` naming `tail` | `PH1`, `s` |
| `01`, `11`, `16` | [T-307](T-307-give-the-chrome-first-and-last-page-controls-and-a-ruler-whose-marks-a-reader-can-aim-at.md) | accepted, raised | First and last page controls, a readout at the mark, and whether dense-mode ticks become targets again | `PH3`, `m` |
| `17` | [T-308](T-308-decide-how-a-deck-records-a-deviation-its-owner-licensed-and-what-the-gate-reports-for-it.md) | accepted, raised | Decide where a deck's licensed deviation lives and what the gate reports for it | `PH3`, `m` |
| `18` | [T-309](T-309-contract-an-inline-term-that-opens-a-definition-bubble.md) | accepted, raised | Contract an inline term with a definition bubble, on the sources box's shape | `PH3`, `m` |

**Child fix tasks raised**

- Eight: `T-303` through `T-310`. Five are `PH1` and carry thirteen of the eighteen records, because a
  defect an adopter met in the published `0.7.0` is `CLAUDE.md`'s one condition for reopening that
  phase. Three are `PH3` and carry the five requests.

**What this triage found that it was not looking for**

- **Five of the eighteen are in the instruments the last report produced.** `08`, `09`, `10`, `13`
  and `14` are in `render.py state`, `slidefacts.py` and `readability.py`, which T-258, T-259 and T-267
  built from the second adopter set and shipped in `0.7.0`. Each was proved on the deck that motivated it, and
  a second deck of a different shape found what that one could not. It is the one-deck measurement
  shape T-225 section 3 already names, so it is recorded here rather than as a new lesson.

## Log

- 2026-09-08 — Raised on delivery of the report. The batch arrived as a pull request from the
  adopting project; no verdict has been taken on any record yet.
- 2026-09-13 — proposed -> specified. The owner started the triage; section 1's acceptance stands as
  written.
- 2026-09-13 — specified -> planned. Section 2's five steps, written at raise, run unchanged.
- 2026-09-13 — planned -> in_progress. All eighteen checked against this tree before any was ruled.
- 2026-09-13 — in_progress -> done. Eighteen accepted and raised into `T-303` to `T-310`: five `PH1`
  tasks carrying thirteen records, three `PH3` carrying five. Nothing merged, deferred or rejected.
  `shipped_in: unreleased`.
- 2026-09-13 — (no change). The owner confirmed that T-307, T-308 and T-309 hold 1.0.0, and answered
  T-308's open question.
