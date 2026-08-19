#!/usr/bin/env python3
"""The build check — the gate a deck must pass, and the account of what it did not check.

One library, two entry points: `run()` for the pipeline (per batch and whole-deck) and this file
as a command taking any HTML file. Both go through `run()`, so the standalone half cannot drift
from the one the pipeline calls.

**The account is the part that matters.** A gate that checks 44 of 111 rules and says nothing about
the other 67 is making a claim about the deck it has not earned, and this project has already
shipped that failure twice (**L-36**): five rules labelled `auto` and `render` with nothing behind
them, and a reference deck carrying a bottom line on none of its twelve slides while a 43-check run
reported zero failures. So every rule the ruleset puts in a gate's jurisdiction ends each run in
exactly one of three states — **checked**, **excused in writing**, or **failing** — and a rule in
none of them **fails the run**. Adding a rule to `DESIGN-SYSTEM.md` with no implementation is
therefore not something to notice later; it is a red run the same afternoon.

The jurisdiction is derived from the ruleset every time (`ruleset.py`), never kept here as a list.
A stored copy of a derivable fact drifts on the first amendment (**L-08**).

    python tools/deck/check.py examples/reference-deck.html
    python tools/deck/check.py deck.html --sources notes/          # adds the content half
    python tools/deck/check.py deck.html --print-pages             # adds the printed page count
    python tools/deck/check.py deck.html --json                    # the report T-004 consumes
    python tools/deck/check.py deck.html --quiet                   # a passing run in one line

**`--quiet` is for the caller who cannot read 169 lines, and it changes no verdict.** A green run
prints its notes and one summary line - 345 bytes against 17,581 - and a run that is not green
prints everything, because the output of a failure is the reason to have run it. The default is
unchanged: a person reading the per-rule listing is why the listing exists. `check_all.py` makes the
same choice one altitude up, with the polarity that suits who calls it (`CE-03`, T-132).

Pure standard library (**L-07**), real Chrome offline through `render.py`.
"""

import inspect
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                       # noqa: E402
import ruleset                                                      # noqa: E402
import audit                                                        # noqa: E402
import contrast                                                     # noqa: E402
import contract                                                     # noqa: E402
import content                                                      # noqa: E402
import printpages                                                   # noqa: E402
import printgeom                                                    # noqa: E402
import figgrid                                                      # noqa: E402
import density                                                      # noqa: E402
import theme                                                        # noqa: E402
import component                                                    # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT

# --------------------------------------------------------------------------- the excusals
# **A rule leaves the silent list by being checked or by being excused in writing, and by no third
# route.** That line is the owner's, 2026-08-08, and it is written as a rule because it is where
# this task's scope was expected to drift.
#
# Each entry is one rule, one reason, and **what would close it** — an excusal is a candidate task,
# never a shrug. The reasons here are facts about THIS INSTRUMENT. Facts about the rule itself live
# in the ruleset's `Reach` column, which this file reads rather than restates; a rule the ruleset
# already excuses never reaches this table.
DEFERRED = {
    # ---- the rule's subject is a reading of the content, not a fact the file records
    "DS-041": ("Which rows are *correlated* is a reading of the content. The DOM records the "
               "tracks; it does not record which values a reader expects to line up, so a grid "
               "can misalign and absolute coordinates can land true. **That review happened "
               "(T-119, 2026-08-17) and it moved the line rather than the rule's `Reach`**: the "
               "reading half is DS-042's, which is `judge` now, and DS-041 keeps the half a check "
               "can see - alignment produced by a shared grid or flex track rather than by "
               "absolute offsets. There is no `Reach: never` in the ruleset to cite any more. "
               "CLOSES WHEN: this gate measures the narrowed clause, which is a check to write "
               "and not a ruleset question.",
               ("amendment", "DS-041")),
    "DS-101": ("Bold in a data table is the value, not emphasis. The reference deck's A-04 ledger "
               "carries twelve bold runs and conforms; any count threshold either forbids the "
               "archetype or is set high enough to check nothing. CLOSES WHEN: the rule exempts "
               "tabular values, or the markup distinguishes emphasis from value. Measured: "
               "`data['boldRuns']`.",
               ("amendment", "DS-101")),
    "DS-209": ("Same subject as DS-101 one altitude up, and the same obstacle: separating the one "
               "emphasis from a row of bold figures is a reading. Measured and reported: "
               "`data['emphasisOutsideBottomLine']`.",
               ("amendment", "DS-209")),
    "DS-117": ("*Labelled* is a spatial-association judgement and the rule gives no distance. "
               "Measured on one conforming deck the connector-to-nearest-label gaps run 18, 32, "
               "56, 86 and 139 design units, so any threshold would be a number invented to fit "
               "this deck (**L-38**). CLOSES WHEN: connectors carry a structural association - an "
               "`aria-describedby`, a `<title>`, a shared group - which is a rule amendment.",
               ("amendment", "DS-117")),
    "DS-026": ("The rule requires a *visible* legend and nothing in the DOM declares one. The "
               "tripwire slide draws its legend as two SVG swatches with labels and no marker, so "
               "a class-based check reports it missing; the check exists and finds 1 of 2. CLOSES "
               "WHEN: DS-026 requires a legend to be identifiable, which would serve a screen "
               "reader too - but adopting it to make a check work is backwards, so it is the "
               "owner's.",
               ("amendment", "DS-026")),
    "DS-120": ("An accumulation effect is not a marked construct: nothing in the DOM says *this is "
               "meant to accumulate*, so the gate cannot find the rule's subject before judging "
               "it. CLOSES WHEN: a person watches the effect, which is CLAUDE.md rule 6 anyway.",
               ("look", None)),
    "DS-149": ("The defect is a z-order outcome and the rule names its cause. Observing it needs "
               "two elements that overlap and the wrong one winning, which the gate cannot "
               "construct from an arbitrary deck. CLOSES WHEN: looked at, or when a deck ships an "
               "overlap the gate can be pointed at.",
               ("look", None)),

    # ---- built elsewhere, or waiting on a task that owns the subject
    # DS-143's excusal was CLOSED by T-016 (2026-08-09): `audit.reduced_motion_data` takes the
    # second render this entry called for, and `reduced_verdicts` reports three rows from it.
    # Kept as a comment rather than deleted, because the entry named its own closing condition and
    # a reader should be able to see that the condition is what happened.
    "DS-222": ("The owner ruled the print row automates the PAGE COUNT and nothing else "
               "(2026-08-08), and narrowed that on 2026-08-13 to admit printed GEOMETRY as well - "
               "a collision is arithmetic rather than a judgement (T-123). DS-222 to DS-225 are "
               "still asserted by a person printing and looking, which CLAUDE.md rule 6 requires "
               "regardless; `print_variants.py` builds the variants for that. The count is checked "
               "here under `--print-pages`, and so is DS-226's geometry.",
               ("look", None)),
    "DS-223": ("The same ruling as DS-222. A slide staying a containing block for its own overlays "
               "is observable only in the printed output, where a panel that escaped its slide "
               "shows up scattered across a break - which is a look at paper, not a page count.",
               ("look", None)),
    "DS-224": ("The same ruling as DS-222. A slide that printed blank because its entrance "
               "animation never played still counts as a page, so the count cannot see it; what "
               "sees it is a person turning the sheet over.",
               ("look", None)),
    "DS-225": ("The same ruling as DS-222. The count does reach half of it: a contents "
               "page that never rendered shows up as `n` rather than `n` + `k`.",
               ("look", None)),
    "DS-226": ("The most reached of the five, by two instruments measuring different things. "
               "`contents_bound.py` measures the compression bound the rule states - 16 entries "
               "with descriptions, 24 without - in a real browser, and exercises the split that "
               "keeps every sheet inside it; run separately because it sweeps seventeen sheet "
               "sizes and eight stage shapes rather than reading the deck in front of it. "
               "**And since T-123 the printed page itself is measured**: PRINT-2 and PRINT-3 above "
               "read the card rectangles out of the printed PDF and assert that none intersects "
               "and none reaches the footnote. What is still excused is the rest of the rule - "
               "whether the compression reads as a compact mode rather than as damage - which is "
               "the judgement the 2026-08-08 ruling left with the person who prints.",
               ("look", None)),

    # ---- `default` rules, held back by the owner's triage order: the account, then the hard ones
    "DS-004": ("Triage: `default`. **Only the cross-engine half is unobservable** - no Firefox, no "
               "Safari, no mobile, and a single-engine harness is not evidence about another engine "
               "(R6 sections 9 and 10). *Degrade gracefully* stopped being unobservable when T-019 "
               "built DS-009: the degraded state ships switched on and `preflight.py prove` renders "
               "it four ways against a control that must not degrade, so that clause is checked "
               "under DS-009 and cited here rather than given a second row - DS-073 guarded by "
               "DS-070 is the same shape. Narrowed by T-097; the ruleset's `Reach` cell says the "
               "same, and CLOSES WHEN a second engine is in the harness.",
               ("harness", "a second browser engine in the harness")),
    "DS-039": ("Triage: `default`. `--measure` is declared and its 45-75ch band is a rendered "
               "line-length measurement this stage does not take.",
               ("work", "a rendered line-length measurement of the prose column, in ch")),
    "DS-047": ("Triage: `default`. *Consistent margins, breathing room* needs a definition of "
               "consistent that the rule does not give.",
               ("amendment", "DS-047")),
    "DS-049": ("Triage: `default`. Card radius and shadow are measurable; nothing has needed it.",
               ("work", "a card radius and shadow measurement")),
    "DS-050": ("Triage: `default`. The stage's field and shadow are measurable; nothing has "
               "needed it.",
               ("work", "a stage field and shadow measurement")),
    "DS-082": ("Triage: `default`. The 8-12 band is measured and reported by the DS-081 row's "
               "count; *past 12 needs a recorded reason* is not in the HTML at all.",
               ("amendment", "DS-082")),
    "DS-087": ("Triage: `default`. No deck in the repository has an appendix, so the check would "
               "have no subject to run against and would pass on nothing (**L-36**).",
               ("deck", "a deck in this repository ships an appendix")),
    "DS-104": ("Triage: `default`. Assumption markers are present and their *subtlety* is the "
               "rule's content.",
               ("amendment", "DS-104")),
    "DS-131": ("Triage: `default`. The navigation set is present; *named targets* is checked in "
               "substance by DS-217's scale verdict, which requires no per-item label at rest.",
               ("work", "a per-item accessible-name check on the navigation set")),
    "DS-133": ("Triage: `default`. The progress indicator's *encodes real position* clause is a "
               "claim about the mapping, which DS-216 counts and does not verify.",
               ("work", "a check that the progress indicator maps to the slide index")),
    "DS-134": ("Triage: `default`. The spine exists and is lit; *the argument's structure is "
               "visible* is the rule's content.",
               ("amendment", "DS-134")),
    "DS-139": ("Triage: `default`. The assumption marker's edge placement is measurable; nothing "
               "has needed it.",
               ("work", "an assumption-marker edge-placement measurement")),
    "DS-145": ("Triage: `default`. Reveal motions are DS-140's vocabulary, checked statically "
               "there; *flows use dashed arrows* is the DS-140 row.",
               ("work", "a check for dashed arrows on flow connectors")),
    "DS-147": ("Triage: `default`. Count-up and the single pulse are present; *one per slide* is "
               "the DS-101 obstacle in miniature.",
               ("amendment", "DS-147")),
    "DS-148": ("Triage: `default`. No diagram in the repository changes mode, so the check would "
               "have no subject.",
               ("deck", "a deck in this repository ships a diagram that changes mode")),
}

# **An excusal's closing condition, as a field rather than a sentence** (T-165). Every entry above
# already ended in prose with what would close it, and prose cannot be evaluated: `staleExcusals`
# fires only when a rule is excused AND checked, so DS-004's reason could half-die when T-019 shipped
# DS-009's preflight and the account stayed a clean partition for nine months. Silent by
# construction, which is the hard case **L-54** names.
#
# The vocabulary is closed and every subject has to bind to something, because a condition that
# points at nothing is the defect this exists to stop - the shape `figures.py`'s `ARTIFACTS` and
# `audit.py`'s `ABSENCE_IS_A_PASS` already use here: a declaration that comes to cover nothing fails
# the run.
CLOSING_KINDS = {
    "rule": "another rule's CHECK closes it. The subject is that rule's id, and this is the one "
            "kind a run can decide: when the named rule is checked, the excusal has come true",
    "amendment": "the rule's own TEXT has to change. The subject is the rule id whose wording is "
                 "the obstacle - usually its own, sometimes a neighbour's",
    "deck": "a deck has to ship the subject the rule judges. Nothing here has one, so a check "
            "would pass on nothing (**L-36**); the subject says what would have to appear",
    "work": "the check has to be built. The subject names the measurement, so what is owed is a "
            "sentence somebody can start from rather than a shrug",
    "harness": "the instrument has to gain a capability that is not ours to write - a second "
               "engine, a device. The subject names it",
    "look": "a person, which is CLAUDE.md rule 6 and owed anyway. It never closes mechanically, "
            "and the subject is None because there is nothing to point at",
}

# A subject that is not a rule id has to be a phrase somebody could act on. Twelve characters is not
# a quality bar - it is the floor that separates a sentence from a placeholder, and the reason the
# number is small is that judging the phrase is the reviewer's job and not this file's.
CLOSING_PHRASE_MIN = 12


# **The account is per rule, and several rules are conjunctions** (T-054). One satisfied row
# moves a rule into `checked`, so a clause nothing reaches disappears inside a rule the run
# reports as covered - which is **L-43** one level down, and the device that guarantees rule-level
# coverage is what stopped the clause-level question being asked.
#
# A clause is `True` when some check decides it, or an excusal in `DEFERRED`'s exact shape:
# `(why, (kind, subject))`. The shape is shared rather than copied so `closing_faults` validates
# both, and a clause excusal is held to the standard a rule excusal is - a reason somebody can
# read, and a condition that would end it.
#
# **This table declares only rules whose statement is a conjunction of separately checkable
# clauses.** A second sentence restating the first (DS-081's *under 6 is a memo*) is rationale,
# not a clause, and listing it would inflate the account rather than sharpen it. The sweep that
# produced this list read all 120 `hard` rules, 2026-08-18.
CLAUSES = {
    "DS-020": (("neutral ground", True),
               ("exactly one accent", True)),
    "DS-034": (("body 24-28 du at line-height 1.40-1.70", True),
               ("display ~67 du",
                "The band is stated for the display role and nothing resolves it. `ds034_body_type` "
                "reads `--fs-body` and `--lh-body` only, so a deck can set a display face far off "
                "the stated size and the rule still reports checked. CLOSES WHEN: the check "
                "resolves `--fs-display` the way it already resolves `--fs-body`.",
                ("work", "resolve --fs-display against the stated ~67 du band")),
               ("subhead ~34 du",
                "Same shape as the display clause and the same gap: no token is resolved for the "
                "subhead role, so the third of the three bands this rule states is unmeasured. "
                "CLOSES WHEN: the check resolves the subhead size token against the stated band.",
                ("work", "resolve the subhead size token against the stated ~34 du band"))),
    "DS-091": (("one headline per slide", True),
               ("the headline is at most six words", True),
               ("at most three supporting fragments",
                "Nothing in the DOM marks a run as a supporting fragment. Counting tier-one runs "
                "instead puts three slides of the *conforming* deck over budget at 4, 5 and 9 - on "
                "the eyebrow, a stat figure and its label (one thing, not two), the assumption "
                "marker and the provenance mark. Those are required by DS-104 and DS-105, so the "
                "count would set three rules against each other, and any threshold sparing them "
                "would be a number chosen to fit one deck (**L-38**). This is the clause T-053 "
                "could not close and had nowhere to record. CLOSES WHEN: a supporting fragment is "
                "structurally identifiable - a class, a container, a list - which is a rule "
                "amendment and the owner's. Adopting markup to make a check work is backwards, "
                "which is the DS-026 precedent.",
                ("amendment", "DS-091"))),
    "DS-092": (("sentence under 20 words", True),
               ("paragraph 3-4 sentences", True),
               ("table cell one line",
                "*One line* is a rendered fact, not a markup one: a cell wraps or does not wrap "
                "depending on the column width the table resolves to, so the static half cannot "
                "decide it and the rendered half does not measure it. CLOSES WHEN: the render "
                "pass reports per-cell line boxes, which is a measurement to add rather than a "
                "rule to change.",
                ("work", "report per-cell line box counts from the real render"))),
    "DS-100": (("active voice",
                "Voice is a reading of the sentence, not a pattern in it. Every proxy tried on the "
                "corpus - forms of *to be* beside a past participle - fires on ordinary "
                "descriptive copy, and the rule is about how the deck argues rather than about "
                "which auxiliaries it uses. CLOSES WHEN: this becomes a `judge` clause the "
                "critique pass owns, or the rule names a structure.",
                ("amendment", "DS-100")),
               ("one dash per paragraph at most",
                "Countable, and nothing counts it. The obstacle is only that *dash* has to mean "
                "the em dash the house style uses and not the hyphen inside a compound, which is "
                "a decision this file should not take alone. CLOSES WHEN: the check counts em "
                "dashes per paragraph in slide copy, on the same subject `ds100` already reads.",
                ("work", "count em dashes per paragraph over the deck's own slide copy")),
               ("no rhetorical questions", True)),
}


def clause_account(clauses=None, checked=(), owned=None):
    """`dict` - what the clause table says about coverage, and every fault in it.

    **Reported on every run, including at zero** (**L-36**): a number that appears only when
    something is in it is a number nobody can see go empty, which is the same argument that puts
    a row here for every rule the ruleset cites rather than for every rule currently broken.

    It deliberately does **not** touch `account()`'s partition. Rule-level coverage answers *did
    any check decide this rule*, and that stays true of a partly-decided rule; this answers the
    narrower question the other one cannot express.
    """
    clauses = CLAUSES if clauses is None else clauses
    owned = ruleset.owned() if owned is None else owned
    total = decided = 0
    partly, faults, unowned = [], [], []
    for rid in sorted(clauses):
        if rid not in owned:
            unowned.append(rid)
        open_here = []
        for text, state in ((c[0], c[1:]) for c in clauses[rid]):
            total += 1
            if state and state[0] is True:
                decided += 1
                continue
            entry = (state[0], state[1]) if len(state) == 2 else state[0]
            open_here.append(text)
            # **The same validator, not a second one.** A clause excusal is an excusal, so it is
            # held to what `closing_faults` already enforces on a rule's (L-08).
            for _rid, what in closing_faults({rid: entry}, checked=checked, owned=owned):
                faults.append("%s clause %r %s" % (rid, text, what))
        if open_here:
            partly.append(rid)
    return {"rulesWithClauses": sorted(clauses), "partlyDecided": partly,
            "clausesTotal": total, "clausesDecided": decided,
            "clausesUnreached": total - decided,
            "clauseExcusalFaults": faults,
            "clausesForRulesNotOwned": unowned}


def closing_faults(deferred=None, checked=(), owned=None):
    """`[(rule, what)]` - every closing condition that is broken, or that has come true.

    Two different failures, deliberately in one list because they are one claim: *this excusal is
    still needed, and here is what would end it.* An entry with no readable condition cannot be
    held to anything; an entry whose condition is satisfied is an excusal that has stopped being
    true. `staleExcusals` catches the second one only after somebody has already written the check
    AND the rule is being counted - this catches it at the moment the closer lands.

    **Only `rule` conditions are decidable, and that is the answer rather than a shortfall**
    (T-165's open question). A run can read the ruleset and the account; it cannot cheaply run a
    second browser engine, write a missing measurement, or look at a slide. What every kind gets
    regardless is BINDING: the subject must resolve to a rule this ruleset owns or be a phrase
    somebody can act on, so an entry can no longer point at nothing.
    """
    deferred = DEFERRED if deferred is None else deferred
    owned = ruleset.owned() if owned is None else owned
    checked = set(checked)
    out = []
    for rid in sorted(deferred):
        entry = deferred[rid]
        if not (isinstance(entry, tuple) and len(entry) == 2
                and isinstance(entry[1], tuple) and len(entry[1]) == 2):
            out.append((rid, "carries no closing condition a check can read - the entry is a "
                             "reason and nothing else, so nothing can ever report it stale"))
            continue
        kind, subject = entry[1]
        if kind not in CLOSING_KINDS:
            out.append((rid, "closes on %r, which is not one of: %s"
                        % (kind, ", ".join(sorted(CLOSING_KINDS)))))
        elif kind in ("rule", "amendment"):
            if subject not in owned:
                out.append((rid, "closes on rule %r and the ruleset does not own it, so the "
                                 "condition binds to nothing" % (subject,)))
            elif kind == "rule" and subject in checked:
                out.append((rid, "closes when %s is checked, and %s IS checked now. The excusal "
                                 "has come true - resolve it or restate why it has not"
                            % (subject, subject)))
        elif kind == "look":
            if subject is not None:
                out.append((rid, "closes on a look and also names %r; a look has nothing to bind "
                                 "to, so the subject is None" % (subject,)))
        elif not (isinstance(subject, str) and len(subject.strip()) >= CLOSING_PHRASE_MIN):
            out.append((rid, "closes on %r and its subject is %r - too short to act on, which is "
                             "a placeholder rather than a condition" % (kind, subject)))
    return out


# The five the rubric cannot reach, proven blind against the seeded-defect deck. Named on every
# run so a clean gate is never read as a good deck (**L-05**, DS-191).
BLIND = "S1 Claim, S2 Evidence, S4 Density, D1 Spine, D4 Consistency"


# **The producers a run cannot reach from markup, and why each is outside the static half.** The
# complement is declared, never the membership: a list of what is *in* is what `static_variants.py`
# kept by hand, and a name nobody adds is a name nobody misses (T-066). A list of what is *out*
# cannot go stale in silence, because `producer_split()` fails the run for a producer in neither -
# which is the only thing that tells a deliberate exclusion from a forgotten one. T-123 added
# `printgeom.verdicts` and it is the first whose absence from the static half is **correct**; before
# this table there was nowhere to write that down (T-095).
NOT_STATIC = {
    "audit.render_verdicts": "reads a measurement taken in real Chrome. There is no markup answer "
                             "to a computed style or a laid-out box",
    "audit.reduced_verdicts": "a second real render with prefers-reduced-motion forced, which is a "
                              "measurement of what the browser did rather than of what the deck says",
    "contract.verdicts": "sweeps four viewports and two resolutions; §2.4 and §2.5 are claims about "
                         "what happens BETWEEN renders and no single one of them decides it",
    "contract.scale_verdicts": "the same sweep, and it delegates after a render it must first take",
    "contract.scale_verdicts_from": "takes the sweep's measurement as its subject, never a deck",
    "printpages.verdicts": "counts the pages a real Chrome print produces, which no markup states",
    "printgeom.verdicts": "reads the card rectangles out of the printed PDF. The fault it exists "
                          "for lives only in paged layout, which no screen measurement reaches "
                          "(T-123, **L-76**)",
    "spec.verdicts": "the content half. Its subject is the specification and the sources beside the "
                     "deck, not the deck's own markup",
    "density.verdicts": "reads the deck from its path so the row can name it; the ranking it "
                        "checks is derived from the markup and `density.kind_verdicts` is the "
                        "static half, which `static_rows` gathers (T-112)",
    "figgrid.verdicts": "measures the leftmost rendered ink against the slide's text edge. The "
                        "markup cannot answer it: the <svg> is on the column in every deck that "
                        "fails, and what is inset is the drawing inside a viewBox scaled by a "
                        "factor only the laid-out page knows (T-184)",
}


def static_rows(html):
    """Every verdict a run reaches from the markup alone - no browser, no print, no sources.

    **One composition, imported rather than restated.** `static_variants.py` seeds a defect into the
    markup and requires the gate to notice it, so it needs exactly this half - and it used to compose
    its own copy by naming the producers. The two descriptions disagreed the first time either
    changed: T-093 moved DS-005 out of `STATIC` into a producer, `gather` picked it up, and the suite
    reported `MISSED` for a rule that was being checked (**L-08**, **L-13**). Which producers this
    function calls is now the definition of the static half; `NOT_STATIC` is the rest, with a reason.
    """
    rows = [(rule, what, bool(fn(html))) for rule, what, fn in audit.STATIC]
    # The editorial split, added by T-016. DS-230 names what tier two is for and stays `judge`;
    # this is the one clause of DS-161 a program can settle, and it needs a count in its text,
    # which `STATIC`'s boolean shape cannot carry.
    rows += audit.split_verdicts(html)
    # DS-105's link half, added by T-069. Same shape and same reason as the row above: the count has
    # to travel in the text, because a deck that cites nothing must not read as a deck whose links
    # were checked. It replaces an excuse that rested on DS-001 banning links, which DS-001 does not.
    rows += audit.provenance_verdicts(html)
    # DS-232, added by T-104. Same shape and same reason: the count travels in the text, because a
    # deck with one slide and no SVG has pointed nowhere and must not read as one whose references
    # were checked.
    rows += audit.marker_verdicts(html)
    # DS-005, added by T-093. Same shape and same reason as the two rows above: the verdict needs a
    # count in its text, and the boolean it replaced forbade `import(blob:)` - the one route R6 §6
    # measured as working, and the one DS-006 exists to make work.
    rows += audit.fetch_verdicts(html)
    rows += contrast.verdicts(html)
    # The theme region, added by T-007. Three partial checks of rules `audit` and `contrast`
    # already reach from another side: DS-011 counts palettes, this counts regions; DS-013 names
    # the roles, this holds the whole token set to `docs/THEME-CONTRACT.md`; DS-010 catches a
    # colour literal, this catches every other value a theme cannot reach.
    rows += theme.verdicts(html)
    # The markup contract, added by T-016. `theme` holds the deck to the values a second theme
    # would change; this holds it to the elements a generator has to emit - the other half of the
    # same claim, and the one T-002 cannot start without.
    rows += component.verdicts(html)
    # DS-237 and DS-238, added by T-112. The split is declared in the stylesheet the deck carries,
    # so both are settled from the markup: a render would say the same thing after a browser start.
    rows += density.kind_verdicts(html)
    return rows


def static_producers():
    """Which verdict producers `static_rows` reaches, read from its own source.

    **Derived, so adding a producer to the composition adds it here too.** Reading the source is the
    same technique `audit.verdict_producers` uses one scope out, and for the same reason: a second
    list agreeing with the code is a list that agrees until somebody edits one of them.
    """
    src = inspect.getsource(static_rows)
    return sorted(n for n in audit.verdict_producers() if "%s(" % n in src)


def producer_split():
    """`(static, elsewhere)` - every verdict producer classified, or the run stops.

    **This is what the hand-kept list could not do.** Deleting the list makes the suite run whatever
    `static_rows` runs, which closes the drift; it does not say whether a producer *missing* from
    the static half is missing on purpose. Three have arrived since this discipline was needed and
    the third is the first whose exclusion is correct, so the question is now permanent: a producer
    in neither the composition nor `NOT_STATIC` fails the run until somebody decides which it is.
    """
    producers = set(audit.verdict_producers())
    static = set(static_producers())
    stray = sorted(producers - static - set(NOT_STATIC))
    if stray:
        sys.exit("SELF-TEST FAILED: %s produce verdict rows and are neither called by "
                 "check.static_rows() nor declared in check.NOT_STATIC. Wire it into the static "
                 "half, or say there why it cannot run without a browser, a print or sources - a "
                 "producer in neither is a family of rows no seeded-defect suite reaches, and the "
                 "suite's own count would still read n of n (T-095)" % ", ".join(stray))
    gone = sorted(set(NOT_STATIC) - producers)
    if gone:
        sys.exit("SELF-TEST FAILED: NOT_STATIC declares %s and no module defines them - an excusal "
                 "that has outlived its subject, which is the shape T-077 was raised from"
                 % ", ".join(gone))
    both = sorted(static & set(NOT_STATIC))
    if both:
        sys.exit("SELF-TEST FAILED: %s are called by static_rows() and declared outside it. The "
                 "table is the complement of the composition, so an entry in both makes it neither"
                 % ", ".join(both))
    for name, why in sorted(NOT_STATIC.items()):
        if len(why) < 40:
            sys.exit("SELF-TEST FAILED: %s is excluded in a phrase, not in writing" % name)
    return sorted(static), sorted(NOT_STATIC)


def gather(deck, sources=None, print_pages=False, skip_contract=False):
    """Every verdict, from every stage, as one list of `(rule, what, ok)` rows.

    Returns `(rows, data, notes)`. `notes` carries what a reader needs to know about the run
    itself - which halves ran, and anything that failed to measure.
    """
    html = open(deck, "r", encoding="utf-8").read()
    rows, notes = [], []

    rows += static_rows(html)

    data, err = audit.render_data(deck)
    if not data:
        # NO RESULT is a failed measurement, never a pass. This is the case T-028 found, where
        # stage 3 printed NO RESULT and the run stayed green.
        rows.append(("RENDER", "the render gate produced no result: %s" % (err or "")[:200], False))
        notes.append("render gate: NO RESULT - every rendered rule is unmeasured, not passing")
    else:
        rows += audit.render_verdicts(data)

    # A second render, with `prefers-reduced-motion` forced. Added by T-016: the deck honoured the
    # query from the start and nothing had ever rendered under it, which is why DS-143 sat excused.
    rdata, rerr = audit.reduced_motion_data(deck)
    if not rdata:
        notes.append("reduced-motion pass: NO RESULT - DS-143 is unmeasured, not passing")
    rows += audit.reduced_verdicts(rdata)

    # DS-236, added by T-184. Its own render rather than a row off `render_data` above, because
    # `figgrid` owns the measurement and a second copy of the probe here is the composition that
    # disagreed the first time either half changed (**L-08**, **L-13**).
    rows += figgrid.verdicts(deck)

    # DS-239, added by T-112. It takes the deck rather than the markup only because it reports the
    # path in its own row; the derivation itself is pure.
    rows += density.verdicts(deck)

    if not skip_contract:
        rows += list(contract.audit(deck, quiet=True))

    ledger = None
    if sources:
        ledger, content_rows = content.audit(deck, sources)
        rows += content_rows
        notes.append("content half: RAN, against %d source file(s)" % ledger["sourceCount"])
    else:
        notes.append("content half: NOT RUN - no sources supplied. A presentation-only run is a "
                     "legitimate result and is not a clean one")

    if print_pages:
        rows += printpages.verdicts(deck, data["slideCount"] if data else None)
        # The geometry rides the same flag as the count. Both need a real print through Chrome, so
        # separating them would buy a caller nothing and cost the one thing T-116 showed matters:
        # a run that asserts the page count and leaves the page's own layout unmeasured (**L-76**).
        rows += printgeom.verdicts(deck)
    else:
        notes.append("printed page count and geometry: NOT RUN - opt-in, printing is a mode and "
                     "not a gate")

    return rows, data, notes, ledger


def account(rows):
    """The coverage declaration, derived from the ruleset at run time.

    **Every owned rule lands in exactly one bucket, and `partitionError` is that claim reported
    rather than assumed.** It used to be asserted only in a docstring, and it was false by one:
    DS-072 was counted `checked` *and* excused by the ruleset, so 79 + 4 + 29 came to 112 against
    111 owned rules and every published figure inherited the error (T-042, F-2).

    `silent` and `stale` are both failures: a rule nothing decided is L-36, and an excusal for a
    rule that IS checked is the same defect with the sign flipped - a hand-written note that
    stopped being true and nothing noticed. `partitionError` is a third, and it is the one that
    catches the other two lying about their size.

    **A rule the ruleset excuses is never `checked`, whatever a stage happens to measure.** That is
    the general rule DS-072 forced (2026-08-09): `off-gate` means *decidable in principle, not by
    this instrument*, so a verdict taken against a double is not the rule being decided, and
    counting it claims a reach the ruleset denies. The measurement is not discarded - it is
    reported under `measuredThoughExcused`, and **it still fails the run when it comes out false**,
    because the account is a claim about coverage and a failure is a fact about the deck.

    **A row whose `ok` is `None` decided nothing**, so the rule is not `checked` and falls to
    `silent` with everything else nothing decided. It stays a failure of the run: a fourth,
    forgiving bucket would let coverage drain into it deck by deck while the gate reported green,
    which is **L-36 rebuilt one storey up**. What it earns is a reason - `silentNoSubject` names the
    rules whose check ran and found no subject, against the rest, which have no check at all. The
    two need opposite fixes, and until T-051 the account could not tell them apart because a
    subjectless check reported `pass` and never reached this function at all.
    """
    own = ruleset.owned()
    decided = {r for r, _w, ok in rows if r in own and ok is not None}
    failed = {r for r, _w, ok in rows if r in own and ok is False}
    no_subject = {r for r, _w, ok in rows if r in own and ok is None} - decided
    by_ruleset = {k for k, v in own.items() if v.excused}
    cited = decided - by_ruleset
    deferred = {k for k in DEFERRED if k in own}
    # **`undecided` is its own bucket and is not a coverage fault (T-065).** A rule enters it only
    # by its check RUNNING and returning None, so nothing can drain here by neglect: a rule with no
    # check never produces a row and still falls to `silent`, which still fails the run. That
    # structural difference is what makes this bucket safe where a general forgiving one would not
    # be, and it is why L-36's argument does not reach it.
    #
    # The deeper reason: coverage is a claim about the GATE, not about one deck. A check that ran
    # and found nothing has full coverage. Failing the run because this deck has no disclosures made
    # the gate's coverage verdict depend on the deck's content, and made a deck specified without
    # disclosures un-passable - which is a check forbidding a design choice (CLAUDE.md).
    undecided = no_subject - by_ruleset - deferred
    silent = set(own) - cited - by_ruleset - deferred - undecided
    stale = deferred & (cited | by_ruleset)
    unknown = set(DEFERRED) - set(own)
    buckets = len(cited) + len(by_ruleset) + len(deferred) + len(silent) + len(undecided)
    return {
        "owned": sorted(own), "checked": sorted(cited), "failing": sorted(failed),
        "excusedByRuleset": sorted(by_ruleset), "deferred": sorted(deferred),
        "silent": sorted(silent), "staleExcusals": sorted(stale),
        "undecided": sorted(undecided),
        "silentNoSubject": sorted(undecided),   # kept: the pipeline reads this key
        "excusalsForRulesNotOwned": sorted(unknown),
        "measuredThoughExcused": sorted((decided | no_subject) & by_ruleset),
        "bucketSum": buckets, "partitionError": buckets - len(own),
    }


def run(deck, sources=None, print_pages=False, skip_contract=False):
    """The entry point the pipeline calls and the command below wraps."""
    ruleset.self_test()
    render.self_test()
    contrast.self_test()
    contract.self_test()
    content.self_test()
    component.self_test()
    audit.self_test()
    self_test()

    rows, data, notes, ledger = gather(deck, sources, print_pages, skip_contract)
    acct = account(rows)
    clauses = clause_account(checked=acct["checked"])
    # `is False`, not `not ok`: a row that decided nothing is not a defect in the deck, and folding
    # it into the failure list would report a missing subject as a broken one (T-051).
    failures = [(r, w) for r, w, ok in rows if ok is False]
    if acct["silentNoSubject"]:
        notes.append("subject absent: %s - the check ran and this deck contains nothing for it to "
                     "judge, so the rule is undecided rather than passing"
                     % " ".join(acct["silentNoSubject"]))
    coverage_faults = (acct["silent"] + acct["staleExcusals"]
                       + acct["excusalsForRulesNotOwned"]
                       + ["CLOSING %s - %s" % (rid, what)
                          for rid, what in closing_faults(checked=acct["checked"])]
                       + ["CLAUSE %s" % what for what in clauses["clauseExcusalFaults"]]
                       + ["CLAUSE TABLE %s - the ruleset does not own it" % rid
                          for rid in clauses["clausesForRulesNotOwned"]])
    if acct["partitionError"]:
        coverage_faults = coverage_faults + [
            "PARTITION %+d (buckets %d, owned %d)"
            % (acct["partitionError"], acct["bucketSum"], len(acct["owned"]))]
    return {
        "deck": paths.display_path(deck, ROOT).replace("\\", "/"),
        "rows": [{"rule": r, "what": w, "ok": ok} for r, w, ok in rows],
        "account": acct,
        "clauses": clauses,
        "ledger": ledger,
        "notes": notes,
        "failures": [{"rule": r, "what": w} for r, w in failures],
        "coverageFaults": coverage_faults,
        "blindTo": BLIND,
        "ok": not failures and not coverage_faults,
    }


def self_test():
    """The gate must be able to tell a covered rule from an uncovered one (**L-04**).

    Both directions are tested, because only one of them has ever been the bug: a missing check
    is loud, and an excusal that quietly outlived its rule is not. **The partition is tested by
    breaking it**, because an arithmetic check that cannot be made to fail is decoration - which
    is what stood here until T-043 replaced `if ...: pass` under a comment claiming the sum was
    asserted somewhere else. It was not asserted anywhere.
    """
    own = ruleset.owned()
    plain = [k for k in sorted(own) if k not in DEFERRED and not own[k].excused]
    if len(plain) < 3:
        sys.exit("SELF-TEST FAILED: fewer than three plainly-checkable rules to test with")

    a = account([(r, "", True) for r in plain[:3]])
    if a["partitionError"]:
        sys.exit("SELF-TEST FAILED: buckets sum to %d against %d owned rules (%+d)"
                 % (a["bucketSum"], len(a["owned"]), a["partitionError"]))
    if set(a["checked"]) != set(plain[:3]):
        sys.exit("SELF-TEST FAILED: the account did not recognise three checked rules")
    if not a["silent"]:
        sys.exit("SELF-TEST FAILED: a run checking three rules reported nothing silent")

    # Break the partition on purpose. A rule excused HERE that a stage also checks is counted in
    # two buckets, so the sum runs one over - and that is exactly the shape the DS-072 defect had,
    # one bucket along. If this stops failing, the assertion above has stopped meaning anything.
    broken = account([(k, "", True) for k in list(DEFERRED)[:1]])
    if broken["partitionError"] != 1:
        sys.exit("SELF-TEST FAILED: a rule both excused here and checked did not break the "
                 "partition - the arithmetic is not being checked")
    if not broken["staleExcusals"]:
        sys.exit("SELF-TEST FAILED: an excusal for a rule that IS checked was not reported")

    # The ruleset's excusal outranks a stage's measurement, and the measurement survives as a note.
    # Without this, DS-072 walks back into `checked` the next time a stage grows a verdict for it.
    excused = sorted(k for k, v in own.items() if v.excused)
    if not excused:
        sys.exit("SELF-TEST FAILED: no rule is excused by the ruleset, so the precedence rule "
                 "between a ruleset excusal and a stage's measurement is untested")
    e = account([(excused[0], "", True)])
    if excused[0] in e["checked"]:
        sys.exit("SELF-TEST FAILED: %s is excused by the ruleset and was counted as checked"
                 % excused[0])
    if e["measuredThoughExcused"] != [excused[0]]:
        sys.exit("SELF-TEST FAILED: the measurement of an excused rule was dropped, not noted")
    if e["partitionError"]:
        sys.exit("SELF-TEST FAILED: measuring an excused rule broke the partition (%+d)"
                 % e["partitionError"])

    for rid, (why, _closes) in DEFERRED.items():
        if len(why) < 40:
            sys.exit("SELF-TEST FAILED: %s is excused in a phrase, not in writing" % rid)

    # T-054. The clause table is held to exactly what the rule table is held to, and the failures
    # are watched rather than reasoned about - each fixture below is built here rather than
    # asserted against the live table (**L-78**, **L-112**).
    live = clause_account()
    if live["clauseExcusalFaults"] or live["clausesForRulesNotOwned"]:
        sys.exit("SELF-TEST FAILED: the live clause table is broken: %s"
                 % "; ".join(live["clauseExcusalFaults"] + live["clausesForRulesNotOwned"]))
    if live["clausesTotal"] <= live["clausesDecided"]:
        sys.exit("SELF-TEST FAILED: the clause table reports every clause decided, which is the "
                 "state it was written to disprove - DS-091's third clause is the instance")
    for rid, (why, _c) in ((r, e[1:]) for r in CLAUSES for e in CLAUSES[r]
                           if len(e) == 3):
        if len(why) < 40:
            sys.exit("SELF-TEST FAILED: a clause of %s is excused in a phrase, not in writing" % rid)
        if "CLOSES WHEN" not in why:
            sys.exit("SELF-TEST FAILED: a clause of %s is excused with no closing condition in "
                     "its reason" % rid)
    own_one = sorted(ruleset.owned())[0]
    for label, table, expect in (
            ("an excusal with no closing condition",
             {own_one: (("a clause", "a reason forty characters long and no more than that"),)}, True),
            ("a closing kind nothing defines",
             {own_one: (("a clause", "a reason forty characters long and nothing else",
                         ("someday", own_one)),)}, True),
            ("a placeholder subject",
             {own_one: (("a clause", "a reason forty characters long and nothing else",
                         ("work", "tbd")),)}, True),
            ("a sound entry",
             {own_one: (("a clause", "a reason forty characters long and nothing else",
                         ("work", "a measurement somebody can start from")),)}, False)):
        got = bool(clause_account(table)["clauseExcusalFaults"])
        if got != expect:
            sys.exit("SELF-TEST FAILED: the clause table accepted or refused the wrong thing - %s "
                     "should have %s and did not" % (label, "faulted" if expect else "passed"))
    if not clause_account({"DS-999": (("a clause", True),)})["clausesForRulesNotOwned"]:
        sys.exit("SELF-TEST FAILED: a clause table naming a rule the ruleset does not own was "
                 "accepted, so the table can point at nothing")

    # T-165: the closing condition. **Every fixture below builds its own table** (**L-78**) - an
    # assertion about the live one is an assertion about the repository's current contents, and the
    # edit it blocks is the edit this field exists to make cheap.
    real, other = sorted(own)[0], sorted(own)[1]
    for label, entry, expect in (
            ("no condition at all", "a reason forty characters long and no more than that", True),
            ("an unknown kind", ("a reason forty characters long and nothing else",
                                 ("someday", real)), True),
            ("a rule id nothing owns", ("a reason forty characters long and nothing else",
                                        ("amendment", "DS-999")), True),
            ("a look that also names a subject", ("a reason forty characters long here",
                                                  ("look", "somebody")), True),
            ("a placeholder phrase", ("a reason forty characters long here", ("work", "tbd")), True),
            ("a sound amendment", ("a reason forty characters long here",
                                   ("amendment", real)), False),
            ("a sound look", ("a reason forty characters long here", ("look", None)), False),
            ("a sound piece of work", ("a reason forty characters long here",
                                       ("work", "a measurement somebody could take")), False)):
        got = bool(closing_faults({"DS-000": entry}, checked=(), owned=own))
        if got != expect:
            sys.exit("SELF-TEST FAILED: %s was %s - a closing condition that binds to nothing has "
                     "to fail the run, and a sound one must not" % (label, "accepted" if got
                                                                    else "rejected"))

    # The case nothing could see before this existed: the excusal's closer has landed. `real` is a
    # rule the ruleset owns; the fixture says DS-000 waits for it and the account says it is checked.
    satisfied = {"DS-000": ("a reason forty characters long here", ("rule", real))}
    if not closing_faults(satisfied, checked={real}, owned=own):
        sys.exit("SELF-TEST FAILED: an excusal whose closing condition is already satisfied was "
                 "not reported - that is DS-004's shape and the whole reason for the field")
    if closing_faults(satisfied, checked={other}, owned=own):
        sys.exit("SELF-TEST FAILED: an excusal was reported closable because some OTHER rule is "
                 "checked, which would make the field fire on every run")

    # And the live table binds. This is not an assertion about its CONTENTS - it says every entry
    # points at something, which is the property, and it stays true through any edit that keeps it.
    live = closing_faults(checked=())
    if live:
        sys.exit("SELF-TEST FAILED: %d deferred entr%s cannot be held to a closing condition: %s"
                 % (len(live), "y" if len(live) == 1 else "ies",
                    "; ".join("%s %s" % (r, w) for r, w in live[:3])))

    # **`--quiet` must never be able to swallow a red run.** The whole objection to a quiet gate is
    # that it hides something, so the one thing it must not hide is asserted rather than reviewed.
    red = {"deck": "x", "notes": [], "account": account([]), "ok": False,
           "failures": [{"rule": "DS-000", "what": "a failure the quiet path must still print"}],
           "rows": [], "blindTo": BLIND}
    out = io.StringIO()
    stdout, sys.stdout = sys.stdout, out
    try:
        code = report(red, quiet=True)
    finally:
        sys.stdout = stdout
    if code != 1 or "DS-000" not in out.getvalue():
        sys.exit("SELF-TEST FAILED: --quiet on a failing run exited %r and %s the failure. A quiet "
                 "mode that reports a red run as one line, or as none, is worse than no quiet mode"
                 % (code, "printed" if "DS-000" in out.getvalue() else "dropped"))

    # Every verdict producer is in the static half or declared outside it. Here as well as in
    # `static_variants.py`, because the composition is this file's and a producer arrives here first.
    producer_split()
    return True


def summary(res):
    """A passing run in one line - the partition, spelled as the sum it has to be.

    **The line is the whole report under `--quiet`, so what it omits is unreachable.** That is why it
    carries counts rather than a verdict: the risk `CE-03` names is a rule that quietly stops being
    checked, and `checked` falling while `owned` holds is what that looks like. A rule that loses its
    check entirely lands in `SILENT`, which is a coverage fault and never reaches this line at all.
    """
    a = res["account"]
    return ("pass  %s  %d owned = %d checked + %d excused here + %d excused in the rules + "
            "%d undecided + %d SILENT, %d failing"
            % (res["deck"], len(a["owned"]), len(a["checked"]), len(a["deferred"]),
               len(a["excusedByRuleset"]), len(a["undecided"]), len(a["silent"]),
               len(res["failures"])))


def report(res, verbose=True, quiet=False):
    a = res["account"]
    print("deck:    %s" % res["deck"])
    for n in res["notes"]:
        print("         %s" % n)
    if quiet and res["ok"]:
        # The notes above stay. They say which halves of the check ran, and a quiet run that hid
        # `content half: NOT RUN` would conceal more than the 169 lines it saved.
        print(summary(res))
        return 0
    if verbose:
        print("\n=== verdicts")
        for row in res["rows"]:
            print("  %-15s %-62s %s"
                  % (row["rule"], row["what"][:62],
                     "NO SUBJECT" if row["ok"] is None else "pass" if row["ok"] else "FAIL"))
    print("\n=== coverage account (derived from DESIGN-SYSTEM.md at run time)")
    print("  owned by a gate      %3d" % len(a["owned"]))
    print("  checked              %3d" % len(a["checked"]))
    print("  failing              %3d   %s" % (len(a["failing"]), " ".join(a["failing"])))
    print("  excused in the rules %3d   %s" % (len(a["excusedByRuleset"]),
                                               " ".join(a["excusedByRuleset"])))
    print("  excused here         %3d" % len(a["deferred"]))
    print("  undecided, no subject%3d   %s" % (len(a["undecided"]), " ".join(a["undecided"])))
    print("  SILENT               %3d   %s" % (len(a["silent"]), " ".join(a["silent"])))
    if a["undecided"]:
        print("      The check ran and found nothing in this deck to judge, so the rule is neither\n"
              "      passed nor failed. This is NOT a coverage fault and does not fail the run: a\n"
              "      rule reaches it only by its check executing, so nothing can drain here by\n"
              "      neglect. A rule with no check at all is SILENT above, and still fails.")
    print("  ------------------------")
    print("  buckets sum to       %3d   %s"
          % (a["bucketSum"],
             "= owned, so the account is a partition" if not a["partitionError"]
             else "PARTITION ERROR %+d - a rule is in two buckets or none" % a["partitionError"]))
    if a["measuredThoughExcused"]:
        print("  measured, not claimed    %s"
              % " ".join(a["measuredThoughExcused"]))
        print("      A stage measured these and the ruleset says no check of its kind reaches "
              "them, so they are\n      excused rather than checked - the measurement is a note "
              "under the excusal, and it still\n      fails the run if it comes out false.")
    # **The clause account, printed whether or not anything is in it** (T-054). `checked` is a
    # per-rule verdict, and several rules are conjunctions: one satisfied row carries the whole
    # rule into the bucket above, so without these three lines a clause nothing reaches is
    # invisible inside a rule the run calls covered.
    c = res.get("clauses")
    if c:
        print("\n  clause-level, for the %d rule(s) whose statement is a conjunction"
              % len(c["rulesWithClauses"]))
        print("    clauses declared   %3d" % c["clausesTotal"])
        print("    decided            %3d" % c["clausesDecided"])
        print("    UNREACHED          %3d" % c["clausesUnreached"])
        print("    partly decided     %3d   %s"
              % (len(c["partlyDecided"]), " ".join(c["partlyDecided"])))
        if verbose:
            for rid in c["rulesWithClauses"]:
                print("    %s" % rid)
                for entry in CLAUSES[rid]:
                    text, state = entry[0], entry[1:]
                    if state and state[0] is True:
                        print("      decided    %s" % text)
                    else:
                        kind, subject = state[1]
                        print("      UNREACHED  %s  [%s: %s]" % (text, kind, subject))
                        print("                 %s" % state[0])
        print("      A rule here is `checked` above and still incomplete. The two answer different\n"
              "      questions: whether any check decided the rule, and how much of it they left.")
    if a["staleExcusals"]:
        print("  STALE EXCUSAL        %3d   %s" % (len(a["staleExcusals"]),
                                                   " ".join(a["staleExcusals"])))
    if a["excusalsForRulesNotOwned"]:
        print("  EXCUSAL WITH NO RULE %3d   %s" % (len(a["excusalsForRulesNotOwned"]),
                                                   " ".join(a["excusalsForRulesNotOwned"])))
    if verbose and a["deferred"]:
        print("\n=== excused here, and what would close each")
        for rid in a["deferred"]:
            why, (kind, subject) = DEFERRED[rid]
            print("  %-8s [%s: %s]\n           %s"
                  % (rid, kind, subject if subject is not None else "a person, rule 6", why))
        # **Every kind, including the ones at zero.** A kind that appears only when something is in
        # it is a kind nobody can see going empty - the same argument that puts a row here for every
        # rule the ruleset cites rather than for every rule currently broken (**L-36**).
        print("\n  by what would close it: %s"
              % "  ".join("%s %d" % (k, sum(1 for r in a["deferred"] if DEFERRED[r][1][0] == k))
                          for k in sorted(CLOSING_KINDS)))
        print("  Only `rule` is decidable on a run, and it is the one at zero: no excusal here is\n"
              "  waiting on another rule's check today. The rest bind to something a person can act\n"
              "  on, which is what an entry pointing at nothing no longer can (T-165).")

    print("\n%d failure(s): %s"
          % (len(res["failures"]), ", ".join(f["rule"] for f in res["failures"]) or "none"))
    for f in res["failures"]:
        print("    %-15s %s" % (f["rule"], f["what"]))
    print("""
**This gate is necessary and nowhere near sufficient, and the banned-terminology row is the
sharpest case: text can pass all five categories and still read as machine-written, so a clean
DS-106 is never "reads as human-written" (DS-107, C-10).** Five of the ten evaluation dimensions -
%s - are invisible to any check here and were proven so
against a seeded-defect deck. A clean run is not a good deck; it is a deck carrying no defect this
gate was built to see (L-05, DS-191).""" % res["blindTo"])
    return 0 if res["ok"] else 1


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    deck = os.path.abspath(args[0]) if args else os.path.join(
        ROOT, "examples", "reference-deck.html")
    sources = None
    for a in argv:
        if a.startswith("--sources="):
            sources = os.path.abspath(a.split("=", 1)[1])
    if "--sources" in argv:
        i = argv.index("--sources")
        if i + 1 < len(argv):
            sources = os.path.abspath(argv[i + 1])
    res = run(deck, sources=sources, print_pages="--print-pages" in argv,
              skip_contract="--skip-contract" in argv)
    if "--json" in argv:
        print(json.dumps(res, indent=1))
        return 0 if res["ok"] else 1
    return report(res, quiet="--quiet" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
