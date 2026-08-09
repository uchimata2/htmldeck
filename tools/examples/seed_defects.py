#!/usr/bin/env python3
"""Derive the seeded-defect deck from the reference deck.

`docs/EVALUATION.md` §7: *a rubric that has never been tested is a rubric that passes
everything.* It requires a deck carrying one known defect per dimension, at score 0, so the
rubric's answer can be graded against a known answer.

The variant **derives** from the good deck rather than being written separately, so everything
except the seeded defect is held constant and the rubric's response is attributable (T-024 §1).

Every edit below asserts that it matched. A seeding script that silently no-ops produces a deck
with fewer defects than its own ledger claims, which is the one failure that would make the
validation worthless (L-04).

    python tools/examples/seed_defects.py            # regenerate the fixture
    python tools/examples/seed_defects.py --check    # fail if the committed fixture is stale

**`--check` exists because "everything except the seeded defect is held constant" is a claim about
a file on disk, and that claim went false twice without anything noticing** (T-044). The fixture
was four reference-deck revisions behind its parent, differing in 601 lines and failing two rules
its ledger does not name - and every gate in the repository was green throughout, because no gate
compares these two files. A resolution to remember was already tried; this is the check instead.

Pure standard library (L-07). Writes UTF-8 (L-10) with LF (L-11).
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "examples", "reference-deck.html")
DST = os.path.join(ROOT, "examples", "reference-deck-seeded-defects.html")

MARKER = "<!-- ============================================================ "

applied = []


def sub(html, dim, why, old, new, count=1):
    """Replace `old` exactly `count` times, or fail loudly."""
    n = html.count(old)
    if n != count:
        sys.exit("SEED %s: expected %d occurrence(s), found %d\n  %.120s" % (dim, count, n, old))
    applied.append((dim, why))
    return html.replace(old, new, count)


def split_slides(html):
    """Return (head, [slide blocks], tail) for the twelve stage sections."""
    start = html.index(MARKER + "1 ")
    end = html.index(MARKER + "chrome")
    body = html[start:end]
    parts = re.split(r"(?=<!-- =+ \d+ )", body)
    parts = [p for p in parts if p.strip()]
    if len(parts) != 12:
        sys.exit("expected 12 slide blocks, found %d" % len(parts))
    return html[:start], parts, html[end:]


def build():
    """The seeded deck as a string, plus nothing written. `main` decides what to do with it."""
    del applied[:]
    html = open(SRC, "r", encoding="utf-8").read()

    # ---------------------------------------------------------------- per-slide dimensions
    # S1 Claim - the heading becomes a topic label; the slide asserts nothing.
    html = sub(html, "S1", "slide 3 headline is a topic label, not a claim",
               '<h2 class="headline rise" style="--i:1">Eleven minutes decides this</h2>',
               '<h2 class="headline rise" style="--i:1">Wait times</h2>')
    html = sub(html, "S1", "and its slide name follows the topic label",
               'data-name="Eleven minutes decides this"', 'data-name="Wait times"')

    # S2 Evidence - a modelled projection is restated as an observation, and the assumptions
    # that qualified it are deleted. An unsourced figure presented as fact.
    html = sub(html, "S2", "slide 7 calls a modelled curve an observation",
               '<text class="lab" x="150" y="500">New daily trips · five years · modelled, not observed</text>',
               '<text class="lab" x="150" y="500">New daily trips · five years · observed across comparable cities</text>')
    # Retargeted by T-028 from the standfirst, which no longer asserts anything to corrupt: it
    # became setup when the deliverable moved to the bottom line. The bottom line is now where the
    # slide makes its claim, so it is where an unsourced claim has to be seeded.
    html = sub(html, "S2", "slide 7 bottom line asserts the projection as measured fact",
               '<b>Bike-share stops growing when its docks fill in\n    2029, and frequency is '
               'still adding trips in 2031.</b>',
               '<b>Bike-share stalls at 3,000 trips and frequency reaches 6,100, as the data '
               'shows.</b>')
    html = re.sub(r'\s*<div class="disc disc--edge" data-disc>.*?</div>\s*</div>\s*(?=<p class="provenance")',
                  "\n  ", html, count=1, flags=re.S)
    applied.append(("S2", "slide 7 assumption marker removed, so no figure is qualified"))

    # S3 Encoding - the before/after network becomes four boxes joined by arrow glyphs.
    old_fig = html[html.index('<svg class="fig" viewBox="0 0 1728 500" role="img"'):
                   html.index("</svg>", html.index('<svg class="fig" viewBox="0 0 1728 500" role="img"')) + 6]
    boxes = """<div class="seeded-boxes">
      <div class="seeded-box"><h4>North Line</h4><p>Route 3 to Centre</p></div>
      <div class="seeded-arrow">&#8594;</div>
      <div class="seeded-box"><h4>Centre</h4><p>Interchange</p></div>
      <div class="seeded-arrow">&#8594;</div>
      <div class="seeded-box"><h4>Market Cross</h4><p>Route 7 from Centre</p></div>
      <div class="seeded-arrow">&#8594;</div>
      <div class="seeded-box"><h4>Timed connection</h4><p>0 minutes</p></div>
    </div>"""
    html = sub(html, "S3", "slide 8 diagram replaced by a card row with arrow glyphs",
               old_fig, boxes)

    # S4 Density - the sentence that decides the slide moves into tier two, so the argument
    # only completes once something is opened.
    # Retargeted by T-028: this used to hollow out `.ledger-note`, which is gone - it became slide
    # 5's bottom line. The defect is unchanged: the deciding sentence moves into tier two and the
    # slot keeps a sentence that decides nothing.
    #
    # Note what the gate does with it. DS-202 and DS-205 both pass here: a bottom line is present
    # and it is not inside a panel. Only a reader can see that "Two options, six rows." is not a
    # deliverable. That is S4 being one of the five dimensions the gate cannot decide, working as
    # documented - not a hole in the checks T-028 added.
    html = sub(html, "S4", "slide 5's deciding line moved behind the disclosure",
               '''  <p class="bottom-line rise" style="--i:4"><b>Operating cost decides it: the grant pays for no
    staff in either column.</b></p>\n''',
               '  <p class="bottom-line rise" style="--i:4"><b>Two options, six rows.</b></p>\n')
    html = sub(html, "S4", "and reappears only inside the panel",
               '<div class="row"><span class="k">Capital</span><span>Both exclude land.',
               '<div class="row"><span class="k">Decides it</span><span>Operating cost. The grant '
               'cannot pay for either column\'s staff, so the general fund carries the difference.</span></div>\n'
               '      <div class="row"><span class="k">Capital</span><span>Both exclude land.')

    # S5 Craft - type below the design-unit floor, and a panel knocked off the grid.
    # A `font-size` attribute on the <g> would be inert: the <text> children carry a class whose
    # CSS font-size wins over an inherited presentation attribute. Seed it with a CSS rule that
    # actually outranks .fig .lab, or the ledger claims a defect the deck does not have.
    html = sub(html, "S5", "slide 6 corridor labels set below the 18-unit floor",
               '<g transform="translate(588,70)">', '<g transform="translate(588,70)" class="seeded-tiny">')
    html = sub(html, "S5", "and one panel shifted off its grid track",
               '<g transform="translate(1176,290)">', '<g transform="translate(1193,307)">')

    # S6 Motion - a continuous ambient pulse on static content, encoding nothing.
    # Retargeted by T-028, which removed the `.cost-aside` this used to throb. The bottom line is
    # the better host anyway: motion on the one element the slide exists to deliver.
    html = sub(html, "S6", "slide 10's bottom line given a looping ambient pulse",
               '<p class="bottom-line rise" style="--i:6"><b>Three corridors wait until month 18,',
               '<p class="bottom-line rise seeded-throb" style="--i:6"><b>Three corridors wait until month 18,')

    # ---------------------------------------------------------------- whole-deck dimensions
    # D3 Close - the ask becomes a recap and a thank-you.
    # Retargeted by T-028: the ask moved out of `.close-sub` and into the shared bottom-line slot.
    html = sub(html, "D3", "slide 12 ends on a summary and a thank-you, not an ask",
               '<h2 class="headline close-h rise" style="--i:1">Approve the frequency package</h2>',
               '<h2 class="headline close-h rise" style="--i:1">Thank you</h2>')
    html = sub(html, "D3", "and the ask becomes a recap",
               '''<b>On 12 March: $4.1M of the grant,
    $6.8M a year from the general fund, $1.5M held for the gate.</b>''',
               '<b>In summary: wait times are long, both options have merit, and frequency looks '
               'promising.</b>')
    html = sub(html, "D3", "and its slide name follows",
               'data-name="Approve the frequency package"', 'data-name="Thank you"')

    # D4 Consistency - the reserve disagrees with the ledger that established it.
    # Retargeted by T-028 from slide 9's standfirst to its bottom line, which is where the figure
    # lives now. A contradiction in the deliverable is a worse defect than one in the setup, so
    # this seed got stronger rather than weaker.
    html = sub(html, "D4", "slide 9 reserve contradicts slide 5's $1.5M",
               "and the\n    $1.5M reserve buys 16 Old Quarter stations if the gate fails.",
               "and the\n    $2.2M reserve buys 16 Old Quarter stations if the gate fails.")
    html = sub(html, "D4", "and again on the gate's own branch",
               '<text class="val t-soft" x="1290" y="130">$1.5M returns to the reserve</text>',
               '<text class="val t-soft" x="1290" y="130">$2.2M returns to the reserve</text>')

    # styles the seeded markup needs, plus the ambient animation S6 depends on
    html = sub(html, "--", "seeded styles",
               "</style>\n</head>",
               """
/* ---- seeded defects only. None of this belongs in a deck that is meant to pass. ---- */
.seeded-boxes{display:flex;align-items:center;gap:var(--sp-2);height:100%}
.seeded-box{flex:1;padding:var(--sp-3);border-radius:var(--radius);
  border:var(--hair) solid var(--ui-line);background:var(--paper-sunk)}
.seeded-box h4{font-family:var(--font-display);font-size:var(--fs-subhead)}
.seeded-box p{color:var(--ink-soft);margin-top:var(--sp-1)}
.seeded-arrow{font-size:calc(48*var(--du));color:var(--ink-faint)}
.fig .seeded-tiny .lab,.fig .seeded-tiny .name,.fig .seeded-tiny .val{font-size:11px}
.seeded-throb{animation:seededThrob 2.4s ease-in-out infinite}
@keyframes seededThrob{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.03);opacity:.82}}
</style>
</head>""")

    # ---- D1 Spine and D2 Pacing both reorder or pad the deck, so they run on whole blocks.
    head, slides, tail = split_slides(html)

    # D1 - the comparison arrives before the problem it compares against, and the timing
    # rationale lands after the argument is over. The sequence stops retiring objections.
    order = [0, 4, 5, 2, 3, 1, 6, 7, 8, 9, 10, 11]
    slides = [slides[i] for i in order]
    applied.append(("D1", "slides reordered so the ledger opens and Why-Now arrives ninth"))

    # D2 - the small multiple is split across three near-identical slides. Same archetype
    # three times running, and the length is set by dumping rather than by decision.
    idx = next(i for i, s in enumerate(slides) if 'data-name="Bikes win three corridors"' in s)
    base = slides[idx]
    part2 = base.replace('data-name="Bikes win three corridors"', 'data-name="Corridors, continued"')
    part2 = part2.replace("Bikes win three corridors", "Corridors, continued")
    part3 = base.replace('data-name="Bikes win three corridors"', 'data-name="Corridors, concluded"')
    part3 = part3.replace("Bikes win three corridors", "Corridors, concluded")
    slides[idx + 1:idx + 1] = [part2, part3]
    applied.append(("D2", "small multiple split into three near-identical slides (14 total)"))

    return head + "".join(slides) + tail


def ledger():
    """What was seeded, printed the same way whether the run wrote the file or only checked it."""
    print("%-4s %s" % ("DIM", "seeded defect"))
    for dim, why in applied:
        print("%-4s %s" % (dim, why))
    dims = sorted({d for d, _ in applied if d != "--"})
    print("\ndimensions carrying a seeded defect: %s (%d)" % (", ".join(dims), len(dims)))
    missing = [d for d in ("S1", "S2", "S3", "S4", "S5", "S6", "D1", "D2", "D3", "D4")
               if d not in dims]
    if missing:
        sys.exit("MISSING a seeded defect for: %s" % ", ".join(missing))


def self_test():
    """The comparison must be able to tell a stale fixture from a current one (**L-04**).

    Tested by mutating the freshly-built deck rather than by trusting `!=`: what has to work is
    that ONE changed line is caught, because the way this fixture goes stale is a handful of lines
    at a time in the deck it derives from - not a wholesale replacement.
    """
    fresh = build()
    if differs(fresh, fresh):
        sys.exit("SELF-TEST FAILED: a deck was reported stale against itself")
    nudged = fresh.replace("</body>", "<!-- one line -->\n</body>", 1)
    if nudged == fresh:
        sys.exit("SELF-TEST FAILED: the mutation used to test the comparison did not apply")
    if not differs(fresh, nudged):
        sys.exit("SELF-TEST FAILED: a one-line difference was not detected")
    return True


def differs(a, b):
    return a != b


def check():
    """Exit non-zero if the committed fixture is not what regenerating would produce."""
    fresh = build()
    if not os.path.exists(DST):
        print("STALE: %s does not exist" % os.path.relpath(DST, ROOT))
        return 1
    have = open(DST, "r", encoding="utf-8", newline="").read().replace("\r\n", "\n")
    if not differs(fresh, have):
        print("OK - %s is exactly what regenerating produces (%d bytes)"
              % (os.path.relpath(DST, ROOT), len(have.encode("utf-8"))))
        ledger()
        return 0
    import difflib
    diff = list(difflib.unified_diff(have.splitlines(), fresh.splitlines(),
                                     "committed", "regenerated", lineterm="", n=0))
    adds = len([d for d in diff if d.startswith("+") and not d.startswith("+++")])
    dels = len([d for d in diff if d.startswith("-") and not d.startswith("---")])
    print("STALE: %s no longer derives from %s"
          % (os.path.relpath(DST, ROOT), os.path.relpath(SRC, ROOT)))
    print("       regenerating would change %d line(s) (+%d/-%d).\n" % (adds + dels, adds, dels))
    for line in diff[:12]:
        print("  %s" % line[:150])
    if len(diff) > 12:
        print("  ... %d more diff line(s)" % (len(diff) - 12))
    print("\n**The fixture is the only evidence the rubric works, and it is only evidence while")
    print("everything except the seeded defect is held constant.** Run this without --check.")
    return 1


def main(argv=()):
    self_test()
    if "--check" in argv:
        return check()

    html = build()
    with open(DST, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print("wrote %s  (%.1f KB)\n" % (os.path.relpath(DST, ROOT), os.path.getsize(DST) / 1024))
    ledger()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
