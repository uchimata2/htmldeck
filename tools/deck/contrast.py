#!/usr/bin/env python3
"""WCAG 2.2 contrast for a deck's theme tokens, read out of the deck itself.

`docs/DESIGN-SYSTEM.md` §7 makes the accessibility floor `hard`: 4.5:1 for text, 3:1 for large
text, UI components, focus indicators and meaningful graphics. Those are the rules that a look at
the rendered deck will never catch — a palette can be wrong by a ratio nobody can see by eye.

Tokens are parsed from the deck rather than restated here, so this cannot drift from what ships
(**L-13**). Runs its own self-test first and refuses to report if it fails (**L-04**).

    python tools/deck/contrast.py examples/reference-deck.html

Pure standard library (**L-07**).
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------- the maths

def _channel(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexstr):
    h = hexstr.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def self_test():
    """Known values from the WCAG definition. If these drift, nothing below is trustworthy."""
    checks = [
        ("#000000", "#FFFFFF", 21.0),
        ("#FFFFFF", "#FFFFFF", 1.0),
        ("#777777", "#FFFFFF", 4.48),   # the classic borderline grey
        ("#767676", "#FFFFFF", 4.54),   # one step darker clears 4.5
    ]
    for fg, bg, want in checks:
        got = ratio(fg, bg)
        if abs(got - want) > 0.02:
            sys.exit("SELF-TEST FAILED: ratio(%s,%s) = %.3f, expected %.2f" % (fg, bg, got, want))
    if abs(ratio("#000", "#FFF") - 21.0) > 0.02:
        sys.exit("SELF-TEST FAILED: three-digit hex not expanded")
    return True


# ---------------------------------------------------------------------------- token parsing

TOKEN = re.compile(r"--([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{3,8})\s*;")


def read_tokens(html):
    """Return {'light': {...}, 'dark': {...}} of colour tokens, dark inheriting from light."""
    light, dark = {}, {}

    root = re.search(r":root\s*\{(.*?)\}", html, re.S)
    if root:
        light = {m.group(1): m.group(2) for m in TOKEN.finditer(root.group(1))}

    dk = re.search(r':root\s*\[data-theme\s*=\s*"dark"\]\s*\{(.*?)\}', html, re.S)
    if dk:
        dark = dict(light)
        dark.update({m.group(1): m.group(2) for m in TOKEN.finditer(dk.group(1))})

    if not light:
        sys.exit("no :root colour tokens found - is this a deck?")
    return {"light": light, "dark": dark or dict(light)}


# ---------------------------------------------------------------------------- the pairs
# (label, foreground token, background token, required ratio, why)
#
# Decorative hairlines are deliberately absent: 1.4.11 covers UI components and graphics that
# carry meaning, not separators. `--line` is a separator; `--ui-line` and `--data-quiet` are not.
PAIRS = [
    ("body text on the ground",        "ink",        "paper",       4.5, "1.4.3 text"),
    ("secondary text on the ground",   "ink-soft",   "paper",       4.5, "1.4.3 text"),
    ("mono labels on the ground",      "ink-faint",  "paper",       4.5, "1.4.3 text"),
    ("mono labels on a sunk panel",    "ink-faint",  "paper-sunk",  4.5, "1.4.3 text"),
    ("mono labels on the accent wash", "ink-faint",  "accent-wash", 4.5, "1.4.3 text"),
    ("panel text on a sunk panel",     "ink-soft",   "paper-sunk",  4.5, "1.4.3 text"),
    ("accent text on the ground",      "accent",     "paper",       4.5, "1.4.3 text"),
    ("ground text on an accent fill",  "paper",      "accent",      4.5, "1.4.3 text"),
    ("positive role on the ground",    "pos",        "paper",       4.5, "1.4.3 text"),
    ("negative role on the ground",    "neg",        "paper",       4.5, "1.4.3 text"),
    ("caution role on the ground",     "caution",    "paper",       4.5, "1.4.3 text"),
    ("body text on the accent wash",   "ink",        "accent-wash", 4.5, "1.4.3 text"),
    ("interactive border",             "ui-line",    "paper",       3.0, "1.4.11 UI"),
    ("interactive border on a panel",  "ui-line",    "paper-sunk",  3.0, "1.4.11 UI"),
    ("focus indicator",                "accent",     "paper",       3.0, "1.4.11 focus"),
    ("accent data mark",               "accent",     "paper",       3.0, "1.4.11 graphic"),
    ("neutral data mark",              "data-quiet", "paper",       3.0, "1.4.11 graphic"),
]


def audit(html, verbose=True):
    themes = read_tokens(html)
    failures = []
    for theme in ("light", "dark"):
        T = themes[theme]
        if verbose:
            print("\n--- %s" % theme)
            print("    %-32s %-16s %7s %6s" % ("pair", "criterion", "ratio", "needs"))
        for label, fg, bg, need, why in PAIRS:
            if fg not in T or bg not in T:
                if verbose:
                    print("    %-32s %-16s %7s %6s  (token absent)" % (label, why, "-", need))
                continue
            r = ratio(T[fg], T[bg])
            ok = r >= need
            if not ok:
                failures.append((theme, label, T[fg], T[bg], round(r, 2), need))
            if verbose:
                print("    %-32s %-16s %7.2f %6.1f  %s"
                      % (label, why, r, need, "pass" if ok else "FAIL"))
    return failures


# DS-013's checkable clause is NOT the token names. The rule lists `--bg` where this deck ships
# `--paper`, so names are illustrative; what the rule spends its sentence on is the separation -
# **a data-series role and a UI-line role, both separate from `--line`** - because 1.4.11 puts a
# 3:1 obligation on a chart mark and an interactive border that a hairline separator does not
# carry. A deck reusing `--line` for either fails a criterion no token in the list names.
#
# Reading the deck's vocabulary by name couples this file to the one shipping theme, which DS-011
# fixes at one. T-007 owns the parametric layer; when it lands, this is the list that moves.
SEPARATE_FROM_LINE = ("ui-line", "data-quiet")


def verdicts(html):
    """(rule, what, ok) rows, in the shape every other stage returns.

    **The citation is the criterion number**, because §7 says so in its own words: *Criterion
    numbers are the IDs*. Until T-005 a contrast failure entered the gate's failure list as
    `contrast/<colour pair>`, which is a label rather than a rule - the same defect T-038 swept out
    of `audit.py`, one file over.

    Pair counts travel in the verdict text on purpose: a ratio check that evaluated no pairs reads
    exactly like one where every pair passed, and the count is what separates them (**L-36**).
    """
    themes = read_tokens(html)
    fails = audit(html, verbose=False)
    evaluated = {"1.4.3": 0, "1.4.11": 0}
    for theme in ("light", "dark"):
        T = themes[theme]
        for _label, fg, bg, _need, why in PAIRS:
            if fg in T and bg in T:
                evaluated["1.4.3" if why.startswith("1.4.3") else "1.4.11"] += 1
    text = [f for f in fails if f[5] == 4.5]
    nontext = [f for f in fails if f[5] != 4.5]

    # Read from the light theme's own declarations: dark inherits from light, so an override
    # cannot introduce a role that was never declared in the first place.
    T = themes["light"]
    bad = sorted(t for t in SEPARATE_FROM_LINE
                 if t not in T or ("line" in T and T[t] == T["line"]))
    # DS-027 - BOTH themes readable, and no component inverting into white-on-light. The second
    # clause is the mechanism of the first: a component that inverts renders light on light, which
    # is a ratio failure in one theme and a pass in the other. So the rule's subject is the pair of
    # themes, and its verdict is that both were evaluated and neither failed - which is a different
    # claim from 1.4.3's, and the reason it gets its own row rather than being folded in.
    per_theme = {}
    for theme in ("light", "dark"):
        T = themes[theme]
        n = len([1 for _l, fg, bg, _n, _w in PAIRS if fg in T and bg in T])
        per_theme[theme] = (n, len([f for f in fails if f[0] == theme]))

    return [
        ("DS-027", "both themes evaluated: light %d pairs / %d failing, dark %d pairs / %d failing"
         % (per_theme["light"][0], per_theme["light"][1],
            per_theme["dark"][0], per_theme["dark"][1]),
         per_theme["light"][0] > 0 and per_theme["dark"][0] > 0
         and not per_theme["light"][1] and not per_theme["dark"][1]),
        ("1.4.3", "text pairs under 4.5:1: %d of %d evaluated"
         % (len(text), evaluated["1.4.3"]), not text and evaluated["1.4.3"] > 0),
        ("1.4.11", "non-text pairs under 3:1: %d of %d evaluated"
         % (len(nontext), evaluated["1.4.11"]), not nontext and evaluated["1.4.11"] > 0),
        ("DS-013", "data and UI roles declared and distinct from --line: %s"
         % ("yes" if not bad else "no (%s)" % ", ".join(bad)), not bad),
    ]


def main(path):
    self_test()
    html = open(path, "r", encoding="utf-8").read()
    print("contrast audit - %s" % os.path.basename(path))
    failures = audit(html)
    print("\n%d failure(s)" % len(failures))
    for theme, label, fg, bg, r, need in failures:
        print("  %-6s %-32s %s on %s  %.2f:1 (needs %.1f)" % (theme, label, fg, bg, r, need))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(os.path.abspath(sys.argv[1]) if len(sys.argv) > 1
                  else os.path.join(os.path.dirname(os.path.dirname(
                      os.path.dirname(os.path.abspath(__file__)))),
                      "examples", "reference-deck.html")))
