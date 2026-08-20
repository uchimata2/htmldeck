#!/usr/bin/env python3
"""The half of a review a program can assemble, so the reviewer can spend on the half it cannot.

A critique has two halves and they are not equally hard. **The mechanical half is already decided
somewhere else** - `check.py` knows which rules failed, `ruleset.py` knows which rules no gate can
reach, `content.py` knows every figure and where it came from. A reviewer that re-derives those by
reading gets a count wrong (**L-08**), and worse, spends its attention there instead of on the five
dimensions and 26 `hard` rules nothing mechanical can see.

So this tool assembles the report's spine and **judges nothing**:

    python tools/deck/critique.py <deck> [--sources <dir>]        # the audit spine
    python tools/deck/critique.py <deck> --worksheet              # the hard-judge sheet, unanswered
    python tools/deck/critique.py --answers <file> [--deck <deck>]  # check a filled-in sheet

**The worksheet ships unanswered and this tool refuses an incomplete one.** `EVALUATION.md` 1.1:
one line per `hard` `judge` rule, `pass` / `fail` / an excusal in writing, and **a rule in none of
those three states fails the run**. That is the one thing a program can enforce about a judgement,
and it is enforced here rather than hoped for.

**It never prints a score.** `EVALUATION.md` 8.2 is settled - the outcome and the findings reach the
user, the numbers do not - and the safest way to honour that is for this tool never to be given
them. Counts of findings are facts about the report and are not scores.

Runs its own self-test first and refuses to report if it fails (**L-04**). Pure standard
library (**L-07**).
"""

import io
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import paths                                                        # noqa: E402
import ruleset as ruleset_mod  # noqa: E402  - sibling tools, not a package

ROOT = os.path.dirname(os.path.dirname(HERE))

# The three states EVALUATION.md 1.1 allows. Anything else is an unanswered row.
VERDICTS = ("pass", "fail", "excused")

# The five dimensions no mechanical check reaches, and the document that says so.
BLIND = (("S1", "Claim"), ("S2", "Evidence"), ("S4", "Density"),
         ("D1", "Spine"), ("D4", "Consistency"))

ANSWER = re.compile(r"^\s*(DS-\d{3})\s+(pass|fail|excused)\b\s*(.*)$", re.I)


def read(path):
    return io.open(path, encoding="utf-8", newline="").read()


# ------------------------------------------------------------------------------- the inputs


def judge_rules():
    """`[(id, text)]` - the hard rules only a person can decide, from the ruleset itself.

    Read through `ruleset.py` rather than listed here: a rule added to `DESIGN-SYSTEM.md` has to
    change this worksheet without anyone editing this file, which is the same reason `theme.py`
    parses its contract (**L-08**, **L-13**).
    """
    return sorted((rule.id, re.sub(r"\s+", " ", rule.text).strip())
                  for rule in ruleset_mod.load().values()
                  if rule.label == "hard" and rule.check == "judge")


def gate(deck, sources=None):
    """`check.py --json` for this deck, or a reason it could not run."""
    cmd = [sys.executable, os.path.join(HERE, "check.py"), deck, "--json"]
    if sources:
        cmd += ["--sources", sources]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    text = out.decode("utf-8", "replace")
    start = text.find("{")
    if start < 0:
        return None, (err.decode("utf-8", "replace") or text)[-400:]
    try:
        return json.loads(text[start:]), None
    except ValueError as exc:
        return None, "check.py --json did not parse: %s" % exc


# ------------------------------------------------------------------------------- the worksheet


def worksheet(rules):
    """The sheet a reviewer fills in. Unanswered on purpose."""
    lines = [
        "# Hard-judge checklist",
        "",
        "One line per rule: `<ID> pass`, `<ID> fail <what and where>`, or `<ID> excused <why, and",
        "what would close the excusal>`. A rule left off this sheet fails the run - that is",
        "EVALUATION.md 1.1, and it is the whole reason the sheet is generated rather than recalled.",
        "",
        "An excusal is about the INSTRUMENT, never the rule. \"No deck here has an appendix\" is a",
        "reason; \"hard to judge\" is not, and a hard rule that cannot be judged is a ruleset finding.",
        "",
    ]
    for ident, text in rules:
        lines.append("# %s  %s" % (ident, text[:96]))
        lines.append("%s " % ident)
        lines.append("")
    return "\n".join(lines)


def read_answers(text, rules):
    """`(answers, missing, unknown, bad)` for a filled-in sheet."""
    answers, bad = {}, []
    known = dict(rules)
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        match = ANSWER.match(line)
        if match:
            ident, verdict, note = match.group(1), match.group(2).lower(), match.group(3).strip()
            if verdict in ("fail", "excused") and not note:
                bad.append((ident, "%s with no reason written beside it" % verdict))
            answers[ident] = (verdict, note)
        elif line.strip():
            head = line.strip().split()[0]
            if re.match(r"^DS-\d{3}$", head):
                bad.append((head, "no verdict - one of %s" % ", ".join(VERDICTS)))
    missing = [i for i, _t in rules if i not in answers]
    unknown = [i for i in answers if i not in known]
    return answers, missing, sorted(unknown), bad


# ------------------------------------------------------------------------------- the spine


def spine(data, rules, sources_given):
    """The lines of the report a program can be trusted with. No judgement, no scores."""
    rows = data.get("rows", [])
    # **A verdict has three states and `not r["ok"]` reads two.** `ok is None` is NO SUBJECT - the
    # check ran and found nothing in this deck to judge - and `check.py` prints it as such while
    # passing the deck. Testing falsiness put those rows under a heading that tells the reviewer to
    # cite them, so a deck the gate passed arrived at the review carrying failures the gate never
    # declared. Reported against `0.4.0` by the first outside build (T-190), and it is T-051's
    # fault reflected: that one read absence as conformance, this one read absence as failure.
    failing = [r for r in rows if r.get("ok") is False]
    no_subject = [r for r in rows if r.get("ok") is None]
    out = []

    out.append("WHICH PASSES RAN")
    out.append("  auto and render     yes - %d rule row(s) decided" % len(rows))
    out.append("  content half        %s" % ("yes, against the sources supplied" if sources_given
                                             else "NO - presentation-only, and a clean report here "
                                                  "is not \"the content is right\""))
    out.append("  hard-judge          the worksheet below, %d rule(s), filled in by a person" % len(rules))
    out.append("  per-slide, whole-deck  the judgement pass - not this tool's, and not skippable")

    out.append("")
    out.append("WHAT THE GATE ALREADY DECIDED - cite these, do not re-find them")
    if failing:
        for r in failing:
            out.append("  FAIL  %-8s %s" % (r.get("rule", "?"), r.get("what", "")))
    else:
        out.append("  no mechanical failure. That is a deck carrying no defect the gate was built")
        out.append("  to see, which is not the same as a good deck (L-05).")

    # **NO SUBJECT is printed, and printed apart.** Silence would hand the reviewer the same wrong
    # picture the bug did, one direction over: a rule the gate could not judge is not a rule the
    # gate cleared, and which rules had no subject in this deck is exactly the kind of thing a
    # reviewer should know before deciding what the review has to cover itself.
    if no_subject:
        out.append("")
        out.append("WHAT THE GATE COULD NOT JUDGE - no subject in this deck, so nobody has decided")
        for r in no_subject:
            out.append("  --    %-8s %s" % (r.get("rule", "?"), r.get("what", "")))

    out.append("")
    out.append("WHAT NO CHECK IN THIS REPOSITORY REACHES - the review is these")
    for code, name in BLIND:
        out.append("  %-3s %s" % (code, name))
    out.append("  and the %d hard rule(s) on the worksheet." % len(rules))
    return out


def ledger(data, deck=None, sources=None):
    """The figure ledger, if the content half ran. `T-004` prioritises what `T-005` counted."""
    fig = [r for r in data.get("rows", []) if str(r.get("rule", "")).startswith("FIG-")]
    if not fig:
        return []
    out = ["", "THE FIGURE LEDGER - which wrong number matters is the review's call"]
    for r in fig:
        out.append("  %-6s %-58s %s" % (r.get("rule"), r.get("what", ""),
                                        "pass" if r.get("ok") else "FAIL"))
    out += source_pairs(deck, sources)
    return out


def source_pairs(deck, sources):
    """FIG-4 - two sources answering one question with two numbers.

    **Candidates, and they reach the reviewer rather than the gate**: no threshold separates a
    restatement that contradicts from a qualified pair that does not, so `content.py` stops at
    *same unit, four shared words, different values* and a person decides. Ten of these on a clean
    corpus is the measured rate, not a malfunction - `content.py`'s `SUBJECT_WORDS` records it.
    """
    if not (deck and sources):
        return []
    try:
        import content as content_mod
        pairs = content_mod.build_ledger(deck, sources)["sourceConflicts"]
    except Exception as exc:                                  # a reading aid must never block a run
        return ["", "  FIG-4  could not be read: %s" % exc]
    if not pairs:
        return ["", "  FIG-4  source pairs to read: none"]
    out = ["", "  FIG-4  source pairs to read - candidates a person confirms, never verdicts: %d"
           % len(pairs)]
    for oa, va, ob, vb, shared in pairs[:12]:
        out.append("      %s=%s / %s=%s  (%s)" % (oa[:26], va, ob[:26], vb, shared))
    return out


# ------------------------------------------------------------------------------- self-test


def self_test():
    """**Reports to stderr, unlike its siblings, and the reason is `--worksheet`.**

    That command's stdout is an artifact a reviewer redirects into a file and fills in. A banner on
    stdout puts twelve lines of provenance at the top of the sheet, and the tool that reads the
    sheet back then has to skip them. Provenance is not product.
    """
    failures, ran = [], []

    def ok(label, condition, detail=""):
        sys.stderr.write("  %-4s %-54s %s\n"
                         % ("ok" if condition else "FAIL", label, "" if condition else detail))
        ran.append(label)
        if not condition:
            failures.append(label)

    rules = judge_rules()
    ok("the worksheet is derived from the ruleset, not listed here",
       len(rules) >= 20 and all(re.match(r"^DS-\d{3}$", i) for i, _t in rules),
       "got %d rule(s)" % len(rules))

    sheet = worksheet(rules)
    ok("and it ships unanswered", all(("%s pass" % i) not in sheet for i, _t in rules))

    answers, missing, unknown, bad = read_answers(sheet, rules)
    ok("an unanswered sheet is reported as unanswered",
       not answers and len(missing) == len(rules))

    filled = "\n".join("%s pass" % i for i, _t in rules)
    answers, missing, unknown, bad = read_answers(filled, rules)
    ok("a complete sheet is accepted", len(answers) == len(rules) and not missing and not bad)

    one_short = "\n".join("%s pass" % i for i, _t in rules[1:])
    _a, missing, _u, _b = read_answers(one_short, rules)
    ok("one missing rule fails the run (EVALUATION 1.1)", missing == [rules[0][0]])

    _a, _m, _u, bad = read_answers("%s fail" % rules[0][0], rules)
    ok("a `fail` with no reason is refused", bool(bad))

    _a, _m, _u, bad = read_answers("%s excused" % rules[0][0], rules)
    ok("an `excused` with no reason is refused", bool(bad))

    _a, _m, _u, bad = read_answers("%s" % rules[0][0], rules)
    ok("a rule with no verdict is refused", bool(bad))

    _a, _m, unknown, _b = read_answers("DS-999 pass", rules)
    ok("a verdict for a rule that is not on the sheet is reported", unknown == ["DS-999"])

    fake = {"rows": [{"rule": "DS-001", "what": "zero external references", "ok": True},
                     {"rule": "DS-035", "what": "type under the floor", "ok": False},
                     {"rule": "DS-140", "what": "no dashed flow in this deck", "ok": None}]}
    text = "\n".join(spine(fake, rules, False))
    ok("the spine names the failure the gate already found", "DS-035" in text)
    # T-190. The whole defect in one assertion: a NO SUBJECT row must not reach the FAIL list.
    # **The first version of this line spelled the padding wrong and passed against the restored
    # bug** - the row prints as `FAIL  DS-140`, two spaces, and the assertion looked for five. An
    # assertion that cannot fail is the fixture failure this repository keeps finding (L-04), and
    # it was caught the only way it can be: by putting the defect back and running.
    ok("and a NO SUBJECT rule is not called a failure",
       "FAIL  DS-140" not in text and "COULD NOT JUDGE" in text)
    ok("and the rule the gate could not judge is still shown", "DS-140" in text)
    ok("and says so when the content half did not run", "presentation-only" in text)
    ok("and never prints a score",
       not re.search(r"\b\d+\s*/\s*(?:24|16)\b", text) and "score" not in text.lower())

    sys.stderr.write("\n%d of %d fixtures behaved as specified.\n\n"
                     % (len(ran) - len(failures), len(ran)))
    return failures


# ------------------------------------------------------------------------------- cli


def main(argv):
    if "--self-test" in argv:
        return 1 if self_test() else 0

    if not argv:
        print(__doc__.strip())
        return 2

    sys.stderr.write("Self-test first - a tool that has not been shown to fail is not "
                     "evidence (L-04).\n\n")
    if self_test():
        sys.stderr.write("SELF-TEST FAILED - the tool itself is wrong; anything below means "
                         "nothing.\n")
        return 2

    rules = judge_rules()

    answers_path = option(argv, "--answers")
    if answers_path:
        answers, missing, unknown, bad = read_answers(read(answers_path), rules)
        for ident in missing:
            print("  UNANSWERED    %s - no verdict on the sheet" % ident)
        for ident, why in bad:
            print("  INCOMPLETE    %s - %s" % (ident, why))
        for ident in unknown:
            print("  NOT A RULE    %s - a verdict for a rule the ruleset does not have" % ident)
        if missing or bad or unknown:
            print("\n%d rule(s) answered of %d. **The run fails** - EVALUATION.md 1.1: a rule in "
                  "none of\nthe three states is not a smaller version of the defect that section "
                  "removed." % (len(answers), len(rules)))
            return 1
        failed = [(i, n) for i, (v, n) in sorted(answers.items()) if v == "fail"]
        excused = [(i, n) for i, (v, n) in sorted(answers.items()) if v == "excused"]
        print("  %d rule(s) answered, all of them." % len(answers))
        print("  %d fail, %d excused in writing, %d pass."
              % (len(failed), len(excused), len(answers) - len(failed) - len(excused)))
        for ident, note in failed:
            print("    FAIL     %s  %s" % (ident, note))
        for ident, note in excused:
            print("    excused  %s  %s" % (ident, note))
        return 1 if failed else 0

    deck = argv[0]
    if "--worksheet" in argv:
        sys.stdout.write(worksheet(rules))
        return 0

    sources = option(argv, "--sources")
    data, why = gate(deck, sources)
    if data is None:
        sys.exit("could not read the gate for %s: %s" % (deck, why))

    print("deck:    %s" % paths.display_path(deck, ROOT).replace("\\", "/"))
    print("")
    for line in spine(data, rules, bool(sources)) + ledger(data, deck, sources):
        print(line)
    print("""
This is the spine, not the review. It says what was decided elsewhere and what nobody has
decided yet; it does not grade a slide, name an anti-pattern or rank a finding. Those are
skills/htmldeck/references/critique.md's, and they are the part a program cannot do (L-05).""")
    return 0


def option(argv, name):
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
        sys.exit("%s needs a value" % name)
    return None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
