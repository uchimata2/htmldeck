---
id: T-075
title: DS-064 probes for the reference deck's own class names, and contract.py is outside the fixture
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-051, T-065, T-066]
work_package: v0.1
owner: the project owner
business_value: critical
effort: m
created: 2026-08-10
updated: 2026-08-10
deliverables:
  - tools/deck/render.py
  - tools/deck/contract.py
  - tools/deck/audit.py
  - tools/deck/theme.py
  - tools/deck/contract_variants.py
---

# T-075 — DS-064 probes for the reference deck's own class names, and contract.py is outside the fixture

## 1. Specify

**Outcome**
DS-064 measures the body run of any conforming deck, and a deck it cannot find one on is **undecided**
rather than failed. And the absent-subject discipline covers every verdict producer the gate consumes,
not every producer that happens to live in one module.

**The report**
From another project, 2026-08-10, on the published `v0.1.3`. [`render.py:123`](../tools/deck/render.py)
finds the run DS-064 measures with `cur.querySelector('.standfirst, .cost-p, .title-note')`. `.cost-p`
and `.title-note` are **composition classes belonging to the reference deck**;
[`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) names neither. A deck whose supporting prose
uses any other class name and which has no `.standfirst` reports `no body run measured at 720p` and
**fails a rule it comfortably satisfies** — theirs measures 26 du, 17.3 CSS px at the 0.6667 scale,
against a 16 px floor. Their argument for why a deck cannot fix this from its own side is the one that
decides the task: the only remedy available to an author is to adopt one of those three class names,
which *"inverts the contract"* — `COMPONENT-CONTRACT.md` becomes advisory and `render.py`'s selector
becomes the real specification, undocumented.

**Confirmed, and it is the seventh instance of a defect this project has now fixed three times.**
[`contract.py:322`](../tools/deck/contract.py) is `out.append(("DS-064", "no body run measured at
720p", False))` — absence read as failure, the identical shape to DS-164, DS-160, DS-113, DS-143 and
DS-135. [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md) built
`ABSENCE_IS_A_FAIL` to end exactly this, and its criterion *"adding a producer that is not [inside the
fixture] fails the run"* is enforced by `audit.py:1783`:

```
producers = sorted(n for n in globals() if n.endswith("_verdicts"))
```

**`globals()` is one module.** `contract.verdicts` and `contract.scale_verdicts` are verdict producers
in a second module, reached by [`check.py:197`](../tools/deck/check.py) through `contract.audit`, and
they have never been through the discipline at all. So the guarantee the project believes it has —
that no row can fail a deck for lacking the thing it judges — holds over `audit.py` and is silent over
`contract.py`, which is why an outside project found the seventh instance rather than the fixture
finding it. **A derivation that cannot see the thing it derives over is the same failure as T-065's
hand-run sweep**, one level up.

By inspection, `contract.py` carries more rows of this shape than the reported one: DS-063's
`NO NON-TEXT ELEMENT MEASURED` and `NO TEXT RUN MEASURED` legs, and the `bool(on_stage)`,
`bool(ratios)` and `bool(roles)` clauses in `verdicts`. Which of those are absent-subject cases and
which are real failures is for the fixture to say, not for this paragraph.

**Two defects, one symptom, and the order matters**
1. **The probe cannot find its subject.** `.body` is contracted — cardinality 1 on every slide
   (`COMPONENT-CONTRACT.md:107`) — and `.standfirst` is contracted at 0-1. The probe already uses
   `.body` for the overflow measurement 30 lines lower. Finding the run by contract instead of by the
   reference deck's composition is the fix, and it retires `.cost-p` and `.title-note`.
2. **Absence is read as failure.** Fixed independently, because a probe can always meet a deck whose
   prose it genuinely cannot locate, and the reporter's own direction is right: *a dimension that
   cannot locate its subject has not been evaluated*. That is **L-44** paid in the other direction,
   and the `undecided` bucket [T-065](T-065-four-rules-still-fail-a-deck-for-not-having-their-subject.md)
   built is where it goes.

Doing (1) alone would close the report and leave the seventh instance live for the eighth deck. Doing
(2) alone would turn a real check silent on the decks it is for.

**Scope**
- In: DS-064's probe finds its subject by contracted component, not by reference-deck class name.
- In: DS-064 returns `None` when no body run is found, and `check.py` counts it undecided.
- In: **the absent-subject fixture covers `contract.py`**, with the producer derivation crossing module
  boundaries so a producer in a third module cannot sit outside it either.
- In: every `contract.py` row the extended fixture reports, declared in `ABSENCE_IS_A_PASS` /
  `ABSENCE_IS_A_FAIL` with a reason, or converted — the same treatment `audit.py`'s rows had.
- In: separating `scale_verdicts`'s Chrome render from its verdict arithmetic, since a fixture cannot
  launch a browser to ask what a row does with nothing.
- In: a fixture failing before the fix (**L-04**), and the reference deck's verdicts unchanged, diffed.
- Out: raising or lowering the 16 px floor. The floor is right; finding the text is what is broken.
- Out: `render.py`'s `--out` defect from the same report, which is
  [T-074](T-074-the-documented-render-command-does-not-exist.md).
- Out: the reporting project's own deck.

**Inputs**
- `docs/DESIGN-SYSTEM.md` §DS-064, `docs/COMPONENT-CONTRACT.md`
- `tools/deck/render.py`, `tools/deck/contract.py`, `tools/deck/audit.py`

**Acceptance criteria**
- [ ] A deck whose body prose carries neither `.cost-p` nor `.title-note` nor `.standfirst` is
      **measured** by DS-064, shown on a variant built for it
- [ ] A deck with no body run at all is undecided on DS-064, not failing
- [ ] A deck whose body genuinely falls under the floor still **fails**, proven on the existing
      `body-type-under-the-floor` variant
- [ ] The extended fixture reports every `contract.py` verdict row, and each is declared or converted
- [ ] Adding a verdict producer in **any** module without declaring its rows fails the run, shown by
      seeding one
- [ ] The reference deck's account is unchanged, diffed before and after
- [ ] `.cost-p` and `.title-note` appear in no gate selector anywhere, checked repository-wide

**Open questions**
- **Is `.body` the run, or the container?** `.body` is a `div` and its computed font size may be an
  inherited value no glyph is set at, which would measure the wrong number. Recommended: measure the
  smallest text-bearing descendant of `.body`, falling back to `.body` itself, and let the fixture
  prove it on the reference deck by reproducing today's 17.3 px. Settle it with a measurement, not a
  reading — this project's own position.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Split the render out of `scale_verdicts` so its rows can be evaluated against nothing | `tools/deck/contract.py` |
| 2 | Extend the fixture across modules; record every row it reports, failing first | The failing run, and the row table in §3 |
| 3 | Declare or convert each row, DS-064 included | `audit.py`'s two tables |
| 4 | Answer the open question by measurement, then fix the probe selector | `tools/deck/render.py` |
| 5 | A variant deck with contract-conformant prose under a foreign class name | `tools/deck/contract_variants.py` |
| 6 | Diff the reference deck's account; run the seeded-defect deck | Both runs |

## 3. Implement

**Decisions & assumptions**

- **It was six producers outside the fixture, not two — 2026-08-10, and this is the finding.** The
  directory scan was written for `contract.py` and its first run named `contrast.verdicts`,
  `theme.verdicts`, `component.verdicts` and `printpages.verdicts` as well. Every one is consumed by
  [`check.py`](../tools/deck/check.py); none had ever been run against a measurement in which nothing
  was found. Two of the eight were inside the discipline. Generalised as **L-57**: a derivation is
  bounded by what it reads, and `globals()` is one module.

- **Nine more rows were reporting conformance about an absent subject, and they were found by the
  boundary moving rather than by looking.** Six `theme.py` band rows (`DS-034`, `DS-036`, `DS-060`,
  `DS-140`, `DS-141`, `DS-168`) read clean on a document declaring **no theme at all**, because
  `validate` reports one region-level problem and no per-rule ones, so `not broke` was true of every
  band. `DS-010` passed for the same reason one step further back: `lits` and `curved` are `[]` when
  there is no region *because the scan never ran*, and a prohibition satisfied by a scan that did not
  happen is not a prohibition satisfied. All seven now report `None` unless a region exists. `DS-200`
  in `contract.py` was the same shape — `not off` over an empty list — and is converted too.

- **The probe finds the run by contract, and the reference deck's number is unchanged — measured, not
  argued.** `.standfirst` is contracted at 0-1 per slide and `.body` at 1, so the selector is the
  standfirst where a slide has one and the first paragraph of the body where it does not. On the
  reference deck that is the same element on every sampled slide: 11 of 13 slides carry a standfirst,
  the closing slide's `.body` holds only a headline, and DS-064 still reports **17.3 px (26 du) on
  *Buy frequency before bikes*, 3 slides sampled**.

- **DS-064 was NOT widened to every prose run, and the reason is a measurement — 2026-08-10.** The
  obvious stronger probe is the smallest text-bearing descendant of `.body`. On the reference deck
  that is `.title-note` at `--fs-small`, which is `--fs-base / --type-ratio` ≈ 21.7 du ≈ **14.4 CSS px
  at 720p** — under the floor. So widening the probe would fail the reference deck on prose the rule
  was probably never written about, and *what counts as body text* is a question for `DESIGN-SYSTEM.md`
  rather than for a selector. One representative run per slide is today's semantics and stays. **The
  finding is recorded rather than acted on**: DS-064 does not see small prose, and that is now known.

- **A rule may be declared in both absence tables, and DS-229 is the first — 2026-08-10.** The
  self-test forbade the overlap outright.
  [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md) had already recorded
  that declarations are per row and that a rule-level overlap check would be refuted; the check
  shipped anyway because nothing had both states. `component.verdicts` emits five DS-229 rows — three
  prohibitions that pass on an empty document, two requirements that fail on it, all five correct. The
  check now requires an overlap to be *earned* by rows in both directions, which is what `stale` and
  `stale_fail` were already enforcing from the other side.

- **`contrast.verdicts` refuses an empty document rather than reporting on one.** It calls `sys.exit`
  when there are no `:root` colour tokens, so the empty document is not its absent subject and cannot
  be. Its nothing-found input is a theme with nothing to measure against it. Left as it is: a
  producer that exits the process instead of returning a row is a separate defect from this one, and
  it is [T-076](T-076-a-verdict-producer-that-exits-instead-of-reporting.md).

- **`contract.scale_verdicts` is declared as delegating rather than exercised, and the declaration is
  checked.** A producer that needs a browser cannot be run against a measurement, so the render was
  split off into `scale_verdicts_from`. `DELEGATING_PRODUCERS` names what it delegates to **first in
  the reason**, and the self-test parses that word, requires the target to be an exercised producer,
  and requires the delegating function's own source to call it. Without that the split would be an
  escape hatch.

- **Two gates were already red on `master` before this task touched anything**, both found by running
  the full set rather than the four the last handoff listed. `tools/docs/figures.py` — the coverage
  split had moved to 82/31 and four documents still said 81/32, with `figures.py`'s own
  `EXCLUDED_PROSE` still excusing the retired `32`. And `content_variants.py`'s self-test, whose
  `same-figure-two-values` anchor read `Illustrative model</p>` while the deck has said
  `Illustrative model<br>Cost model</p>` since `bf43e08`. Both fixed here, out of scope and reported:
  **the suite's own self-test is the only thing that reads its anchors, and the routine gate set does
  not run it.**

**Outputs produced**
- [`tools/deck/render.py`](../tools/deck/render.py) — the DS-064 probe selector
- [`tools/deck/contract.py`](../tools/deck/contract.py) — `scale_verdicts_from`, four conversions,
  `PROBE_FOUND_NOTHING` and the two nothing-found models, `hasDoc`, undecided in `main`
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `verdict_producers`, `DELEGATING_PRODUCERS`, ten
  new table entries, the overlap rule
- [`tools/deck/theme.py`](../tools/deck/theme.py) — seven rows guarded by the region existing
- [`tools/deck/contract_variants.py`](../tools/deck/contract_variants.py) — the new variant,
  `MUST_PASS`, count-declared edits, `good is False`
- [`tools/deck/content_variants.py`](../tools/deck/content_variants.py) — the stale anchor
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-57**

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck whose prose carries none of the three class names is **measured** | **met** | `body-prose-under-a-foreign-class`, a variant that renames the deck's prose classes and changes nothing else. `8 of 8 variants behaved as specified`. With the pre-T-075 probe patched back in, the same deck reports `no body run measured at 720p` |
| A deck with no body run at all is undecided, not failing | **met** | Asserted by name in `audit.self_test`. Reverting the row to `False` gives `SELF-TEST FAILED: DS-064 FAIL against a measurement in which nothing was found` |
| A deck genuinely under the floor still fails | **met** | `body-type-under-the-floor` → `13.3 px (20 du)`, CAUGHT |
| The extended fixture reports every `contract.py` row, each declared or converted | **met** | And four further modules it found on the way. Declared: DS-060, DS-062, DS-071, DS-011, DS-013, DS-027, 1.4.3, 1.4.11, DS-229, PRINT-1. Converted: DS-063 (both legs), DS-064, DS-072, DS-074, DS-200, and seven `theme.py` rows |
| A producer in **any** module without declared rows fails the run | **met** | Shown by the scan itself: written for one module, it immediately failed on four others by name |
| The reference deck's account is unchanged, diffed | **met** | `113 / 82 / 0 / 4 / 27`, `undecided 0`, `SILENT 0`, partition holds — identical before and after. DS-064 unchanged at 17.3 px (26 du), 3 slides sampled |
| The seeded-defect deck still fails everything it should | **met** | `4 failure(s): DS-035 DS-075 DS-141 DS-142`, unchanged |
| `.cost-p` and `.title-note` appear in no gate selector, checked repository-wide | **met** | The only remaining occurrences are the reference deck's own markup and CSS, and the new variant's rename anchors |
| The open question answered by measurement | **met** | `.body` is a container; the smallest descendant is `--fs-small` at 14.4 px. See §3 — the probe takes one representative run per slide and the widening question is recorded, not taken |
| Every other suite still green | **met** | `static_variants 24 of 24` · `content_variants 3 of 3` · `deliverable_variants 7 of 7` · `contract_variants 8 of 8` · `critique 12 of 12` · `check_scaffold 14 of 14` · `taskmd check` and `refcheck` clean |
| The deck opened and looked at (**L-01**) | **met** | Slides 1 and 3 re-rendered through the changed probe in real Chrome with DNS black-holed, and slide 1 examined: standfirst, title note, ruler, counter and bottom line all render correctly. This task produces no deck; the probe it changes runs inside one, which is what was looked at |

**Child fix tasks raised**
- [T-076](T-076-a-verdict-producer-that-exits-instead-of-reporting.md) — `contrast.verdicts` exits
  the process on a document it will not report on, which takes the whole gate down with it

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | **Shipped in `v0.1.4`. The reported defect was one row; the fixture that was supposed to make it impossible could see two of the package's eight verdict producers.** DS-064's probe now finds its subject by contracted component, and a deck it cannot find one on is undecided rather than failed — the reporter's own direction, and the right one. The larger half is that `audit.self_test` derived its producer list from `globals()`, so `contract.py`, `contrast.py`, `theme.py`, `component.py` and `printpages.py` were outside the absent-subject discipline entirely. Moving the derivation to the directory found four modules nobody was looking at and **nine further rows reporting conformance about subjects that were not there**, six of them in `theme.py` reading clean on a document with no theme. DS-229 became the first rule legitimately declared in both tables, which retires a check T-066 had already argued was wrong. The reference deck's account is byte-identical and the seeded deck still fails its four. Generalised as **L-57**. |
| 2026-08-10 | → in_progress | Specified and planned in one pass, since the mechanism was already reproduced when the task was raised. The plan's first step — splitting the render out of `scale_verdicts` — is what made every later step possible: while a producer needs a browser, no fixture can ask it what it does with nothing. |
| 2026-08-10 | → proposed | **Reported from another project against the published `v0.1.3` and confirmed by reading the probe.** The reported half is that DS-064's selector names two composition classes belonging to the reference deck, so a conforming deck's prose is invisible and the rule fails a deck that satisfies it — the contract inverted, with `render.py`'s selector as the real specification. **The half found while confirming it is larger**: `contract.py` produces verdict rows that `check.py` consumes and sits entirely outside the absent-subject fixture, because `audit.self_test` derives its producer list from `globals()` — one module. T-066's criterion that an undeclared producer fails the run is therefore true only of the module it was written in, which is T-065's hand-run sweep repeated as a scoping error. `v0.1` because the published gate fails a legitimate deck for a rule it passes, and DS-064 was explicitly ruled **out** of T-065 as a genuine finding about that project's deck — it was not. |
