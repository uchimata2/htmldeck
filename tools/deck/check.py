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

Pure standard library (**L-07**), real Chrome offline through `render.py`.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render                                                       # noqa: E402
import ruleset                                                      # noqa: E402
import audit                                                        # noqa: E402
import contrast                                                     # noqa: E402
import contract                                                     # noqa: E402
import content                                                      # noqa: E402
import printpages                                                   # noqa: E402
import theme                                                        # noqa: E402

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
    "DS-041": "Which rows are *correlated* is a reading of the content. The DOM records the "
              "tracks; it does not record which values a reader expects to line up, so a grid "
              "can misalign and absolute coordinates can land true. The same limit put DS-042 at "
              "`Reach: never` in the ruleset. CLOSES WHEN: DS-041's `Reach` is reviewed against "
              "DS-042's, which is a ruleset edit and not this gate's.",
    "DS-101": "Bold in a data table is the value, not emphasis. The reference deck's A-04 ledger "
              "carries twelve bold runs and conforms; any count threshold either forbids the "
              "archetype or is set high enough to check nothing. CLOSES WHEN: the rule exempts "
              "tabular values, or the markup distinguishes emphasis from value. Measured: "
              "`data['boldRuns']`.",
    "DS-209": "Same subject as DS-101 one altitude up, and the same obstacle: separating the one "
              "emphasis from a row of bold figures is a reading. Measured and reported: "
              "`data['emphasisOutsideBottomLine']`.",
    "DS-117": "*Labelled* is a spatial-association judgement and the rule gives no distance. "
              "Measured on one conforming deck the connector-to-nearest-label gaps run 18, 32, "
              "56, 86 and 139 design units, so any threshold would be a number invented to fit "
              "this deck (**L-38**). CLOSES WHEN: connectors carry a structural association - an "
              "`aria-describedby`, a `<title>`, a shared group - which is a rule amendment.",
    "DS-026": "The rule requires a *visible* legend and nothing in the DOM declares one. The "
              "tripwire slide draws its legend as two SVG swatches with labels and no marker, so "
              "a class-based check reports it missing; the check exists and finds 1 of 2. CLOSES "
              "WHEN: DS-026 requires a legend to be identifiable, which would serve a screen "
              "reader too - but adopting it to make a check work is backwards, so it is the "
              "owner's.",
    "DS-120": "An accumulation effect is not a marked construct: nothing in the DOM says *this is "
              "meant to accumulate*, so the gate cannot find the rule's subject before judging "
              "it. CLOSES WHEN: a person watches the effect, which is CLAUDE.md rule 6 anyway.",
    "DS-149": "The defect is a z-order outcome and the rule names its cause. Observing it needs "
              "two elements that overlap and the wrong one winning, which the gate cannot "
              "construct from an arbitrary deck. CLOSES WHEN: looked at, or when a deck ships an "
              "overlap the gate can be pointed at.",

    # ---- built elsewhere, or waiting on a task that owns the subject
    # DS-143's excusal was CLOSED by T-016 (2026-08-09): `audit.reduced_motion_data` takes the
    # second render this entry called for, and `reduced_verdicts` reports three rows from it.
    # Kept as a comment rather than deleted, because the entry named its own closing condition and
    # a reader should be able to see that the condition is what happened.
    "DS-222": "The owner ruled the print row automates the PAGE COUNT and nothing else "
              "(2026-08-08). DS-222 to DS-226 are asserted by a person printing and looking, "
              "which CLAUDE.md rule 6 requires regardless; `print_variants.py` builds the "
              "variants for that. The count is checked here under `--print-pages`.",
    "DS-223": "The same ruling as DS-222. A slide staying a containing block for its own overlays "
              "is observable only in the printed output, where a panel that escaped its slide "
              "shows up scattered across a break - which is a look at paper, not a page count.",
    "DS-224": "The same ruling as DS-222. A slide that printed blank because its entrance "
              "animation never played still counts as a page, so the count cannot see it; what "
              "sees it is a person turning the sheet over.",
    "DS-225": "The same ruling as DS-222. The count does reach half of it: a contents "
              "page that never rendered shows up as `n` rather than `n` + 1.",
    "DS-226": "The same ruling as DS-222, and this one already has an instrument: "
              "`contents_bound.py` measures the compression bound the rule states - 16 entries "
              "with descriptions, 24 without - in a real browser, and is run separately because "
              "it sweeps nine deck sizes rather than reading the one in front of it.",

    # ---- `default` rules, held back by the owner's triage order: the account, then the hard ones
    "DS-004": "Triage: `default`. *Other engines degrade gracefully* is unobservable from a "
              "single-engine harness, which the ruleset's own `Reach` cell already says.",
    "DS-039": "Triage: `default`. `--measure` is declared and its 45-75ch band is a rendered "
              "line-length measurement this stage does not take.",
    "DS-047": "Triage: `default`. *Consistent margins, breathing room* needs a definition of "
              "consistent that the rule does not give.",
    "DS-049": "Triage: `default`. Card radius and shadow are measurable; nothing has needed it.",
    "DS-050": "Triage: `default`. The stage's field and shadow are measurable; nothing has "
              "needed it.",
    "DS-082": "Triage: `default`. The 8-12 band is measured and reported by the DS-081 row's "
              "count; *past 12 needs a recorded reason* is not in the HTML at all.",
    "DS-087": "Triage: `default`. No deck in the repository has an appendix, so the check would "
              "have no subject to run against and would pass on nothing (**L-36**).",
    "DS-104": "Triage: `default`. Assumption markers are present and their *subtlety* is the "
              "rule's content.",
    "DS-105": "Triage: `default`. The provenance mark is present on every slide; *never a dead "
              "link* is decidable and there are no links to test, DS-001 having banned them.",
    "DS-131": "Triage: `default`. The navigation set is present; *named targets* is checked in "
              "substance by DS-217's scale verdict, which requires no per-item label at rest.",
    "DS-133": "Triage: `default`. The progress indicator's *encodes real position* clause is a "
              "claim about the mapping, which DS-216 counts and does not verify.",
    "DS-134": "Triage: `default`. The spine exists and is lit; *the argument's structure is "
              "visible* is the rule's content.",
    "DS-139": "Triage: `default`. The assumption marker's edge placement is measurable; nothing "
              "has needed it.",
    "DS-145": "Triage: `default`. Reveal motions are DS-140's vocabulary, checked statically "
              "there; *flows use dashed arrows* is the DS-140 row.",
    "DS-147": "Triage: `default`. Count-up and the single pulse are present; *one per slide* is "
              "the DS-101 obstacle in miniature.",
    "DS-148": "Triage: `default`. No diagram in the repository changes mode, so the check would "
              "have no subject.",
}

# The five the rubric cannot reach, proven blind against the seeded-defect deck. Named on every
# run so a clean gate is never read as a good deck (**L-05**, DS-191).
BLIND = "S1 Claim, S2 Evidence, S4 Density, D1 Spine, D4 Consistency"


def gather(deck, sources=None, print_pages=False, skip_contract=False):
    """Every verdict, from every stage, as one list of `(rule, what, ok)` rows.

    Returns `(rows, data, notes)`. `notes` carries what a reader needs to know about the run
    itself - which halves ran, and anything that failed to measure.
    """
    html = open(deck, "r", encoding="utf-8").read()
    rows, notes = [], []

    rows += [(rule, what, bool(fn(html))) for rule, what, fn in audit.STATIC]
    rows += contrast.verdicts(html)
    # The theme region, added by T-007. Three partial checks of rules `audit` and `contrast`
    # already reach from another side: DS-011 counts palettes, this counts regions; DS-013 names
    # the roles, this holds the whole token set to `docs/THEME-CONTRACT.md`; DS-010 catches a
    # colour literal, this catches every other value a theme cannot reach.
    rows += theme.verdicts(html)

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
    else:
        notes.append("printed page count: NOT RUN - opt-in, printing is a mode and not a gate")

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
    silent = set(own) - cited - by_ruleset - deferred
    stale = deferred & (cited | by_ruleset)
    unknown = set(DEFERRED) - set(own)
    buckets = len(cited) + len(by_ruleset) + len(deferred) + len(silent)
    return {
        "owned": sorted(own), "checked": sorted(cited), "failing": sorted(failed),
        "excusedByRuleset": sorted(by_ruleset), "deferred": sorted(deferred),
        "silent": sorted(silent), "staleExcusals": sorted(stale),
        "silentNoSubject": sorted(no_subject & silent),
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
    audit.self_test()
    self_test()

    rows, data, notes, ledger = gather(deck, sources, print_pages, skip_contract)
    acct = account(rows)
    # `is False`, not `not ok`: a row that decided nothing is not a defect in the deck, and folding
    # it into the failure list would report a missing subject as a broken one (T-051).
    failures = [(r, w) for r, w, ok in rows if ok is False]
    if acct["silentNoSubject"]:
        notes.append("subject absent: %s - the check ran and this deck contains nothing for it to "
                     "judge, so the rule is undecided rather than passing"
                     % " ".join(acct["silentNoSubject"]))
    coverage_faults = (acct["silent"] + acct["staleExcusals"]
                       + acct["excusalsForRulesNotOwned"])
    if acct["partitionError"]:
        coverage_faults = coverage_faults + [
            "PARTITION %+d (buckets %d, owned %d)"
            % (acct["partitionError"], acct["bucketSum"], len(acct["owned"]))]
    return {
        "deck": os.path.relpath(deck, ROOT).replace("\\", "/"),
        "rows": [{"rule": r, "what": w, "ok": ok} for r, w, ok in rows],
        "account": acct,
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

    for rid, why in DEFERRED.items():
        if len(why) < 40:
            sys.exit("SELF-TEST FAILED: %s is excused in a phrase, not in writing" % rid)
    return True


def report(res, verbose=True):
    a = res["account"]
    print("deck:    %s" % res["deck"])
    for n in res["notes"]:
        print("         %s" % n)
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
    print("  SILENT               %3d   %s" % (len(a["silent"]), " ".join(a["silent"])))
    if a["silentNoSubject"]:
        print("      of which NO SUBJECT  %s" % " ".join(a["silentNoSubject"]))
        print("      The check ran and found nothing in this deck to judge. That is a different\n"
              "      fault from a rule with no check behind it, and it is fixed in the deck or in\n"
              "      the rule's jurisdiction rather than in the gate.")
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
    if a["staleExcusals"]:
        print("  STALE EXCUSAL        %3d   %s" % (len(a["staleExcusals"]),
                                                   " ".join(a["staleExcusals"])))
    if a["excusalsForRulesNotOwned"]:
        print("  EXCUSAL WITH NO RULE %3d   %s" % (len(a["excusalsForRulesNotOwned"]),
                                                   " ".join(a["excusalsForRulesNotOwned"])))
    if verbose and a["deferred"]:
        print("\n=== excused here, and what would close each")
        for rid in a["deferred"]:
            print("  %-8s %s" % (rid, DEFERRED[rid]))

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
    return report(res)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
