"""Decide R6 section 8's conditions 2 to 8 - the decomposition of *renders glitch-free*.

    python tools/deck/glitchfree.py <deck.html> [...]

**CLAUDE.md rule 2 requires a deck to render glitch-free in recent Chrome/Edge, and that is a
testable statement only once it is decomposed.**
[`R6 section 8`](../../docs/research/R6-portability-contract.md) decomposed it into nine conditions
*"for T-005 to implement"*, [`BRIEF.md`](../../docs/BRIEF.md) relayed the assignment, and T-005's own
section 1 wrote a narrower criterion scoped to the restricted-origin class - met it, and closed.
**Seven of the nine were never anyone's.** Nothing was recorded falsely; the gap sat between two
documents that each read correctly alone (**L-39**). T-041 is where it closes.

**The IDs are `GF-2` to `GF-8`, numbered off R6's own table**, so a verdict names the row it comes
from and the two cannot drift apart while staying individually true - which is the failure above,
one level down. `GF-1` is deliberately absent: condition 1 is DS-001 and already decided, and a
second ID for it would put one condition in two accounts. Condition 9 is **L-01** and is not a
check; `check.py` prints it as the gate's boundary beside the five blind dimensions.

**One render, one walk.** Every condition here is answered from a single pass that clicks through
every slide, which is what T-041's answered open question settled: a second browser run introduces
the failure mode of two runs that disagree, where the error is real in one and absent in the other
and nothing says which reading is the deck's. The walk is instant because `MOTION_PIN` has already
pinned the transitions off, so the DOM is settled the moment `next` is clicked.

**A measurement that did not happen is a failure, never a pass** - the case T-028 found, where a
stage printed NO RESULT and the run stayed green. A probe that returns nothing fails all seven
rather than emitting one row about itself, because it is seven conditions that went unmeasured.

Three conditions can return **NO SUBJECT** (`ok is None`) rather than a boolean, and each states
why in its own row. That is `check.py`'s third state, which `run()` excludes from `failures` by
`is False` and `account()` documents as *not a coverage fault*: the check ran and this deck holds
nothing for it to judge. **The subject being absent is not the subject being sound** - the row says
so in words, which is the whole point of preferring it to a silent pass.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paths                                                            # noqa: E402
import render                                                           # noqa: E402

ROOT = render.ROOT

# **The stage this reads at, and why one rather than a sweep.** `figgrid` measures at 1920x1234 and
# `check.py` gathers both, so two rendered stages reading one deck at one size is a page they can be
# argued about together. A sweep belongs to `contract.py`, whose subject is what changes BETWEEN
# renders; nothing here is such a claim.
STAGE_W, STAGE_H = 1920, 1234

# How far a box may move between first paint and `document.fonts.ready` before GF-6 calls it a
# shift. Sub-pixel movement is rounding in the layout engine, not reflow.
SHIFT_TOLERANCE_PX = 0.5


PROBE = r"""
<script>
(function(){
  var FIRST = null;
  function fam(s){
    s = String(s || '').split(',')[0].trim().toLowerCase();
    var c = s.charAt(0);
    if (c === '"' || c === String.fromCharCode(39)) s = s.slice(1, -1);
    return s.trim();
  }
  function boxes(){
    var out = [], els = document.querySelectorAll('.slide[data-current] *');
    for (var i = 0; i < els.length && i < 200; i++){
      var r = els[i].getBoundingClientRect();
      out.push([+r.left.toFixed(2), +r.top.toFixed(2)]);
    }
    return out;
  }
  /* First paint, taken before `document.fonts.ready` resolves. Under `--virtual-time-budget` a
     clock is frame production rather than time (**L-26**), so these two moments can fall in one
     frame - and then *no shift* means *no interval*, which reads exactly like a pass. The font
     status at this instant is what tells them apart, and it travels with the snapshot.
     **Two racers, and the timer is not redundant.** On `requestAnimationFrame` alone this returned
     *no frame was painted* on two of the four decks in this repository - not a fact about those
     decks, a fact about whether headless produced a frame inside the window. A `setTimeout(0)` is
     a macrotask, so it lands before the 120 ms one that runs the walk, and whichever racer arrives
     first is the snapshot. What that converts is an unmeasured condition into a measured one: if
     the fonts have genuinely settled by then, the row says so and declines, which is a different
     sentence from the instrument having missed its moment. */
  function takeFirst(){
    if (FIRST) return;
    FIRST = { status: (document.fonts && document.fonts.status) || 'unknown', boxes: boxes() };
  }
  requestAnimationFrame(takeFirst);
  setTimeout(takeFirst, 0);

  function run(){
    var E = window.__htmldeckErr || null;
    /* `vw` and `vh` are `render.calibrate`'s contract, not this probe's subject: --window-size is
       the OUTER window and every probe read through `calibrate` has to report the viewport back so
       the shortfall can be corrected. A probe that omits them fails in `calibrate` with a KeyError
       rather than a message, which is how this one first ran. */
    var out = { vw: window.innerWidth, vh: window.innerHeight,
                trap: !!E, errLoad: E ? E.slice(0, 20) : [], errWalk: [],
                slides: 0, reached: 0, stalled: null,
                fonts: { status: 'none', total: 0, unloaded: [] },
                textNodes: 0, fallback: [],
                overflow: [], canvas: { total: 0, blank: [], unreadable: [] },
                shift: { status: FIRST ? FIRST.status : 'no-frame', moved: 0, set: 'same' } };
    var nLoad = E ? E.length : 0;

    /* ---- condition 3: every DECLARED face reports loaded. Not that `document.fonts.load()`
       resolved, which reports only that faces matched the query (R6 section 8). */
    var emb = {};
    if (document.fonts && document.fonts.forEach){
      out.fonts.status = document.fonts.status;
      document.fonts.forEach(function(f){
        out.fonts.total++;
        emb[fam(f.family)] = true;
        if (f.status !== 'loaded' && out.fonts.unloaded.length < 10)
          out.fonts.unloaded.push(fam(f.family) + ':' + f.status);
      });
    }

    /* ---- condition 6: layout stable across the font settle. */
    if (FIRST){
      var now = boxes();
      if (now.length !== FIRST.boxes.length) out.shift.set = 'changed';
      else for (var b = 0; b < now.length; b++)
        if (Math.abs(now[b][0] - FIRST.boxes[b][0]) > 0.5 ||
            Math.abs(now[b][1] - FIRST.boxes[b][1]) > 0.5) out.shift.moved++;
    }

    var seenFam = {};
    function perSlide(name){
      /* ---- condition 5: nothing overflows its stage, by R6's stated test. */
      var st = document.getElementById('stage');
      if (st && (st.scrollWidth > st.clientWidth || st.scrollHeight > st.clientHeight)
          && out.overflow.length < 10)
        out.overflow.push(name + ' ' + st.scrollWidth + 'x' + st.scrollHeight +
                          ' in ' + st.clientWidth + 'x' + st.clientHeight);
      var cur = document.querySelector('.slide[data-current]');
      /* ---- condition 4: no text renders in a family the deck did not embed. */
      if (cur){
        var w = document.createTreeWalker(cur, NodeFilter.SHOW_TEXT, null, false), t;
        while ((t = w.nextNode())){
          if (!t.nodeValue || !t.nodeValue.trim()) continue;
          var p = t.parentElement;
          if (!p) continue;
          var tag = p.tagName;
          if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'TITLE' || tag === 'NOSCRIPT') continue;
          out.textNodes++;
          var f = fam(getComputedStyle(p).fontFamily);
          if (!emb[f] && !seenFam[f]){
            seenFam[f] = true;
            if (out.fallback.length < 10)
              out.fallback.push(f + ' (' + name + ': ' + t.nodeValue.trim().slice(0, 24) + ')');
          }
        }
      }
    }

    /* ---- condition 7: every canvas surface drew something.
       **Document-wide and taken once, after the walk rather than inside it.** The subject is the
       deck's surfaces, not one slide's: scanning per slide counts a surface once per visit, and
       scanning before the walk gives a canvas drawn on entry to slide 9 no chance to have drawn.
       Running it last means every slide has been current at least once. */
    function readCanvas(){
      var cvs = document.querySelectorAll('canvas');
      for (var i = 0; i < cvs.length; i++){
        var c = cvs[i], id = c.id || ('canvas ' + i);
        out.canvas.total++;
        var ctx = null;
        try { ctx = c.getContext('2d'); } catch (e) { ctx = null; }
        if (!ctx){
          out.canvas.unreadable.push(id + ': no readable 2d context - a WebGL framebuffer needs ' +
                                     'preserveDrawingBuffer and this one did not declare it');
          continue;
        }
        var d = null;
        try { d = ctx.getImageData(0, 0, c.width, c.height).data; }
        catch (e) { out.canvas.unreadable.push(id + ': ' + (e.message || 'getImageData threw')); }
        if (!d) continue;
        /* Any pixel differing from the first one is ink. A surface filled edge to edge in one
           opaque colour reads as blank by this test and that is the honest answer: nothing
           distinguishes it from a canvas the deck never touched. */
        var drew = false;
        for (var q = 0; q + 3 < d.length && !drew; q += 16)
          if (d[q + 3] !== d[3] || d[q] !== d[0] || d[q + 1] !== d[1] || d[q + 2] !== d[2])
            drew = true;
        if (!drew) out.canvas.blank.push(id);
      }
    }

    /* ---- condition 8: every slide reached, first to last, without a script error. */
    out.slides = document.querySelectorAll('.slide').length;
    var next = document.getElementById('next');
    function cur(){
      var c = document.querySelector('.slide[data-current]');
      return c ? (c.dataset.name || '?') : null;
    }
    var name = cur();
    if (name === null){ out.stalled = 'no slide carries data-current'; }
    else {
      out.reached = 1;
      perSlide(name);
      for (var n = 1; n < out.slides; n++){
        if (!next){ out.stalled = 'no next control to advance with'; break; }
        var before = name;
        try { next.click(); }
        catch (e){ out.stalled = 'next threw at slide ' + n + ': ' + (e.message || e); break; }
        name = cur();
        if (name === before){
          out.stalled = 'slide ' + (n + 1) + ' never became current - stuck on ' + before;
          break;
        }
        out.reached++;
        perSlide(name);
      }
    }
    readCanvas();
    if (E) out.errWalk = E.slice(nLoad, nLoad + 20);

    document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
    document.documentElement.setAttribute('data-probe-done', '');
  }

  if (document.fonts && document.fonts.ready)
    document.fonts.ready.then(function(){ setTimeout(run, 120); });
  else window.addEventListener('load', run);
})();
</script>
"""


def measure(deck):
    """The one render. Returns the probe payload, or `None`."""
    probe = render.make_probe(deck, name="glitchfree.html", extra=PROBE, out=render.out_dir(deck))
    cw, ch = render.calibrate(probe, STAGE_W, STAGE_H)
    data, err = render.read_result(render.file_url(probe), cw, ch)
    if not data:
        print("  !! no result for %s\n%s" % (deck, (err or "")[:300]))
        return None
    return data


def _verdict_rows(d):
    """The seven rows, over a payload supplied directly.

    **Singular in the name on purpose.** `audit.verdict_producers` discovers a producer by matching
    `def *verdicts*` across the package, so a helper called `_verdicts_from` is counted as a second
    producer and `check.producer_split` stops the run over it. `figgrid._verdict_from` is the
    precedent; this matches it rather than being excused in `NOT_STATIC`, which would declare a
    private helper to be a family of rows.

    **Separated from `verdicts` for `figgrid`'s reason** (**L-07**): the browser is the only thing
    that makes `verdicts` take a deck, and the self-test has no browser. Both callers reach the
    logic here, so what the suite proves is what the gate runs.
    """
    if d is None:
        # Seven rows, not one about the probe. Seven conditions went unmeasured, and a single row
        # saying so would leave six of them with no verdict in an account that reads row by row.
        return [(r, "no render result - this condition is unmeasured, which is not passing", False)
                for r in ("GF-2", "GF-3", "GF-4", "GF-5", "GF-6", "GF-7", "GF-8")]

    rows = []

    # ---- GF-2 --------------------------------------------------------------------------------
    if not d.get("trap"):
        rows.append(("GF-2", "the console trap never installed, so the console is unread rather "
                             "than clean", False))
    else:
        errs = list(d["errLoad"]) + list(d["errWalk"])
        rows.append(("GF-2", "console errors and unhandled rejections over the load and one pass "
                             "through every slide: %d%s"
                             % (len(errs), "" if not errs else " - " + "; ".join(errs[:3])),
                     not errs))

    # ---- GF-3 --------------------------------------------------------------------------------
    f = d["fonts"]
    if not f["total"]:
        rows.append(("GF-3", "no @font-face is declared, so there is no declared face to have "
                             "failed to load - nothing measured, not nothing wrong", None))
    else:
        bad = f["status"] != "loaded" or bool(f["unloaded"])
        rows.append(("GF-3", "declared faces reporting loaded: %d of %d, set status %r%s"
                             % (f["total"] - len(f["unloaded"]), f["total"], f["status"],
                                "" if not f["unloaded"] else " - " + "; ".join(f["unloaded"][:3])),
                     not bad))

    # ---- GF-4 --------------------------------------------------------------------------------
    if not d["textNodes"]:
        rows.append(("GF-4", "no text node was reached, so no text was rendered in anything - "
                             "nothing measured, not nothing wrong", None))
    else:
        fb = d["fallback"]
        rows.append(("GF-4", "text whose first computed family is not an embedded face: %d distinct "
                             "famil%s over %d node(s)%s"
                             % (len(fb), "y" if len(fb) == 1 else "ies", d["textNodes"],
                                "" if not fb else " - " + "; ".join(fb[:3])),
                     not fb))

    # ---- GF-5 --------------------------------------------------------------------------------
    ov = d["overflow"]
    rows.append(("GF-5", "slides whose stage scrolls past its own box: %d of %d%s"
                         % (len(ov), d["reached"],
                            "" if not ov else " - " + "; ".join(ov[:3])),
                 not ov))

    # ---- GF-6 --------------------------------------------------------------------------------
    sh = d["shift"]
    if sh["status"] == "no-frame":
        rows.append(("GF-6", "no frame was painted before the fonts settled, so there is no "
                             "interval to have shifted across", None))
    elif sh["status"] == "loaded":
        # **The risk T-041 section 2 named, met.** Not a pass: *no shift* and *no interval* are the
        # same boolean and not the same fact (**L-36**).
        rows.append(("GF-6", "the fonts had already settled at first paint, so first paint and "
                             "document.fonts.ready are one frame and no interval was observed",
                     None))
    elif sh["set"] == "changed":
        rows.append(("GF-6", "the element set changed between first paint and document.fonts.ready, "
                             "so the two snapshots are not comparable box for box", None))
    else:
        rows.append(("GF-6", "boxes moving more than %.1f px between first paint (fonts %r) and "
                             "document.fonts.ready: %d"
                             % (SHIFT_TOLERANCE_PX, sh["status"], sh["moved"]), not sh["moved"]))

    # ---- GF-7 --------------------------------------------------------------------------------
    c = d["canvas"]
    if not c["total"]:
        # **The decision T-041 section 2 took, and the criterion whose wording it deviates from.**
        # The criterion says *fails on a deck with no canvas rather than passing*; its own gloss
        # says why - *the subject being absent is not the subject being sound*. `None` says exactly
        # that. `False` would make a canvas-free deck un-passable, which is a check forbidding a
        # design choice CLAUDE.md rule 3 permits rather than requires.
        rows.append(("GF-7", "this deck draws no canvas or WebGL surface, so nothing was measured - "
                             "which is not the same as nothing being wrong", None))
    elif len(c["unreadable"]) == c["total"]:
        rows.append(("GF-7", "all %d surface(s) are unreadable back: %s"
                             % (c["total"], "; ".join(c["unreadable"][:2])), None))
    else:
        rows.append(("GF-7", "canvas surfaces that drew nothing: %d of %d readable, %d unreadable%s"
                             % (len(c["blank"]), c["total"] - len(c["unreadable"]),
                                len(c["unreadable"]),
                                "" if not c["blank"] else " - " + "; ".join(c["blank"][:3])),
                     not c["blank"]))

    # ---- GF-8 --------------------------------------------------------------------------------
    ok8 = d["reached"] == d["slides"] and not d["errWalk"] and not d["stalled"]
    rows.append(("GF-8", "slides reached first to last without a script error: %d of %d%s%s"
                         % (d["reached"], d["slides"],
                            "" if not d["stalled"] else " - " + d["stalled"],
                            "" if not d["errWalk"] else " - during the walk: "
                            + "; ".join(d["errWalk"][:2])),
                 ok8))
    return rows


def verdicts(deck):
    """`GF-2` to `GF-8` as `[(rule, what, ok)]` - the shape `check.py` gathers."""
    if not deck:
        return _verdict_rows(None)
    return _verdict_rows(measure(deck))


def report(deck, d):
    """One deck's seven rows, printed. Returns them."""
    rows = _verdict_rows(d)
    print("%s" % paths.display_path(deck, ROOT).replace("\\", "/"))
    for rid, what, ok in rows:
        print("  %-6s %-84s %s"
              % (rid, what[:84], "NO SUBJECT" if ok is None else "pass" if ok else "FAIL"))
    return rows


def _clean():
    """A payload from a deck with nothing wrong - the self-test's baseline."""
    return {"trap": True, "errLoad": [], "errWalk": [], "slides": 12, "reached": 12,
            "stalled": None,
            "fonts": {"status": "loaded", "total": 3, "unloaded": []},
            "textNodes": 240, "fallback": [],
            "overflow": [], "canvas": {"total": 0, "blank": [], "unreadable": []},
            "shift": {"status": "loading", "moved": 0, "set": "same"}}


def self_test():
    """Both directions, for every row (**L-04**).

    **A check that has never been seen to fail is a claim about the instrument** (**L-36**,
    **L-42**). The seeded variants in `static_variants.py` prove that through a real browser for
    the conditions a browser can be made to break; this proves the row logic itself, with no
    browser, so a change to the wording or the arithmetic is caught in the second it is made.
    """
    def verdict(d, rid):
        for r, _w, ok in _verdict_rows(d):
            if r == rid:
                return ok
        sys.exit("SELF-TEST FAILED: %s produced no row at all" % rid)

    base = _clean()
    for rid in ("GF-2", "GF-3", "GF-4", "GF-5", "GF-6", "GF-8"):
        if verdict(base, rid) is not True:
            sys.exit("SELF-TEST FAILED: %s did not pass a payload with nothing wrong in it" % rid)
    if verdict(base, "GF-7") is not None:
        sys.exit("SELF-TEST FAILED: GF-7 returned a boolean for a deck with no canvas. The subject "
                 "being absent is not the subject being sound, and it is not the subject being "
                 "broken either (T-041)")

    def broken(**kw):
        d = _clean()
        d.update(kw)
        return d

    # **GF-7's pass, which no deck in this repository can produce.** None of the four draws a
    # canvas, so without this case the only state ever observed is NO SUBJECT and the only state
    # ever seeded is FAIL - a check never seen to succeed is **L-36** with the sign flipped. The
    # browser half of the same direction is `static_variants.GF_PASS_VARIANTS`.
    if verdict(broken(canvas={"total": 2, "blank": [], "unreadable": []}), "GF-7") is not True:
        sys.exit("SELF-TEST FAILED: GF-7 did not pass a deck whose every canvas drew something")

    # The seeded half: one break per row, each of which must come back False.
    cases = [
        ("GF-2", broken(errLoad=["error: x is not defined"])),
        ("GF-2", broken(errWalk=["rejection: fetch failed"])),
        ("GF-2", broken(trap=False)),
        ("GF-3", broken(fonts={"status": "loaded", "total": 3, "unloaded": ["deck sans:error"]})),
        ("GF-3", broken(fonts={"status": "loading", "total": 3, "unloaded": []})),
        ("GF-4", broken(fallback=["sans-serif (cover: Portfolio review)"])),
        ("GF-5", broken(overflow=["agenda 1960x1300 in 1920x1234"])),
        ("GF-6", broken(shift={"status": "loading", "moved": 27, "set": "same"})),
        ("GF-7", broken(canvas={"total": 2, "blank": ["chart canvas 0"], "unreadable": []})),
        ("GF-8", broken(reached=7)),
        ("GF-8", broken(stalled="no next control to advance with")),
        ("GF-8", broken(errWalk=["error: goTo is not a function"])),
    ]
    for rid, d in cases:
        if verdict(d, rid) is not False:
            sys.exit("SELF-TEST FAILED: %s did not fail a payload seeded to break it - %s"
                     % (rid, json.dumps(d)[:200]))

    # NO SUBJECT, in every shape that earns it. Each of these is a check that RAN and found nothing
    # to judge, which is `check.py`'s third state and is not a pass.
    subjectless = [
        ("GF-3", broken(fonts={"status": "loaded", "total": 0, "unloaded": []})),
        ("GF-4", broken(textNodes=0)),
        ("GF-6", broken(shift={"status": "loaded", "moved": 0, "set": "same"})),
        ("GF-6", broken(shift={"status": "no-frame", "moved": 0, "set": "same"})),
        ("GF-6", broken(shift={"status": "loading", "moved": 0, "set": "changed"})),
        ("GF-7", broken(canvas={"total": 1, "blank": [], "unreadable": ["cover canvas 0: no ctx"]})),
    ]
    for rid, d in subjectless:
        if verdict(d, rid) is not None:
            sys.exit("SELF-TEST FAILED: %s decided a payload it has no subject in. A pass here is "
                     "L-36 and a fail forbids a design choice - it is neither" % rid)

    # And the whole set, when the render produced nothing: seven failures, no pass anywhere.
    none_rows = _verdict_rows(None)
    if len(none_rows) != 7 or any(ok is not False for _r, _w, ok in none_rows):
        sys.exit("SELF-TEST FAILED: a render that produced nothing did not fail all seven "
                 "conditions. That is T-028's case - a stage printing NO RESULT and the run "
                 "staying green")


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    self_test()
    bad = 0
    decks = [d for d in argv if not d.startswith("-")]
    for deck in decks:
        for _r, _w, ok in report(deck, measure(deck)):
            if ok is False:
                bad += 1
        print("")
    print("%d failing condition(s) across %d deck(s)." % (bad, len(decks)))
    print("GF-2 to GF-8 are R6 section 8's conditions 2 to 8; condition 1 is DS-001 and condition "
          "9 is a person (L-01).")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
