---
id: T-068
title: Bind a prose figure to the field that produces it, not to the whole output
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-060]
work_package: PH2
shipped_in: 0.2.0
owner: the project owner
business_value: medium
effort: s
created: 2026-08-10
updated: 2026-08-12
deliverables: [tools/docs/figures.py]
---

# T-068 — Bind a prose figure to the field that produces it, not to the whole output

## 1. Specify

**Outcome**
`figures.py` reports a prose numeral as `compared` only when it matches **the figure it claims to
be**, rather than when it occurs anywhere in the union of the bound commands' output.

**Why this one**
Raised by [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md)'s
review as the gap that task deliberately did not close. The check confirms a numeral **occurs**
somewhere in the corpus. So if the README's *"the judgement half is 25 `hard` rules"* were edited to
say **81**, the run stays green: `81` is in the gate's account as `checked 81`. The number would be
correct, present in the corpus, and describing the wrong thing.

**This is a weaker version of the false pass T-060 already fixed once.** Three prose figures were
matching rule IDs — `163` against `DS-163`, `113` against `DS-113`, `221` against `DS-221` — and were
reported as `compared`. Tightening the word boundary fixed those, and it fixed the *symptom*: the
binding is still numeral-to-corpus rather than numeral-to-field, so a different coincidence produces
the same false pass. **A check that reports a coincidence as a comparison is the failure this
repository treats hardest** (**L-36**, **L-44**).

**Scope**
- In: the prose pass in [`tools/docs/figures.py`](../tools/docs/figures.py) — how a numeral is bound
  to a figure.
- In: whatever the README has to say for that binding to be possible. If a sentence cannot name
  which figure it quotes, that is a finding about the sentence.
- In: **a figure stated in a document `figures.py` does not read** — added 2026-08-10 by the owner,
  rather than raised as a task of its own, because it is the same binding question one scope out.
  The coverage split lived in four documents beside the README (`CLAUDE.md`, `docs/BRIEF.md`,
  `docs/EVALUATION.md`, `skills/htmldeck/references/pipeline.md`) and drifted to three different
  values — 80, 81 and 82 — while the README's own figure stayed bound and correct.
  [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) corrected the identical figure
  in the identical five places once already, by hand, which is the argument for binding it rather
  than sweeping again.
- Out: the fenced-block pass, which is bound by adjacency and is not affected.
- Out: the `volatile` split, settled in T-060 and not reopened here.
- Out: spelled-out numbers, excluded as a class in T-060 with the closing condition stated there.

**Inputs**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `audit`'s prose pass and `EXCLUDED_PROSE`.
- [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md) §4 — the gap as
  the review stated it, and the coincidence that motivated it.
- [`docs/LESSONS.md`](../docs/LESSONS.md) **L-44** — a check that ran, found nothing to look at and
  said `pass`; **L-54** on deriving a fixture's inputs from the thing being modelled.

**Acceptance criteria**
- [ ] A prose numeral moved to a sentence describing a different figure **fails the run**,
      demonstrated on a staled copy — the `25` → `81` case above is the fixture
- [ ] The binding is derived from the document or the command output, not from a hand-kept table of
      which sentence quotes which field (**L-54**)
- [ ] Any sentence that cannot be bound is reported as undeclared rather than passing quietly, so
      the partition still holds
- [ ] No numeral currently reported as `compared` regresses to `excluded` to make the check pass —
      the count of genuinely compared prose figures does not go down

**Open questions**
- ~~**Does the README have to change for this to be possible?**~~ **No — decided 2026-08-10 at
  `specify`**, in favour of the second candidate. Every corpus line is `<label> <value>`, so a
  value's label is the text between it and the previous numeral on its line — `checked`,
  `owned by a gate`, `gated by judgement (judge)`, `examples/reference-deck.html`. A prose numeral
  is `compared` only when its sentence names a distinctive token of that label: *"the judgement half
  is 25 `hard` rules"* binds on `judgement`, *"163 rules, each with a stable `DS-nnn` ID"* on
  `rule`, *"A gate that checks 82 of 113 rules"* on `check` and `gate`. Nothing is marked up and no
  table records which sentence quotes which field — the binding is the document's own words against
  the command's own labels, which is the shape [`bind()`](../tools/docs/figures.py) already uses for
  fences. A prose marker was rejected as noise in a human-facing page; *accept some stay undeclared*
  was rejected because it leaves the page's two live false passes (below) unfixed.

**What the specification found before any code was written**
- **The defect is not hypothetical: `12` is a live false pass, twice.** *"12 slides and a colophon"*
  and *"12 slides, **220 KB**"* are both reported `compared`, because `8-12` occurs in a `DS-082`
  triage note about slide-count bands. The reference deck's slide count is a real figure that **no
  bound command prints**, so this is the T-060 coincidence exactly, still firing.
- **Fixing it by excusing `12` is closed off by the fourth criterion**, correctly. It is fixed by
  `deck_facts()` printing the slide count it already has the file open to count — the figure becomes
  derived rather than excused.
- **The owner's clause needs a live/historical split, and the split is structural rather than
  per-document.** `docs/BRIEF.md` carries the coverage figure as a **live claim** (*"decides 82 of
  the 113 rules"*) and as **dated history** in two struck-through `**done**` rows (*"161 rows were
  163"*, *"113 rules owned, 81 checked and 18 failing"*). Both are correct; a checker that cannot
  tell them apart is wrong on the second every time — the failure `TASK-WORKFLOW.md` §6 records for
  bare paths. **A table row marked `~~…~~ **done YYYY-MM-DD**` is a dated record and is skipped**,
  which is a rule about the row's own shape, not a list of sentences.
  `docs/DESIGN-RATIONALE.md` states its figures as history in ordinary prose (*"took the gate to 78
  of the 111 rules owned at the time"*, *"checked **80 → 81**"*) with no such marker, so it is
  declared out with that reason rather than checked.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **`fields(corpus)`** — one row per numeral in a command's output: value, label (the text back to the previous numeral on that line), and which command printed it. A label with no distinctive token (≥4 letters, not a stopword) makes the field **unbindable**, which is what disqualifies `The 8-`**`12`** | `figures.py` |
| 2 | **`binds(sentence, label)`** — stem-insensitive token test, so `checks`/`checked` and `owns`/`owned` match. Paths in a label split into segments, so `examples/sort-window/sort-window.html` binds a sentence naming `examples/sort-window` | `figures.py` |
| 3 | **Rewrite the prose pass to bind before it compares.** `compared` now carries *which field*, printed in the report; a numeral whose value exists in the corpus but whose sentence names no matching label is `UNDECLARED`, not `compared` | `figures.py` |
| 4 | **`deck_facts()` prints the slide count** of both decks alongside their size, so `12 slides` binds to the deck it describes instead of to a triage note. Counted from the markup, not declared | `figures.py` |
| 5 | **Extend the scan to the declared documents**, each with its reason: the four the owner named plus `examples/README.md`. There the numerals are not a partition — an **anchored** sentence (one numeral bound by label) requires its *other* numerals to be printed by the anchoring command; an unanchored sentence is skipped and counted | `figures.py` |
| 6 | **Skip a `~~…~~ **done YYYY-MM-DD**` table row**, with the reason recorded where the skip happens | `figures.py` |
| 7 | **Two fixtures, both derived** (**L-54**): a compared prose numeral moved onto a sentence that describes a different field must fail; and a numeral in a declared document moved off its command's account must fail | `figures.py` self-test |
| 8 | Run the three gates, then `docs/PUBLISHING.md` §6's figure check over the live page | a green run, or the figures it found |

## 3. Implement

**Decisions & assumptions**
- **The binding is the label the command prints beside the value**, as planned. `fields()` reads
  every numeral in every bound command's output with the text between it and the previous numeral
  on its line; `bound()` reports a match only when the prose sentence names a distinctive word of
  that label. `stem()` takes both sides to the same root, so `checks` reaches `checked` and `gates`
  reaches `gated`.
- **The stem strips a trailing `e` last and unconditionally.** Without it `rules` → `rul` and
  `rule` → `rule` are unequal and `163` regressed to `UNDECLARED` — caught by running the tool, not
  by reading it.
- **`deck_facts()` prints one fact per line.** `231 KB` and `12 slides` on one line would leave the
  second labelled ` KB `, binding nothing. The colophon carries `slide close` and is not counted,
  which is why the page's *"12 slides and a colophon"* is now two checked figures rather than one.
- **The declared-document half was built twice, and the first build is the finding.** Anchoring a
  sentence on any numeral bound by label, then holding the sentence's other numerals to that
  command's account, gave **30 false alarms against 5 true bindings** — on prose about external
  references, inline SVG counts and effect sizes, because `checked`, `owned`, `rules`, `gate`,
  `reference` and `deck` are ordinary English these documents use in their ordinary sense. It was
  replaced rather than tuned.
- **What replaced it binds on the claim's construction**: *part* of *whole*, where the whole is a
  figure a command prints under a label the sentence names, the part must be a figure of that same
  account, and *"the other N"* must be the subtraction. It reaches all five documents, catches the
  drift in every one, and its false-alarm count is zero. Sentences it cannot bind are counted and
  reported as not judged — 419 of them, which is the honest number for pages that are not accounts
  of a run.
- **`EXCLUDED_PROSE` is empty, and was emptied by deriving rather than deleting.** Its last entry
  excused `31` as *"113 − 82, stated as the remainder in the same sentence"*; the claim rule now
  checks that subtraction, so the figure is compared. Its declared closing condition — the gate
  growing a row for the unchecked count — was not needed. Fixture 6 moved onto `EXCLUDED_FENCES`
  to keep the stale-excusal case exercised.
- **`docs/DESIGN-RATIONALE.md` is deliberately not read**, with the reason recorded next to the
  list: it states the account as history in ordinary prose (*"took the gate to 78 of the 111 rules
  owned at the time"*), with no marker separating that from a live claim. A `~~…~~ **done <date>**`
  row **is** such a marker and is skipped, which is what keeps `BRIEF.md` readable — it carries the
  split live in one place and as history in two.

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — the binding, the claim rule, the
  five-document pass, and eight fixtures.

```
  prose figures, and the field each is bound to
    163    'rule rows in the table', printed by python tools/deck/ruleset.py --counts
    82     'checked', printed by python tools/deck/check.py examples/reference-deck.html
    113    'owned by a gate', printed by python tools/deck/check.py examples/reference-deck.html
    31     the remainder, 113 - 82, which this sentence states
    12     'examples/reference-deck.html', printed by the deck files themselves
    231    'examples/reference-deck.html', printed by the deck files themselves
    12     'examples/reference-deck.html', printed by the deck files themselves
    220    'examples/sort-window/sort-window.html', printed by the deck files themselves
    25     'gated by judgement (judge)', printed by python tools/deck/ruleset.py --gates

  prose numerals                the same figures in 5 document(s) that paste no output
    compared       9              compared      10
    total          9              unanchored   419   = in a sentence that names no field
```

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A prose numeral moved to a sentence describing a different figure **fails the run**, demonstrated on a staled copy — the `25` → `81` case is the fixture | **met** | Run as `25` → `82`, the value `checked` carries today: `UNDECLARED  82  no command prints it under a label this sentence names`. The same `82` stays `compared` in the sentence that does name it, which is the discrimination the criterion is about. Fixture 7 derives the swap from the field table rather than naming it |
| The binding is derived from the document or the command output, not from a hand-kept table of which sentence quotes which field (**L-54**) | **met** | Two derived bindings and no table: the label a command prints beside a value, and the *part of whole* construction. What is written down is which five documents are read, with a reason each — the same shape as `EXCLUDED_FENCES` |
| Any sentence that cannot be bound is reported as undeclared rather than passing quietly, so the partition still holds | **met** | The README stays a total partition — 9 of 9 numerals accounted for, an unbound one is `UNDECLARED` and fails. The five other documents are not accounts of a run and are not held to a partition; their 419 unjudged numerals are counted and printed |
| No numeral currently reported as `compared` regresses to `excluded` to make the check pass — the count of genuinely compared prose figures does not go down | **met** | It went **up**, 8 → 9, and the one exclusion was closed rather than added to. Two of the old eight were coincidences: `12`, twice, covered by `8-12` inside a `DS-082` triage note. Both are now bound to the deck they describe |

**What this still cannot see.** A numeral whose sentence names its field's label but quotes a
*different* figure of the same account — *"163 rules"* edited to `164`, which `= rule IDs the
document declares` prints and whose label shares the word `rule`. The claim rule closes this
wherever the sentence states a part of a whole; a bare figure in a sentence naming only its own
label is bound to the label and not to the row. Narrower than what T-060 left, and still there.

**Child fix tasks raised**
- none. The declared-document half landed here rather than becoming a task of its own, which is
  what the owner's clause asked for.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → in_progress → done | Built, and the second half was built twice. Binding a prose numeral to the label its command prints beside it works on the README and closed the two live false passes; the same rule pointed at five documents that paraphrase produced **30 false alarms against 5 true bindings**, because a gate's labels are ordinary English. Rebuilt to bind on the claim's own construction — *part of whole*, plus the remainder — which reaches all five, catches the drift in each, and false-alarms nowhere. `EXCLUDED_PROSE` is now empty: its last entry was derived instead of excused (**L-63**). |
| 2026-08-10 | → specified → planned | Specified and planned in one sitting. The open question is **decided against changing the README**: a value's label is already printed beside it, so the binding is the command's labels against the document's words. Specifying it found the defect **live on the page** — `12` reported `compared` off `8-12` inside a `DS-082` note, twice — which moves this from a false pass needing a second coincidence to one already firing. The owner's clause needed one thing the scope did not anticipate: `BRIEF.md` states the coverage figure **both** live and as dated history, so the live/historical split had to be structural (a `**done**` row is skipped) rather than a choice of which documents to read. |
| 2026-08-10 | → proposed | Raised by [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md)'s review, which closed with this gap named rather than buried. **PH2**: the figures on the published page are correct today and T-060's check keeps the stale-figure class red, so nothing shipped is wrong — this closes a *false pass* that needs a second coincidence to bite. `medium` rather than `high` for that reason, and because T-060 already removed the instance that was actually firing. |
