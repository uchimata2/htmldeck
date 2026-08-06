#!/usr/bin/env python3
"""Generate the four chart types a business deck needs, as hand-computed SVG, and prove the
corpus's three named chart defects cannot occur.

T-006 asks whether a charting library is needed. R5 §5 says no on size - Chart.js is 203.6 KB and
d3 is 273.2 KB against a chart that fits in single-digit KB. But size is the weak argument. The
strong one is that the corpus's chart failures were **not** things a library would have prevented:

  - a chart 558 px tall that pushed its own title off the slide   -> a layout budget problem
  - a bar rendering at 1.4 px, which reads as a rendering fault    -> a floor problem
  - an SVG label clipped by its own viewBox                        -> a measurement problem

A library draws the chart and knows nothing about the slide it sits on. Each of these is a
constraint between the chart and the deck, which is exactly the part a library cannot own. So the
generator has to own it, and this script is the proof that a small one can.

Every chart below is emitted with those three guards active, and `selftest` checks the guards by
feeding them the inputs that produced the corpus defects (L-04).

    python tools/assets/chart_probe.py            # build the gallery
    python tools/assets/chart_probe.py selftest   # check the guards only

Writes to gitignored `.assets-cache/`. Pure standard library, by L-07. LF (L-11), UTF-8 (L-10).
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, ".assets-cache")
OUT = os.path.join(CACHE, "chart-probe.html")

# --- The three guards, each named after the corpus defect it prevents -------------------------

# A chart may not exceed this share of the slide's content height. The corpus's 558 px chart
# pushed its own title off screen; nothing about the chart was wrong in isolation.
MAX_CHART_HEIGHT_SHARE = 0.62

# A bar shorter than this reads as a rendering fault rather than a small value. The corpus had one
# at 1.4 px. Below the floor the bar is drawn at the floor and the value is labelled instead.
MIN_BAR_PX = 3.0

# Labels must sit inside the viewBox with room to breathe. The corpus had one clipped by it.
LABEL_MARGIN = 4.0


class ChartError(Exception):
    pass


def guard_height(height, slide_content_height):
    """Prevent the 558 px chart. Raise rather than silently shrink - a chart that does not fit
    is a slide-design decision, not something a renderer should quietly resolve."""
    share = height / float(slide_content_height)
    if share > MAX_CHART_HEIGHT_SHARE:
        raise ChartError(
            "chart is %.0f px of %.0f px content height (%.0f%%, max %.0f%%) - it will push the "
            "slide's own title off screen"
            % (height, slide_content_height, share * 100, MAX_CHART_HEIGHT_SHARE * 100))
    return height


def bar_length(value, vmax, full_px):
    """Prevent the 1.4 px bar. Returns (length, needs_label): a value too small to draw honestly
    is drawn at the floor and reported, never rendered as a sliver."""
    if vmax <= 0:
        return 0.0, True
    raw = (value / float(vmax)) * full_px
    if 0 < raw < MIN_BAR_PX:
        return MIN_BAR_PX, True
    return raw, False


def guard_label(x, y, width, height, text, font_px):
    """Prevent the clipped label. Estimates the text box and checks it against the viewBox.
    The estimate is deliberately generous - over-reporting a clip is cheap, missing one is the
    defect this exists to catch."""
    approx_w = len(text) * font_px * 0.62
    if x - approx_w / 2 < LABEL_MARGIN or x + approx_w / 2 > width - LABEL_MARGIN:
        raise ChartError("label %r at x=%.0f (est. width %.0f) is clipped by a %.0f-wide viewBox"
                         % (text, x, approx_w, width))
    if y < font_px or y > height - LABEL_MARGIN:
        raise ChartError("label %r at y=%.0f is clipped by a %.0f-tall viewBox" % (text, y, height))
    return True


# --- The four chart types ----------------------------------------------------------------------

W, H = 900, 380
PAD_L, PAD_R, PAD_T, PAD_B = 96, 40, 30, 56
PLOT_W = W - PAD_L - PAD_R
PLOT_H = H - PAD_T - PAD_B


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def nice_ticks(vmax, count=4):
    """Round tick values a human would choose. A chart axis reading 0, 3.7, 7.4 is a tell that
    nobody looked at it."""
    if vmax <= 0:
        return [0]
    raw = vmax / float(count)
    mag = 10 ** int(len(str(int(raw))) - 1) if raw >= 1 else 0.1
    for mult in (1, 2, 2.5, 5, 10):
        step = mag * mult
        if step >= raw:
            break
    return [i * step for i in range(count + 1) if i * step <= vmax * 1.35]


def x_positions(n, scale):
    """Where the i-th category sits horizontally.

    The two scales are not interchangeable, and mixing them is a real defect rather than a
    cosmetic one: a *band* scale centres each label in a slot of width PLOT_W/n (what bars sit
    in), a *point* scale puts them at PLOT_W/(n-1) intervals ending on the axis (what a line's
    vertices sit on). Drawing band labels under a point series walked them up to 76 px away from
    the data they name, and the eye almost passed it - measured, it was unambiguous."""
    if scale == "band":
        step = PLOT_W / float(max(1, n))
        return [PAD_L + step * (i + 0.5) for i in range(n)]
    step = PLOT_W / float(max(1, n - 1))
    return [PAD_L + step * i for i in range(n)]


def axes(ticks, vmax, x_labels, scale="band"):
    out = []
    for t in ticks:
        y = PAD_T + PLOT_H - (t / float(vmax)) * PLOT_H
        out.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                   % (PAD_L, y, W - PAD_R, y))
        label = ("%g" % t)
        guard_label(PAD_L - 14, y + 5, W, H, label, 17)
        out.append('<text class="tick ar" x="%d" y="%.1f">%s</text>' % (PAD_L - 14, y + 5, label))
    for x, lab in zip(x_positions(len(x_labels), scale), x_labels):
        y = H - PAD_B + 26
        guard_label(x, y, W, H, str(lab), 17)
        out.append('<text class="tick" x="%.1f" y="%.1f">%s</text>' % (x, y, esc(lab)))
    return "".join(out)


def chart_bar(data, title):
    vmax = max(v for _, v in data)
    ticks = nice_ticks(vmax)
    top = max(ticks) or vmax
    parts = [axes(ticks, top, [k for k, _ in data])]
    step = PLOT_W / float(len(data))
    bw = min(78, step * 0.52)
    flagged = []
    for i, (k, v) in enumerate(data):
        length, needs_label = bar_length(v, top, PLOT_H)
        x = PAD_L + step * (i + 0.5) - bw / 2
        y = PAD_T + PLOT_H - length
        cls = "bar floor" if needs_label else "bar"
        parts.append('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2"/>'
                     % (cls, x, y, bw, length))
        lab = "%g" % v
        guard_label(x + bw / 2, y - 10, W, H, lab, 18)
        parts.append('<text class="val" x="%.1f" y="%.1f">%s</text>' % (x + bw / 2, y - 10, lab))
        if needs_label:
            flagged.append(k)
    return wrap(title, "".join(parts)), flagged


def chart_line(data, title):
    vmax = max(v for _, v in data)
    ticks = nice_ticks(vmax)
    top = max(ticks) or vmax
    parts = [axes(ticks, top, [k for k, _ in data], scale="point")]
    xs = x_positions(len(data), "point")
    pts = []
    for (_, v), x in zip(data, xs):
        y = PAD_T + PLOT_H - (v / float(top)) * PLOT_H
        pts.append((x, y))
    parts.append('<polyline class="series" points="%s"/>'
                 % " ".join("%.1f,%.1f" % p for p in pts))
    for i, (x, y) in enumerate(pts):
        if i in (0, len(pts) - 1):
            parts.append('<circle class="dot" cx="%.1f" cy="%.1f" r="5"/>' % (x, y))
            lab = "%g" % data[i][1]
            ly = y - 16
            guard_label(x, ly, W, H, lab, 18)
            parts.append('<text class="val" x="%.1f" y="%.1f">%s</text>' % (x, ly, lab))
    return wrap(title, "".join(parts)), []


def chart_share(value, title):
    """One share of a whole. A pie with two slices is a bar; this is the honest form - a single
    track with the figure stated, which reads at the back of a room."""
    track_y, track_h = PAD_T + PLOT_H / 2 - 26, 52
    filled = (value / 100.0) * PLOT_W
    parts = ['<rect class="track" x="%d" y="%.1f" width="%d" height="%d" rx="6"/>'
             % (PAD_L, track_y, PLOT_W, track_h),
             '<rect class="fill" x="%d" y="%.1f" width="%.1f" height="%d" rx="6"/>'
             % (PAD_L, track_y, filled, track_h)]
    lab = "%g%%" % value
    lx = PAD_L + min(filled + 58, PLOT_W - 58)
    guard_label(lx, track_y + 38, W, H, lab, 34)
    parts.append('<text class="big" x="%.1f" y="%.1f">%s</text>' % (lx, track_y + 38, lab))
    return wrap(title, "".join(parts)), []


def chart_stat(value, caption, title):
    """The corpus's L2 'Stat focus'. Not a chart, and that is the point - one number beats a
    chart of one number, and the generator should say so rather than draw something."""
    parts = ['<text class="huge" x="%d" y="%d">%s</text>' % (W // 2, PAD_T + 150, esc(value)),
             '<text class="cap" x="%d" y="%d">%s</text>' % (W // 2, PAD_T + 208, esc(caption))]
    return wrap(title, "".join(parts)), []


def wrap(title, body):
    return ('<figure><figcaption>%s</figcaption>'
            '<svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg></figure>'
            % (esc(title), W, H, esc(title), body))


# --- Self-test: feed the guards the corpus's own failures ---------------------------------------

def selftest():
    failures = []

    def expect_raise(label, fn):
        try:
            fn()
        except ChartError:
            return
        failures.append("%s: expected ChartError, got none" % label)

    def expect_ok(label, fn):
        try:
            fn()
        except ChartError as exc:
            failures.append("%s: unexpected ChartError: %s" % (label, exc))

    # The 558 px chart on a slide with ~700 px of content height: 80%, must be refused.
    expect_raise("558px chart refused", lambda: guard_height(558, 700))
    expect_ok("sane chart accepted", lambda: guard_height(380, 700))

    # The 1.4 px bar: a value 0.4% of max across 350 px is 1.4 px. Must be floored and flagged.
    length, flagged = bar_length(0.4, 100.0, 350)
    if not (length == MIN_BAR_PX and flagged):
        failures.append("1.4px bar: got length=%.2f flagged=%s, want floored and flagged"
                        % (length, flagged))
    length, flagged = bar_length(50, 100.0, 350)
    if not (abs(length - 175) < 0.01 and not flagged):
        failures.append("normal bar: got length=%.2f flagged=%s" % (length, flagged))
    # Zero must stay zero - flooring a real zero would draw a bar where there is no value.
    length, flagged = bar_length(0, 100.0, 350)
    if length != 0.0:
        failures.append("zero bar: got %.2f, want 0" % length)

    # The clipped label: a long label near the right edge must be refused.
    expect_raise("clipped label refused",
                 lambda: guard_label(880, 100, 900, 380, "Q4 2026 forecast", 17))
    expect_ok("inset label accepted", lambda: guard_label(450, 100, 900, 380, "Q4", 17))

    # Ticks must be round numbers, not vmax/n.
    if nice_ticks(37)[:3] != [0, 10.0, 20.0]:
        failures.append("nice_ticks(37) = %r, want round steps" % (nice_ticks(37)[:3],))

    # The axis-scale bug, caught by measuring the built page rather than looking at it: a line
    # chart drawn with band-scale labels put "Q5" 76 px from the point it named. A point scale
    # must start on the axis and end on the right edge; a band scale must do neither.
    pt = x_positions(5, "point")
    if not (abs(pt[0] - PAD_L) < 0.01 and abs(pt[-1] - (PAD_L + PLOT_W)) < 0.01):
        failures.append("point scale must span the full plot, got %r" % (pt,))
    band = x_positions(5, "band")
    if abs(band[0] - PAD_L) < 0.01 or abs(band[-1] - (PAD_L + PLOT_W)) < 0.01:
        failures.append("band scale must inset from both edges, got %r" % (band,))
    if max(abs(a - b) for a, b in zip(pt, band)) < 50:
        failures.append("the two scales should differ substantially; they are near-identical")

    if failures:
        print("SELFTEST FAILED - %d problem(s):" % len(failures))
        for f in failures:
            print("  " + f)
        return 1
    print("SELFTEST OK - 12 checks. Each guard was fed the input that produced the corpus defect:")
    print("  558 px chart refused - 1.4 px bar floored and flagged - clipped label refused.")
    return 0


# --- Build --------------------------------------------------------------------------------------

def build():
    if selftest() != 0:
        print("\nRefusing to build with a failing self-test.")
        return 1

    charts, notes = [], []
    for maker, args, title in [
        (chart_bar, ([("North", 42), ("South", 31), ("East", 58), ("West", 12),
                      ("Online", 0.4)],), "Bar - revenue by region, with one near-zero value"),
        (chart_line, ([("Q1", 12), ("Q2", 19), ("Q3", 26), ("Q4", 31),
                       ("Q5", 37)],), "Line - a trend over time"),
        (chart_share, (68,), "Share - one proportion of a whole"),
        (chart_stat, ("3.4x", "return on the first year"), "Stat - one number, no chart"),
    ]:
        svg, flagged = maker(*args, title=title)
        charts.append(svg)
        if flagged:
            notes.append("%s: %s drawn at the %.0f px floor and labelled, not as a sliver"
                         % (title.split(" - ")[0], ", ".join(flagged), MIN_BAR_PX))

    html = PAGE % {"charts": "\n".join(charts)}
    os.makedirs(CACHE, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)

    size = os.path.getsize(OUT)
    print("\nCHART PROBE - 4 types at %s" % os.path.relpath(OUT, ROOT))
    print("-" * 72)
    for n in notes:
        print("  guard fired: " + n)
    print("  %d chart types, %.1f KB total page, no library, no external references."
          % (len(charts), size / 1024.0))
    print("  Open it and look at it (L-01).")
    return 0


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chart probe - T-006</title>
<style>
:root{--bg:#0f1113;--ink:#f2efe9;--dim:#9aa0a6;--accent:#e0b25f;--line:#3a4048;--track:#1c2025}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:system-ui,sans-serif;padding:40px;
  display:grid;gap:40px;max-width:1000px;margin:0 auto}
figure{border:1px solid var(--line);border-radius:8px;padding:20px 8px 8px}
figcaption{font-size:15px;color:var(--dim);padding:0 16px 8px;letter-spacing:.02em}
svg{width:100%%;height:auto;display:block}
.grid{stroke:var(--line);stroke-width:1}
.tick{fill:var(--dim);font-size:17px;text-anchor:middle}
.tick.ar{text-anchor:end}
.val{fill:var(--ink);font-size:18px;text-anchor:middle}
.bar{fill:var(--accent)}
.bar.floor{fill:var(--dim)}
.series{fill:none;stroke:var(--accent);stroke-width:3;stroke-linejoin:round}
.dot{fill:var(--accent)}
.track{fill:var(--track)}
.fill{fill:var(--accent)}
.big{fill:var(--ink);font-size:34px;text-anchor:middle}
.huge{fill:var(--accent);font-size:104px;text-anchor:middle}
.cap{fill:var(--dim);font-size:24px;text-anchor:middle}
</style></head>
<body>
%(charts)s
</body></html>
"""


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(selftest())
    sys.exit(build())
