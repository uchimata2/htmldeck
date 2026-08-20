# Critique mode

> **`$HTMLDECK` is the plugin's own directory.** Resolve it once as `SKILL.md` §0 says, and substitute the printed path into every command below. It is not an environment variable and nothing exports it.

Load this whenever a review is being written: at pipeline stage 5, at stage 7, and when a user
points at a deck and asks what is wrong with it. It is **one mode over two inputs**, not two modes —
the only difference is whether the artifact is a specification or a rendered deck.

**It reports. It does not fix.** A reviewer that edits its own subject cannot be re-run to prove the
fix landed, and two reports of the same deck stop being comparable. Inside the convergence loop the
fixes belong to the build step, with `$HTMLDECK/docs/EVALUATION.md` §6.2's ledger
keeping them attributable.

---

## 1. Get the spine before writing a word

```
python $HTMLDECK/tools/deck/critique.py <deck> [--sources <dir>]
```

That prints which passes ran, **what the gate already decided**, the figure ledger, and the list of
things no check in the repository reaches. Three things follow from reading it first:

- **Never re-find a mechanical failure.** If `check.py` says DS-035 failed, cite it in one line and
  move on. A review that re-derives the gate is padding, and the reader stops before the part that
  is worth their time.
- **The review is what the spine says nobody has decided** — S1 Claim, S2 Evidence, S4 Density,
  D1 Spine, D4 Consistency, and the 25 `hard` rules on the worksheet.
- **Say which half ran.** If no sources were supplied the run is presentation-only, and that goes in
  the report. A presentation-only check presented as a clean pass is a false one.

**`FIG-4` is a reading list, not a verdict.** It pairs two sources answering one question with two
numbers, and it cannot tell a real contradiction from a qualified pair — *peak* and *off-peak* are
contrastive, which is semantics rather than counting. Read every pair it prints and decide; a clean
corpus produced ten false candidates in the one place this was measured, so finding them false is
the normal outcome, not evidence the pass is broken.

## 2. The hard-judge checklist is not optional

```
python $HTMLDECK/tools/deck/critique.py <deck> --worksheet > sheet.txt
python $HTMLDECK/tools/deck/critique.py --answers sheet.txt
```

26 `hard` rules that no mechanical gate can reach. **One line each: `pass`, `fail` with what and
where, or `excused` with why and what would close the excusal.** A rule in none of those three
states fails the run — `$HTMLDECK/docs/EVALUATION.md` §1.1, and the tool enforces it.

**An excusal is about the instrument, never the rule.** *"No deck here has an appendix"* is a
reason. *"Hard to judge"* is not, and a `hard` rule that genuinely cannot be judged is a **ruleset
finding to raise**, not a row quietly skipped.

Run it in **one read of the whole deck, before scoring anything** — these are judgements about the
deck a reader actually meets, not twelve separate judgements.

## 3. Three formats

### 3.1 Specification review — stage 5, before any HTML exists

**In:** `<slug>.slides.md`. **Out:** findings, then open decisions, then counts.

| Column | |
| :--- | :--- |
| `ID` | Sequential within the report — `SR-01`, `SR-02` |
| `Severity` | **Major** · **Minor** · **Note** |
| `Slide` | The number, or `deck` for a whole-deck finding |
| `Finding` | What is wrong, naming the rule or anti-pattern it violates |
| `Fix` | What to do. One line. Not applied here |

Then **"Open — needs a decision"**, then the counts by severity.

**It scores what a specification can carry** — S1 Claim, S2 Evidence, D1 Spine, D2 Pacing, D3 Close,
and D4's source-reconciliation half. It does not touch S3 Encoding, S4 Density, S5 Craft, S6 Motion
or D4's visual half: those need a rendered artifact and belong to the build review.

**Do not guess an open question closed.** An unresolved item recorded as resolved is the defect that
section exists to prevent.

### 3.2 Design audit — stage 7, and whenever a user points at a deck

1. **The verdict, first, in two or three sentences.** What this deck is, whether it works, and the
   single thing most worth changing. A review that opens with three compliments is one nobody acts
   on.
2. **The coverage table** — which passes ran, and what each did not reach. Straight from the spine.
3. **The findings**, ordered by severity, each naming the `DS-nnn` rule or `X-nn` anti-pattern it
   violates and the slide it is on. **No general advice.** *"Slide 6 tightens the type"* is a
   finding; *"consider improving the typography"* is not.
4. **An explicit keep-versus-rebuild split.** Which slides stand, which need work, which should not
   exist. This is the part a reader acts on, and leaving it implicit is how a review becomes a list
   of complaints.

### 3.3 Specification conformance — the deck against the specification that briefed it

**Runs only when a specification is supplied**, and it takes two inputs where every other pass takes
one. With no specification, say the step was skipped and that a deck can arrive without one; do not
infer a specification from the deck, which would compare the deck against itself.

A specification is **a plan being read as a description**. Every sentence asserting a property of
the built deck — *spans the full width*, *three figures at display weight*, *the diagram occupies
the upper two thirds* — was written before the artifact existed. Nothing downstream of a false one
breaks, so nothing catches it: the claim that found this rule survived a build, four gates, a
render, a presentation, and two readings of the markup (DS-234).

Go **claim by claim** through each slide's `Structure` and `Visuals` fields, and for each one report
the slide, the sentence, what the deck does, and **which of the two things to repair**. Both repairs
are live. The claim that found this rule is *fix the specification*: the deck is right and a review
that assumed otherwise would have argued for removing a measure doing its job.

**The calibration, which is the whole of the technique.** Judge a size claim against **the container
the element sits in**, never against the stage. The content column is the stage less its horizontal
padding, and every full-bleed element fills that column exactly — so a diagram measuring 90% of the
stage is at full width, not short of it. Measured on both shipped decks 2026-08-18: judged against
the stage, *full width* reads false three times and is truly false once. **Two false alarms against
one hit** is why this pass is judgement and no checker ships for it.

**The one shape that is decidable without looking**, and worth knowing by heart: an element the
theme caps *below* its container cannot fill it, on any slide of any deck. `.bottom-line` is the
case — `max-width:var(--bottom-measure)` at 1500 du inside a 1726 du column — so *the bottom line
spans the full width* is false wherever it appears, and it is false in the shipped
`measure-first` specification. Any other claim of this shape is a token comparison and needs no
render either.

Everything else here is judgement, and the fractional claims are the trap: *upper two thirds* against
a diagram filling 83% of its container is an approximation a reader accepts and a checker would
flag. Report a fraction only when the deck contradicts the claim's **intent** — the diagram is not
where the sentence puts it, or the thing beneath it is not beneath it.

## 4. What to look for that no check can

The anti-patterns are `$HTMLDECK/docs/DESIGN-SYSTEM.md` §6, twelve of them with `X-nn`
IDs, and the dimension anchors are `$HTMLDECK/docs/EVALUATION.md` §3 and §4. **Read
them; do not restate them here or in the report.** A finding cites the ID.

Two tests worth running by hand because nothing else does:

- **Close every panel and read the deck.** If a slide stops making its argument, the tier split is
  wrong — that is X-09, and it is the failure progressive disclosure is most prone to.
- **Read the bottom lines alone, in order.** They should be the argument. If they read as a list of
  topics, D1 Spine is the finding, whatever the slides look like.
- **Open every quick view and ask what form the source was available in.** DS-110 lets a quick view
  quote a raster because a screenshot is often the only form a source has — and it says the builder
  takes the vector form wherever the source offers one. **No check can see that**: the gate reads the
  deck and cannot know what sat beside the source on disk. A quick view showing a screenshot of a
  document that exists as text is a DS-110 finding, and this is the only pass that can raise it.
- **List the treatments used on one slide only, then read each one in the reading view.** That is
  DS-233, and the listing is arithmetic even though the verdict is not: take every modifier class
  (`block--modifier`) on the stage, keep the ones appearing on a single slide, and **drop the ones
  whose base component appears three or more times on that slide** — those contrast with siblings
  that travel with them when `buildDoc()` clones the slide. What is left borrows its meaning from
  the *other* slides, and the reading view is one continuous column where those neighbours are gone.
  Ask of each: does it still say the same thing? On the three shipped decks that leaves **one
  treatment per deck** and no false alarms, so this costs a minute and is not a nag.

## 5. The four outcomes are not interchangeable

`$HTMLDECK/docs/EVALUATION.md` §6.1 owns them; each reports something different.

| Outcome | What the report is |
| :--- | :--- |
| **PASS** | What was fixed, and every remaining `Note`. **A pass is not "no findings".** |
| **CAP** | The remaining findings as *"Open — needs a decision"*. There is no fourth attempt |
| **STALL** | *These are not defects the loop can fix* — almost always design decisions wearing a finding's clothes. Escalate, do not retry |
| **OSCILLATION** | **Stop and name the two rules in tension.** This is a finding about the *ruleset*, and it is recorded in `$HTMLDECK/docs/DESIGN-RATIONALE.md` §2, not papered over with a third fix |

## 6. Voice, and the one number rule

**Blunt, bottom line up front, no diplomatic padding.** No compliment sandwich. Say what is wrong,
where, and what it violates. This is the critique voice and it is deliberate — the harshest review in
the corpus was the most useful artifact in it.

**The deck's own voice is the opposite** and stays respectful, positive and professional. Reviewing
a deck never licenses rewriting it in this register.

**No score reaches the report.** Not a slide total, not a deck total, not a per-dimension number —
`$HTMLDECK/docs/EVALUATION.md` §8.2. A dimension at 0 or 1 reaches the reader as **a
finding naming the dimension**. The numbers imply a precision the rubric does not have, and a visible
number invites fixes aimed at the number.
