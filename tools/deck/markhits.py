#!/usr/bin/env python3
"""Find marks that overlap other marks inside a deck's diagrams.

    python tools/deck/markhits.py <deck> [<deck> ...]

**What it is for.** On 2026-08-21 the portfolio-review deck passed `check.py` (91 decided rules),
`check_all.py` (35 commands) and `printgeom.py` while carrying fifteen chart defects. Nine were
found by one person looking, four more by a second look at the same deck, two more by a third look
over all twelve slides after those four were fixed. **Nothing here could see a label drawn on top
of another mark**, so the only instrument was a person, and three separate looks each missed some.
That is what this measures (T-204).

**It compares text to text and text to line, and nothing else.** Not because the other pairs do not
matter, but because they are not decidable from the drawing:

- **Text over a filled mark is permitted** - DS-219's on-mark label puts a value inside its own bar
  on purpose. Excluding it is not a special case here; the tool simply never forms that pair.
- **A connector meeting the wrong bar** needs to know which bar the line *claims* to join. That is
  authoring intent, and it is nowhere in the markup. Excused with a reason rather than approximated.
- **Content reaching the slide's frame** is not a mark collision at all and belongs to whatever owns
  the frame.

**Typed geometry, not bounding boxes, and that is the whole design.** A diagonal line's bounding box
is mostly empty: measure a label against it and every label near a sloping axis is a hit. So a
`<line>` comes back as a **segment**, a `<text>` as a **box**, a `<circle>` as a **disc**, and each
pair is decided by the predicate that fits it. `seg_hits_box` is Liang-Barsky; both predicates came
from `tools/examples/portfolio_charts.py`, where T-203 proved them against seeded defects, and they
live here now so there is one copy (**L-13**).

**Every number is in one coordinate system** - the slide's own rect, in design units. SVG geometry
is taken through `getScreenCTM()` and boxes through `getBoundingClientRect()`, both reduced by the
stage's `--k` before anything is compared. **L-123** is the reason: a number read from the DOM is in
a coordinate system nobody established.

Real Chrome, offline, through `render.py`'s runner. Pure standard library (**L-07**).
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import paths                                                            # noqa: E402
import render                                                           # noqa: E402

ROOT = render.ROOT

RULE = "DS-244"

# **Both thresholds are fractions of the mark, never design units, and that is deliberate.** An
# absolute number is a statement about one face at one size: it has to be re-tuned for every deck
# that sets its labels larger, and re-tuning a tolerance until the noise fits is how a check stops
# meaning anything. A fraction of the box is a statement about *reading*, and it transports.
#
# `OVERLAP_FRACTION` - two labels collide when they share more than this of the smaller one's
# extent **in both axes**. Measured on the four shipped decks: two stacked lines of one label share
# 16% of their height, because a glyph box carries the ascender and descender space above and below
# the ink. Two labels genuinely set on top of each other share 40%. Nothing measured falls between.
OVERLAP_FRACTION = 0.30

# **Only `text/text` decides the gate.** `text/line` is measured and printed and never fails a
# deck, and that is a measured decision rather than caution - T-204 section 3 has the run. Counted
# across the four shipped decks, 2026-08-21: a label meets a line **16 times**, and exactly **one**
# of those is a known defect. The other fifteen are the deck setting a label on the line it names,
# which is ordinary chart vocabulary and reads perfectly - eight route names along their own edges
# on one slide of the reference deck alone.
#
# **The obvious discriminator was tried and it inverts.** *How deeply the line crosses the label*
# looks decisive and is backwards: the one real defect grazes the outer edge (depth 0.95 of the box)
# while the deliberate placements run through the dead centre (0.001). A label set ON its own line is
# geometrically indistinguishable from a label a line ran over - what separates them is intent, and
# intent is not in the drawing. T-115 shipped no checker at two false alarms against one hit; this is
# fifteen, so it reports.
#
# Against that, `text/text` over the same 30 slides is **1 true hit and 0 false alarms**, which is
# the other side of the same calibration and why half of this tool gates.
#
# *Re-run 2026-08-29 on the same four decks and the same 30 slides: **15**, not 16. The decks have
# been rebuilt several times since, and the figure moved with them - the pre-T-260 tool answers 15
# on today's tree too, so nothing here moved it. The ratio the decision rests on is unchanged and
# the historical number is left as it was measured rather than quietly restated.*
#
# **`text/shape` is new in T-260 and reports for the same reason `text/line` does.** It is the
# adopter's finding that this tool sees a label over a label and never a label over the box it
# names (report 013), and the owner's ruling was *report, calibrate, then decide* - T-204's own
# precedent, taken here rather than argued again. A kind that gates the day it is written has no
# false-alarm rate anybody has measured, and this one has the shape that produces them: a diagram is
# made of labels sitting in and beside boxes. The calibration is in T-260 section 3, and moving this
# kind into the tuple is that decision rather than this one.
GATED_KINDS = ("text/text",)

# How much of a label has to fall OUTSIDE a filled rectangle before it counts as crossing its edge.
# A glyph box carries ascender and descender space, so a label centred in its box can exceed it by a
# few per cent in height alone without a reader seeing anything; 15% of the label's own area is well
# clear of that and well under the third-of-the-label a crossing shows.
STRADDLE_FRACTION = 0.15

# A text run this long is a paragraph the figure happens to contain rather than a label, and its box
# is a line box rather than a glyph box. Measuring one against a line reports the leading, not ink.
MAX_LABEL_CHARS = 60

PROBE = r"""
<script>
(function () {
  /* **Pinned before anything is read** (T-206, L-128). A probe that measures a page mid-entrance
     can agree with itself and be wrong: every reading this deck's own geometry rule took was
     exactly `--rise-dist` from settled, and the rule passed because both renderings were equally
     wrong. This one is born pinned rather than waiting to be swept. */
  /* Pinned by `render.MOTION_PIN`, injected for every probe by `make_probe`
     (T-209). This file was born with its own copy under T-204; the copy is what
     T-209 removed, not the guarantee. */

  function mapper(fig, m, sr, k) {
    var owner = fig.ownerSVGElement || fig;
    return function (xa, ya) {
      var pt = owner.createSVGPoint();
      pt.x = xa; pt.y = ya;
      var q = pt.matrixTransform(m);
      return [(q.x - sr.left) / k, (q.y - sr.top) / k];
    };
  }

  /* **What the reader can actually see of this label** (T-260). Two labels at one point, one of
     them at `opacity:0`, are a cross-fade in place - the ordinary way to animate a value changing
     - and reading them as a collision refused a standard technique three times on one slide
     (adopter report 022). Opacity multiplies down the tree and `visibility`/`display` end it, so
     the whole chain is walked rather than the element read alone.

     **The frame is at rest, and there is only one.** `render.MOTION_PIN` forces `transition:none`
     and `animation:none` before this runs, so every computed opacity here is the settled value and
     a pair that overlaps only mid-transition is not measured at all. That is stated in the verdict
     rather than detected per element: the pin also erases `animation-name`, so nothing in this page
     can tell an animated opacity from a static one afterwards, and a per-element claim would be a
     guess dressed as a measurement. */
  /* **`visibility` is measured against the slide, not against the document** - it is an inherited
     property, and every slide but the current one is `visibility:hidden`, so reading it absolutely
     reported every label on eleven slides of twelve as invisible. The first run of this guard did
     exactly that: 129 hidden labels on the reference deck and T-204's sixteen label-on-line
     placements gone to zero, which is a guard swallowing the rule it was meant to narrow. What it
     costs is that a label hidden by `visibility` ON an off-screen slide cannot be told from the
     slide's own hiding; `opacity` is not inherited and carries the cross-fade this exists for. */
  function seen(el, top, slideVis) {
    var o = 1, n = el;
    while (n && n.nodeType === 1) {
      var cs = getComputedStyle(n);
      if (cs.display === 'none') { return 0; }
      if (cs.visibility === 'hidden' && slideVis !== 'hidden') { return 0; }
      var v = parseFloat(cs.opacity);
      if (isFinite(v)) { o *= v; }
      if (n === top) { break; }
      n = n.parentNode;
    }
    return o;
  }

  function go() {
    setTimeout(function () {
      var stage = document.getElementById('stage');
      var k = stage ? (parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 1) : 1;
      var out = [];
      var slides = document.querySelectorAll('.slide');
      for (var i = 0; i < slides.length; i++) {
        var sl = slides[i], sr = sl.getBoundingClientRect();
        var slideVis = getComputedStyle(sl).visibility;
        if (sr.width < 2) { continue; }
        var figs = sl.querySelectorAll('svg');
        var texts = [], segs = [], discs = [], rects = [];
        for (var f = 0; f < figs.length; f++) {
          var fig = figs[f];
          /* **A nested `<svg>` is the same drawing seen twice.** `querySelectorAll` returns the
             outer element and the inner one, and every mark inside the inner one is collected by
             both - which reported eight collisions on a slide that has four. Skip anything with an
             `<svg>` above it; the outer element already covers its contents. */
          if (fig.parentNode && fig.parentNode.closest && fig.parentNode.closest('svg')) { continue; }
          if (fig.getBoundingClientRect().width < sr.width / 4) { continue; }  /* an icon */

          /* Boxes, in slide-local design units. getBoundingClientRect on SVG text is the glyph
             extent, which is what a reader sees. */
          var tl = fig.querySelectorAll('text');
          for (var t = 0; t < tl.length; t++) {
            var el = tl[t], r = el.getBoundingClientRect();
            if (r.width <= 0.5 || r.height <= 0.5) { continue; }
            texts.push({s: (el.textContent || '').trim(),
                        cls: el.getAttribute('class') || '',
                        op: +seen(el, fig, slideVis).toFixed(3),
                        box: [(r.left - sr.left) / k, (r.top - sr.top) / k,
                              (r.right - sr.left) / k, (r.bottom - sr.top) / k]});
          }

          /* **Filled rectangles, and only rectangles** (T-260). A label running across the box it
             names is the commonest way a hand-built figure goes wrong, and three of them shipped
             past a green gate in one evening (adopter report 013). A `rect` is the one shape whose
             bounding box IS the shape, which is why the comparison stops here: for a filled
             `<path>`, box-versus-box is precisely the false alarm this tool's own self-test exists
             to refuse, and a claim about a path's interior needs its geometry rather than its
             extent. Stroked, unfilled marks are already `text/line` and are not collected twice. */
          var rl = fig.querySelectorAll('rect');
          for (var q2 = 0; q2 < rl.length; q2++) {
            var rc = rl[q2], rr = rc.getBoundingClientRect();
            if (rr.width < 2 || rr.height < 2) { continue; }
            var rcs = getComputedStyle(rc);
            if (!rcs.fill || rcs.fill === 'none' || rcs.fill === 'rgba(0, 0, 0, 0)') { continue; }
            if (seen(rc, fig, slideVis) <= 0.05) { continue; }
            rects.push({cls: rc.getAttribute('class') || 'rect',
                        box: [(rr.left - sr.left) / k, (rr.top - sr.top) / k,
                              (rr.right - sr.left) / k, (rr.bottom - sr.top) / k]});
          }

          /* Segments. `getScreenCTM` maps the element's own user space to the screen, which is the
             only way to compare a line drawn inside a viewBox with a box measured outside it.

             **Stroked and unfilled, or it is not a line.** A `<path>` can be the area under a
             series as easily as the series itself, and text over a FILLED mark is DS-219's
             permitted on-mark label. Deciding by the paint rather than by the tag name is what
             keeps that distinction out of a list of element names that would go stale. */
          var ll = fig.querySelectorAll('line,path,polyline');
          for (var n = 0; n < ll.length; n++) {
            var ln = ll[n], m = ln.getScreenCTM();
            if (!m) { continue; }
            var cs = getComputedStyle(ln);
            if (cs.stroke === 'none' || parseFloat(cs.strokeWidth) <= 0) { continue; }
            if (cs.fill && cs.fill !== 'none') { continue; }
            var map = mapper(fig, m, sr, k);
            var cls = ln.getAttribute('class') || ln.tagName;
            if (ln.tagName === 'line') {
              var a = map(parseFloat(ln.getAttribute('x1')), parseFloat(ln.getAttribute('y1')));
              var b = map(parseFloat(ln.getAttribute('x2')), parseFloat(ln.getAttribute('y2')));
              if (!isFinite(a[0]) || !isFinite(b[0])) { continue; }
              segs.push({cls: cls, a: a, b: b});
              continue;
            }
            /* A curve is sampled into segments rather than approximated by its bounding box -
               which for a drawdown line is most of the figure. `getPointAtLength` is the browser's
               own arithmetic, so the samples are on the drawn path and not on a reconstruction. */
            var len = 0;
            try { len = ln.getTotalLength(); } catch (e) { continue; }
            if (!isFinite(len) || len <= 0) { continue; }
            var steps = Math.max(2, Math.min(240, Math.ceil(len / 4)));
            var prev = null;
            for (var q = 0; q <= steps; q++) {
              var pt = ln.getPointAtLength(len * q / steps);
              var cur = map(pt.x, pt.y);
              if (prev && isFinite(cur[0]) && isFinite(prev[0])) {
                segs.push({cls: cls, a: prev, b: cur});
              }
              prev = cur;
            }
          }

          var cl = fig.querySelectorAll('circle');
          for (var c = 0; c < cl.length; c++) {
            var ci = cl[c], cr = ci.getBoundingClientRect();
            if (cr.width <= 0.5) { continue; }
            discs.push({cls: ci.getAttribute('class') || '',
                        cx: ((cr.left + cr.right) / 2 - sr.left) / k,
                        cy: ((cr.top + cr.bottom) / 2 - sr.top) / k,
                        r: (cr.width / 2) / k});
          }
        }
        if (!texts.length) { continue; }
        out.push({slide: sl.dataset.name || ('slide ' + (i + 1)), i: i + 1,
                  texts: texts, segs: segs, discs: discs, rects: rects});
      }
      /* `vw` and `vh` are not decoration: `render.calibrate` reads them back to correct the
         outer-window shortfall, so a probe that omits them cannot be calibrated at all. */
      var el = document.createElement('div');
      el.textContent = 'RESULT' + JSON.stringify(
        {vw: document.documentElement.clientWidth, vh: document.documentElement.clientHeight,
         k: k, slides: out}) + 'ENDRESULT';
      document.body.appendChild(el);
    }, 700);
  }
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { setTimeout(go, 120); });
  } else {
    window.addEventListener('load', go);
  }
})();
</script>
"""


# ---------------------------------------------------------------------------- the arithmetic

def seg_hits_box(x1, y1, x2, y2, box):
    """Liang-Barsky: does the segment meet the rectangle at all?

    **Moved here from `tools/examples/portfolio_charts.py`** (T-204), which is where T-203 wrote it
    and proved it against seeded defects. The generator imports it from this module now, so the
    arithmetic has one home and the deck-specific caller borrows it (**L-13**).
    """
    bx0, by0, bx1, by1 = box
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
        if p == 0:
            if q < 0:
                return False
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return False
    return True


def box_hits_disc(box, cx, cy, r):
    """Does the rectangle reach the disc? The nearest point on the box, against the radius."""
    bx0, by0, bx1, by1 = box
    nx = min(max(cx, bx0), bx1)
    ny = min(max(cy, by0), by1)
    return (nx - cx) ** 2 + (ny - cy) ** 2 <= r * r


def overlap(a, b):
    """How much two boxes share, as a fraction of the smaller box, in the axis that shares least.

    **The weaker axis, not the area.** Two labels set side by side can share a large area while
    touching along a hair, and two stacked lines of one label share their whole width while sharing
    only the leading. Taking the smaller of the two fractions makes *a hit* mean *a hit in both
    directions*, which is what a reader sees as a collision.
    """
    ox = min(a[2], b[2]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[1], b[1])
    if ox <= 0 or oy <= 0:
        return 0.0
    w = min(a[2] - a[0], b[2] - b[0])
    h = min(a[3] - a[1], b[3] - b[1])
    if w <= 0 or h <= 0:
        return 0.0
    return min(ox / w, oy / h)


def core(box, fraction):
    """The middle `fraction` of a box, in both axes.

    **Kept although nothing gates on it**, because it is how the depth measurement in T-204 section 3
    was taken and the next person to propose *just check whether the line crosses the middle* should
    be able to re-run it rather than re-derive it. The answer is that it inverts.
    """
    x0, y0, x1, y1 = box
    dx = (x1 - x0) * (1 - fraction) / 2.0
    dy = (y1 - y0) * (1 - fraction) / 2.0
    return (x0 + dx, y0 + dy, x1 - dx, y1 - dy)


def outside_fraction(box, rect):
    """How much of `box` lies outside `rect`, as a fraction of `box`'s own area.

    **The test is *crosses an edge*, never *touches the shape*** (T-260). A label centred in the box
    it names is the correct placement and is what a diagram is made of, so any test that fires on
    contact fires on every well-built figure. `0.0` means wholly inside - nothing to say - and `1.0`
    means wholly outside, which `hits_in` separates by requiring an intersection first.
    """
    bx0, by0, bx1, by1 = box
    area = (bx1 - bx0) * (by1 - by0)
    if area <= 0:
        return 0.0
    ox = min(bx1, rect[2]) - max(bx0, rect[0])
    oy = min(by1, rect[3]) - max(by0, rect[1])
    if ox <= 0 or oy <= 0:
        return 1.0
    return max(0.0, 1.0 - (ox * oy) / area)


# ---------------------------------------------------------------------------- the measurement

def hits_in(row, fraction=OVERLAP_FRACTION):
    """Every collision on one slide's row, as `[{kind, a, b, by}]`. No browser (**L-07**).

    Both kinds come back. Which of them can fail a deck is `GATED_KINDS`, decided once at the
    verdict rather than by leaving the measurement out - a check that does not measure what it
    declines to gate on cannot report how often it would have been wrong.
    """
    out = []
    labels = [t for t in row["texts"] if t["s"] and len(t["s"]) <= MAX_LABEL_CHARS]
    # **A label nobody can see is not colliding with anything** (T-260). `op` is the opacity chain
    # at rest, and a cross-fade in place - two labels at one point, one at zero - is the ordinary
    # way to animate a value changing. A row measured before `op` existed carries no key, and the
    # default of 1 keeps such a row readable rather than silently dropping every label in it.
    visible = [t for t in labels if t.get("op", 1) > 0.05]
    for i in range(len(visible)):
        for j in range(i + 1, len(visible)):
            by = overlap(visible[i]["box"], visible[j]["box"])
            if by > fraction:
                out.append({"kind": "text/text", "a": visible[i]["s"], "b": visible[j]["s"],
                            "by": round(by, 3)})
    for t in visible:
        box = tuple(t["box"])
        for s in row["segs"]:
            if seg_hits_box(s["a"][0], s["a"][1], s["b"][0], s["b"][1], box):
                out.append({"kind": "text/line", "a": t["s"], "b": s["cls"] or "line", "by": 0.0})
                break
        # **A label that straddles the edge of a filled rectangle**, which is what *label over the
        # box it names* looks like from outside the author's head. It has to intersect and to leave:
        # wholly inside is the correct placement, wholly outside is no relation at all.
        worst, worst_cls = 0.0, None
        for rc in row.get("rects", []):
            off = outside_fraction(box, rc["box"])
            if 0.0 < off < 1.0 and off > worst:
                worst, worst_cls = off, rc["cls"]
        if worst >= STRADDLE_FRACTION:
            out.append({"kind": "text/shape", "a": t["s"], "b": worst_cls or "rect",
                        "by": round(worst, 3)})
    return out


def gated(hits):
    return [h for h in hits if h["kind"] in GATED_KINDS]


def noted_of(rows, kind):
    """How many hits of one kind were measured and not gated - counted per kind since T-260.

    One number covering every ungated kind would have hidden a new kind's firing rate inside an old
    kind's, which is the figure the calibration this rule is waiting on consists of.
    """
    return sum(1 for r in rows for h in r["hits"] if h["kind"] == kind and kind not in GATED_KINDS)


def measure(deck):
    """`[{slide, i, hits, marks}]` - one row per slide with a diagram, or `None` if nothing rendered."""
    probe = render.make_probe(deck, name="markhits.html", extra=PROBE, out=render.out_dir(deck))
    cw, ch = render.calibrate(probe, 1920, 1234)
    data, err = render.read_result(render.file_url(probe), cw, ch)
    if not data:
        print("  !! no result for %s\n%s" % (deck, err[:300]))
        return None
    rows = []
    for row in data["slides"]:
        rows.append({"slide": row["slide"], "i": row["i"], "hits": hits_in(row),
                     # Labels the reader cannot see travel as their own count, so *nothing collided*
                     # and *nothing was visible to collide* stay different answers (T-260, L-36).
                     "hidden": sum(1 for t in row["texts"] if t.get("op", 1) <= 0.05),
                     "marks": len(row["texts"]) + len(row["segs"]) + len(row["discs"])
                     + len(row.get("rects", []))})
    return rows


def report(deck, rows):
    """One deck's rows, and the count that is the finding. Returns `(slides_with_hits, slides)`."""
    name = paths.display_path(deck, ROOT).replace("\\", "/")
    if rows is None:
        print("%s - no result" % name)
        return (0, 0)
    if not rows:
        print("%s - no diagram measured" % name)
        return (0, 0)
    bad = [r for r in rows if gated(r["hits"])]
    print("%s - %d slide(s) with a diagram, %d setting a label over another label, "
          "%d label-on-line and %d label-across-a-box placement(s); %d label(s) hidden at rest "
          "and not paired"
          % (name, len(rows), len(bad), noted_of(rows, "text/line"), noted_of(rows, "text/shape"),
             sum(r.get("hidden", 0) for r in rows)))
    for r in rows:
        if not r["hits"]:
            continue
        print("   slide %-3d %s" % (r["i"], r["slide"][:52]))
        for h in r["hits"]:
            print("       %-6s %-10s %-36s %s%s"
                  % ("GATES" if h["kind"] in GATED_KINDS else "notes", h["kind"],
                     repr(h["a"])[:36], repr(h["b"])[:30],
                     "" if not h["by"] else "  by %.0f%% of the smaller" % (100 * h["by"])))
    return (len(bad), len(rows))


def _verdict_from(rows):
    """`verdicts` over a measurement supplied directly - what `self_test` holds the row to.

    The browser is the only reason `verdicts` takes a deck rather than rows (**L-07**), and the
    absence discipline is the same one `figgrid` states: *0 of 0* and *0 of 9* are the same boolean
    and not the same fact (**L-36**), so the denominator travels in the text.
    """
    if rows is None:
        return (RULE, "no render result - every diagram's marks are unmeasured, not passing", False)
    bad = [r for r in rows if gated(r["hits"])]
    detail = "" if not bad else " - " + "; ".join(
        "slide %d %r over %r" % (r["i"], gated(r["hits"])[0]["a"][:24],
                                 gated(r["hits"])[0]["b"][:24]) for r in bad[:3])
    # **Every ungated count travels even though none of them can fail the deck.** A measurement
    # taken and then dropped from the row is a measurement nobody can ever check, and *0 of 9* would
    # read as *nothing touches anything* on a deck where twelve labels sit on their own lines
    # (**L-36**). Since T-260 they are counted per kind, because a new kind's firing rate hidden
    # inside an old kind's is exactly the number its calibration needs.
    #
    # **And the frame is named.** Everything here is read at rest, with motion pinned, so a pair
    # that overlaps only part-way through a transition is not measured at all - which is a limit to
    # state rather than a gap to leave a reader to infer from a green row (adopter report 022).
    return (RULE, "slides setting one diagram label over another: %d of %d%s; measured at rest, "
                  "motion pinned; %d label-on-line and %d label-across-a-box placement(s) measured "
                  "and not gated; %d label(s) hidden at rest and not paired"
                  % (len(bad), len(rows), detail,
                     noted_of(rows, "text/line"), noted_of(rows, "text/shape"),
                     sum(r.get("hidden", 0) for r in rows)),
            not bad)


def verdicts(deck):
    """DS-244's row - `[(rule, what, ok)]`, the shape `check.py` gathers."""
    if not deck:
        return [(RULE, "no deck to measure - the mark-collision gate has no subject", False)]
    return [_verdict_from(measure(deck))]


def self_test():
    """The arithmetic, and the ways of reading it wrongly (**L-04**), both directions (**L-125**)."""
    if seg_hits_box(0, 0, 10, 0, (0, 5, 10, 8)):
        sys.exit("SELF-TEST FAILED: a horizontal segment above a box was read as crossing it")
    if not seg_hits_box(0, 0, 10, 10, (4, 4, 6, 6)):
        sys.exit("SELF-TEST FAILED: a diagonal through the middle of a box was read as missing")
    # **The case the whole design is for.** The segment's BOUNDING BOX covers the label; the
    # segment does not. A box-versus-box check reports this, and is wrong.
    if seg_hits_box(0, 0, 100, 100, (5, 80, 15, 90)):
        sys.exit("SELF-TEST FAILED: a label inside a diagonal's bounding box but far from the line "
                 "itself was reported as hit - that is box-versus-box, and it is the false alarm "
                 "this tool exists not to raise")
    if not box_hits_disc((0, 0, 10, 10), 11, 5, 2):
        sys.exit("SELF-TEST FAILED: a disc overlapping the box edge was read as clear")
    if box_hits_disc((0, 0, 10, 10), 20, 5, 2):
        sys.exit("SELF-TEST FAILED: a distant disc was read as touching")

    # `overlap` takes the weaker axis as a FRACTION, so a long thin share is not a collision.
    if overlap((0, 0, 100, 10), (0, 9.5, 100, 20)) > 0.1:
        sys.exit("SELF-TEST FAILED: two rows of text sharing half a design unit of band were "
                 "reported as overlapping by the width they share")
    if abs(overlap((0, 0, 10, 10), (5, 5, 15, 15)) - 0.5) > 1e-9:
        sys.exit("SELF-TEST FAILED: a half-and-half overlap did not measure as half")
    # **The measured shape of the false alarm, kept as a fixture.** Two stacked lines of one label
    # in `measure-first` slide 10 share 16% of their height and all of their width. If that ever
    # reads as a collision the tool is reporting ordinary leading.
    if overlap((0, 0, 100, 28), (0, 23.4, 100, 51.4)) > OVERLAP_FRACTION:
        sys.exit("SELF-TEST FAILED: two stacked lines of one label were read as a collision - that "
                 "is leading, and it is the false alarm the fraction was calibrated against")
    # And the real one it must stay above: 40% of the smaller box, `portfolio-review` slide 4.
    if overlap((0, 0, 100, 28), (10, 11.2, 110, 39.2)) <= OVERLAP_FRACTION:
        sys.exit("SELF-TEST FAILED: two labels set on top of each other fell under the threshold")

    # `core` still has to be right, because T-204 section 3's depth measurement is taken with it and
    # the finding it produced - that depth INVERTS - is only as good as the shrink it used.
    if seg_hits_box(0, 27, 100, 27, core((0, 0, 100, 28), 0.5)):
        sys.exit("SELF-TEST FAILED: a line along a label's lower edge was read as crossing its core")
    if not seg_hits_box(0, 14, 100, 14, core((0, 0, 100, 28), 0.5)):
        sys.exit("SELF-TEST FAILED: a line straight through the middle of a label missed its core")

    # **The partition is the finding, so it is asserted rather than left to a constant.** If
    # `text/line` ever joins the gate, it must be because someone re-ran the corpus - not because a
    # tuple grew a member while eleven false alarms went on being eleven.
    if "text/line" in GATED_KINDS:
        sys.exit("SELF-TEST FAILED: text/line is gating. Across the four shipped decks it fires 16 "
                 "times for 1 real defect, because a label set ON the line it names is normal chart "
                 "vocabulary and is geometrically identical to a label a line ran over (T-204)")
    if "text/text" not in GATED_KINDS:
        sys.exit("SELF-TEST FAILED: nothing gates, so this rule cannot fail a deck at all")

    # Both directions, on rows shaped exactly as the probe emits them (**L-125**).
    clean = {"texts": [{"s": "Calder wind 13%", "cls": "name", "box": (0, 0, 100, 20)},
                       {"s": "Norbeck solar 11%", "cls": "name", "box": (120, 0, 220, 20)}],
             "segs": [{"cls": "axis", "a": (0, 60), "b": (300, 60)}], "discs": []}
    if hits_in(clean):
        sys.exit("SELF-TEST FAILED: a clean slide reported a collision")
    dirty = dict(clean, texts=[{"s": "+21 points", "cls": "callout", "box": (0, 0, 100, 28)},
                               {"s": "Renewables 31 to 52", "cls": "name", "box": (10, 11.2, 110, 39.2)}])
    got = hits_in(dirty)
    if len(got) != 1 or got[0]["kind"] != "text/text":
        sys.exit("SELF-TEST FAILED: two labels set on top of each other were not caught - that is "
                 "T-207's slide 4, and it is the defect this was written for")
    crossed = dict(clean,
                   texts=[{"s": "5.1 PTS RENEWABLES", "cls": "note", "box": (0, 0, 100, 40)}],
                   segs=[{"cls": "series", "a": (-10, 45), "b": (110, -5)}])
    got = hits_in(crossed)
    if len(got) != 1 or got[0]["kind"] != "text/line":
        sys.exit("SELF-TEST FAILED: a label crossed by the line it annotates was not measured - "
                 "that is T-207's slide 10. It does not gate, but it must still be counted")
    if gated(got):
        sys.exit("SELF-TEST FAILED: a label-on-line placement reached the gate")

    # A paragraph is not a label: its box is a line box, and measuring one against a line reports
    # the leading rather than any ink.
    para = dict(clean,
                texts=[{"s": "x" * (MAX_LABEL_CHARS + 1), "cls": "p", "box": (0, 0, 300, 80)}],
                segs=[{"cls": "axis", "a": (0, 40), "b": (300, 40)}])
    if hits_in(para):
        sys.exit("SELF-TEST FAILED: a paragraph inside a figure was measured as a label")

    # The absence discipline, and a render that produced nothing.
    _rid, what, ok = _verdict_from(rows=[])
    if not ok or "of 0" not in what:
        sys.exit("SELF-TEST FAILED: a deck drawing no diagram must pass, and must print its own "
                 "denominator so *0 of 0* does not read like *0 of 9* (**L-36**)")
    _rid, what, ok = _verdict_from(rows=None)
    if ok:
        sys.exit("SELF-TEST FAILED: a render that produced nothing was reported as a pass (T-028)")
    _rid, what, ok = _verdict_from(
        rows=[{"i": 4, "hits": [{"kind": "text/text", "a": "+21 points", "b": "Renewables"}]},
              {"i": 5, "hits": []}])
    if ok or "1 of 2" not in what or "slide 4" not in what:
        sys.exit("SELF-TEST FAILED: one dirty slide and one clean did not report exactly that")
    # A deck whose only finding is a label on a line PASSES, and still says how many there were.
    _rid, what, ok = _verdict_from(
        rows=[{"i": 7, "hits": [{"kind": "text/line", "a": "Route 3", "b": "quiet-s"}]}])
    if not ok:
        sys.exit("SELF-TEST FAILED: a label set on its own line failed the deck")
    if "1 label-on-line" not in what:
        sys.exit("SELF-TEST FAILED: the label-on-line count was measured and then dropped from the "
                 "row, so nothing downstream can ever see it (**L-36**)")

    # ---- T-260: opacity, and the box a label runs across ------------------------------------
    # The same partition assertion `text/line` carries, for the same reason: a kind joins the gate
    # because someone re-ran the corpus, never because a tuple grew a member.
    if "text/shape" in GATED_KINDS:
        sys.exit("SELF-TEST FAILED: text/shape is gating with no calibration behind it. The ruling "
                 "was report, calibrate, then decide - T-204's precedent - and the count lives in "
                 "T-260 section 3 (T-260)")

    # `outside_fraction` is the whole of *crosses an edge* rather than *touches the shape*.
    if outside_fraction((10, 10, 20, 20), (0, 0, 100, 100)) != 0.0:
        sys.exit("SELF-TEST FAILED: a label centred in its own box read as leaving it - that is the "
                 "correct placement, and every diagram is made of it")
    if outside_fraction((200, 200, 210, 210), (0, 0, 100, 100)) != 1.0:
        sys.exit("SELF-TEST FAILED: a label nowhere near a box did not read as wholly outside it")
    if abs(outside_fraction((90, 0, 110, 10), (0, 0, 100, 100)) - 0.5) > 1e-9:
        sys.exit("SELF-TEST FAILED: a label half over a box's right edge was not measured at half")

    inbox = dict(clean, texts=[{"s": "No rung fits", "cls": "lab", "box": (20, 20, 80, 40)}],
                 segs=[], rects=[{"cls": "rung", "box": (0, 0, 100, 100)}])
    if hits_in(inbox):
        sys.exit("SELF-TEST FAILED: a label sitting wholly inside the box it names was reported. "
                 "The test is *crosses an edge*, and this is what a correct diagram looks like")
    across = dict(inbox, texts=[{"s": "No rung fits", "cls": "lab", "box": (60, 20, 160, 40)}])
    got = hits_in(across)
    if len(got) != 1 or got[0]["kind"] != "text/shape":
        sys.exit("SELF-TEST FAILED: a label running out of the box it names was not measured - "
                 "that is adopter report 013's slide 8, and it shipped past a green gate")
    if gated(got):
        sys.exit("SELF-TEST FAILED: a label-across-a-box placement reached the gate before anyone "
                 "measured how often it is wrong")

    # A cross-fade in place: two labels at one point, one of them invisible at rest. Reading them
    # as a collision refused a standard technique three times on one slide (report 022).
    fade = dict(clean, segs=[],
                texts=[{"s": "62", "cls": "v", "op": 1, "box": (0, 0, 100, 28)},
                       {"s": "71", "cls": "v", "op": 0, "box": (0, 0, 100, 28)}])
    if hits_in(fade):
        sys.exit("SELF-TEST FAILED: a cross-fade in place was reported as two labels colliding - "
                 "only one of the pair is ever visible (report 022)")
    both = dict(fade, texts=[dict(t, op=1) for t in fade["texts"]])
    if not [h for h in hits_in(both) if h["kind"] == "text/text"]:
        sys.exit("SELF-TEST FAILED: two labels that ARE both visible at one point stopped being a "
                 "collision, so the opacity guard swallowed the rule it was meant to narrow")

    # The frame is named in the row, because a limit a reader has to infer from a green verdict is
    # not a stated limit.
    _rid, what, _ok = _verdict_from(rows=[])
    if "at rest" not in what:
        sys.exit("SELF-TEST FAILED: the row does not say which frame it measured, so a pair that "
                 "overlaps only mid-transition reads as a pair that does not overlap (report 022)")
    return True


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    self_test()
    render.self_test()
    print("browser: %s" % render.CHROME)
    total_bad = total = 0
    for deck in argv:
        if deck.startswith("-"):
            continue
        b, n = report(deck, measure(deck))
        total_bad += b
        total += n
        print("")
    print("%d of %d slide(s) with a diagram set one label over another." % (total_bad, total))
    print("%s gates on %s, at an overlap fraction of %.2f, measured at rest with motion pinned.\n"
          "Label-on-line and label-across-a-box placements are measured and reported: T-204 "
          "section 3\nhas the count that decided the first, T-260 section 3 the second."
          % (RULE, "/".join(GATED_KINDS), OVERLAP_FRACTION))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
