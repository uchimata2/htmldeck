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
