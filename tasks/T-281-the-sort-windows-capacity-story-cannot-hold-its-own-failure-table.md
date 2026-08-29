---
id: T-281
title: The sort-window deck's capacity story cannot hold its own failure table, and the fix changes its headline
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-248]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-30
updated: 2026-08-30
deliverables: [examples/sort-window/sources/throughput-model.md, examples/sort-window/sort-window.html]
---

# T-281 — The sort-window deck's capacity story cannot hold its own failure table, and the fix changes its headline

## 1. Specify

**Outcome**
`examples/sort-window/` states one capacity story and every figure derived from it follows. Today it
states three that cannot all be true, and the settlement is a decision about what the deck argues
rather than a number to correct — which is why [T-248](T-248-four-content-errors-in-three-shipped-decks.md)
deferred it rather than taking it.

**Carries** `PR-84` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3, deferred there
2026-08-30 with the arithmetic recorded. **The statement stays in the register** and is not restated
here (the method's umbrella condition 2); what is below is only the decision and what each answer
costs.

**The three statements, and why no two of them hold together.** Measured 2026-08-30 while working
`T-248`:

| Stated | Where | What it implies |
| :--- | :--- | :--- |
| One sorter line at **3,100/hr** | `throughput-model.md`, and the deck's own headline | At most **16,533** parcels sorted between 19:40 and the 01:00 cut-off |
| Peak night **27,600** parcels, peak miss **12.4%** | the volume and failure tables | About **24,700** sorted by the cut-off |
| Overlap of the first trunk's sort into the second's is a **future** limit, above 31,900 a day | slide 10's tripwire | The first trunk clears before **23:40** |

Row 1 and row 2 differ by 8,200 parcels — a **40%** miss where the deck observes 12.4%. Rows 2 and 3
pull opposite ways at **every** constant rate: a rate high enough to leave the ~3,000 unsorted at
01:00 that 84% of a 12.4% miss implies puts the first trunk past 23:40, so the overlap is already
happening; a rate low enough to keep the overlap in the future clears the night before the cut-off
and leaves nothing unsorted to miss.

**Scope**
- In: the capacity statement in
  [`examples/sort-window/sources/throughput-model.md`](../examples/sort-window/sources/throughput-model.md),
  and everything derived from it — the trunk table's finish times, the ledger row in
  `sort-window.foundation.md`, slide 5's night-flow diagram and derivation panel, and slide 10's
  tripwire
- In: the deck's headline, **if the answer is the two-line one**. That is the whole reason this is a
  separate task
- Out: the failure tables. `12.4%`, the 84/16 split and the district table are the deck's observed
  evidence; a model is fitted to them, not the other way round
- Out: any other finding on this deck

**Inputs**
- `PR-84` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3 — the statement, the
  evidence and the deferral, which carries the full arithmetic
- [T-248](T-248-four-content-errors-in-three-shipped-decks.md) §3 — what was measured and what was
  refused

**Acceptance criteria**
- [ ] one capacity statement, and every derived figure re-derived from it rather than edited toward
      it — the trunk finishes, the ledger row, slide 5's working and slide 10's tripwire
- [ ] the deck's own arithmetic reproduces its failure table to within the sampling the source
      already states, and the reproduction is shown
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately
- [ ] the rebuilt slides **looked at**, per `CLAUDE.md` rule 6 — recorded in
      [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) if this task cannot look

**Open questions**
- ~~**Does the depot have one sorter line or two?**~~ **Ruled 2026-08-30 by the owner: two.** The
  question as it was put, and what each answer cost, is kept below because a ruling is only worth
  what the alternatives were.
- **Does the depot have one sorter line or two?** — the owner. **The recommendation is two, running
  until the evening shift ends and one through the night**, because it is the only arrangement found
  that reproduces the deck's existing working rather than replacing it: the first trunk's 20,400 at
  6,200/hr finishes **22:57**, the second trunk's 7,200 at 3,100/hr still finishes **01:59** exactly
  as slide 5 derives today, **3,067** are unsorted at the cut-off for a **13.2%** miss against the
  stated 12.4%, and the tripwire moves from 31,900 to about **33,500 a day**. What it costs is the
  headline — *One depot, one sorter line, and a nightly window that closes at 01:00* — which is the
  title slide's standfirst and a sentence `sort-window.slides.md` discusses as a term. The
  alternative is to keep one line and rewrite the failure tables to about 40%, which keeps the
  headline and changes what the deck is about: a depot that misses two parcels in five at peak is a
  different argument from one that misses one in eight.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Put the question to the owner with both answers priced, not with a preference | **Ruled 2026-08-30: two lines** |
| 2 | Write the capacity statement in the source, and derive every figure from it rather than editing toward it | the trunk table, the two derivations, the unsorted count and the overlap threshold |
| 3 | Move the deck's figures to match, including the night-flow bar's geometry | slide 5's lane, slide 10's tripwire, the title slide's premise |
| 4 | Let the derived things be derived | the embedded quick view refreshed from the corrected source |
| 5 | Show the deck's own arithmetic reproducing its failure table | 3,067 unsorted at the cut-off against the 84% share of a 12.4% miss |

## 3. Implement

**Decisions & assumptions**
- **Two sorter lines, ruled by the owner 2026-08-30**, from the two answers priced in §1. The
  recommendation was two and the reason it was recommended is the reason it holds: it is the only
  arrangement found that **reproduces the deck's existing working rather than replacing it**.
- **The shift boundary is 23:00, chosen rather than derived** — 2026-08-30. The arithmetic fixes
  only that the second line stops after the first trunk is done (22:57) and before the second lands
  (23:40). 23:00 is the round number inside that window, and the title slide states it, so a reader
  can check the story rather than take it.
- **Every figure is re-derived, none edited toward the answer** — 2026-08-30:
  - first trunk, 20,400 on both lines at 6,200/hr: **3h 17m**, so 19:40 + 3h 17m = **22:57**, clear
    of the second trunk by 43 minutes;
  - second trunk, 7,200 on the night line at 3,100/hr: **2h 19m**, so 23:40 + 2h 19m = **01:59** —
    **unchanged**, which is the point: slide 5's derivation panel already showed this working and
    still does;
  - at the 01:00 cut-off the night line has done 1h 20m of its 2h 19m, so **3,067** of 7,200 are
    still on the belt. The source's failure table says 84% of a **12.4%** peak miss is *still
    unsorted at the cut-off*, which is 2,875 parcels against this 3,067 — a modelled peak night
    against a 31-night mean, and they agree to within 7%;
  - the overlap starts when the first trunk cannot finish in its four hours, and both lines sort
    **24,800** in four hours. At the modelled split (73.9% of the night on the first trunk) that is
    a day of about **33,500**, which replaces the tripwire's 31,900.
- **31,900 stays on slide 10** — 2026-08-30. It is the observed busiest day and it has a ledger row;
  the new sentence keeps it as the comparison — *5% past December's busiest 31,900* — which says how
  little headroom there is, and is a better tripwire than a bare threshold.
- **The night-flow bar's geometry was re-derived, not nudged** — 2026-08-30. The lane's 674 px
  spanned 19:40 to 00:14, so the scale is **2.46 px a minute**; 19:40 to 22:57 is 197 minutes, so
  the bar is **485 px** and its two labels move to the new end. Checked against the figure's own
  landmarks before writing: at that scale the second trunk's 23:40 lands on x=838 and the 01:00 rule
  on x=1035, which is where they already are.
- **The specification is amended, not annotated** — 2026-08-30, and this departs from
  [T-247](T-247-the-portfolio-generators-documents-against-the-deck.md)'s pattern on purpose. That
  task wrote deviations *beside* the reviewed wording because the build had diverged from a
  reviewed design. Here the model underneath the wording was wrong: one line at 3,100 an hour cannot
  sort a peak night by the cut-off at all, so the reviewed sentence and the deck's own failure table
  could never both have been true. Each amended line says so and dates it.

**Outputs produced**
- [`examples/sort-window/sources/throughput-model.md`](../examples/sort-window/sources/throughput-model.md)
  — the capacity statement, the trunk table, both derivations, the unsorted count and a *Where the
  overlap starts* section
- [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) — the title
  slide's premise, slide 5's lane geometry, labels and aria-label, the derivation panel's input row,
  slide 10's tripwire, and the embedded quick view refreshed from the source
- [`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)
  — the finish-time row, and a row for the two-line rate
- [`examples/sort-window/sort-window.slides.md`](../examples/sort-window/sort-window.slides.md) —
  four amended lines, each dated and pointing here

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| One capacity statement, every derived figure re-derived from it | pass | The trunk finishes, the ledger row, slide 5's working and slide 10's tripwire all come from *two lines to 23:00, one after*. Nothing was edited toward a target |
| The deck's arithmetic reproduces its failure table, and the reproduction is shown | pass | **3,067** unsorted at the cut-off against the **2,875** implied by 84% of a 12.4% miss — a modelled peak night against a 31-night mean, agreeing to within 7%. Shown in the source rather than asserted here |
| `lint.py` and `check_all.py` green, run separately | pass | Run separately |
| The rebuilt slides **looked at** | owed | [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md). The lane's geometry was recomputed without a render, which is exactly what rule 6 exists for |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-30 | → proposed | Raised out of [T-248](T-248-four-content-errors-in-three-shipped-decks.md) in **B12**, which measured `PR-84`'s three candidate answers and refused all three as number fixes. **A `decision` rather than a `fix`**: the arithmetic is settled and recorded on the register row, and what is left is whether the depot has one sorter line or two — which changes the deck's headline either way it is answered. `PH3` by `CLAUDE.md`'s rule: the published `0.6.0` ships this deck, but no adopter met this as a defect in the plugin, and it is an example's content rather than the product's behaviour. |
| 2026-08-30 | proposed → done | **Ruled two lines by the owner**, put to them with both answers priced. Carried out the same day: the source states the capacity once and every figure is re-derived from it. The second trunk's **01:59** is unchanged, which is the evidence the answer is the right one — it was slide 5's own working before this task and it still is. The deck's arithmetic now reproduces its own failure table to within 7%, where one line at 3,100 could not reach it at all. One look owed on the rebuilt lane. |
