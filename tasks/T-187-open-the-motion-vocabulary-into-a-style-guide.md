---
id: T-187
title: Open DS-140's closed motion vocabulary into a style guide, keeping the rules that protect behaviour
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-057, T-112, T-016]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-19
updated: 2026-08-22
shipped_in: unreleased
deliverables: [docs/MOTION-GUIDE.md]
---

# T-187 — Open DS-140's closed motion vocabulary into a style guide, keeping the rules that protect behaviour

## 1. Specify

**Outcome**
DS-140 stops being an allow-list. A motion that follows the project's motion principles is
admissible whether or not it carries one of four names, and the four names survive as a **suggested
starter set**. The rules that protect observable behaviour — the duration cap, print, reduced
motion, the stop control — stay `hard` and unchanged. What replaces the closure is a written motion
style guide the critique pass can argue from and a person can extend.

**The owner's ruling, recorded 2026-08-19**
Asked whether the wobble in [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)
is a fifth motion or an exemption, the owner rejected the frame of the question:

> *"Please don't limit the animation to a specific 'allow list'. Any animation, that aligned with the
> rules can be implemented. I prefer a list of suggested animation to add to enrich the document for
> highlighting, or emphasizing content. Some principles, but not complete rules:*
> 1. *Keep animation gentle.*
> 2. *Add significant animation when it is specifically requested.*
> 3. *Ease in/out is the preferred default for almost everything.*
> 4. *Sequence length might default to 300-500ms. It can be longer, if it's for illustration or upon request.*
> 5. *Add 1-1 animation to the content of each page, but if there's no room for that, skip it.*
> 6. *Don't design the page driven by the animation itself, only if its topic is about motion,
>    transition, animation, or specifically requested. Or, later, when the selected theme for the deck
>    is an animation-rich or 3D style.*
> 7. *...and so on. These are not hard rules, more like a style guide. And can be adjusted, refined,
>    extended."*

Put a second time with the blast radius stated, the owner chose **open the list, keep the safety
rules** over opening it fully, over adding a fifth name, and over writing the guide while leaving the
rule contradicting it.

**Two of the six principles are already rules, and that is the finding that makes this tractable**
Principles 3 and 4 restate **DS-141** as amended by T-016 — eased rather than linear, entries and
transitions inside 500 ms. So the guide does not replace DS-141; it agrees with it. What is genuinely
new is principle 6, which no rule states: *the page is not designed around its own animation*.

**The blast radius, measured 2026-08-19**
DS-140's closure is load-bearing for six rules and one self-test. Each has to be re-derived, not
merely re-worded, because each currently reasons *from* the closure:

| Cites the closure | What it reasons from today | What it needs once the list opens |
| :--- | :--- | :--- |
| DS-141 | a duration over 500 ms is admitted only when DS-140 names the motion | a stated exception condition that does not depend on a name |
| DS-146 | a chart draw-in must be Rise, because a stroke-dash draw "would add one to a vocabulary DS-140 fixes at four" | the rule's own reason, restated without the count |
| DS-218 | `Current` is infinite, therefore a stop control | unchanged in force; the trigger becomes *any* looping motion, which it already says |
| DS-221, DS-224 | pin motion off before capture / for print | unchanged; they name DS-140 as the source of looping and of pre-animation state, not as a limit |
| DS-230 | copies DS-140's closure as the precedent for its own closed list of four editorial kinds | **decide explicitly** whether that precedent survives. Opening DS-140 does not open DS-230, and the borrowed argument must not be read as opened by inheritance |
| DS-238 | "DS-140's vocabulary ... binds unchanged at 100" | reworded; density still never admits a non-conformant motion, but conformance stops meaning *named* |
| `audit.py` self-test | asserts the DS-140 row reports a verdict at all — the T-051 fault, absence read as conformance | the row becomes a principles check; the self-test must still fail loudly when it returns nothing |

**Scope**
- In: amending DS-140 from a closed vocabulary to a suggested set plus admission principles, with the
  reason stated per DS-000.
- In: the six dependent rules above, each re-derived rather than patched.
- In: a written motion style guide — the owner's principles, extended where the ruleset already
  implies one, and marked as guidance rather than as gates.
- In: what `check.py` and `audit.py` can still decide once names stop being the test, and saying
  plainly which motion judgements move from `auto` to `judge`.
- In: principle 6 as a new rule or as guidance — argued either way, not assumed.
- Out: **building any new motion.** T-057's 3D visual is the first consumer, not part of this.
- Out: DS-230's editorial vocabulary. It borrowed DS-140's argument; whether it keeps it is a
  decision this task records and does not take on DS-230's behalf.
- Out: the density default. [T-188](T-188-raise-the-shipped-motion-density-default-to-100.md) carries it.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.2 — DS-140, DS-141, DS-146, DS-218, DS-221,
  DS-224, DS-230, DS-237, DS-238.
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §4 — the argument that a named vocabulary
  is what stops animation becoming decoration. **This is the argument being overturned**, so the task
  answers it rather than ignoring it.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8 — what a motion declares to be
  part of the layer rather than beside it.
- [T-016](T-016-the-interaction-and-motion-layer.md) §1 — the exemption case the owner has now
  superseded with a wider ruling.

**Acceptance criteria**
- [ ] DS-140 states a suggested set and an admission test, with DS-000's stated reason, and no
      sentence in the ruleset still asserts a count of four motions.
- [ ] Each of the six dependent rules is re-derived, and the table above is filled in with what each
      became — including DS-230's precedent decided explicitly either way.
- [ ] The motion style guide exists, is reachable from the brief, and is marked guidance.
- [ ] Every rule that protects observable behaviour is still `hard` and still fails a deck that
      breaks it: a proof for each of the 500 ms cap, print, reduced motion, and the stop control,
      run against a seeded defect rather than asserted.
- [ ] `audit.py`'s DS-140 self-test still fails loudly when the row returns nothing.
- [ ] `python tools/check_all.py` green; the rule count in `CLAUDE.md` re-measured rather than
      carried forward.

**Open questions**
- Does DS-230's closed editorial vocabulary keep the argument it borrowed? Owner, once the amended
  DS-140 is written and the borrowing can be read in its new form.

## 2. Plan

**The one design decision the plan rests on.** DS-141's cap is the safety rule the owner kept, and
today it is enforced by a **name**: `ds141_durations` waives the 500 ms cap for a declaration reading
`--pulse-dur` or `--current-dur`. Remove the closure and that waiver has nothing to test, so the cap
either stops being `auto` — a real loss of gate coverage, against acceptance criterion 4 — or it
gets a licence that does not depend on a name.

**The licence is declared, not named:** a rule that starts a motion over the cap declares
**`--motion-long`**, carrying *why*. This is the ruleset's own established idiom — DS-237's
`--motion-kind`, DS-230's `data-disc`, DS-217's `data-scale`: the author states a claim on the
artifact, a checker reads that the claim was made, and a reader judges whether it is true.
`density.py`'s `motion_rules()` already parses per-rule and reads `--motion-kind`, so the parser
exists and is proven.

**The reason values are enumerated, and that is not the closure coming back.** They constrain *why
the cap may be exceeded* — one axis, the one carrying the safety property — and say nothing about
what motions exist. Any motion, named or unnamed, may carry any reason. Enumerating is what keeps
DS-141 in the `auto` column, which is the acceptance criterion.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Amend **DS-140** — suggested starter set plus an admission test, with DS-000's stated reason. No sentence in it asserts a count | `docs/DESIGN-SYSTEM.md` §5.2 |
| 2 | Add the one genuinely new principle as a rule: **the page is not designed around its own animation** (owner's principle 6). Argued as a rule rather than guidance, because it is what replaces the closure in `DESIGN-RATIONALE.md` §4 | new `DS-243`, `hard`/`judge`/`—` |
| 3 | Re-derive **DS-141**: the `--motion-long` licence above, replacing *is one of DS-140's four* | `docs/DESIGN-SYSTEM.md`, `docs/THEME-CONTRACT.md` |
| 4 | Re-derive **DS-146** from its own reason — a stroke-dash draw is animation-led, which is DS-243 — with no count in it | `docs/DESIGN-SYSTEM.md` |
| 5 | Reword **DS-218, DS-221, DS-224, DS-238** so each cites `Current` as an *instance* of looping rather than as the closure that defines it. Force unchanged in all four | `docs/DESIGN-SYSTEM.md` |
| 6 | Decide **DS-230** explicitly and restate its argument in its own terms so it stops borrowing | `docs/DESIGN-SYSTEM.md` |
| 7 | Write the motion style guide — the owner's six principles, extended where the ruleset already implies one, marked guidance, reachable from the brief | `docs/MOTION-GUIDE.md`, `docs/BRIEF.md` |
| 8 | Declare `--motion-long` on the two shipped long motions, and add the contract rows | `shell/components.css`, `docs/COMPONENT-CONTRACT.md` §3.8 |
| 9 | Rewrite `ds141_durations` per-rule against the declared licence; keep `audit.py`'s DS-140 self-test loud; fix every code comment reasoning from the count | `tools/deck/audit.py`, `tools/deck/check.py` |
| 10 | **Prove** the four behaviour rules still fail — seed a defect for the cap, print, reduced motion and the stop control, one run each. Not asserted | evidence in §3 |
| 11 | Re-measure the counts rather than carrying them forward; `python tools/check_all.py` green | `CLAUDE.md`, `README.md`, `docs/BRIEF.md` |

## 3. Implement

**Decisions & assumptions**

- **D1 — the licence is declared, not named.** `--motion-long` on the rule that starts the motion.
  Taken because the alternative loses gate coverage: `ds141_durations` waived the cap for a
  declaration reading `--pulse-dur` or `--current-dur`, so opening DS-140 leaves that waiver with
  nothing to test and drops DS-141 out of the `auto` column. Declaring keeps it `auto` and puts the
  *reason* on the artifact, which the critique pass can disagree with.
- **D2 — the four reason values are closed and the motions are not.** They constrain why the cap may
  be exceeded, not what motions exist. `emphasis` is in the set because Pulse-once ships at 1.2 s and
  a set that excluded it would have failed three decks on the day it landed.
- **D3 — principle 6 became a rule, DS-243, not guidance.** `DESIGN-RATIONALE.md` §4 rests the whole
  motion position on *a named vocabulary is what stops animation becoming decoration*; opening the
  vocabulary leaves that with no answer unless something replaces it, and guidance cannot fail a
  deck. The other five principles went to the guide.
- **D4 — DS-230's closure survives, restated in its own terms. This was §1's open question and it is
  decided here rather than handed back, and it is reversible on the owner's word.** The two rules
  govern different species: DS-140 governs an expressive medium, where a motion nobody has named can
  be a legitimate design act; DS-230's four kinds are a rejection test, and a fifth is a new claim
  about what belongs behind a click rather than a new way of saying something. The owner's
  principles are about animation and say nothing about disclosure.
- **D5 — the three shipped decks were re-synced and the blindness fixture regenerated**, because the
  licence lives in `shell/components.css` and a deck built before it carries none. `shell.py sync
  --write` on each, then `seed_defects.py`, then `--check` clean.
- **D6 — deviation from §1's scope, reported rather than asked.** `skills/htmldeck/references/build.md`
  gained a bullet. Not on the scope list, but the gate now fails a deck for a missing declaration the
  skill never mentioned, and an adopter would meet an error naming a property no document they were
  given describes.
- **D7 — one stale line fixed in passing.** The same file said *at the shipped density of 10*;
  [T-188](T-188-raise-the-shipped-motion-density-default-to-100.md) raised the default to 100 on
  2026-08-20 and left this behind.

**Outputs produced**

- [`docs/MOTION-GUIDE.md`](../docs/MOTION-GUIDE.md) — new, guidance, reachable from
  [`docs/BRIEF.md`](../docs/BRIEF.md)'s document table.
- `docs/DESIGN-SYSTEM.md` — DS-140 opened, DS-243 added, DS-141 and DS-146 re-derived, DS-218,
  DS-221, DS-224, DS-230 and DS-238 reworded.
- `docs/DESIGN-RATIONALE.md` §4 and F-05; `docs/THEME-CONTRACT.md` §4; `docs/COMPONENT-CONTRACT.md`
  §3.8.
- `tools/deck/audit.py` — `ds141_durations` rewritten per rule against the declared licence;
  `tools/deck/check.py` — DS-145's triage wording.
- `shell/components.css` — `--motion-long` on `.current` and `.pulse`; the three decks re-synced.
- `README.md` — the two rule totals re-derived, 175 → 176 rows and 177 declared IDs.

**Evidence — every behaviour rule proven against a seeded defect, none asserted**

| Rule | Seed | Result |
| :--- | :--- | :--- |
| DS-141 cap | `.opening` at 900 ms, no licence | **FAIL** — the gate names the row |
| DS-141 cap | the same, `--motion-long:because` (outside the set) | **FAIL** — a bogus reason is not a licence |
| DS-141 cap | the same, `--motion-long:illustration` | **pass** — the licence works in the other direction |
| DS-143 reduced motion | the `@media (prefers-reduced-motion)` block **and** `deck.js`'s `setMotion(...)` both removed | **FAIL** — 9 still animating, 5 of 5 risen elements hidden |
| DS-218 stop control | the control moved inside `.more-menu` (T-114's failure) | **FAIL** — `persistent: False` while `present: True` |
| DS-224 print | the print rule pinning `.rise` removed | **measured on paper** — see below |
| DS-140 self-test | the row silenced | **exit 1** — *the declaration outlived the row it was written for* |
| DS-140 self-test | the row kept but made to always pass | **exit 1** — *pass against a measurement in which nothing was found* |

**DS-143's first seed passed, and that is a fact about the seed.** Deleting the reduced-motion CSS
block alone changed nothing the check could see, because `shell/deck.js` implements DS-143 a second
time — it calls `setMotion(false)` at load when the preference matches. The deck was still honouring
the preference and the check was right. **L-124** again: seed with the form the artifact contains.

**DS-224 is excused by the gate on a 2026-08-08 owner ruling — *look: a person, rule 6* — so it was
measured rather than gated.** Printed both decks: **14 pages each**, and the printed PDF fell from
**280,010 to 115,938 bytes**. Per page, page 6 carries **703 text characters printed correctly and 46
with the pin removed**. Looked at both renderings offline: the real page 6 is the full comparison
ledger; the seeded one is **blank except the provenance mark**, and still counts as one of fourteen —
which is simultaneously the proof of the rule and the proof that the page count cannot see it.

## 4. Review

**What each dependent rule became** — §1's table, filled in.

| Cites the closure | What it became |
| :--- | :--- |
| DS-141 | The exception is `--motion-long`, declared on the rule, valued from a closed set of four reasons. Still `hard`/`auto`, and the cap is unchanged |
| DS-146 | Re-derived from DS-243: a line drawing itself makes the reader watch the drawing rather than read the shape. Same prohibition, no count |
| DS-218 | Reworded — the trigger is *any* looping motion, and `Current` is named as the instance every deck meets. Force unchanged |
| DS-221 | Reworded the same way; it named DS-140 as the source of looping, not as a limit |
| DS-224 | Reworded — *the deck's own motion*, not *the deck's own motion vocabulary*. Force unchanged |
| DS-230 | **Closure survives**, restated in its own terms and no longer borrowing. D4 above is the argument |
| DS-238 | Reworded — *DS-140's admission test* rather than *DS-140's vocabulary*, and DS-243 added to the list that binds at 100 |
| `audit.py` self-test | Unchanged and still loud. Proven by two mutations, both exit 1 |

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| DS-140 states a suggested set and an admission test, DS-000's reason stated, no sentence in the ruleset asserts a count of four | **met** | `grep` over `docs/`, `tools/`, `shell/`, `skills/`, `README.md`, `CLAUDE.md` returns only research files, one lesson and task records — all dated accounts of a past state, which are records rather than assertions |
| Each of the six dependent rules re-derived; the table filled in; DS-230 decided explicitly | **met** | Table above. DS-230 decided in D4 and written into the rule; **reversible on the owner's word** |
| The motion style guide exists, is reachable from the brief, marked guidance | **met** | [`docs/MOTION-GUIDE.md`](../docs/MOTION-GUIDE.md); linked from `BRIEF.md`'s document table; the first line says it gates nothing |
| Every behaviour rule still `hard` and still fails a seeded defect — the cap, print, reduced motion, the stop control | **met** | §3's evidence table. The cap proven in both directions; print measured on paper because the gate excuses it by ruling, not by oversight |
| `audit.py`'s DS-140 self-test still fails loudly when the row returns nothing | **met** | Two mutations, two different guards, exit 1 each. Note the instrument: the self-test runs under `check.py`, not under `audit.py` directly — the first attempt used the wrong one and reported a false green |
| `python tools/check_all.py` green; the rule count in `CLAUDE.md` re-measured rather than carried forward | **met** | Re-measured: **121 owned by a gate, 91 checked — both unchanged**, because DS-243 is `judge`/`—` and a gate owns neither. So `CLAUDE.md`'s *91 of the 121* stands as written and was not carried forward. The totals that did move are in `README.md` |

**Child fix tasks raised**
- none. Nothing found that this task did not close.

**Kept beyond this task**
- **[L-125](../docs/lessons/L-125.md)** — *before amending a rule, read what its gate actually
  tests.* DS-141's cap was implemented as two token names, so the amendment would have emptied the
  check while every deck went on passing.

**Left for the owner**
- **DS-230's closure was decided here, not by them.** §1 assigned the question to the owner once the
  amended DS-140 could be read. It is decided (D4) so the ruleset does not carry a dangling
  question, and reverting it is one edit to that row.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (no status change) | **`shipped_in` set to `unreleased`, which it should have carried since the day it closed.** It closed 2026-08-21 and `v0.5.1` was tagged 2026-08-20, so this task shipped in nothing and said so by carrying an empty field — the same silence a task still in flight makes. Found while reading the unreleased set for `docs/PUBLISHING.md` §8.1's row, where it matters twice: this is the task that opened DS-140 and replaced DS-141's name-based waiver with `--motion-long`, so a release set missing it understates what an adopter must change. Eight other `done` tasks carry no `shipped_in` and are a different case — all closed 2026-08-19, before the tag — so theirs is a past release's step 8 and is corrected there, not here. |
| 2026-08-21 | → done | Closed in one session, all four phases. **The design decision the whole task turned on was not in §1**: DS-141's cap was enforced by a *name*, so opening DS-140 would have silently dropped the cap out of the `auto` column. Declaring the licence (`--motion-long`) keeps the coverage and puts the reason on the artifact. **DS-230's open question was decided here rather than handed back** — from the rule's own reason, recorded as reversible. Two findings worth more than the task: `deck.js` implements DS-143 a second time, so the obvious seed proved nothing (**L-124** again), and the DS-140 self-test runs under `check.py` and not under `audit.py`, so the first mutation run reported a false green. |
| 2026-08-21 | → planned, → in_progress | Specify was already complete from 2026-08-19. Planned, implemented and reviewed the same day. |
| 2026-08-19 | → proposed | Created from the owner's ruling of the same day, taken while resuming a handoff whose whole purpose was to put four open questions to them. It supersedes T-057's open question rather than answering it: asked to choose between a fifth motion and an exemption, the owner rejected the allow-list itself. Raised as its own task because DS-140's closure is cited by six rules and one self-test, so this is a ruleset change under DS-000 and not an edit to one row. |
