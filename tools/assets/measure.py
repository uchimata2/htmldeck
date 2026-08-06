#!/usr/bin/env python3
"""Measure what each embeddable asset actually costs inside one HTML file.

The question T-013 asks is not "how big is this library" but "how many bytes does it add to a
deck that has to work with the network off". Those differ: a font is fetched as a per-script
subset, a script is inlined as text, and anything embedded as a `data:` URI pays a base64
surcharge. This measures the number that matters - bytes added to the .html - and nothing else.

Sources are the ones a browser would really use, not a mirror: the Google Fonts CSS API for the
per-subset woff2 a browser downloads, and jsDelivr for the minified dist a CDN tag would load.
So the figures are production bytes, not repository bytes.

Commands
--------
  fonts     latin-subset woff2 per family, raw and base64-inlined
  libs      minified library builds, raw, gzipped, and base64-inlined
  icons     individual SVG icons, per icon and per set of 24
  all       every one of the above
  selftest  check the measurement itself against hand-worked answers (L-04)

Downloads are cached in `.assets-cache/` (gitignored) so a re-run is offline and free. Pass
`--refresh` to re-fetch. Pure standard library, by L-07. Console output is ASCII - the Windows
console mangles em-dashes under cp1252 (L-10).
"""

import argparse
import base64
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, ".assets-cache")

# Google serves a different format to every browser generation. Ask as a current Chrome or the
# API returns full unhinted TTF - roughly ten times the bytes, and not what a deck would embed.
CHROME_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# Every family here is SIL Open Font License 1.1, which permits redistribution including
# embedding, provided the licence travels with the file. Verified per family by `licences.py`;
# this list is the measurement subject, not the licence record.
FONTS = [
    # (family, axis spec, role)
    ("Inter",                "wght@400..700", "text sans - the current default everywhere"),
    ("Source Sans 3",        "wght@400..700", "text sans - Adobe, wide language coverage"),
    ("IBM Plex Sans",        "wght@400;600",  "text sans - static weights only"),
    ("Public Sans",          "wght@400..700", "text sans - USWDS, plain by design"),
    ("Libre Franklin",       "wght@400..700", "text sans - Franklin Gothic lineage"),
    ("Instrument Sans",      "wght@400..700", "text sans - contemporary, less ubiquitous"),
    ("Figtree",              "wght@400..700", "text sans - geometric"),
    ("Source Serif 4",       "wght@400..700", "serif - pairs with Source Sans"),
    ("Newsreader",           "wght@400..700", "serif - editorial, optical sizes"),
    ("Fraunces",             "wght@400..700", "display serif - highly characterful"),
    ("Instrument Serif",     "",              "display serif - single weight"),
    ("Bricolage Grotesque",  "wght@400..700", "display grotesque - deliberately odd"),
    ("Space Grotesk",        "wght@400..700", "display grotesque - technical feel"),
    ("JetBrains Mono",       "wght@400..700", "mono - code and figures"),
    ("IBM Plex Mono",        "wght@400;600",  "mono - pairs with Plex Sans"),
]

# Minified production builds, from the path a CDN <script> tag would actually resolve to.
LIBS = [
    # (label, jsDelivr path, licence as verified, note)
    ("anime.js 4",   "npm/animejs@4/lib/anime.iife.min.js",        "MIT",       "motion"),
    ("motion 12",    "npm/motion@12/dist/motion.min.js",           "MIT",       "motion"),
    ("gsap 3",       "npm/gsap@3/dist/gsap.min.js",                "no-charge", "motion, not OSI"),
    ("three.js",     "npm/three@0.180.0/build/three.module.min.js", "MIT",      "3D"),
    ("reveal.js 5",  "npm/reveal.js@5/dist/reveal.js",             "MIT",       "deck framework"),
    ("impress.js 1", "npm/impress.js@1/js/impress.js",             "MIT",       "deck framework"),
    ("mermaid 11",   "npm/mermaid@11/dist/mermaid.min.js",         "MIT",       "diagrams"),
    ("chart.js 4",   "npm/chart.js@4/dist/chart.umd.js",           "MIT",       "charts"),
    ("d3 7",         "npm/d3@7/dist/d3.min.js",                    "ISC",       "charts, general"),
]

# One representative icon from each set, at the set's own default size and stroke. Icon sets are
# measured per icon because a deck inlines the dozen it uses, never the library.
ICONS = [
    ("lucide",           "npm/lucide-static@latest/icons/arrow-right.svg",        "ISC"),
    ("tabler",           "npm/@tabler/icons@latest/icons/outline/arrow-right.svg", "MIT"),
    ("phosphor",         "npm/@phosphor-icons/core@latest/assets/regular/arrow-right.svg", "MIT"),
    ("heroicons",        "npm/heroicons@latest/24/outline/arrow-right.svg",       "MIT"),
    ("feather",          "npm/feather-icons@latest/dist/icons/arrow-right.svg",   "MIT"),
    ("bootstrap-icons",  "npm/bootstrap-icons@latest/icons/arrow-right.svg",      "MIT"),
]

TYPICAL_ICONS_PER_DECK = 24


# ---------------------------------------------------------------------------- fetching

def fetch(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": CHROME_UA})
    for attempt in range(3):
        try:
            return urllib.request.urlopen(req, timeout=40).read()
        except (urllib.error.URLError, OSError) as exc:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))
            last = exc
    raise last


def cached(key, url, refresh=False, headers=None):
    """Fetch once, keep it. The cache is what makes a re-run offline and repeatable."""
    path = os.path.join(CACHE, key.replace("/", "_"))
    if os.path.exists(path) and not refresh:
        with open(path, "rb") as fh:
            return fh.read()
    data = fetch(url, headers)
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return data


# ---------------------------------------------------------------------------- measuring

def inlined_bytes(raw):
    """What a `data:` URI costs in the file. base64 is 4 bytes per 3, rounded up to a multiple
    of 4 with padding - the surcharge is a third, and it is paid on every embedded binary."""
    return len(base64.b64encode(raw))


def gzipped_bytes(raw):
    """What the deck costs in transit if it is ever served rather than double-clicked. It does
    not shrink the file on disk, which is the number a recipient actually sees."""
    return len(gzip.compress(raw, 9))


def kb(n):
    return "%.1f" % (n / 1024.0)


# ---------------------------------------------------------------------------- fonts

def font_css_url(family, axes):
    spec = family.replace(" ", "+")
    if axes:
        spec += ":" + axes
    return "https://fonts.googleapis.com/css2?family=%s&display=swap" % spec


def latin_woff2_url(css):
    """Pull the `latin` block's URL out of the CSS. Google emits one @font-face per script with
    a unicode-range; `latin` is the one a Western deck needs and the only one worth embedding.
    Taking any other block, or the first one, silently measures Cyrillic."""
    blocks = re.split(r"/\*\s*([a-z0-9-]+)\s*\*/", css)
    for i in range(1, len(blocks) - 1, 2):
        if blocks[i].strip() == "latin":
            m = re.search(r"url\((https://[^)]+\.woff2)\)", blocks[i + 1])
            if m:
                return m.group(1)
    return None


def cmd_fonts(args):
    rows = []
    for family, axes, role in FONTS:
        try:
            css = cached("css_" + family, font_css_url(family, axes), args.refresh).decode()
            url = latin_woff2_url(css)
            if not url:
                rows.append((family, None, None, "no latin subset returned", role))
                continue
            raw = cached("font_" + family, url, args.refresh)
            variable = "400..700" in axes or ".." in axes
            rows.append((family, len(raw), inlined_bytes(raw),
                         "variable" if variable else "static", role))
        except Exception as exc:                                  # noqa: BLE001 - report, continue
            rows.append((family, None, None, "FETCH FAILED: %s" % exc, role))

    print("\nFONTS - latin subset woff2, the file a browser downloads")
    print("%-22s %9s %9s  %-9s %s" % ("family", "raw KB", "b64 KB", "axes", "role"))
    print("-" * 96)
    for family, raw, b64, kind, role in sorted(rows, key=lambda r: (r[1] is None, r[1] or 0)):
        if raw is None:
            print("%-22s %9s %9s  %s" % (family, "-", "-", kind))
            continue
        print("%-22s %9s %9s  %-9s %s" % (family, kb(raw), kb(b64), kind, role))
    ok = sorted([r for r in rows if r[1]], key=lambda r: r[1])
    if ok:
        print("\n  cheapest %s at %s KB inlined; dearest %s at %s KB"
              % (ok[0][0], kb(ok[0][2]), ok[-1][0], kb(ok[-1][2])))
    return rows


# ---------------------------------------------------------------------------- libraries

def cmd_libs(args):
    rows = []
    for label, path, licence, note in LIBS:
        url = "https://cdn.jsdelivr.net/" + path
        try:
            raw = cached("lib_" + label, url, args.refresh)
            rows.append((label, len(raw), gzipped_bytes(raw), licence, note))
        except Exception as exc:                                  # noqa: BLE001
            rows.append((label, None, None, licence, "FETCH FAILED: %s" % exc))

    print("\nLIBRARIES - minified build, inlined as text in a <script> tag")
    print("%-14s %9s %9s  %-10s %s" % ("library", "raw KB", "gzip KB", "licence", "role"))
    print("-" * 96)
    for label, raw, gz, licence, note in sorted(rows, key=lambda r: (r[1] is None, r[1] or 0)):
        if raw is None:
            print("%-14s %9s %9s  %-10s %s" % (label, "-", "-", licence, note))
            continue
        print("%-14s %9s %9s  %-10s %s" % (label, kb(raw), kb(gz), licence, note))
    print("\n  JavaScript inlines as text, so raw KB is what it adds to the file;")
    print("  gzip KB only matters if the deck is ever served rather than opened from disk.")
    return rows


# ---------------------------------------------------------------------------- icons

def cmd_icons(args):
    rows = []
    for name, path, licence in ICONS:
        url = "https://cdn.jsdelivr.net/" + path
        try:
            raw = cached("icon_" + name, url, args.refresh)
            svg = raw.decode("utf-8", "replace")
            tight = re.sub(r">\s+<", "><", re.sub(r"\s+", " ", svg)).strip()
            rows.append((name, len(raw), len(tight.encode()), licence))
        except Exception as exc:                                  # noqa: BLE001
            rows.append((name, None, None, "FETCH FAILED: %s" % exc))

    print("\nICONS - one SVG, inlined as markup (never as a data: URI - see the note below)")
    print("%-18s %10s %10s %12s  %s"
          % ("set", "raw B", "minified B", "x%d KB" % TYPICAL_ICONS_PER_DECK, "licence"))
    print("-" * 96)
    for name, raw, tight, licence in sorted(rows, key=lambda r: (r[1] is None, r[1] or 0)):
        if raw is None:
            print("%-18s %10s %10s %12s  %s" % (name, "-", "-", "-", licence))
            continue
        print("%-18s %10d %10d %12s  %s"
              % (name, raw, tight, kb(tight * TYPICAL_ICONS_PER_DECK), licence))
    print("\n  Inline <svg> beats a data: URI on both counts: no base64 surcharge, and the icon")
    print("  inherits currentColor so one glyph themes with the deck instead of being a picture.")
    return rows


# ---------------------------------------------------------------------------- self-test

def cmd_selftest(args):
    """L-04: the measurement is believed only after it reproduces answers worked out by hand."""
    failures = []

    def check(label, got, want):
        if got != want:
            failures.append("%s: got %r, want %r" % (label, got, want))

    # base64 of 3 bytes is exactly 4; of 4 bytes it is 8 with padding. A measurement that does
    # not pay the padding is under-reporting every embedded font in the table.
    check("b64 of 3 bytes", inlined_bytes(b"abc"), 4)
    check("b64 of 4 bytes", inlined_bytes(b"abcd"), 8)
    check("b64 of 1000 bytes", inlined_bytes(b"x" * 1000), 1336)

    # gzip must shrink something repetitive and must not claim to shrink random-ish input much.
    check("gzip shrinks repetition", gzipped_bytes(b"a" * 10000) < 200, True)

    # The latin-subset picker is the one piece of real parsing here, and picking the wrong block
    # measures the wrong script entirely. Hand-built CSS with latin deliberately not first.
    css = ("/* cyrillic */\n@font-face { src: url(https://x/cyr.woff2) format('woff2');\n"
           "  unicode-range: U+0400-045F; }\n"
           "/* latin */\n@font-face { src: url(https://x/lat.woff2) format('woff2');\n"
           "  unicode-range: U+0000-00FF; }\n")
    check("latin subset picked", latin_woff2_url(css), "https://x/lat.woff2")
    check("absent latin reported", latin_woff2_url("/* greek */\n@font-face {}"), None)

    check("kb rounding", kb(1536), "1.5")

    if failures:
        print("SELFTEST FAILED - %d problem(s):" % len(failures))
        for f in failures:
            print("  " + f)
        return 1
    print("SELFTEST OK - 7 checks: base64 padding, gzip, latin-subset selection, rounding.")
    print("  It checks the arithmetic and the parsing, not whether a source URL still resolves.")
    return 0


# ---------------------------------------------------------------------------- entry

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["fonts", "libs", "icons", "all", "selftest"])
    ap.add_argument("--refresh", action="store_true", help="re-fetch instead of using the cache")
    ap.add_argument("--json", metavar="PATH", help="also write the raw figures as JSON")
    args = ap.parse_args()

    os.chdir(ROOT)

    if args.command == "selftest":
        return cmd_selftest(args)

    # The self-test runs first, always. A measurement nobody checked is a number, not evidence.
    if cmd_selftest(args) != 0:
        print("\nRefusing to measure with a failing self-test.")
        return 1

    out = {}
    if args.command in ("fonts", "all"):
        out["fonts"] = cmd_fonts(args)
    if args.command in ("libs", "all"):
        out["libs"] = cmd_libs(args)
    if args.command in ("icons", "all"):
        out["icons"] = cmd_icons(args)

    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(out, fh, indent=2)
        print("\nwrote %s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
