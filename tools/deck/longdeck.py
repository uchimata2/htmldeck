#!/usr/bin/env python3
"""Splice a deck to any slide count, so a long-deck question can be asked twice.

**Why this exists.** The ruler degrades past a measured capacity bound and everything known about
what that looks like was found on a deck built by hand, in a scratch directory, once (T-178). A
fixture that dies with the session cannot be re-rendered when the answer is questioned, so the
finding is unfalsifiable the moment the session ends - the same shape of problem as a number quoted
out of a comment (**L-36**). This makes the fixture a command.

    python tools/deck/longdeck.py examples/reference-deck.html 25
    python tools/deck/longdeck.py examples/reference-deck.html 43 --css candidate.css
    python tools/deck/longdeck.py examples/reference-deck.html 17 --name probe-a
    python tools/deck/longdeck.py examples/reference-deck.html 25 --solo-stage
    python tools/deck/longdeck.py --self-test

**What it does not do, deliberately.** The spliced deck is a *fixture*, not a deck this repository
ships: filler slides carry no argument and the original slides keep their printed eyebrow numbers,
which go stale the moment anything is inserted before them. Nothing here reads those numbers - the
ruler is built from `manifest()`, which derives every entry from the sections themselves - and
renumbering them would mean editing twelve authored slides to answer a question about the twelfth
pixel of a tick. If a future question needs them correct, that is a change to this tool and it
should say why.

**Section count is held fixed on purpose.** Fillers are inserted at the end of the stage run they
belong to, never as a new stage, so a deck spliced from 13 to 43 still has seven section marks. That
is what makes the fixture answer the question it was built for: what changes with length is the
number of *small* marks competing with a fixed number of large ones.

**`--solo-stage` moves where one stage ends, and changes nothing else.** It leaves the
second-to-last stage holding a single slide, which is the only arrangement that puts two section
marks side by side on the ruler - and it is a shape length alone never reaches, however long the
deck gets. `T-263` needs it: past the dense threshold two adjacent section marks were what made the
ruler's own `data-scale` claim unverifiable, and the fixture proving that has to be a command for
the same reason this whole tool is one.

Pure standard library (**L-07**). Output goes to the **deck's own project** (T-074), via `paths`.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SLIDE_OPEN = re.compile(r'<section class="slide[^"]*"')
STAGE_ATTR = re.compile(r'data-stage="([^"]*)"')
STAGES_JS = re.compile(r"var STAGES\s*=\s*\[([^\]]*)\]")

FILLER = """<section class="slide" data-name="%(name)s" data-stage="%(stage)s" aria-label="Slide %(n)d">
  <header>
    <p class="eyebrow rise" style="--i:0"><span class="tick"></span>%(nn)s &middot; %(stagename)s</p>
    <h2 class="headline rise" style="--i:1">%(name)s</h2>
  </header>
  <div class="body">
    <p class="rise" style="--i:2">Filler slide, spliced in by longdeck.py to reach the fixture
    length. It carries no argument: the navigator is the subject, not the page.</p>
  </div>
  <p class="bottom-line">Filler slide %(nn)s carries no claim.</p>
</section>
"""


def stage_names(html):
    """The deck's own stage names, read out of its shipped script.

    Read rather than assumed, because a filler that names a stage the deck does not have would put
    a wrong label under a tick and the picture would be of the fixture's defect, not the deck's.
    """
    m = STAGES_JS.search(html)
    if not m:
        return []
    return [s.strip().strip("'\"") for s in m.group(1).split(",") if s.strip()]


def split_slides(html):
    """`(head, [slide, ...], tail)` - the slides as raw strings, in document order.

    Split on the opening tag rather than parsed, and the closing `</section>` is never searched for:
    a slide ends where the next one begins, and the last ends at `</main>`. That holds whatever a
    slide contains, which a nesting-aware split would have to be taught.
    """
    starts = [m.start() for m in SLIDE_OPEN.finditer(html)]
    if not starts:
        return html, [], ""
    end = html.find("</main>", starts[-1])
    if end < 0:
        end = len(html)
    bounds = starts + [end]
    return (html[:starts[0]],
            [html[bounds[i]:bounds[i + 1]] for i in range(len(starts))],
            html[end:])


def stage_of(slide):
    m = STAGE_ATTR.search(slide)
    return m.group(1) if m else ""


def solo_stage(content):
    """`content` with one stage left holding a single slide, so two section marks sit side by side.

    The ruler marks the **first** slide of each stage, so two marks are adjacent only where a stage
    holds exactly one slide - and nothing else about a deck produces that arrangement. That makes
    it a shape a fixture has to ask for rather than one a longer deck arrives at, which is why it
    is a flag here instead of a length (T-263).

    The stage **set** is unchanged, which is the property `--solo-stage` shares with the splice
    itself: the tail of the second-to-last stage is reassigned to the last one, so the same stages
    exist and the same slides are in the same order. Only where one stage ends and the next begins
    moves.
    """
    order = []
    for s in content:
        st = stage_of(s)
        if st not in order:
            order.append(st)
    if len(order) < 2:
        raise ValueError("a solo stage needs at least two stages; this deck has %d" % len(order))
    donor, host = order[-2], order[-1]
    seen = 0
    out = []
    for s in content:
        if stage_of(s) == donor:
            seen += 1
            if seen > 1:
                s = STAGE_ATTR.sub('data-stage="%s"' % host, s, count=1)
        out.append(s)
    return out


def build(html, target, solo=False):
    """The deck respliced to `target` slides. Raises `ValueError` when that is fewer than it has.

    Shortening is refused rather than implemented: dropping authored slides would silently change
    which stages exist, and every question this fixture serves is about *more* slides than the
    capacity bound, never fewer.
    """
    head, slides, tail = split_slides(html)
    if not slides:
        raise ValueError("no slides found - is this a deck?")
    names = stage_names(html)
    content = [s for s in slides if stage_of(s) != "back"]
    back = [s for s in slides if stage_of(s) == "back"]
    need = target - len(slides)
    if need < 0:
        raise ValueError("deck already has %d slides; cannot splice down to %d"
                         % (len(slides), target))

    # The distinct stages, in the order the deck introduces them. Fillers are shared out over these
    # round-robin, so a long fixture stays roughly proportioned rather than growing one stage.
    order = []
    for s in content:
        st = stage_of(s)
        if st not in order:
            order.append(st)
    share = {st: 0 for st in order}
    for i in range(need):
        share[order[i % len(order)]] += 1

    out, n = [], 0
    for st in order:
        for s in content:
            if stage_of(s) == st:
                n += 1
                out.append(renumber(s, n))
        for _ in range(share[st]):
            n += 1
            sname = names[int(st)] if st.isdigit() and int(st) < len(names) else "Stage %s" % st
            out.append(FILLER % {"name": "Filler slide %02d" % n, "stage": st, "n": n,
                                 "nn": "%02d" % n, "stagename": sname})
    if solo:
        out = solo_stage(out)
    for s in back:
        n += 1
        out.append(renumber(s, n))
    return head + "".join(out) + tail


def renumber(slide, n):
    """`aria-label="Slide N"` brought back into line with the slide's new position.

    Only the accessible name. The eyebrow's printed number is left alone - see the module docstring.
    """
    return re.sub(r'aria-label="Slide \d+"', 'aria-label="Slide %d"' % n, slide, count=1)


def inject_css(html, css):
    """`css` appended to the deck's last `<style>` block, so it wins on source order.

    The **last** block, not the first: a deck carries several, and a candidate treatment that lands
    in an earlier one is overridden by the shipped rule it was written to replace - which looks
    exactly like a candidate that does not work.
    """
    i = html.rfind("</style>")
    if i < 0:
        raise ValueError("no </style> in the deck - nowhere to put the candidate CSS")
    return html[:i] + "\n/* ---- longdeck.py: candidate treatment ---- */\n" + css + "\n" + html[i:]


def write(deck, target, out=None, css=None, name=None, solo=False):
    html = open(deck, encoding="utf-8").read()
    spliced = build(html, target, solo=solo)
    if css:
        spliced = inject_css(spliced, css)
    dest_dir = out or os.path.join(paths.output_root(deck), ".assets-cache", "deck")
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    dest = os.path.join(dest_dir, "%s.html" % (name or "longdeck-%02d" % target))
    # Binary, and `\n` kept as written: text mode on Windows rewrites every line ending, which
    # changes the byte size of a fixture whose size is sometimes the thing being compared.
    with open(dest, "wb") as fh:
        fh.write(spliced.encode("utf-8"))
    return dest


def self_test():
    deck = os.path.join(ROOT, "examples", "reference-deck.html")
    if not os.path.isfile(deck):
        print("skip  self-test needs examples/reference-deck.html, which is not here")
        return
    html = open(deck, encoding="utf-8").read()
    _, slides, _ = split_slides(html)
    base = len(slides)
    fail = []

    if base < 2:
        fail.append("split_slides found %d slide(s) in the reference deck - the split is wrong, "
                    "and every assertion below would pass vacuously" % base)

    for target in (17, 25, 43):
        got = build(html, target)
        _, out, _ = split_slides(got)
        if len(out) != target:
            fail.append("splicing to %d produced %d slide(s)" % (target, len(out)))
        # The property the fixture exists for: length changes, section count does not.
        was = sorted({stage_of(s) for s in slides})
        now = sorted({stage_of(s) for s in out})
        if was != now:
            fail.append("splicing to %d changed the stage set %r -> %r, so the fixture would have "
                        "a different number of section marks and answer a different question"
                        % (target, was, now))
        if got.count('data-stage="back"') != html.count('data-stage="back"'):
            fail.append("splicing to %d changed the back-matter count" % target)

    # `--solo-stage` produces the one arrangement length never reaches: two adjacent section marks.
    # Asserted on the SEQUENCE rather than on the flag, because what the fixture claims is a
    # property of the ruler the deck builds, not of the option that asked for it.
    def firsts(seq):
        out, seen = [], set()
        for i, st in enumerate(seq):
            if st != "back" and st not in seen:
                seen.add(st)
                out.append(i)
        return out

    plain = [stage_of(s) for s in split_slides(build(html, 25))[1]]
    solo = [stage_of(s) for s in split_slides(build(html, 25, solo=True))[1]]
    if len(plain) != len(solo):
        fail.append("--solo-stage changed the slide count %d -> %d" % (len(plain), len(solo)))
    if sorted(set(plain)) != sorted(set(solo)):
        fail.append("--solo-stage changed the stage set %r -> %r" % (sorted(set(plain)),
                                                                    sorted(set(solo))))
    f = firsts(solo)
    if not any(b - a == 1 for a, b in zip(f, f[1:])):
        fail.append("--solo-stage left no two section marks adjacent; stage firsts are %r in %r"
                    % (f, solo))
    if any(b - a == 1 for a, b in zip(firsts(plain), firsts(plain)[1:])):
        fail.append("the plain splice ALREADY has two adjacent section marks, so the assertion "
                    "above passes without --solo-stage doing anything")

    # Shortening is refused, not silently ignored.
    try:
        build(html, base - 1)
        fail.append("splicing DOWN to %d was accepted; it must raise" % (base - 1))
    except ValueError:
        pass

    # The candidate CSS lands in the last style block, which is the whole of `inject_css`.
    marked = inject_css(html, ".probe{color:red}")
    if marked.rfind(".probe{color:red}") > marked.rfind("</style>"):
        fail.append("inject_css put the candidate CSS after the last </style>, where it is inert")
    if marked.count("</style>") != html.count("</style>"):
        fail.append("inject_css changed the number of style blocks")

    if fail:
        sys.exit("SELF-TEST FAILED:\n  - " + "\n  - ".join(fail))
    print("self-test OK - spliced %d-slide deck to 17, 25 and 43 with the stage set unchanged, "
          "put two section marks side by side with --solo-stage and not without it, refused to "
          "splice down, and placed candidate CSS inside the last style block" % base)


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if len(argv) < 2:
        sys.exit(__doc__.strip().splitlines()[0] + "\n\n"
                 "    python tools/deck/longdeck.py <deck> <slides> "
                 "[--out <dir>] [--css <file>] [--name <stem>] [--solo-stage]\n"
                 "    python tools/deck/longdeck.py --self-test")
    deck, rest = argv[0], argv[1:]
    try:
        target = int(rest[0])
    except ValueError:
        sys.exit("second argument is the target slide count, got %r" % rest[0])
    opts, rest, solo = {}, rest[1:], False
    while rest:
        a = rest.pop(0)
        if a in ("--out", "--css", "--name"):
            if not rest:
                sys.exit("%s needs a value" % a)
            opts[a.lstrip("-")] = rest.pop(0)
        elif a == "--solo-stage":
            solo = True
        else:
            sys.exit("unknown option %r" % a)
    css = None
    if "css" in opts:
        css = open(opts["css"], encoding="utf-8").read()
    dest = write(deck, target, out=opts.get("out"), css=css, name=opts.get("name"), solo=solo)
    print("%s  (%d slides)" % (paths.display_path(dest, ROOT), target))
    return dest


if __name__ == "__main__":
    main(sys.argv[1:])
