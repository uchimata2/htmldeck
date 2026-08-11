# Critique mode

Load this whenever a review is being written: at pipeline stage 5, at stage 7, and when a user
points at a deck and asks what is wrong with it. It is **one mode over two inputs**, not two modes —
the only difference is whether the artifact is a specification or a rendered deck.

**It reports. It does not fix.** A reviewer that edits its own subject cannot be re-run to prove the
fix landed, and two reports of the same deck stop being comparable. Inside the convergence loop the
fixes belong to the build step, with `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §6.2's ledger
keeping them attributable.

---

## 1. Get the spine before writing a word

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/critique.py <deck> [--sources <dir>]
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
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/critique.py <deck> --worksheet > sheet.txt
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/critique.py --answers sheet.txt
```

25 `hard` rules that no mechanical gate can reach. **One line each: `pass`, `fail` with what and
where, or `excused` with why and what would close the excusal.** A rule in none of those three
states fails the run — `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §1.1, and the tool enforces it.

**An excusal is about the instrument, never the rule.** *"No deck here has an appendix"* is a
reason. *"Hard to judge"* is not, and a `hard` rule that genuinely cannot be judged is a **ruleset
finding to raise**, not a row quietly skipped.

Run it in **one read of the whole deck, before scoring anything** — these are judgements about the
deck a reader actually meets, not twelve separate judgements.

## 3. Two formats

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

## 4. What to look for that no check can

The anti-patterns are `${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md` §6, twelve of them with `X-nn`
IDs, and the dimension anchors are `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §3 and §4. **Read
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

## 5. The four outcomes are not interchangeable

`${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §6.1 owns them; each reports something different.

| Outcome | What the report is |
| :--- | :--- |
| **PASS** | What was fixed, and every remaining `Note`. **A pass is not "no findings".** |
| **CAP** | The remaining findings as *"Open — needs a decision"*. There is no fourth attempt |
| **STALL** | *These are not defects the loop can fix* — almost always design decisions wearing a finding's clothes. Escalate, do not retry |
| **OSCILLATION** | **Stop and name the two rules in tension.** This is a finding about the *ruleset*, and it is recorded in `${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-RATIONALE.md` §2, not papered over with a third fix |

## 6. Voice, and the one number rule

**Blunt, bottom line up front, no diplomatic padding.** No compliment sandwich. Say what is wrong,
where, and what it violates. This is the critique voice and it is deliberate — the harshest review in
the corpus was the most useful artifact in it.

**The deck's own voice is the opposite** and stays respectful, positive and professional. Reviewing
a deck never licenses rewriting it in this register.

**No score reaches the report.** Not a slide total, not a deck total, not a per-dimension number —
`${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §8.2. A dimension at 0 or 1 reaches the reader as **a
finding naming the dimension**. The numbers imply a precision the rubric does not have, and a visible
number invites fixes aimed at the number.
