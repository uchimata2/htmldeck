"""Mechanical extraction of the deck corpus into the local knowledgebase.

Counts what can be counted so the analysis rests on reproducible numbers rather than
recollection -- the "count, don't read" lesson in docs/BRIEF.md. Nothing here interprets;
interpretation happens in the write-up, against this output.

    python tools/kb/extract.py inventory   # classify + deduplicate the corpus tree
    python tools/kb/extract.py decks       # measure every deck
    python tools/kb/extract.py selftest    # verify the measurements on a known case

Writes to .kb/, which is gitignored: the corpus carries client and personal data and must
never publish. Pure standard library. Console output is ASCII; the Windows console mangles
anything else under cp1252.
"""

import hashlib
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KB = os.path.join(ROOT, ".kb")
CONFIG = os.path.join(KB, "config.json")

EXTS = (".md", ".html", ".htm", ".svg", ".js", ".py", ".css")

# Duplicate and third-party trees, as path substrings so they survive separator differences.
# Generic ones only -- anything naming a real client or project goes in the local config,
# which is gitignored. This file publishes; the corpus it reads must not leak into it.
DEFAULT_EXCLUDE = (
    "\\_export\\LocalWorkFiles",   # byte-identical local copies
    "\\_export\\Notion_HTML",      # exported HTML, not hand-authored
    "\\_export\\Notion_Markdown",
    " - Backup\\",                 # explicit backup trees
)


def load_config():
    """Corpus location and extra exclusions, from .kb/config.json or the environment.

    Kept out of this file deliberately: the path names a person and a client tree, and
    tools/ is published. Set HTMLDECK_CORPUS, or write .kb/config.json:
        {"corpus": "X:\\\\path\\\\to\\\\notes", "exclude": ["\\\\Some Client\\\\Source"]}
    """
    corpus = os.environ.get("HTMLDECK_CORPUS", "")
    extra = []
    if os.path.exists(CONFIG):
        with open(CONFIG, encoding="utf-8") as fh:
            cfg = json.load(fh)
        corpus = corpus or cfg.get("corpus", "")
        extra = cfg.get("exclude", [])
    if not corpus:
        sys.exit("No corpus configured. Set HTMLDECK_CORPUS or write .kb/config.json "
                 "-- see load_config() in this file.")
    if not os.path.isdir(corpus):
        sys.exit("Corpus path does not exist or is not reachable: %s" % corpus)
    return corpus, tuple(DEFAULT_EXCLUDE) + tuple(extra)


CORPUS, EXCLUDE = "", DEFAULT_EXCLUDE  # bound in main; selftest needs neither


def rel(path):
    """Corpus-relative path, or the path unchanged when it is not under the corpus.

    The self-test measures a synthetic string, which lives on no drive at all; relpath
    raises across Windows mount points rather than falling back.
    """
    try:
        return os.path.relpath(path, CORPUS)
    except ValueError:
        return path


def walk():
    """Yield every candidate file under the corpus, excluded paths removed."""
    for root, dirs, files in os.walk(CORPUS):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
        for name in files:
            full = os.path.join(root, name)
            if not name.lower().endswith(EXTS):
                continue
            if any(marker.lower() in (full + "\\").lower() for marker in EXCLUDE):
                continue
            yield full


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


# --------------------------------------------------------------------------- inventory

def cmd_inventory():
    """Classify every file and collapse content-identical duplicates."""
    seen, records = {}, []
    for full in walk():
        try:
            size = os.path.getsize(full)
            sha = digest(full)
        except OSError as exc:
            print("SKIP  %s (%s)" % (rel(full), exc))
            continue
        rec = {
            "path": rel(full),
            "ext": os.path.splitext(full)[1].lower().lstrip("."),
            "size": size,
            "sha256": sha[:16],
        }
        if sha in seen:
            rec["duplicate_of"] = seen[sha]
        else:
            seen[sha] = rec["path"]
        records.append(rec)

    records.sort(key=lambda r: (-r["size"], r["path"]))
    unique = [r for r in records if "duplicate_of" not in r]
    write_json("inventory/files.json", {
        "corpus": CORPUS,
        "total_files": len(records),
        "unique_files": len(unique),
        "duplicates": len(records) - len(unique),
        "by_ext": dict(Counter(r["ext"] for r in unique).most_common()),
        "files": records,
    })
    print("inventory: %d files, %d unique, %d duplicates collapsed"
          % (len(records), len(unique), len(records) - len(unique)))
    for ext, n in Counter(r["ext"] for r in unique).most_common():
        print("  %-5s %d" % (ext, n))


# ------------------------------------------------------------------------ measurement

EXTERNAL_REF = re.compile(
    r"""(?:src|href)\s*=\s*["']\s*(https?://|//)[^"']+""", re.I)
FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;}\n]+)", re.I)
HEX_COLOUR = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
CSS_VAR_DEF = re.compile(r"(--[\w-]+)\s*:\s*([^;}\n]+)")
AT_FONT_FACE = re.compile(r"@font-face", re.I)
DATA_URI_FONT = re.compile(r"url\(\s*['\"]?data:(?:application|font)[^)]*\)", re.I)

# Interaction and motion signals -- the owner's signature layer.
SIGNALS = {
    "details_summary": re.compile(r"<details\b", re.I),
    "checkbox_toggle": re.compile(r'type\s*=\s*["\']checkbox["\']', re.I),
    "target_anchor": re.compile(r":target\b"),
    "tabs": re.compile(r'\b(?:role\s*=\s*["\']tab["\']|class\s*=\s*["\'][^"\']*\btabs?\b)', re.I),
    "tooltip": re.compile(r"\btooltip\b|data-tip\b|\btitle\s*=", re.I),
    "flip_card": re.compile(r"\bflip\b|rotateY|backface-visibility", re.I),
    "modal_overlay": re.compile(r"\bmodal\b|\boverlay\b|\bdialog\b", re.I),
    "accordion": re.compile(r"\baccordion\b|\bcollaps", re.I),
    "css_transition": re.compile(r"\btransition\s*:", re.I),
    "css_animation": re.compile(r"@keyframes\b|\banimation\s*:", re.I),
    "transform_3d": re.compile(r"perspective|translateZ|rotate3d|preserve-3d", re.I),
    "canvas": re.compile(r"<canvas\b", re.I),
    "webgl": re.compile(r"getContext\(\s*['\"]webgl", re.I),
    "intersection_observer": re.compile(r"IntersectionObserver", re.I),
    "scroll_snap": re.compile(r"scroll-snap", re.I),
    "print_styles": re.compile(r"@media\s+print", re.I),
    "reduced_motion": re.compile(r"prefers-reduced-motion", re.I),
    "keyboard_nav": re.compile(r"(?:keydown|keyup|ArrowRight|ArrowLeft)", re.I),
    "dark_mode": re.compile(r"prefers-color-scheme", re.I),
    "grid": re.compile(r"display\s*:\s*grid", re.I),
    "flex": re.compile(r"display\s*:\s*flex", re.I),
    "clamp": re.compile(r"\bclamp\s*\(", re.I),
    "aria": re.compile(r"\baria-[\w-]+\s*=", re.I),
}

SLIDE_CONTAINER = re.compile(r"<(section|article)\b[^>]*", re.I)
HEADINGS = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.I | re.S)
TAG_STRIP = re.compile(r"<[^>]+>")


def looks_like_deck(path, text):
    """A deck, not a diagram fragment or a document export."""
    if not path.lower().endswith((".html", ".htm")):
        return False
    if len(text) < 4000:
        return False
    sections = len(SLIDE_CONTAINER.findall(text))
    return sections >= 4


def measure(path, text):
    lower = text.lower()
    sections = SLIDE_CONTAINER.findall(text)
    externals = [m.group(0)[:120] for m in EXTERNAL_REF.finditer(text)]

    families = []
    for m in FONT_FAMILY.finditer(text):
        fam = m.group(1).strip().strip("'\"")
        if fam and fam not in families:
            families.append(fam)

    palette = Counter(c.lower() for c in HEX_COLOUR.findall(text))
    tokens = {}
    for name, value in CSS_VAR_DEF.findall(text):
        tokens.setdefault(name, value.strip())

    headings = []
    for level, inner in HEADINGS.findall(text):
        txt = TAG_STRIP.sub(" ", inner)
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt:
            headings.append({"level": int(level), "chars": len(txt), "words": len(txt.split())})

    signals = {name: len(rx.findall(text)) for name, rx in SIGNALS.items()}

    return {
        "path": rel(path),
        "bytes": len(text.encode("utf-8")),
        "sections": len(sections),
        "script_tags": lower.count("<script"),
        "inline_svg": lower.count("<svg"),
        "img_tags": lower.count("<img"),
        "external_refs": len(externals),
        "external_ref_samples": externals[:10],
        "font_families": families[:12],
        "at_font_face": len(AT_FONT_FACE.findall(text)),
        "embedded_font_data_uri": len(DATA_URI_FONT.findall(text)),
        "distinct_hex_colours": len(palette),
        "top_colours": palette.most_common(12),
        "css_custom_properties": len(tokens),
        "css_custom_property_names": sorted(tokens)[:60],
        "headings": {
            "count": len(headings),
            "by_level": dict(Counter(h["level"] for h in headings)),
            "median_words": median([h["words"] for h in headings]),
            "max_words": max([h["words"] for h in headings], default=0),
        },
        "signals": {k: v for k, v in signals.items() if v},
    }


def median(values):
    if not values:
        return 0
    s = sorted(values)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else round((s[mid - 1] + s[mid]) / 2, 1)


def cmd_decks():
    decks, skipped, dupes, seen = [], 0, 0, {}
    for full in walk():
        if not full.lower().endswith((".html", ".htm")):
            continue
        text = read(full)
        if not looks_like_deck(full, text):
            skipped += 1
            continue
        # Belt and braces: the path exclusions catch known duplicate trees, content
        # hashing catches copies they miss. One deck measured twice skews every ratio.
        sha = digest(full)
        if sha in seen:
            dupes += 1
            continue
        seen[sha] = rel(full)
        decks.append(measure(full, text))

    decks.sort(key=lambda d: -d["sections"])
    write_json("inventory/decks.json", {"deck_count": len(decks), "decks": decks})

    print("decks: %d measured, %d html files skipped as non-decks\n" % (len(decks), skipped))
    print("%-52s %6s %5s %5s %5s %5s %6s" % ("deck", "KB", "sect", "svg", "ext", "scr", "vars"))
    for d in decks:
        print("%-52s %6d %5d %5d %5d %5d %6d" % (
            os.path.basename(d["path"])[:52], d["bytes"] // 1024, d["sections"],
            d["inline_svg"], d["external_refs"], d["script_tags"],
            d["css_custom_properties"]))

    agg = Counter()
    for d in decks:
        agg.update(d["signals"].keys())
    print("\ninteraction / motion signals, decks containing each:")
    for name, n in agg.most_common():
        print("  %-24s %d/%d" % (name, n, len(decks)))


# ---------------------------------------------------------------------------- selftest

SELFTEST_HTML = """<!doctype html><html><head>
<link rel="stylesheet" href="https://example.com/a.css">
<style>
:root { --brand: #ff0000; --ink: #123456; }
body { font-family: "Test Sans", serif; display: grid; }
@media print { .x { display: block } }
@keyframes spin { from { transform: rotate(0) } }
.card { transition: transform .3s; backface-visibility: hidden; }
</style></head><body>
<section><h1>One two three</h1><svg></svg></section>
<section><h2>Four five</h2><svg></svg><details><summary>d</summary></details></section>
<section><h2>Six</h2><canvas></canvas></section>
<section><h3>Seven eight nine ten</h3></section>
<script src="https://cdn.example.com/b.js"></script>
<script>document.addEventListener('keydown', e => e.key === 'ArrowRight')</script>
</body></html>"""

# Counted by hand from the string above.
EXPECTED = {
    "sections": 4,
    "script_tags": 2,
    "inline_svg": 2,
    "external_refs": 2,
    "at_font_face": 0,
    "css_custom_properties": 2,
}
EXPECTED_HEADINGS = {"count": 4, "by_level": {1: 1, 2: 2, 3: 1}, "median_words": 2.5, "max_words": 4}
EXPECTED_SIGNALS = ("details_summary", "canvas", "css_animation", "css_transition",
                    "flip_card", "print_styles", "keyboard_nav", "grid")


def cmd_selftest():
    got = measure("selftest.html", SELFTEST_HTML)
    failures = []

    for key, want in EXPECTED.items():
        if got[key] != want:
            failures.append("%s: expected %r, got %r" % (key, want, got[key]))

    for key, want in EXPECTED_HEADINGS.items():
        if got["headings"][key] != want:
            failures.append("headings.%s: expected %r, got %r" % (key, want, got["headings"][key]))

    for name in EXPECTED_SIGNALS:
        if name not in got["signals"]:
            failures.append("signal %s: expected detected, got absent" % name)

    if "#ff0000" not in dict(got["top_colours"]):
        failures.append("palette: expected #ff0000 among colours")
    if not any("Test Sans" in f for f in got["font_families"]):
        failures.append("font_families: expected 'Test Sans'")

    if failures:
        print("SELFTEST FAILED - %d problem(s):" % len(failures))
        for f in failures:
            print("  " + f)
        return 1
    print("SELFTEST OK - %d assertions on a hand-counted case" % (
        len(EXPECTED) + len(EXPECTED_HEADINGS) + len(EXPECTED_SIGNALS) + 2))
    return 0


# -------------------------------------------------------------------------------- glue

def write_json(relpath, payload):
    dest = os.path.join(KB, relpath.replace("/", os.sep))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    print("wrote %s" % os.path.join(".kb", relpath))


# ------------------------------------------------------------------------------- libs

# Library fingerprints, matched against the whole file so a vendored copy with no network
# reference is still detected -- the case that matters for T-013.
#
# Flags are scoped, not global. A blanket re.I made "THREE." match the ordinary word
# "three." in prose and reported three.js in two decks that have never referenced it.
# Filenames are matched case-insensitively; JS global objects are not.
LIBS = {
    "font-awesome": re.compile(r"(?i:font-?awesome)|\bfa-(?:solid|regular|brands|fw)\b"),
    "google-fonts": re.compile(r"(?i:fonts\.(?:googleapis|gstatic)\.com)"),
    "chart.js": re.compile(r"(?i:chart(?:\.umd)?(?:\.min)?\.js)\b|new\s+Chart\s*\("),
    "d3": re.compile(r"(?i:\bd3(?:\.v\d+)?(?:\.min)?\.js)\b|\bd3\.(?:select|scale)\w*\("),
    "gsap": re.compile(r"(?i:\bgsap(?:\.min)?\.js)\b|\bgsap\.(?:to|from|timeline)\b|TweenMax|ScrollTrigger"),
    "anime.js": re.compile(r"(?i:\banime(?:\.min)?\.js)\b|\banime\s*\(\s*\{"),
    "three.js": re.compile(r"(?i:\bthree(?:\.module)?(?:\.min)?\.js)\b|\bTHREE\.\w"),
    "lucide": re.compile(r"(?i:\blucide\b)"),
    "feather-icons": re.compile(r"(?i:feather-icons|feather\.min\.js)"),
    "aos": re.compile(r"(?i:\baos(?:\.min)?\.(?:js|css))\b|data-aos="),
    "particles": re.compile(r"(?i:(?:ts)?particles(?:\.min)?\.js)"),
    "tailwind": re.compile(r"(?i:tailwind)"),
    "bootstrap": re.compile(r"(?i:\bbootstrap(?:\.min)?\.(?:js|css))\b"),
    "mermaid": re.compile(r"(?i:\bmermaid(?:\.min)?\.js)\b|\bmermaid\.initialize"),
    "reveal.js": re.compile(r"(?i:\breveal(?:\.min)?\.(?:js|css))\b|\bReveal\.initialize"),
    "lottie": re.compile(r"(?i:\blottie(?:-\w+)?(?:\.min)?\.js)\b"),
    "highlight.js": re.compile(r"(?i:highlight(?:\.min)?\.js)\b|\bhljs\."),
    "stock-photos": re.compile(r"(?i:loremflickr|unsplash\.com|picsum\.photos)"),
}


def cmd_libs():
    """Which libraries the decks reach for, and whether they are linked or vendored."""
    rows, hosts = [], Counter()
    for full in walk():
        if not full.lower().endswith((".html", ".htm")):
            continue
        text = read(full)
        if not looks_like_deck(full, text):
            continue
        for m in EXTERNAL_REF.finditer(text):
            frag = m.group(0)
            host = frag.split("//")[-1].split("/")[0].strip("\"' ")
            if host:
                hosts[host] += 1
        found = {}
        for name, rx in LIBS.items():
            hits = len(rx.findall(text))
            if not hits:
                continue
            # Linked if the library's name appears inside an external reference.
            linked = any(rx.search(m.group(0)) for m in EXTERNAL_REF.finditer(text))
            found[name] = {"hits": hits, "linked": linked}
        rows.append({"path": rel(full), "libs": found})

    write_json("analysis/libraries.json", {"hosts": dict(hosts.most_common()), "decks": rows})

    tally = Counter()
    linked_tally = Counter()
    for r in rows:
        for name, info in r["libs"].items():
            tally[name] += 1
            if info["linked"]:
                linked_tally[name] += 1
    print("libraries detected across %d decks (linked = fetched over the network):\n" % len(rows))
    print("%-16s %8s %8s" % ("library", "decks", "linked"))
    for name, n in tally.most_common():
        print("%-16s %8d %8d" % (name, n, linked_tally[name]))
    print("\nexternal hosts:")
    for host, n in hosts.most_common():
        print("  %-34s %d" % (host, n))


COMMANDS = {"inventory": cmd_inventory, "decks": cmd_decks, "libs": cmd_libs,
            "selftest": cmd_selftest}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] != "selftest":
        CORPUS, EXCLUDE = load_config()
    sys.exit(COMMANDS[sys.argv[1]]() or 0)
