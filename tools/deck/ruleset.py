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

Pure standard library (**L-07**).
"""

import io
import os
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
    return True


def main():
    self_test()
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
    sys.exit(main())
