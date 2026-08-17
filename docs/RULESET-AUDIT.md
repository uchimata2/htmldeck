# htmldeck — the ruleset audit

**Every rule in [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) tested against one question: does satisfying
it make a deck better, or only different?** Run 2026-08-17 by
[T-119](../tasks/T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md). Tier 3 —
loaded by nothing, read when someone asks whether a rule was ever examined.

**This is a dated snapshot and it does not update itself.** The ID, Label and Check/Reach columns
were read out of `DESIGN-SYSTEM.md` when it ran, so they cannot be mistyped; the three verdicts are
this audit's judgement and live here only. A rule amended after 2026-08-17 has a verdict about the
wording it used to carry. **What changed as a result is [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md)
§6** — this file is the examination, that one is the record.

---

## 1. The result

**165 rules examined. 161 left exactly as they were.** That figure is the audit's
main product and it is stated first on purpose: an audited ruleset is one a later reader can trust,
and the value of examining a rule that survives is the same as the value of removing one that does
not.

**4 rules changed. Nothing was deleted.** **16 rules failed a test**, and the two
numbers are different on purpose: 13 of those failures are rules with no instrument, and the
fix was to give them one rather than to touch the rule. *A rule that fails a test is not a rule that
has to move* — reading those two counts as one is the mistake this table exists to stop, and it was
the generator's own first defect.

| Rule | Test it failed | What was done |
| :--- | :--- | :--- |
| **DS-042** | 2 — effect | **Reclassified `auto`/`never` → `judge`/`—`.** It is the ruleset's only `Reach: never`: a `hard` rule handed to the gate that no program can ever decide, so in the whole life of this project it has not fired once and could not have. `judge` puts it on EVALUATION.md §1.1's hard-judge checklist, where a person decides it — an instrument, not a demotion |
| **DS-041** | 3 — scope | **Split.** *Align by construction, not by coordinates* is a technique a check can see. *Correlated rows share a grid track* is a reading of the content — the same limit as DS-042, and now the same home. The gate keeps the half it can decide |
| **DS-138** | 3 — scope | **Narrowed to tier two.** The reason is that content a reader is reading must fit on the stage; the wording said *any popover*, which is how it blocked a two-item chrome menu sitting where *below* is the one direction with no room. The general obligation is stated so nothing is lost. **Extended 2026-08-18 by [T-114](../tasks/T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md)**, which checked the new boundary before spending it: tier two alone released the multi-source mark's direction as well, which this narrowing's own test said it must not, so the direction clause names the provenance box beside tier two |
| **DS-007** | 3 — filing | **Moved to §8.** It binds whoever is debugging, which is the class §8 declares and holds; filed under *Portability* it read as something a deck must satisfy. §8 said four such rules and had five |

**13 rules had no instrument at all, and that is the finding worth the audit.** Not gated,
not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill:

> **DS-022** · **DS-025** · **DS-029** · **DS-038** · **DS-083** · **DS-094** · **DS-095** · **DS-096** · **DS-098** · **DS-169** · **DS-170** · **DS-206** · **DS-213**

None of them is wrong. Every one is a real preference this project holds, written down, and then
never applied by anything — because a rule is applied by an instrument and none of these has one.
**They were fixed by naming them, not by deleting them**: five small edits to
[`EVALUATION.md`](EVALUATION.md) and the build pipeline put all 13 in reach of the scoring
pass. §1's rule for a test-2 failure is *given an instrument or demoted to `guidance`*, and an
instrument was available for every one, so nothing was demoted.

> **The thirteen are the finding and they are stated, not recomputed.** Re-running the search after
> the fix returns nothing, so a live count would report its own remedy and lose what the audit was
> for. It was re-run once the edits landed, on 2026-08-17: **still uninstrumented, 0** —
> none — every one of the thirteen is named by a dimension or by the pipeline. **Anyone can re-run it**, and it is one expression rather than a tool: the `judge`
> rules in `DESIGN-SYSTEM.md`, less the `hard` ones (§1.1's checklist has those), less every id
> named or ranged in `EVALUATION.md`, less every id named under `skills/`. A non-empty answer is a
> rule nothing applies.

**How they got there is a mechanism, not carelessness.** The rubric names its rules in ranges —
`DS-034 to DS-037`, `DS-041 to DS-049`, `DS-140 to DS-150` — and a range has two ends. DS-038, DS-039
and DS-040 sit in the gap between the first two; DS-039 and DS-040 are gated so nothing was lost, and
DS-038 is `judge` and fell straight through. **A rule becomes invisible by being numbered between two
ranges**, which no reading of any single rule can catch.

---

## 2. The dead-legislation claim did not survive

T-119 was raised on three kinds of evidence, and the first named **DS-146** and **DS-147** as rules
governing a component that does not exist, on this probe:

```
grep -c -i "chart" shell/components.css   →  0
```

The count is right and it settles nothing. **Both rules govern behaviour, and behaviour is not in the
stylesheet.** `shell/deck.js:410` carries DS-146 by name; `shell/deck.js:825` is DS-147's `countUp()`;
both ship in all three decks. The subject is there too — `examples/reference-deck.html` holds a
hand-authored line chart, `<polyline>` twice under an `aria-label` naming it, which is what
**DS-122** requires a chart to be. *No chart library. Hand-written SVG.* So the probe searched the
stylesheet for a component the ruleset forbids anyone to write.

**The class survives; both of its instances do not.** What the audit takes from it is a constraint on
its own method, carried into test 1 below: **probe the mechanism the rule names, never a name that
sounds like the rule.**

---

## 3. The three tests, and what each could actually decide

| Test | The question | What decided it | Its ceiling |
| :--- | :--- | :--- | :--- |
| **1 Subject** | Could anything a deck may contain fall under it? | The rule's own verb, probed in the file that implements it | *Possible*, not *present* — a prohibition is satisfied vacuously by every conforming deck, and that is the rule working. A low bar, and every rule cleared it |
| **2 Effect** | Has any instrument ever been able to apply it? | The gate's live coverage account, the hard-judge checklist, every rubric dimension, and every rule id the skills name | It cannot tell a gated rule that has **caught** something from one that has always passed. The gate reports today's verdict, not its history |
| **3 Scope fit** | Does the wording reach exactly as far as its reason? | The rule text against its stated reason | Judgement, and the expensive one. It is the test that found three of the four changes |

**Test 2's ceiling is stated rather than worked around.** `examples/reference-deck-seeded-defects.html`
seeds **five** defects — DS-035, DS-075, DS-141, DS-142, DS-229 — so it proves five rules can fail and
is silent on the other 110 the gate owns. Manufacturing a defect per rule is a larger task than this
one and it is [T-054](../tasks/T-054-record-which-clauses-of-a-rule-the-gate-decides.md)'s
neighbourhood. **29 rules are recorded `unverified`**, which §1 rules is the correct
outcome and not a gap: *a rule that has never fired is unverified, not proven*. 27 of them
the gate owns and excuses on every deck built here, each excusal stating its own closing condition in
`check.py`; the rest are `off-gate` in the ruleset itself — DS-072, DS-210 and DS-211, where the
instrument is wrong rather than absent, since a headless run has no fullscreen gesture and the gate
is handed one HTML file with no outline beside it.

---

## 4. What was examined and left alone

Two findings are recorded here and deliberately **not** acted on. Both are the audit's own cost test
turned on itself.

**DS-115** — *particles, connectors and custom diagrams may be drawn freely in SVG or canvas* — is a
permission, and a permission cannot be violated. DS-111 already carries it. It was **not** merged:
the ID column promises that a retired rule keeps its number and is marked retired, `ruleset.py` has
no notion of a retired row and would keep counting it, so the merge costs a tooling convention and
returns one `guidance` row.

**The count itself is not the problem.** §1 asked whether 165 rules is too many to hold, and
whether merging near-duplicates beats deleting weak ones. The near-duplicates are real — DS-046,
DS-048, DS-101 and DS-209 all say *one emphasis, not three*, at four scales — but they are cheap
(`judge` or excused), each is cited from somewhere, and DS-209 states its relationship to DS-101 in
its own text rather than hiding it. **A ruleset that says the same thing at four scales and admits
it is not the failure mode this audit was looking for.** The failure mode was a rule nothing could
ever apply, and that was 13 rules and DS-042.

---

## 5. Every rule, with its verdict

**Reading the table.** `Check/Reach` is the pair read from `DESIGN-SYSTEM.md` **as it stands after
this audit** — so for the four changed rules it shows the new value and the reason names the old one.
That is the one column that stays true if the file is regenerated, which is why it is the current
value rather than a pinned historical one. The three verdicts are
**1 Subject · 2 Effect · 3 Scope**. `pass` means the test was applied and the rule cleared it;
`unverified` means no instrument has ever seen it fire; `FAIL`, `NARROW` and `RECLASSIFY` are the
verdicts that produced a change; `noted` is a finding recorded and not acted on. The reason column
carries the one that decided the row. **A ·  after the ID marks a rule this audit changed.**

| ID | Label | Check/Reach | 1 | 2 | 3 | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-001** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-002** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-003** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-004** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-005** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-006** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-007** **·** | guidance | —/— | pass | n/a | noted | the wording fits its reason; the **filing** does not. It binds whoever is debugging, which is §8's declared class, and it sits in §1.1 Portability implying a deck must satisfy it. **Moved to §8** |
| **DS-008** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-009** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-010** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-011** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-012** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-013** | default | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-020** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-021** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-022** | guidance | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-023** | default | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-024** | default | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-025** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-026** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-027** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-028** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-029** | guidance | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-030** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-031** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-032** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-033** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-034** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-035** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-036** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-037** | default | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-038** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-039** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-040** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-041** **·** | hard | render/yes | pass | unverified | NARROW | two clauses at different reaches. *Align by construction* is a technique a check can see; *correlated rows share a track* is a reading of the content, which is DS-042's limit and DS-042's classification. `check.py`'s own deferral asks for exactly this review by name. **Split: the gate keeps the technique, the reading goes to DS-042** |
| **DS-042** **·** | hard | judge/— | pass | FAIL | RECLASSIFY | *which boxes read as a set is a reading of the content* is the definition of `judge`, not of `auto`. **`judge` / `—`**, which hands it to the hard-judge checklist — the first instrument it has ever had |
| **DS-043** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-044** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-045** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-046** | default | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-047** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-048** | default | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-049** | default | auto/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-050** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-060** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-061** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-062** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-063** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-064** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-065** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-070** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-071** | default | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-072** | hard | render/off-gate | pass | unverified | pass | `off-gate` — decidable in principle but not by this instrument, which is a named gap someone may close rather than a failure |
| **DS-073** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-074** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-075** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-076** | default | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-080** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-081** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-082** | default | auto/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-083** | guidance | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-084** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-085** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-086** | default | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-087** | default | auto/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-088** | default | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-090** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-091** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-092** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-093** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-094** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-095** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-096** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-097** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-098** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-099** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-100** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-101** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-102** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-103** | default | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-104** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-105** | default | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-106** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-107** | hard | —/— | pass | n/a | pass | it constrains a check rather than a deck, so *firing* is not a thing it does |
| **DS-110** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-111** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-112** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-113** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-114** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-115** | guidance | —/— | pass | n/a | noted | *may be drawn freely in SVG or canvas* is a permission, and a permission cannot be violated. DS-111 already carries it. **Not merged**: retiring a row needs a convention `ruleset.py` does not implement, and the return is one `guidance` row — the audit's own cost test, applied to the audit |
| **DS-116** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-117** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-118** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-119** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-120** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-121** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-122** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-123** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-130** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-131** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-132** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-133** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-134** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-135** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-136** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-137** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-138** **·** | hard | render/yes | pass | pass | NARROW | the reason is that tier-two content a reader is reading must fit on the stage; the scope is *any popover at all*, so it reached a two-item chrome menu at the foot of the stage, where below is the one direction with no room. **Bound to tier two, with the fits-on-the-stage obligation stated generally so nothing is lost**. **Extended 2026-08-18 by [T-114](../tasks/T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md)** to name the multi-source provenance box beside tier two — binding the direction to tier two alone released the mark, which the narrowing's own boundary forbade |
| **DS-139** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-140** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-141** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-142** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-143** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-144** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-145** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-146** | hard | render/yes | pass | pass | pass | **the withdrawn dead-legislation instance.** `shell/deck.js:410` carries it by name and `examples/reference-deck.html` holds a real hand-authored line chart |
| **DS-147** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-148** | default | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-149** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-150** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-160** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-161** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-162** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-163** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-164** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-165** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-166** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-167** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-168** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-169** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-170** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-190** | hard | —/— | pass | n/a | pass | it constrains a check rather than a deck, so *firing* is not a thing it does |
| **DS-191** | hard | —/— | pass | n/a | pass | it constrains a check rather than a deck, so *firing* is not a thing it does |
| **DS-200** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-201** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-202** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-203** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-204** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-205** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-206** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-207** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-208** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-209** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-210** | hard | auto/off-gate | pass | unverified | pass | `off-gate` — decidable in principle but not by this instrument, which is a named gap someone may close rather than a failure |
| **DS-211** | hard | auto/off-gate | pass | unverified | pass | `off-gate` — decidable in principle but not by this instrument, which is a named gap someone may close rather than a failure |
| **DS-212** | default | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-213** | default | judge/— | pass | FAIL | pass | no instrument: not gated, not `hard` so not on the hard-judge checklist, named by no rubric dimension and by no skill |
| **DS-214** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-215** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-216** | default | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-217** | default | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-218** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-219** | hard | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-220** | hard | —/— | pass | n/a | pass | it constrains a check rather than a deck, so *firing* is not a thing it does |
| **DS-221** | hard | —/— | pass | n/a | pass | it constrains a check rather than a deck, so *firing* is not a thing it does |
| **DS-222** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-223** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-224** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-225** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-226** | hard | render/yes | pass | unverified | pass | owned by the gate and excused on every deck built here; the excusal states its own closing condition |
| **DS-227** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-228** | default | render/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-229** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-230** | hard | judge/— | pass | pass | pass | a deck may contain the thing it governs, and the shipped decks do |
| **DS-231** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |
| **DS-232** | hard | auto/yes | pass | pass | pass | the gate decided it on a shipped deck, so a subject was there to decide |

---

## 6. What this audit could not do

**It did not look at a deck.** Every verdict above is about a rule's text, its classification and its
instrument. Whether the ruleset as a whole produces a *good* deck is `CLAUDE.md` rule 6's question and
it is answered by rendering one and looking at it, which nothing here replaces.

**It did not test a rule by removing it.** The acceptance criterion asks that any rule whose removal
changes a deck be reported as evidence the removal was wrong. Nothing was removed, so the check ran
in the only form left to it: the three shipped decks were re-gated after the four changes, and none
of them changed verdict.

**It has one instrument's blind spot.** Test 2 asks whether a rule has an instrument, and the way it
asks is by searching the instruments for the rule's id. A rule applied by an instrument that never
names it would read as an orphan, and a rule named in a document nobody runs would read as
instrumented. The 13 were each read individually against the rubric's dimensions before
being called orphans; the 161 that passed were not.
