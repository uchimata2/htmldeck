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
import hashlib
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
import markhits                                                     # noqa: E402
import density                                                      # noqa: E402
import glitchfree                                                   # noqa: E402
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
    # DS-224's excusal was CLOSED by T-232 (2026-08-29), on DS-143's precedent above.
    # `component.uncollapsed_motions` reads the deck's own keyframes and fails any motion whose
    # first painted frame is empty and which `@media print` does not switch off - which is what
    # made the printed page blank. It caught three: the two in `PR-80`, and `.opening` on its
    # first run. Kept as a comment rather than deleted, because the entry it replaces claimed the
    # whole rule was a look and a reader should be able to see which half stopped being one.
    # **The other half is still a person turning the sheet over** - a slide the reader never
    # advanced to, and whether what printed reads as a page - and that is CLAUDE.md rule 6 rather
    # than an excusal, which is exactly what DS-222's ruling says.
    "DS-225": ("The same ruling as DS-222. The count does reach half of it: a contents "
               "page that never rendered shows up as `n` rather than `n` + `k`.",
               ("look", None)),
    "DS-226": ("The most reached of the five, by two instruments measuring different things. "
               "`contents_bound.py` measures the compression bound the rule states - 16 entries "
               "with descriptions, 24 without - in a real browser, and exercises the split that "
               "keeps every sheet inside it; run separately because it sweeps seventeen sheet "
               "sizes and eight stage shapes rather than reading the deck in front of it. "
               "**And since T-123 the printed page itself is measured under `--print-pages`**: "
               "PRINT-2 and PRINT-3 above read the card rectangles out of the printed PDF and "
               "assert that none intersects and none reaches the footnote. *That clause said the "
               "geometry was measured, flat, while the same run printed `NOT RUN - opt-in` for "
               "those two rows three lines above it - so a default run's account claimed an "
               "instrument it had not used. DS-222's neighbouring entry had the conditional form "
               "right all along, which is what made the omission a slip rather than a question "
               "(`PR-46`, T-244).* What is still excused is the rest of the rule - "
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
    "DS-145": ("Triage: `default`. This rule is two clauses and only the second is decided. "
               "*Flows use dashed arrows, slowly animated* is DS-140's `Current renders dashed` "
               "row, which reads the dasharray off the render. **The reveal clause is decided by "
               "nothing.** *This entry used to excuse it on the ground that reveal motions are "
               "DS-140's starter set, checked statically there - wrong twice by the time it was "
               "read. DS-140's rows test the duration bands and the dash, and neither asks which "
               "motion a reveal uses; and T-187 opened the vocabulary on 2026-08-21, so there is "
               "no closed starter set left to check against. The entry also contradicted itself: "
               "it called the dashed-arrow clause covered while its closing condition asked for "
               "work on exactly that clause* (`PR-46`, T-244).",
               ("work", "a check that a hidden element's reveal opens, turns or scales")),
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
# not a clause, and listing it would inflate the account rather than sharpen it.
#
# **Which rules have been read is `SWEPT` below, tied to the ruleset** (T-244). This comment used
# to end *the sweep that produced this list read all 120 `hard` rules, 2026-08-18* - a dated
# sentence about a moving set, which is `L-136`'s shape: the ruleset held **130** `hard` rules by
# the time anyone checked, and **24** of them carried a later date, so the account's own statement
# of its coverage was the part that had gone stale. A sentence cannot notice that; `SWEPT` does.
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
    # ---- added by T-244 (`PR-43`), the two the register named -----------------------------------
    # Both reported `checked` on the strength of a row deciding one clause, which is the device
    # this table exists to see through: rule-level coverage is true of a partly-decided rule.
    "DS-073": (("carries all content, tier two included", True),
               ("carries it inlined - every panel open in normal flow", True),
               ("the disclosure control not rendered at all",
                "The two rows above decide what the reflow view CONTAINS; nothing decides what it "
                "must not contain. A control printed with nothing to reveal is the half of this "
                "rule that names a defect rather than a requirement, and it is unreached - the "
                "subject is in the DOM and cheap to read, which is why this is `work` and not an "
                "amendment. CLOSES WHEN: a check asserts no disclosure control renders in the "
                "reflow view, on the same subject `ds073_reflow` already walks.",
                ("work", "assert no disclosure control renders in the reflow view")),
               ),
    "DS-242": (("a lobby is single, first, and in front of an argument", True),
               ("the counter counts the argument rather than the file",
                "The row above decides the lobby's shape and says nothing about the counter. "
                "DS-216 counts *encodings of position* and finds two, which is a different "
                "question - that there are two, not that either is right. So a deck could number "
                "its lobby as slide 1 of 13 and pass both. CLOSES WHEN: a check reads the "
                "counter's total against the count of slides that are argument rather than "
                "matter, which the stage table already distinguishes.",
                ("work", "read the counter's total against the argument-slide count")),
               ("matter keeps its box on the printed contents page",
                "Print-only, and unlike DS-226's geometry no instrument reaches it: PRINT-2 and "
                "PRINT-3 measure card rectangles for collision, not whether a card is marked as "
                "matter. DS-225's excusal already says the page count reaches half of its own "
                "rule and no more, and this is the same boundary one rule along. CLOSES WHEN: a "
                "check under `--print-pages` asserts the contents page marks matter as matter, or "
                "the 2026-08-08 ruling is read as leaving this with the person who prints.",
                ("work", "assert matter is marked as matter on the printed contents page")),
               ),
}


# **What has been read, and the exact statement that was read** (T-244, `PR-43`). One entry per
# `hard` rule; the value is a digest of that rule's whole row in the ruleset at the moment somebody
# swept it and decided whether its statement is a conjunction.
#
# **The digest covers the whole row, amendment notes included, and that is deliberate.** A rule
# acquires a second testable assertion in exactly that prose - DS-218 gained one the day this was
# written - so a hash over some tidier slice of the row would go quiet at the moment the question
# matters. The cost is that any edit to a rule re-opens it, which is the intended friction: an edit
# is when to re-ask *did this become a conjunction?*
#
# **There is no `--sweep` writer, on purpose.** The failure prints the line to paste. A command that
# re-recorded the digest would let a rule be swept by running it, which is the one thing this
# structure exists to prevent - it would be the dated sentence again, with a nicer interface.
SWEPT = {
    "DS-001": "6b4c660297",
    "DS-002": "e158695597",
    "DS-003": "622428e293",
    "DS-005": "6caa275b79",
    "DS-006": "76618ad3ed",
    "DS-008": "6dae42fc7d",
    "DS-009": "e803f1f81a",
    "DS-010": "8ec58c5e4c",
    "DS-011": "abc73633b8",
    "DS-012": "633364d4c1",
    "DS-020": "ccda8ed425",
    "DS-021": "523ccc9311",
    "DS-026": "8e4d3c8480",
    "DS-027": "347f53242d",
    "DS-028": "f4c996952c",
    "DS-030": "bebf5098be",
    "DS-031": "c3f954be9d",
    "DS-032": "41ce762eda",
    "DS-033": "f5fb419124",
    "DS-034": "5fd9da0329",
    "DS-035": "295575bd77",
    "DS-036": "ca6e9090ca",
    "DS-040": "bf4859ead5",
    "DS-041": "db57ccba08",
    "DS-042": "96035ddf80",
    "DS-043": "084335da4e",
    "DS-044": "f0bc1a9508",
    "DS-045": "9263627110",
    "DS-060": "9d6ec81c4e",
    "DS-061": "97cfd160ad",
    "DS-062": "0ac68c6549",
    "DS-063": "e8a0bdf1ec",
    "DS-064": "3c6058e5d5",
    "DS-065": "511bb602f8",
    "DS-070": "004a6ed3b2",
    "DS-072": "1d5ae7eef0",
    "DS-073": "203165a5d2",
    "DS-074": "069716e374",
    "DS-075": "847b4a27c5",
    "DS-080": "66007ebf2d",
    "DS-081": "b2d96cb25e",
    "DS-084": "1cc1b86fc6",
    "DS-085": "40c2509277",
    "DS-090": "33c3591364",
    "DS-091": "d9a933935f",
    "DS-092": "8af674db55",
    "DS-093": "c8f4d7621c",
    "DS-097": "a2f334adfe",
    "DS-099": "13e91de6d5",
    "DS-100": "f49b6a7b3f",
    "DS-101": "1ef6a27347",
    "DS-102": "21f09dd01c",
    "DS-106": "73c9912936",
    "DS-107": "c84c20a9a6",
    "DS-110": "d3cec982ca",
    "DS-111": "eaef5cd7b5",
    "DS-112": "f7fb6dea85",
    "DS-113": "ef6c49615a",
    "DS-114": "5510649d43",
    "DS-116": "fc382f6aa7",
    "DS-117": "eae85236fb",
    "DS-118": "d2ff4f804e",
    "DS-119": "e9fde7cac3",
    "DS-120": "732da3a5e0",
    "DS-121": "8e0c6df3af",
    "DS-122": "16a1cf4073",
    "DS-123": "460e066d73",
    "DS-130": "b83cf68fe2",
    "DS-132": "6b909e6fa2",
    "DS-135": "8b9f2f112c",
    "DS-136": "dca68b60a0",
    "DS-137": "189e12c311",
    "DS-138": "041b5234a0",
    "DS-140": "aaf4830ee8",
    "DS-141": "c98bb96d44",
    "DS-142": "481a4a62c1",
    "DS-143": "22d9795e1a",
    "DS-144": "369c62ee3f",
    "DS-146": "f4a592f9e7",
    "DS-149": "dbd06a9f97",
    "DS-150": "5f63df59e6",
    "DS-160": "c176005ce9",
    "DS-161": "15bc84e731",
    "DS-162": "91e6518b4e",
    "DS-163": "3ebcfaaaf6",
    "DS-164": "29ac90f3c1",
    "DS-165": "5ad4f97ff2",
    "DS-166": "153d03bb00",
    "DS-167": "e7025afa05",
    "DS-168": "08e69e8e54",
    "DS-190": "24b6600b91",
    "DS-191": "45bd03b75f",
    "DS-200": "01e0869f9e",
    "DS-201": "1a0dc46927",
    "DS-202": "dd67289a12",
    "DS-203": "be76461730",
    "DS-204": "7cade605c9",
    "DS-205": "cc0ed7cbfb",
    "DS-207": "29e7c1a55d",
    "DS-208": "baf126a4b2",
    "DS-209": "183ca713ec",
    "DS-210": "004dabd0ba",
    "DS-211": "1d8f91e2e8",
    "DS-214": "528846f9cc",
    "DS-215": "f5e3501eda",
    "DS-218": "bac85949f7",
    "DS-219": "a2b3e36c18",
    "DS-220": "ff318bdb81",
    "DS-221": "ed8dca05dc",
    "DS-222": "2636751626",
    "DS-223": "1c5ab18cda",
    "DS-224": "2298231b8f",
    "DS-225": "5ea5e93909",
    "DS-226": "9478b4cb39",
    "DS-227": "f5733e555e",
    "DS-229": "b6c7605edc",
    "DS-230": "dc2a8d0544",
    "DS-231": "11db18d1a1",
    "DS-232": "75ae632f71",
    "DS-233": "11b9ee7ac4",
    "DS-235": "58ddad15f0",
    "DS-236": "648c32a0de",
    "DS-237": "266ea37604",
    "DS-238": "ea2430582b",
    "DS-239": "98c011e87a",
    "DS-240": "102cea8a8a",
    "DS-241": "f972c08048",
    "DS-242": "2cd3e89a8d",
    "DS-243": "9796e90016",
    "DS-244": "d4388e88b1",
}


# **Read, judged a conjunction, and its clause rows not written yet** (T-244).
#
# Without this set `SWEPT` says only *somebody read this*, and a reader takes that for *and found
# it states one thing* - so a conjunction could be swept into silence by the very record built to
# prevent it. The sweep of the 24 rules that had arrived under the dated sentence found **nine**
# conjunctions beyond the two the register named, which is four times the remedy's estimate and
# why they are a queue rather than an afternoon: each clause needs somebody to decide whether a
# check reaches it and to write a closing condition where none does.
#
# **This does not fail the run, and that is a decision rather than a softness.** It is a backlog of
# work with a named owner, in the shape `OWED-LOOKS.md` already uses; failing on it would make the
# gate red for as long as the queue is non-empty, which turns an honest count into a reason to
# stop counting. What DOES fail is a rule in here that is also in `CLAUSES` - the row exists, so
# the debt does not - or one nothing has swept.
CONJUNCTIONS_OWED = {
    "DS-110": "no rasterised diagram / no raster carrying the argument",
    "DS-122": "charts are hand-written SVG / a declared engine must emit SVG",
    "DS-141": "the 500 ms cap / eased rather than linear / the declared licence",
    "DS-146": "charts draw in once / the draw-in is Rise, not a stroke-dash",
    "DS-202": "one sentence / factual / not the headline restated",
    "DS-218": "the stop control is reachable / the deck still reads with motion off",
    "DS-229": "every part matches its contract row / every styled class has a row",
    "DS-230": "tier two answers a question the face provokes / it is one of four kinds",
    "DS-238": "density never reaches affordance motion / a content motion runs at or above its rank",
}


def sweep_debt(swept=None, clauses=None, owed=None):
    """`(faults, owed)` - the conjunctions read but not yet given rows, and any contradiction.

    The count is the point. A rule read and judged a conjunction is a known hole in the account
    until its clauses are written down, and the difference between a known hole and an unknown one
    is whether anybody wrote the number.
    """
    swept = SWEPT if swept is None else swept
    clauses = CLAUSES if clauses is None else clauses
    owed = CONJUNCTIONS_OWED if owed is None else owed
    faults = []
    for rid in sorted(owed):
        if rid in clauses:
            faults.append("SWEEP %s is owed clause rows and already has them - it is in CLAUSES, "
                          "so the debt is paid and the entry is stale" % rid)
        if rid not in swept:
            faults.append("SWEEP %s is recorded as a conjunction owing rows and has never been "
                          "swept - the two records disagree about whether anyone read it" % rid)
    return faults, sorted(owed)


def rule_rows(path=None):
    """`{rule id: the row's whole line}` for every rule the ruleset tabulates."""
    out = {}
    for line in io.open(path or ruleset.SPEC, encoding="utf-8"):
        if line.startswith("| DS-"):
            out[line.split("|")[1].strip()] = line.rstrip("\n")
    return out


def rule_digest(line):
    return hashlib.sha1(line.encode("utf-8")).hexdigest()[:10]


def sweep_faults(swept=None, rules=None, rows_by_id=None):
    """`[fault]` - every `hard` rule the clause sweep has not read, or has not read as it stands.

    Two kinds, and they are different failures. **UNSWEPT** is a rule that arrived after the last
    sweep: nobody has asked whether its statement is a conjunction, so a clause of it can be
    unreached without anything saying so. **CHANGED** is a rule whose row has moved since it was
    read, which is the same question re-opened rather than a new one.

    This is what replaces the dated sentence. A sweep recorded as prose cannot notice the ruleset
    growing under it; 24 rules had arrived or moved under the last one before anybody counted.

    **The population is every `hard` rule, not the ones this gate owns**, and the two differ by 34.
    The sweep asks *does this rule's statement carry more than one testable assertion*, which is a
    question about the rule; whether some check here reaches it is the next question and the one
    `CLAUSES` answers. Scoping the sweep to the jurisdiction would have excused a conjunction from
    being noticed on the ground that nothing checks it - which is the reasoning this whole account
    exists to refuse.
    """
    swept = SWEPT if swept is None else swept
    rows_by_id = rule_rows() if rows_by_id is None else rows_by_id
    rules = ruleset.load() if rules is None else rules
    hard = {r for r, v in rules.items() if getattr(v, "label", "") == "hard"}
    faults = []
    for rid in sorted(hard):
        line = rows_by_id.get(rid)
        if line is None:
            continue
        now = rule_digest(line)
        if rid not in swept:
            faults.append("SWEEP %s UNSWEPT - nobody has asked whether its statement is a "
                          "conjunction. Read it, add a CLAUSES row if it is, then record it: "
                          '"%s": "%s",' % (rid, rid, now))
        elif swept[rid] != now:
            faults.append("SWEEP %s CHANGED since it was read - re-read it and either add a "
                          'CLAUSES row or re-record: "%s": "%s",' % (rid, rid, now))
    # A recorded rule the ruleset no longer owns is the mirror fault, and it is the one that makes
    # this a partition rather than a floor.
    for rid in sorted(set(swept) - hard):
        faults.append("SWEEP %s recorded and not a `hard` rule the ruleset owns - the id was "
                      "renamed or its label changed" % rid)
    return faults


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
    "glitchfree.verdicts": "walks every slide in a real browser with a console trap listening. "
                           "Six of its seven conditions are facts about what the browser DID - "
                           "which faces loaded, which family text actually rendered in, whether a "
                           "canvas drew - and the markup states none of them (T-041)",
    "markhits.verdicts": "measures one diagram label's box against another's. The markup cannot "
                         "answer it either: how wide a label is depends on the face, and only a "
                         "browser with that face loaded knows (T-204)",
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
    rows += audit.eyebrow_verdicts(html)
    rows += audit.front_matter_verdicts(html)
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
    if os.path.isdir(deck):
        sys.exit("not a deck: %s is a directory. Point this at the .html file inside it."
                 % paths.display_path(deck, ROOT))
    if not os.path.isfile(deck):
        sys.exit("no such deck: %s" % paths.display_path(deck, ROOT))
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

    # DS-244, added by T-204. Its own render for `figgrid`'s reason: the tool owns the measurement,
    # and a second copy of the probe here is the composition that disagreed the first time either
    # half changed (**L-08**, **L-13**). Only its text-against-text half can fail a deck; the
    # label-on-line count travels in the row's text and gates nothing, which is the calibration
    # T-204 section 3 recorded rather than a hedge.
    rows += markhits.verdicts(deck)

    # DS-239, added by T-112. It takes the deck rather than the markup only because it reports the
    # path in its own row; the derivation itself is pure.
    rows += density.verdicts(deck)

    # GF-2 to GF-8, added by T-041. R6 section 8 decomposed CLAUDE.md rule 2 into nine conditions
    # for T-005 to implement; T-005's own criterion was narrower and seven of the nine were never
    # anyone's (**L-39**). Its own render for `figgrid`'s reason - the tool owns the measurement,
    # and a second copy of the probe here is the composition that disagreed the first time either
    # half changed (**L-08**, **L-13**). Condition 1 is DS-001 and condition 9 is a person, which
    # the closing text names rather than this list.
    rows += glitchfree.verdicts(deck)

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
                          for rid in clauses["clausesForRulesNotOwned"]]
                       + sweep_faults() + sweep_debt()[0])
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

    # **The sweep has to be able to fail, in both of its directions** (T-244). It is silent on a
    # tree where nothing has moved, which is the state it will be in on almost every run - so
    # without these two it is indistinguishable from a function that returns nothing (**L-36**,
    # and the same argument `theme.py`'s negative fixtures answer one file along).
    _rules, _rows = ruleset.load(), rule_rows()
    if sweep_faults(swept={k: v for k, v in SWEPT.items() if k != "DS-218"},
                    rules=_rules, rows_by_id=_rows) == []:
        sys.exit("SELF-TEST FAILED: a `hard` rule with no sweep record raised nothing. That is "
                 "the dated-sentence failure this replaced - a rule can arrive and no clause of "
                 "it is ever asked about")
    _moved = dict(_rows)
    _moved["DS-218"] = _moved["DS-218"] + " a second testable assertion."
    if sweep_faults(swept=SWEPT, rules=_rules, rows_by_id=_moved) == []:
        sys.exit("SELF-TEST FAILED: a rule whose row changed since it was swept raised nothing. "
                 "An amendment is exactly where a rule acquires a second clause")

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

    # The three readings `CE-19` asks for, and the flags that override them. The red case is
    # asserted above with a seeded failure; these are the two that decide a *green* run, and a
    # default that silently stopped depending on `isatty` is exactly what would go unnoticed.
    class Tty(object):
        def isatty(self):
            return True

    class Pipe(object):
        def isatty(self):
            return False

    if quiet_wanted([], stdout=Tty()):
        sys.exit("SELF-TEST FAILED: a run at a terminal would print one line. A person watching "
                 "loses the account, which is the half of L-153 that costs nothing to keep")
    if not quiet_wanted([], stdout=Pipe()):
        sys.exit("SELF-TEST FAILED: a piped green run would print the whole account. That is the "
                 "29,980 bytes CE-19 measured, paid again on every later turn of the session")
    if not quiet_wanted(["--quiet"], stdout=Tty()):
        sys.exit("SELF-TEST FAILED: --quiet did not win at a terminal")
    if quiet_wanted(["--report"], stdout=Pipe()):
        sys.exit("SELF-TEST FAILED: --report did not win when piped. It is the only way back to "
                 "the account from a captured stream")

    # Every verdict producer is in the static half or declared outside it. Here as well as in
    # `static_variants.py`, because the composition is this file's and a producer arrives here first.
    producer_split()
    return True


def quiet_wanted(argv, stdout=None):
    """Whether a green run prints one line (**L-153**). `--report` says no and `--quiet` says yes,
    outright; otherwise a terminal gets the account and anything else gets the line.

    **This tool prints most and was the last to get it.** Measured 2026-09-02 (`CE-19`): a green run
    printed **29,980 bytes** by default, up from 17,391 on 2026-08-13, against 398 under `--quiet` -
    and the four document tools had carried the rule since `T-286` while the one whose output a
    session actually captures did not. Nothing about the green account changes; what changes is that
    a captured stream stops paying for it on every later turn.
    """
    if "--report" in argv:
        return False
    if "--quiet" in argv:
        return True
    stdout = sys.stdout if stdout is None else stdout
    return not (hasattr(stdout, "isatty") and stdout.isatty())


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
        # **Printed at zero, like everything else in this account** (L-36). The sweep is silent on
        # a tree where no rule has moved, which is most runs - so the line that says how many
        # rules it read is the only evidence it is still reading them (T-244).
        print("\n  clause sweep       %3d `hard` rule(s) read, statement by statement"
              % len(SWEPT))
        _owed = sweep_debt()[1]
        print("    conjunctions owing rows %3d   %s" % (len(_owed), " ".join(_owed)))
        if _owed:
            print("      Read and judged conjunctions; their clause rows are not written yet, so "
                  "a clause of each\n      is unreached without this account being able to say "
                  "which. A counted backlog, not a\n      fault - it does not fail the run.")
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
gate was built to see (L-05, DS-191).

**A clean copy run is not "reads easily" either, and that is a second sentence rather than the
same one.** The two rules over copy measure LENGTH (DS-092) and a WORD LIST (DS-106). Neither
measures difficulty, and both were green on a deck whose own author called it hard - the difficulty
was vocabulary, noun stacks and abstraction (T-258, adopter report 025). Nothing here reads for
that, and nothing here should: a threshold on prose invites writing to the threshold. What exists
is a REPORT, which names the hardest lines and passes judgement on none of them:

    python tools/deck/readability.py <deck>

**And R6 section 8's ninth condition is a person.** GF-2 to GF-8 above decide conditions 2 to 8 and
DS-001 decides condition 1, so *renders glitch-free* is eight-ninths measured here. The ninth is
*looked at* - a human opens the deck offline and reads it - and it is not deferred, not excused and
not scheduled: no check replaces it and none ever will (L-01). CLAUDE.md rule 6 says what looking is
and what it excludes; `tasks/TASK-WORKFLOW.md` section 7 says when it is owed. **This gate reaching
green is the moment that becomes due, not the moment it is discharged.**""" % res["blindTo"])
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
    return report(res, quiet=quiet_wanted(argv))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
