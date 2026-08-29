# Remediation order — the pre-release backlog, batched for unattended sessions

**Tier 3. Loaded by nothing**; opened when a session asks *what do I work next*. It is a schedule,
not a decision: what each task does is its own record, and this file never restates one.

Written 2026-08-29, after the pre-release audit's triage (cycle 40) and the ClaimAI adopter triage
([T-225](../tasks/T-225-triage-the-claimai-adopter-report.md)) put 49 tasks on the board at once.
**[T-057](../tasks/T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) is out of
scope by the owner's instruction** — the 3D visual is deferred, not scheduled here. That leaves 47
tasks plus [T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md)'s two remaining
cycles.

**Three tasks have joined it since, each following a ruling** — `T-274` and `T-275` from §3's two
post-B7 questions, and `T-276` from the third. *The title said* the 47 tasks *until 2026-08-29,
which is a count of what the triage put on the board and reads as a count of what this file holds.
The sentence below forbids exactly that, and the title was the one place nobody applied it.*

**A batch keeps its membership whether or not its tasks are closed — this is a schedule, not a board.** How many are still open is [`../tasks/README.md`](../tasks/README.md)'s answer and never this file's, so nothing here carries a count that decays. **B1 to B10 landed 2026-08-29.**

---

## 1. The three rules that decide the order

Everything below follows from these. They are stated first because a batch that violates one costs
more than it saves.

1. **An instrument is fixed before anything it measures.** Three were producing wrong answers when
   this file was written — `density.py write` wrote invalid markup, `render.py motion` reported a
   working motion as dead, and the scaffold gate read nought of the skill's eighteen commands. Work
   verified against a lying instrument has to be verified again. **All three were fixed in B1 on
   2026-08-29**, which is what makes wave 2 onwards worth running; the rule stands for whatever the
   later batches find.
2. **A rule changes before any document that counts it.** Sixteen open tasks state a figure that a
   rule change moves — rule totals, `auto`/`judge` splits, coverage counts. Fix the documents first
   and every one of them moves twice. **This is why every documentation task is in the last third**,
   including the ones ranked `High`.
3. **A deck is rebuilt once.** Five tracked decks are gated byte-for-byte. Every task that changes
   the shell, a theme, a rule's check or a generator invalidates them, so the deck work sits after
   all of it and the rebuild happens in one batch.

**The release is cut after all forty-seven**, ruled by the owner 2026-08-29. So no finding
needs a deferral reason, cycle 41 re-reads a settled tree, and the eighteen `PH1` tasks are
worked where this order puts them rather than pulled forward — which is the whole reason the
corollary below is affordable.

**The corollary nobody likes:** the `High` and `critical` bands do **not** run first. Severity
measures the audience's cost; this order measures rework. Where they disagree, a `critical`
documentation fix waits behind a `medium` instrument fix, because the instrument decides whether the
documentation fix can be verified at all.

---

## 2. The batches

Each batch is one unattended session: one subject area, no file conflicts inside it, and no decision
that is still the owner's. **A batch ends at a commit.** Six batches carried a question when this
file was written; all eight questions were ruled the same day and §3 holds the answers, so no batch
is blocked.

### Wave 1 — the instruments (nothing downstream is trustworthy until these land)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B1** — landed 2026-08-29 | [T-254](../tasks/T-254-density-py-write-corrupts-every-self-closing-svg-tag.md), [T-255](../tasks/T-255-render-py-motion-seeks-past-the-delay.md), [T-231](../tasks/T-231-two-packaging-checks-have-no-subject-at-all.md), **+[T-272](../tasks/T-272-render-py-motion-enumerates-a-different-animation-set-across-runs.md)** | `s`·4 | Three instruments that answer wrongly today. `density.py write` is refused outright by the adopter's launcher and is the tool `DS-239` makes necessary; `render.py motion` prints a verdict about its own seek as a finding about the deck; the scaffold gate has read nothing since 2026-08-20. Files are disjoint: `density.py`, `render.py`, `check_scaffold.py`. **`T-272` was found while closing `T-255` and absorbed into the batch under §4** — the same instrument enumerating a different animation set across runs of one unchanged deck |
| **B2** — landed 2026-08-29 | [T-261](../tasks/T-261-ds-035-measures-a-text-run-through-its-transform.md) | `s` | **Alone, because it changes what every geometry rule measures.** The probe must be pinned for `DS-035` and unpinned for `DS-140`, `DS-142` and `DS-218`, so it is a split rather than a flag, and its blast radius wants its own gate run. **The split is in time rather than in a flag**: the probe reads its motion facts, pins, then measures. T-209's *identical both ways* was re-derived and does not generalise — two geometry rows move on a deck whose entrance moves the axis |
| **B3** — landed 2026-08-29 | [T-246](../tasks/T-246-two-docs-instruments-misdescribe-their-own-behaviour.md) | `s` | `figures.py`'s `bind()` decides every pasted figure in the tree, and sixteen later tasks paste figures. Fixing what it actually pairs before they run is the difference between one sweep and two |

### Wave 2 — rules and checks (they move the counts, so they precede every document)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B4** — landed 2026-08-29 | [T-243](../tasks/T-243-five-checks-bound-on-a-name-rather-than-on-structure.md), [T-230](../tasks/T-230-the-resolution-contract-samples-four-slides-by-fixed-index.md) | `m`,`s` | Five checks re-bound on structure, plus the adopter's `DS-229` and `DS-239` records. **Needed B1** — `T-243`'s `DS-239` half was unverifiable while `density.py write` corrupted what it wrote. **Six register rows and two adopter records closed across seven files**, and the batch found two more defects in code it had to read: a CSS comment reaching a selector in two modules, and an `rstrip` taking a character set rather than a suffix ([L-140](lessons/L-140.md)). **`PR-49`'s stated remedy was refused by its own measurement, and so were two of the replacements** - the pattern the register's section 5 predicts, now in a fifth consecutive batch |
| **B5** — landed 2026-08-29 | [T-263](../tasks/T-263-ds-217-fails-on-any-deck-past-eighteen-sections.md), [T-262](../tasks/T-262-ds-092-counts-a-sources-box-as-prose.md), [T-264](../tasks/T-264-ds-141s-request-licence-has-nowhere-to-put-its-number.md) | `s`·3 | Three rules that a correct deck cannot satisfy. Independent of each other; all three change `audit.py` and a rule row. **`T-264`'s question is ruled** — §3. **Three adopter records closed, and `T-263`'s stated cause refused by measurement**: the sub-pixel rounding it blames is 1e-4 CSS px, and what actually breaks the ruler is two mark sizes sitting side by side. Kept as [L-141](lessons/L-141.md). `T-264` needed a **fourth token kind** — `optional` — because *unset by default* and DS-013 could not both hold, and it closed a DS-010 hole after measuring that closing it costs nothing (18 declarations newly scanned, 0 offending). **A sixth consecutive batch refusing a proposed remedy** |
| **B6** — landed 2026-08-29 | [T-256](../tasks/T-256-ds-219-cannot-see-a-painted-svg-ancestor.md), [T-260](../tasks/T-260-ds-244-tests-proximity-where-it-means-obstruction.md) | `m`·2 | The two rules whose *scope* is in question rather than their code. **Both questions are ruled** (§3). Held together because both re-open what a rule measures and both are gated by `T-204`'s calibration precedent. **Both rulings held under measurement and neither rule lost force.** `DS-219`'s ground now composites every painted layer under the mark, and the adopter's *the rule is wrong* was refused: the rule was asking the right two numbers against the wrong surface ([L-142](lessons/L-142.md)). `DS-244` reads opacity before pairing and measures a label across the box it names — **reporting, because the calibration came back empty**: zero firings on five decks, so there is no false-alarm rate to gate on. The batch's own worst moment is [L-143](lessons/L-143.md): the first opacity guard silenced the rule entirely, and what caught it was re-running `T-204`'s count rather than reading the diff |
| **B7** — landed 2026-08-29 | [T-229](../tasks/T-229-ds-106s-check-omits-a-word-the-rule-names.md), [T-242](../tasks/T-242-the-contracts-against-the-checkers-that-decide-them.md), **+[T-273](../tasks/T-273-the-owed-looks-have-no-queue-to-accumulate-in.md)** | `s`,`m`,`xs` | Deriving a check from its rule row, and reconciling the two contracts with their checkers. Both are *derive rather than restate* work and share the idiom. **Both tasks found the subject wrong before the list was.** DS-106's check read the whole file, so `actually` sat in **seven** shell comments per deck against one in slide copy, and adding the word the rule names would have failed all five decks; `component.py` iterated the contract and never the CSS, so a rule with **no row at all** was invisible — and the new direction found a third unrowed motion on its first run. **Three findings closed, two deferred**: `PR-36`'s Turn half and `PR-77` are one `DS-000` question and are recorded together where it will be taken, rather than answered as a ninth. **`T-273` was raised while closing the batch and worked in it** under §4: the owed looks had no queue to accumulate in, so the pass this order promises before the release had nothing to run |
| **B8** — landed 2026-08-29 | [T-265](../tasks/T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md), [T-266](../tasks/T-266-a-deck-cannot-name-a-repeated-figure-treatment-once.md), [T-270](../tasks/T-270-two-rules-whose-escape-hatch-teaches-the-wrong-habit.md) | `s`·3 | The three rule **decisions**. Grouped because each is a `DS-000` ruleset change with a stated reason, and one session can hold that frame once. **All three are ruled** (§3), so the session writes the change rather than deciding it. **Two written as ruled, and one ruling refused by its own measurement.** `DS-110` narrows by place on top of T-070's by scope, and `DS-229` reserves `.d-` for a deck's own repeated treatments — both proved on `measure-first.html` rather than on a fixture. **`T-270`'s `DS-100` half was refused**: the ruled condition holds on 38 of 38 slides, so it is an off switch rather than a narrowing, and the question went back to §3 with a recommendation ([L-144](lessons/L-144.md)). A seventh consecutive batch refusing a proposed remedy, and the first to refuse a **ruling** |

### Wave 3 — the product (shell, tools, themes)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B9** — landed 2026-08-29 | [T-232](../tasks/T-232-two-entrance-motions-do-not-collapse-for-print.md), [T-268](../tasks/T-268-three-chrome-and-timing-defects-in-deck-js.md), **+[T-274](../tasks/T-274-build-the-card-reveal-so-turns-two-dials-have-a-reader.md)** | `s`·2,`m` | The shell: the print block's entrance collapse, and three chrome and timing defects the presenter reported. `components.css` and `deck.js`, and both end in a print or a look. **`T-274` joins them from §3's ninth ruling** — the card reveal is a new component in the same file, and it has to land before B12 rebuilds the decks that will carry it . **Landed, and it moved a boundary this order drew.** `T-268`'s three fixes are proved by a browser probe, and two implementations of `data-arrived` were refused by it before the third passed. `T-232`'s wider half was refused in the shape the register proposed and rebuilt to bind on the hazard `DS-224` names — it found a third instance on its first run, and caught `T-274`'s brand-new component before that shipped anywhere. **The five decks were synced here rather than in B12**, under §4's *where a task's own proof needs it*: the new `DS-224` verdict fails a deck built before its own fix, and `static_variants.py` refuses to run against a red baseline, so the regression instrument every later batch depends on was down until it landed. B12 still rebuilds them for its own content work. Three looks are now owed ([`OWED-LOOKS.md`](OWED-LOOKS.md)) and all three are answerable |
| **B10** - landed 2026-08-29 | [T-269](../tasks/T-269-three-build-path-defects-the-adopter-worked-around.md), [T-245](../tasks/T-245-seven-tool-defects-in-tools-deck.md) | `s`,`m` | Ten small defects across the build path and the deck tools. Each carries its own reproduction, so the batch is ten independent seeded proofs. **Landed, and it needed a ruling.** Three of the ten proposed remedies were refused by their own measurement: `004`'s separator would have broken every tracked specification, `007` named a path that was already correct, and `PR-42`'s selector fix found a **correctly placed** figure that DS-236 as written could not pass - a rule question, which section 4 does not cover, so it **stopped the batch** and went to the owner. Ruled the same day: a diagram answers to the text column it sits in; DS-236 amended under DS-000 and reversible. **`PR-78`'s wider hypothesis is left open** as a second rule question, one ruling per batch being what section 4 allows. Two gates that had never run a line of their refusal path now do, and [L-145](lessons/L-145.md) is what the batch found twice |
| **B11** | **[T-277](../tasks/T-277-put-motion-back-inside-the-more-menu.md)**, [T-228](../tasks/T-228-the-second-theme-fails-the-contract-it-demonstrates.md), [T-244](../tasks/T-244-the-gates-own-coverage-account.md) | `s`,`s`,`m` | The theme validation step, and deriving the gate's clause-level account. **`T-244` must follow every rule change above** — it derives what the gate decides, and a table derived before the rules settle is derived twice. **`T-277` joins them from §3's reversal, and it goes first**: it amends `DS-218`, so `T-244` cannot derive the account until it has landed, and it changes the chrome tail every deck carries, so it must precede B12's one rebuild. Both ordering rules point the same way |

### Wave 4 — the decks (rebuilt once, after everything above)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B12** | [T-233](../tasks/T-233-a-shipped-deck-carries-eleven-copies-of-one-source.md), [T-248](../tasks/T-248-four-content-errors-in-three-shipped-decks.md), [T-247](../tasks/T-247-the-portfolio-generators-documents-against-the-deck.md), **+[T-275](../tasks/T-275-retire-accent-ink-from-the-contract-the-themes-and-the-decks.md)** | `s`,`m`,`s`,`s` | Every change that invalidates a deck has landed, so the five tracked decks are rebuilt **once** here. Ten dead quick-view payloads removed, four content errors corrected against their source models, and the generator's documents reconciled |
| **B13** | [T-257](../tasks/T-257-ds-218-passes-the-shipped-example-vacuously.md), [T-226](../tasks/T-226-a-shipped-deck-is-in-neither-human-facing-document.md) | `s`·2 | The example's own defects: a rule it passes vacuously, and a deck missing from both human-facing documents. **`T-257`'s question is ruled** — §3 |

### Wave 5 — new capability

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B14** | [T-259](../tasks/T-259-nothing-prints-what-a-slide-actually-contains.md), [T-258](../tasks/T-258-the-gate-passes-copy-its-own-reader-calls-difficult.md) | `m`·2 | Two printers that report rather than gate, built against a tree whose rules have settled. `T-259` first: the fact printer is what a later verdict would rest on |
| **B15** | [T-267](../tasks/T-267-render-py-cannot-capture-a-decks-interactive-states.md), [T-271](../tasks/T-271-a-quick-view-scoped-to-a-document-section.md) | `m`·2 | Interactive capture, and the per-section quick view. **`T-271` stays deferred past the release** by §3's ruling, so B15 is `T-267` alone unless the owner reschedules it |

### Wave 6 — documentation and counts (last, because every figure depends on everything above)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B16** | [T-227](../tasks/T-227-the-front-pages-adoption-route-names-a-variable-the-skill-removed.md), [T-235](../tasks/T-235-the-skills-documents-against-the-tools-they-describe.md) | `s`·2 | What an adopter receives. **`T-235` needs B1** — its proof is vacuous while the scaffold gate reads nothing. `T-227` carries the adopter's launcher record and settles what `$HTMLDECK` resolves to |
| **B17** | [T-234](../tasks/T-234-the-front-pages-own-figures-and-claims.md), [T-236](../tasks/T-236-tier-1-and-the-brief-against-what-they-measure.md), [T-220](../tasks/T-220-derive-the-release-chronologys-task-count-instead-of-typing-it.md) | `s`,`m`,`s` | The front page, tier 1 and the brief — every figure in them re-derived against a tree that has stopped moving |
| **B18** | [T-240](../tasks/T-240-the-evaluation-document-against-itself-and-the-code.md), [T-241](../tasks/T-241-the-design-system-and-the-rationale-against-what-shipped.md) | `m`,`s` | The evaluation and the ruleset's rationale. **`T-241` needs B6** — `PR-97`'s unresolved conflict is `DS-219`'s, and `T-256` is what settles it |
| **B19** | [T-237](../tasks/T-237-the-release-machinery-and-its-record.md), [T-238](../tasks/T-238-the-trackers-own-rules-against-its-own-records.md) | `m`,`s` | The release documents against the releases that ran, and the tracker's own rules |
| **B20** | [T-249](../tasks/T-249-the-two-prior-audits-registers.md), [T-250](../tasks/T-250-two-lessons-state-a-figure-and-two-link-to-a-dead-anchor.md), [T-251](../tasks/T-251-a-research-note-and-a-memory-entry-describe-a-state-that-changed.md), [T-252](../tasks/T-252-the-ignore-rules-come-from-three-files-and-one-ships.md) | `s`·4 | Four small record repairs: the prior audit registers, four lessons, a research note and a memory entry, and the ignore rules |
| **B21** | [T-239](../tasks/T-239-the-audits-own-record-against-what-it-did.md) | `s` | The audit's own plan and ledger, reconciled **after** the remedies exist rather than before — the same reason cycle 41 waits |

### Wave 7 — the batch, and the audit's close

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B22** | [T-253](../tasks/T-253-the-low-findings-batch.md) | `l` | **Last of the remediation.** Forty-nine `Low` findings, many of them in documents waves 4 to 6 rewrite. Running it earlier means fixing a line and then rewriting the paragraph around it |
| **B23** | [T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md) cycle 41 | — | Re-read cycles 1, 3 and 5 plus every cycle a remedy touched. **This is where the audit's own damage shows**, and it cannot run before the remedies exist |
| **B24** | [T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md) cycle 42 | — | Phase 2: predicted against measured, per finding. It has to name at least one prediction the measurement refused, or it was not run honestly |

---

## 3. The eight rulings — answered 2026-08-29, before B1

Six batches carried a question that was the owner's rather than a session's. **All eight are ruled
and none of them stops a batch.** Each was put with its recommendation and the owner took the
recommendation in every case, so the column below is the ruling rather than a proposal.

**One of the eight has since been reversed by the owner** — `T-257`'s, on 2026-08-29, the day it was
made. It is struck through below rather than rewritten, because a ruling that changed is a fact about
this programme and the row is the only place that can carry it. **A ruling is reversible on the owner's
word and this is what that looks like in practice**, so the sentence above — *the owner took the
recommendation in every case* — describes how they were answered, not how they stand.

**Each is reversible on the owner's word, and the task that implements it records it as a `DS-000`
change with the stated reason** — which is the ordinary route for a ruleset change, not an exception
bought by the authority in §5.

| Batch | Task | The question | **Ruled** |
| :--- | :--- | :--- | :--- |
| B5 | `T-264` | A per-deck motion band the theme contract names, or a `DS-010` exemption for a duration inside a `--motion-long` rule? | **The band.** It keeps the value where a generator can find it, which is the argument `DS-013` rests on |
| B6 | `T-256` | Once the ground walk is fixed, does `DS-219` keep its force, or does `DESIGN-RATIONALE.md` §5.7's doubt retire it? | **Fix the walk, keep the rule, re-measure.** The doubt is about over-firing, and a corrected walk is the only thing that can settle whether it still does |
| B6 | `T-260` | Does `DS-244`'s new shape comparison **gate** or **report**? | **Report, calibrate, then decide** — `T-204`'s own precedent, which took text-against-line to report at 16 firings for 1 real defect |
| B8 | `T-265` | Does `DS-110` narrow by where a raster sits? | **The record's weaker form**, not its primary: allow one that is not inside `.body` and carries no `role="img"` naming data |
| B8 | `T-266` | Reserve a deck-local class prefix so a deck can name a repeated figure treatment once? | **Yes.** `DS-229` keeps its real job — stopping a deck redefining a *component* — and stops policing figure internals no contract can anticipate |
| B8 | `T-270` | Accept only the two narrow halves of `DS-100` and `DS-202`, rejecting *make the rule reviewable* and *replace the sentence count*? | **Yes**, for the reasons in `T-225` §3 |
| B13 | `T-257` | Is a control one click inside a shut menu genuinely disqualifying? | ~~**Yes, keep the rule**~~ → **REVERSED 2026-08-29, same day, by the owner: no.** *Motion* goes back inside the menu, and `DS-218`'s placement clause is what gives way. The first answer was taken as a recommendation and the owner has since said it was a misunderstanding of what was being asked — they had wanted the menu form throughout, and read the question as being about the example rather than about the control's home. **The rule's trigger is untouched**: looping motion still ships with a persistent, keyboard-operable stop, and what changes is that a control one click inside a **persistent, keyboard-reachable** menu button counts as reachable. [T-277](../tasks/T-277-put-motion-back-inside-the-more-menu.md) carries it, in **B11**, and the example fix `T-257` still owes is now independent of this question |
| B15 | `T-271` | Build the per-section quick view now, or keep it deferred past the release? | **Keep it deferred.** It is the only record asking for a new component and it competes with nothing else |

### Two more, answered after B7

**The eight above were answered before B1 and none of them stopped a batch.** These two were raised
*by* a batch: [T-242](../tasks/T-242-the-contracts-against-the-checkers-that-decide-them.md) met them
while closing `PR-36` and `PR-77`, deferred both as `DS-000` questions §4's authority does not cover,
and recorded them where the decision would be taken. **That is the escape working rather than
failing** — the batch finished, and the questions reached the owner with their measurements attached.

| Batch | Finding | The question | **Ruled** |
| :--- | :--- | :--- | :--- |
| B9 | `PR-36` | Turn's two dials are read by nothing. Build the card reveal DS-140 names, or retire them and let its starter set lose a name? | **Build it**, [T-274](../tasks/T-274-build-the-card-reveal-so-turns-two-dials-have-a-reader.md). Put with *retire* recommended as the cheaper answer; the owner priced the lost name higher than the build |
| B12 | `PR-77` | `--accent-ink` is four hand-chosen values with no surface. Give it one, or retire the row? | **Retire it**, [T-275](../tasks/T-275-retire-accent-ink-from-the-contract-the-themes-and-the-decks.md). The register asked for this and `PR-36` to be decided together and they were — **answered differently on purpose**: Turn is a named member of a set a rule publishes, and this is a colour role nothing publishes |

**Both are reversible on the owner's word and each is recorded as a `DS-000` change with its stated
reason**, on the same terms as the eight above.

### One more, raised in B8 — a ruling that could not be carried out, and the one that replaced it

**`T-270`'s `DS-100` half is refused by its own measurement.** The ruling above accepts report
[`023`](adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md)'s proposal 1,
whose condition the report states as *a `?` followed, within the slide, by a declarative bottom
line*. Measured on this repository's three decks before a line of it was written: **38 slides, 38
with a bottom line, 38 declarative — the condition holds on 100% of them.** The component contract
puts exactly one `.bottom-line` on every slide and `DS-202` requires it to be one factual sentence,
so the guard is satisfied by construction. It is not a narrowing; it is an off switch, and it would
have taken a `hard` rule to zero findings behind a green verdict — **L-143**, which B6 paid for once
already.

**So the batch implemented `T-270`'s `DS-202` half, refused the `DS-100` half, and put the question
here** — the same escape `PR-36` and `PR-77` used above, and for the same reason: the mechanism is a
new rule question, not a detail of the one ruled.

| Batch | Task | The question | **Ruled** |
| :--- | :--- | :--- | :--- |
| B8 | [`T-270`](../tasks/T-270-two-rules-whose-escape-hatch-teaches-the-wrong-habit.md) | *A question the slide answers* has no checkable form — the one the report offers exempts every slide. What should `DS-100` measure instead? | **Narrow by where the question sits: a `?` in a slide's `<header>` fails, one anywhere else in slide copy passes.** A rhetorical question on a slide is a headline device, which is what the corpus measured; a question inside body copy is one the face is about to answer. It admits both of the adopter's cases and still fails *Why does this matter?* as a headline. **Its stated limit: it cannot be calibrated here.** All three decks carry **zero** `?` in copy, so there is no firing rate to compare — the recommendation rests on the argument, not on a count, and `T-204`'s *report, calibrate, then decide* is the cheaper alternative if that is not enough . **Ruled 2026-08-29: take the recommendation**, [T-276](../tasks/T-276-narrow-ds-100-to-the-question-a-slide-puts-in-its-header.md), landed the same day. The owner read the limit and took it anyway; a question in body copy is now unpoliced and that is the decision |

**Answered 2026-08-29, and the escape hatch is closed.**
[T-276](../tasks/T-276-narrow-ds-100-to-the-question-a-slide-puts-in-its-header.md) implements the
recommendation: a `?` in a slide's `.eyebrow`, `.headline` or `.standfirst` fails, one anywhere else
in the deck's own copy passes. Seeded both ways on `measure-first.html` — headline `1 failure(s)`,
body copy `0 failure(s)`, control green — and no tracked deck's verdict moved. **The limit went to
the owner with the recommendation and was accepted rather than waved past**: there is no firing rate
to calibrate against, so this rests on the argument.

**What the escape from §4 bought, twice over.** `PR-36` and `PR-77` reached the owner with their
measurements and came back as `T-274` and `T-275`. This one reached the owner as a *refusal of a
ruling he had already given*, with the number that refuted it, and came back as `T-276`. A batch
that had implemented the sentence as written would have shipped a `hard` rule that decided
nothing.

---

## 4. What an unattended session may do

Ruled by the owner 2026-08-29, in the same pass as §3. **These are standing authorities for this
programme of work, not general ones**: they are scoped to **the batches in §2 and whatever a ruling in §3 adds to them** — which is three tasks so far, and is why this reads as the schedule rather than as a count — and they expire when B24
closes.

| May | Bound |
| :--- | :--- |
| **Commit and push each batch** | Per task where the task is the unit, and push at the end of the batch — the same shape every audit cycle used |
| **Amend a `DESIGN-SYSTEM.md` rule row** | Only where the task calls for it, with `DS-000`'s stated reason, and marked reversible. §3's eight are already ruled; a *ninth* rule question is not covered and stops the batch |
| **Rebuild and commit the five tracked decks** | They are gated byte-for-byte, so every rebuild is a reviewable diff. Rebuild in B12 where it can be done once; earlier, only where a task's own proof needs it |
| **Absorb what a batch finds** | **A small fix in place is made in place.** Anything with potential impact on other work becomes a task — **and that task is added to the running batch and worked in it**, rather than filed for later. A batch is elastic: it finishes what it started and what it found |

**The one thing a session may not do is look.** `CLAUDE.md` rule 6 is a person, and three of this
audit's findings were passed by every machine and caught by an eye. So:

- a task owing a look does **everything measurable**, records the look as **owed** — naming the deck,
  the slide and what to look for — and **closes**;
- the owed looks accumulate as a queue, **[`OWED-LOOKS.md`](OWED-LOOKS.md)**, and the owner runs
  **one looking pass** over it. *The queue was a sentence here and not a file until 2026-08-29, so
  the record lived in whichever task wrote it and the pass had nothing to run —
  [T-273](../tasks/T-273-the-owed-looks-have-no-queue-to-accumulate-in.md), raised while closing B7
  and worked in it;*
- **that pass happens before the release is cut**, which is what keeps rule 6 true rather than
  merely deferred. B12, B13 and B9 are the batches that will owe most of it.

---

## 5. What this order costs if it is wrong

**The risk is concentrated in wave 2.** If a rule decision in B6 or B8 comes back the other way, the
documents in wave 6 move again — which is the rework this order exists to avoid, arriving through
the one door it cannot close. That is why the questions in §3 are asked before B4 rather than when
each batch reaches them.

**The cheapest thing a reader can do with this file is disbelieve §2's dependencies and check them.**
Three are stated as hard and the rest are economics: `T-235` after `T-231`, `T-243` after `T-254`,
`T-241` after `T-256`. Everything else is *this saves a second pass*, and a session that finds a
better order should take it and say so here.
