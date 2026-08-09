#!/usr/bin/env python3
"""Read `docs/DESIGN-SYSTEM.md` as data: one record per `DS-nnn` rule.

**This exists so no list of rules is ever kept by hand.** A stored copy of a derivable fact drifts
on the first amendment (**L-08**), and the coverage account in `check.py` is exactly such a fact:
which rules the gate owns, which it may excuse, and which it has said nothing about. Adding a rule
to the ruleset has to change the gate's answer without anyone editing the gate.

**Parsing the `Reach` cell is the one subtle part.** Its value is the **leading token**; everything
after it is a free-text reason, introduced by an em dash that is punctuation rather than structure -
because `—` is itself a value, the same null the `Check` column uses at DS-007. Splitting on the
dash makes every `judge` row parse as empty, which is how the column's contract was written wrong
the first time (DESIGN-SYSTEM.md, *How to read a `Reach` cell*).

    python tools/deck/ruleset.py            # the table, and the counts that size a gate
    python tools/deck/ruleset.py --counts   # every figure the documents quote, derived
    python tools/deck/ruleset.py --gates    # every `hard` rule and which gate owns it

**`--counts` exists because the documents kept getting these wrong.** `EVALUATION.md` §1 records
the set going stale twice in three days and instructs *"re-derive them, never adjust them by
hand"* - and until T-043 nothing derived them, so re-deriving meant reading the table and
counting. Paste from this command; do not copy a figure out of another document.

Pure standard library (**L-07**).
"""

import io
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(ROOT, "docs", "DESIGN-SYSTEM.md")

LABELS = ("hard", "default", "guidance")
CHECKS = ("auto", "render", "judge", "—")
REACHES = ("yes", "never", "off-gate", "—")

# The `Check` values that put a rule inside a gate's jurisdiction. `judge` is the evaluator's and
# `—` belongs to the four rules that bind whoever builds a check rather than the deck.
OWNED = ("auto", "render")


class Rule(object):
    __slots__ = ("id", "text", "label", "check", "reach", "reason")

    def __init__(self, rid, text, label, check, reach, reason):
        self.id, self.text, self.label = rid, text, label
        self.check, self.reach, self.reason = check, reach, reason

    @property
    def owned(self):
        """In a gate's jurisdiction at all."""
        return self.check in OWNED

    @property
    def excused(self):
        """The RULESET itself says no check of this kind reaches it. Not the same as unbuilt: a
        rule nobody has got to yet is `yes` and is the gate's problem, not the ruleset's."""
        return self.reach in ("never", "off-gate")

    def __repr__(self):
        return "<%s %s/%s/%s>" % (self.id, self.label, self.check, self.reach)


def parse_row(line):
    """One `| DS-nnn | ... | label | check | reach |` row, or None if the line is not one.

    Reads the last three cells rather than fixed positions: the rule text routinely contains
    pipes inside code spans, so counting from the left finds the wrong columns.
    """
    if not line.startswith("| DS-"):
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 5:
        return None                     # a table without the Check/Reach pair - not a rule table
    rid, label, check, reach_cell = cells[0], cells[-3], cells[-2], cells[-1]
    text = "|".join(cells[1:-3]).strip()
    parts = reach_cell.split()
    reach = parts[0] if parts else ""
    reason = reach_cell[len(reach):].lstrip(" —-").strip()
    return Rule(rid, text, label, check, reach, reason)


def load(path=SPEC):
    rules = {}
    for line in io.open(path, encoding="utf-8"):
        r = parse_row(line)
        if r is None:
            continue
        if r.id in rules:
            sys.exit("RULESET: %s appears twice - IDs are permanent and never reused" % r.id)
        rules[r.id] = r
    if len(rules) < 100:
        sys.exit("RULESET: parsed only %d rules from %s - the format moved under the parser"
                 % (len(rules), path))
    return rules


def owned(rules=None):
    rules = rules if rules is not None else load()
    return {k: v for k, v in rules.items() if v.owned}


def off_table(path=SPEC, rules=None):
    """`(id, label)` for every rule ID the document uses that is not a row, in document order.

    **This is why two totals are in circulation, and the label is the half nobody wrote down.**
    DS-000 is the override clause, stated as prose in §0 as `(DS-000, guidance)` rather than as a
    row - so the table holds 160 with 5 `guidance` rules, and the document declares 161 with 6.
    Both published sets are right and neither says which rule moves between them.

    Derived rather than hard-coded, so a second prose rule shows up here instead of quietly
    widening the gap, and a citation of a rule ID that no longer exists shows up with no label.
    """
    rules = rules if rules is not None else load()
    seen, out = set(), []
    for line in io.open(path, encoding="utf-8"):
        for rid in re.findall(r"DS-\d{3}", line):
            if rid in rules or rid in seen:
                continue
            seen.add(rid)
            m = re.search(r"\(%s,\s*(\w+)\)" % rid, line)
            out.append((rid, m.group(1) if m and m.group(1) in LABELS else ""))
    return out


def counts(path=SPEC):
    """Every figure `BRIEF.md` and `EVALUATION.md` quote about the ruleset, derived in one pass.

    The one figure NOT here is the gate's own `checked` split, because that is a fact about a run
    against a deck rather than about the ruleset - `check.py` prints it, and deriving it here
    would mean rendering a deck to answer a question about a table.
    """
    rules = load(path)
    own = owned(rules)
    extra = off_table(path, rules)

    def tally(attr, values):
        return [(v, len([r for r in rules.values() if getattr(r, attr) == v])) for v in values]

    return {
        "rows": len(rules), "offTable": extra, "declared": len(rules) + len(extra),
        "byLabel": tally("label", LABELS),
        "byLabelDeclared": [(v, n + len([1 for _r, lab in extra if lab == v]))
                            for v, n in tally("label", LABELS)],
        "byCheck": tally("check", CHECKS),
        "byReach": tally("reach", REACHES),
        "owned": len(own),
        "ownedByCheck": [(v, len([r for r in own.values() if r.check == v])) for v in OWNED],
        "ownedAndHard": len([r for r in own.values() if r.label == "hard"]),
        "hardNotOwned": sorted(k for k, v in rules.items() if v.label == "hard" and not v.owned),
        "excusedByRuleset": sorted(k for k, v in own.items() if v.excused),
    }


def gates(path=SPEC):
    """Every `hard` rule, split by which gate owes a verdict for it.

    **`EVALUATION.md` describes these gates and must never list their members.** A list in prose
    is a stored copy of a derivable fact and drifts on the first amendment (**L-08**) - and this
    one drifted silently into twenty-five `hard` rules that were declared gates with nothing
    gating them, eleven of which the document never mentioned at all (T-042, F-3).
    """
    rules = load(path)
    hard = {k: v for k, v in rules.items() if v.label == "hard"}
    return {
        "mechanical": sorted(k for k, v in hard.items() if v.check in OWNED),
        "judgement": sorted(k for k, v in hard.items() if v.check == "judge"),
        "bindTheChecker": sorted(k for k, v in hard.items() if v.check == "—"),
        "hard": sorted(hard),
    }


def print_gates(path=SPEC):
    g = gates(path)
    rules = load(path)
    print("%s\n" % os.path.relpath(path, ROOT))
    print("  hard rules                        %3d" % len(g["hard"]))
    print("  gated mechanically (auto|render)  %3d   tools/deck/check.py" % len(g["mechanical"]))
    print("  gated by judgement (judge)        %3d   EVALUATION.md 1.1, the hard-judge checklist"
          % len(g["judgement"]))
    print("  bind the checker, not the deck    %3d   %s"
          % (len(g["bindTheChecker"]), " ".join(g["bindTheChecker"])))
    total = len(g["mechanical"]) + len(g["judgement"]) + len(g["bindTheChecker"])
    print("  ------------------------")
    print("  %3d %s" % (total, "= hard, so every hard rule has an owner"
                        if total == len(g["hard"]) else
                        "AGAINST %d hard - a hard rule is owned twice or not at all"
                        % len(g["hard"])))
    print("\n  THE HARD-JUDGE CHECKLIST - one pass/fail each, no scores")
    print("  %-8s %s" % ("ID", "RULE"))
    for k in g["judgement"]:
        print("  %-8s %s" % (k, rules[k].text[:96]))
    return 0


def print_counts(path=SPEC):
    c = counts(path)
    row = lambda pairs: "   ".join("%s %d" % (v, n) for v, n in pairs)   # noqa: E731
    print("%s\n" % os.path.relpath(path, ROOT))
    print("  rule rows in the table            %3d" % c["rows"])
    print("  + declared in prose, not a row    %3d   %s"
          % (len(c["offTable"]), " ".join("%s (%s)" % (r, lab or "no label")
                                          for r, lab in c["offTable"])))
    print("  = rule IDs the document declares  %3d   <- the figure that counts DS-000"
          % c["declared"])
    print("\n  by Label, rows only      %s   = %d" % (row(c["byLabel"]), c["rows"]))
    print("  by Label, declared       %s   = %d"
          % (row(c["byLabelDeclared"]), c["declared"]))
    print("      Both published sets are right. The rule that moves between them is DS-000, and")
    print("      it moves the `guidance` figure and nothing else.")
    print("\n  by Check   %s" % row(c["byCheck"]))
    print("  by Reach   %s" % row(c["byReach"]))
    print("      Reach and Check are counted over the ROWS, so `Reach —` is every `judge` rule")
    print("      PLUS the rules whose Check is `—`. It is not 'every judge rule'.")
    print("\n  owned by a gate                   %3d   %s" % (c["owned"], row(c["ownedByCheck"])))
    print("  owned and hard                    %3d" % c["ownedAndHard"])
    print("  hard but NOT owned                %3d   (judge, or Check `—`)" % len(c["hardNotOwned"]))
    print("  excused by the ruleset            %3d   %s"
          % (len(c["excusedByRuleset"]), " ".join(c["excusedByRuleset"])))
    print("\n  The gate's own checked/excused split is a fact about a RUN, not about this table:")
    print("      python tools/deck/check.py examples/reference-deck.html")
    return 0


def self_test():
    """Refuse to run if the parser has stopped agreeing with the document (**L-04**).

    Each assertion below is a property the coverage account depends on, not a spot check: a wrong
    `Reach` split silently converts 43 `judge` rules into rules the gate must account for.
    """
    row = parse_row("| DS-042 | Boxes that read as a set are siblings in one container. | hard "
                    "| auto | never — which boxes *read as a set* is a reading of the content |\n")
    if row is None or row.id != "DS-042":
        sys.exit("SELF-TEST FAILED: a well-formed rule row did not parse")
    if (row.label, row.check, row.reach) != ("hard", "auto", "never"):
        sys.exit("SELF-TEST FAILED: %r parsed as %s/%s/%s" % (row.id, row.label, row.check, row.reach))
    if not row.reason.startswith("which boxes"):
        sys.exit("SELF-TEST FAILED: the free-text reason was lost or kept its dash: %r" % row.reason)

    # The `—`-is-a-value trap. Splitting on the dash rather than on the leading token turns every
    # judge row into an empty value, and the gate then owes an account for 43 rules it never owned.
    null = parse_row("| DS-021 | The accent carries meaning wherever it appears. | hard | judge | — |\n")
    if null is None or null.reach != "—" or null.reason:
        sys.exit("SELF-TEST FAILED: a null Reach cell parsed as %r with reason %r"
                 % (null and null.reach, null and null.reason))
    if null.owned or null.excused:
        sys.exit("SELF-TEST FAILED: a judge rule is neither owned nor excused, and parsed as owned")

    # Pipes inside the rule text, which the real document has in every code span.
    piped = parse_row("| DS-013 | Core tokens: `--ink` | `--bg` and the rest. | default | auto | yes |\n")
    if piped is None or (piped.label, piped.check, piped.reach) != ("default", "auto", "yes"):
        sys.exit("SELF-TEST FAILED: a rule row with a pipe in its text lost its columns")

    if parse_row("| Criterion | Level | The number |\n") is not None:
        sys.exit("SELF-TEST FAILED: a non-rule table row parsed as a rule")

    rules = load()
    for r in rules.values():
        if r.label not in LABELS:
            sys.exit("RULESET: %s has label %r, which is not one of %s" % (r.id, r.label, LABELS))
        if r.check not in CHECKS:
            sys.exit("RULESET: %s has Check %r, which is not one of %s" % (r.id, r.check, CHECKS))
        if r.reach not in REACHES:
            sys.exit("RULESET: %s has Reach %r, which is not one of %s" % (r.id, r.reach, REACHES))
        if r.reach in ("never", "off-gate") and not r.reason:
            sys.exit("RULESET: %s is %r with no reason, which the column requires" % (r.id, r.reach))
        if r.check == "judge" and r.reach != "—":
            sys.exit("RULESET: %s is judge with Reach %r - judge rules are outside the gate's "
                     "jurisdiction and read `—`" % (r.id, r.reach))

    # Every published figure has to partition, or `--counts` is a prettier way to be wrong. The
    # vocabularies are closed (LABELS, CHECKS, REACHES) and every row is validated against them
    # above, so a tally that does not sum to the row count means a value went missing between the
    # two - which is how the `render` figure drifted by six before anyone re-derived it.
    c = counts()
    for name in ("byLabel", "byCheck", "byReach"):
        total = sum(n for _v, n in c[name])
        if total != c["rows"]:
            sys.exit("SELF-TEST FAILED: %s sums to %d against %d rule rows"
                     % (name, total, c["rows"]))
    if sum(n for _v, n in c["ownedByCheck"]) != c["owned"]:
        sys.exit("SELF-TEST FAILED: the owned rules do not split cleanly by Check")
    if c["declared"] <= c["rows"]:
        sys.exit("SELF-TEST FAILED: no rule is declared outside the table, so the 160/161 "
                 "discrepancy has no derived explanation - DS-000 was expected")

    # **Every `hard` rule has exactly one gate.** This is the partition F-3 found broken: 25 were
    # declared gates with nothing gating them, and nothing anywhere said so because no arithmetic
    # covered `hard` at all. Same device as `check.py`'s coverage account, one layer up.
    g = gates()
    owned = len(g["mechanical"]) + len(g["judgement"]) + len(g["bindTheChecker"])
    if owned != len(g["hard"]):
        sys.exit("SELF-TEST FAILED: %d hard rules split into %d owners - a hard rule is owned "
                 "twice or not at all" % (len(g["hard"]), owned))
    if not g["judgement"]:
        sys.exit("SELF-TEST FAILED: no hard rule is `judge`, so the checklist EVALUATION.md 1.1 "
                 "describes has no jurisdiction - one of the two is wrong")
    return True


def main(argv=()):
    self_test()
    if "--counts" in argv:
        return print_counts()
    if "--gates" in argv:
        return print_gates()
    rules = load()
    own = owned(rules)
    print("%s\n%d rules, %d owned by a gate (%d auto, %d render)"
          % (os.path.relpath(SPEC, ROOT), len(rules), len(own),
             len([r for r in own.values() if r.check == "auto"]),
             len([r for r in own.values() if r.check == "render"])))
    print("  owned and hard        %3d" % len([r for r in own.values() if r.label == "hard"]))
    print("  excused in the ruleset %2d   %s"
          % (len([r for r in own.values() if r.excused]),
             " ".join(sorted(k for k, v in own.items() if v.excused))))
    print("\n  %-8s %-8s %-7s %s" % ("ID", "LABEL", "CHECK", "REACH"))
    for k in sorted(own):
        r = own[k]
        print("  %-8s %-8s %-7s %s" % (r.id, r.label, r.check, r.reach))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
