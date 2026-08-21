#!/usr/bin/env python3
"""Compose `examples/portfolio-review/portfolio-review.html` from its specification's figures.

**Why this exists, and why it is a script rather than twelve hand-typed slides.**
[T-113] needs a chart-intensive deck to measure chart-library candidates against; the repository
had none, and every deck it ships carries at most one chart - the case hand-authored SVG already
wins. DS-122 requires those charts to be hand-written SVG *borrowing scale arithmetic as a few
lines*, and this file is what that sentence looks like when a deck needs seven charts instead of
one: the arithmetic is computed here, once, and the marks it produces are ordinary SVG.

**So it is also the measurement.** T-113 step 7 costs hand-authored SVG honestly, and an estimate
would not have been worth reading. What that costs is this file's length, and what it does not buy
is anything interactive: every hover value in this deck is the deck's own disclosure component, not
the chart's.

`tools/assets/chart_probe.py` already owns the three guards a chart in a slide must pass - the
558 px chart that pushed its own title off screen, the 1.4 px bar, and the label clipped by its own
viewBox. They are imported rather than restated (L-08), and the three chart kinds this deck needs
that the probe does not have - stacked area, waterfall and scatter - are added here rather than
there, because the probe's four are the ones a *business* deck needs and these three are the ones a
*financial* deck adds. That difference is itself a T-113 finding.

Every figure below comes from `examples/portfolio-review/sources/`, and every one of them is
illustrative: there is no Meridian Infrastructure Fund.

    python tools/examples/portfolio_charts.py           # compose the deck
    python tools/examples/portfolio_charts.py selftest   # check the arithmetic only

Pure standard library, by L-07. LF (L-11), UTF-8 (L-10).
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "assets"))

from chart_probe import guard_height, guard_label, MIN_BAR_PX          # noqa: E402

DECK = os.path.join(ROOT, "examples", "portfolio-review", "portfolio-review.html")
SOURCES = os.path.join(ROOT, "examples", "portfolio-review", "sources")

# --- The plot box, shared by every figure ------------------------------------------------------
# The content column starts at 120 and the viewBox starts there too, so a diagram's ink begins
# where the slide's text begins (`build.md` 2). Every chart below draws inside this box.

L, R = 120.0, 1660.0            # plot left and right
TOP, BASE = 40.0, 360.0         # plot top and baseline
NAMES_Y = 404.0                 # the row of category names under the baseline
NOTE_Y = 452.0                  # the one-line note under that
VIEWBOX = "120 0 1728 470"
SLIDE_CONTENT_H = 620.0         # what a slide gives its body, in the same units


# --- The model ---------------------------------------------------------------------------------
# Mirrors `sources/portfolio-model.md` and `sources/market-outlook.md`. Kept as data so the
# self-test can assert the identities the deck's own quality bar promises: the allocation columns
# sum to 100, the contributions sum to 12.4, and the waterfall closes on 2,400.

YEARS = [2022, 2023, 2024, 2025, 2026]

# bottom band first, which is the stacking order and the reading order
ALLOCATION = [
    ("Renewables",   [31, 36, 42, 47, 52]),
    ("Transmission", [22, 21, 20, 19, 18]),
    ("Digital",      [14, 17, 19, 21, 20]),
    ("Water",        [18, 15, 12,  9,  7]),
    ("Transport",    [15, 11,  7,  4,  3]),
]

CONTRIBUTION = [                      # percentage points of the FY26 total return
    ("Renewables",   8.1),
    ("Digital",      3.4),
    ("Transmission", 1.4),
    ("Water",        0.2),
    ("Transport",   -0.7),
]
FY26_RETURN = 12.4

WATERFALL = [                          # ($M) name, value, kind
    ("opening",       2150, "total"),
    ("contributions",  180, "up"),
    ("distributions", -145, "down"),
    ("realised",        95, "up"),
    ("revaluation",    172, "up"),
    ("fees, carry",    -52, "down"),
    ("closing",       2400, "total"),
]

RISK_RETURN = [                        # sector, net IRR %, volatility %
    ("Digital",      16.8, 15.4),
    ("Renewables",   14.2, 12.1),
    ("Transmission",  9.1,  6.2),
    ("Water",         7.4,  4.8),
    ("Transport",     5.9,  9.6),
]

CURVE = [(2026, 78), (2027, 74), (2028, 69), (2029, 64), (2030, 61)]
CURVE_LO, CURVE_HI = 55, 80            # a truncated axis, labelled as one on the slide

TOP3 = [("Calder wind", 13), ("Norbeck solar", 11), ("Aldis transmission", 10)]
TOP3_LIMIT = 30

DRAWDOWN = [                           # FY26 by quarter-end, cumulative % from the peak
    ("Q1", 0.0), ("Q2", -2.1), ("Q3", -6.8), ("Q4", -1.4), ("FY", 0.0),
]

TRANCHES = [("Q1 2027", 70, 49), ("Q3 2027", 60, 47), ("Q1 2028", 40, 45)]


# --- Scale arithmetic --------------------------------------------------------------------------
# Four functions. This is the whole of what DS-122 means by "borrowing scale arithmetic as a few
# lines", and it is what a chart library would replace.

def linear(v, lo, hi, out_lo, out_hi):
    """Map a value onto a pixel range. Nothing here clamps: a value outside the domain is a data
    error and drawing it off the plot is how it gets noticed."""
    if hi == lo:
        raise ValueError("empty domain %r-%r" % (lo, hi))
    return out_lo + (float(v) - lo) * (out_hi - out_lo) / float(hi - lo)


def y_of(v, lo, hi):
    """Value to a y coordinate, inverted, because SVG's y grows downward."""
    return linear(v, lo, hi, BASE, TOP)


def band(n, lo=None, hi=None, inset=0.5):
    """n band centres across the plot. `inset` is the half-band kept at each end so the first and
    last marks do not sit on the axis ends."""
    lo = L if lo is None else lo
    hi = R if hi is None else hi
    step = (hi - lo) / (n - 1 + 2 * inset)
    return [lo + step * (inset + i) for i in range(n)]


def fmt(v, dp=0, group=False):
    """A number as it is read, not as Python prints it."""
    s = format(float(v), ",.%df" % dp) if group else (("%%.%df" % dp) % v)
    return s.replace("-", "−")            # a real minus sign, not a hyphen


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def svg(aria, body, viewbox=VIEWBOX):
    return ('<svg class="fig" preserveAspectRatio="xMinYMid meet" viewBox="%s" role="img"\n'
            '         aria-label="%s">\n%s\n    </svg>' % (viewbox, esc(aria), body))


def text(x, y, s, cls="val", anchor="middle"):
    return ('      <text class="%s" x="%s" y="%s" text-anchor="%s">%s</text>'
            % (cls, fmt(x, 1).rstrip("0").rstrip("."), fmt(y, 1).rstrip("0").rstrip("."),
               anchor, esc(s)))


def rect(x, y, w, h, cls):
    return ('      <rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
            % (cls, x, y, max(w, 0.0), max(h, 0.0)))


# --- The seven figures --------------------------------------------------------------------------

def fig_curve():
    """Slide 2. Five points, one series, a deliberately truncated axis that says so."""
    # This chart shares its slide with two figures, so it is drawn to a column-sized viewBox
    # rather than a full-width one. A full-width viewBox in a two-thirds column scales every
    # label down with it, and the axis note landed at 12.5 du against DS-035's 16.
    base, top, right = 300.0, 60.0, 1160.0
    xs = band(len(CURVE), 200, 1080)
    ys = [linear(v, CURVE_LO, CURVE_HI, base, top) for _, v in CURVE]
    guard_height(base - top, SLIDE_CONTENT_H)
    o = ['      <line class="axis" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>' % (L, base, right, base)]
    o.append('      <path class="accent-s" fill="none" stroke-width="4" d="%s"/>'
             % " ".join(("M" if i == 0 else "L") + "%.1f %.1f" % (xs[i], ys[i])
                        for i in range(len(xs))))
    for i, (yr, v) in enumerate(CURVE):
        first_or_last = i in (0, len(CURVE) - 1)
        o.append('      <circle class="%s" cx="%.1f" cy="%.1f" r="%d"/>'
                 % ("accent" if first_or_last else "quiet", xs[i], ys[i], 10 if first_or_last else 8))
        if first_or_last:
            o.append(text(xs[i], ys[i] - 28, "$%d" % v, "val t-accent"))
        o.append(text(xs[i], base + 44, str(yr), "name" if first_or_last else "name t-soft",
                      "start" if i == 0 else ("end" if first_or_last else "middle")))
    o.append(text(L, top - 14, "$/MWh — axis starts at 55, not zero", "lab t-soft", "start"))
    o.append(text(L, base + 96, "Contracted new supply of 14.2 GW against 3.1 GW of demand growth.",
                  "val t-soft", "start"))
    return svg("Modelled wholesale power price, 2026 to 2030: $78, $74, $69, $64 and $61 per MWh. "
               "The axis starts at 55 rather than zero. The fall is 22 percent.", "\n".join(o),
               "120 0 1060 400")


def fig_limit_bar():
    """Slide 3. One bar, one limit rule, and the overshoot drawn as the overshoot."""
    y, h = 62.0, 72.0
    x45, x52 = linear(45, 0, 100, L, R), linear(52, 0, 100, L, R)
    guard_height(h, SLIDE_CONTENT_H)
    o = [rect(L, y, x45 - L, h, "quiet"),
         rect(x45, y, x52 - x45, h, "accent"),
         '      <line class="axis" x1="%.1f" y1="%.0f" x2="%.1f" y2="%.0f"/>'
         % (x45, y - 22, x45, y + h + 22),
         text(x45, y - 34, "single-sector ceiling 45%", "lab t-soft"),
         text(x52 + 18, y + h / 2 + 10, "52%", "val t-accent", "start"),
         text(L, y + h + 62, "share of net asset value", "lab t-soft", "start")]
    return svg("Renewables at 52 percent of net asset value against a 45 percent policy limit. "
               "The seven-point overshoot is drawn beyond the limit rule.", "\n".join(o),
               "120 0 1728 210")


def fig_area():
    """Slide 4. Five bands stacked to 100 at every year. The densest chart in the deck."""
    xs = band(len(YEARS), 220, 1360, inset=0.0)
    keyx = 1400.0
    o = ['      <line class="axis" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>' % (L, BASE, 1360, BASE)]
    floor = [0.0] * len(YEARS)
    for si, (name, series) in enumerate(ALLOCATION):
        tops = [floor[i] + series[i] for i in range(len(YEARS))]
        up = ["%.1f %.1f" % (xs[i], y_of(tops[i], 0, 100)) for i in range(len(YEARS))]
        down = ["%.1f %.1f" % (xs[i], y_of(floor[i], 0, 100)) for i in range(len(YEARS) - 1, -1, -1)]
        o.append('      <path class="%s" d="M%s L%s Z"/>'
                 % ("accent" if si == 0 else "quiet", up[0], " L".join(up[1:] + down)))
        mid = (floor[-1] + tops[-1]) / 2.0
        ky = y_of(mid, 0, 100) + 6
        guard_label(keyx, ky, 1728 - 120, 470, name, 22)
        o.append(text(keyx, ky, "%s  %d → %d" % (name, series[0], series[-1]),
                      "name", "start"))
        floor = tops
    for i, yr in enumerate(YEARS):
        o.append(text(xs[i], NAMES_Y, str(yr), "name t-soft"))
    o.append(text(keyx, y_of(52, 0, 100) - 34, "renewables  +21 points", "val t-accent", "start"))
    o.append(text(L, TOP - 8, "share of NAV, %  —  every column sums to 100",
                  "lab t-soft", "start"))
    return svg("Share of net asset value by sector, 2022 to 2026, stacked to 100 percent. "
               "Renewables rises from 31 to 52, transmission 22 to 18, digital 14 to 20, "
               "water 18 to 7, transport 15 to 3.", "\n".join(o))


def fig_contribution():
    """Slide 5. Five bars against one axis, one of them negative and crossing the zero rule."""
    lo, hi = -1.0, 8.6
    bar_l, bar_r = 560.0, R                  # the names occupy the column edge, the bars start clear
    zero = linear(0, lo, hi, bar_l, bar_r)
    top, bh, gap = 60.0, 44.0, 20.0
    o = ['      <line class="axis" x1="%.1f" y1="%.0f" x2="%.1f" y2="%.1f"/>'
         % (zero, top - 16, zero, top + len(CONTRIBUTION) * (bh + gap))]
    for i, (name, v) in enumerate(CONTRIBUTION):
        y = top + i * (bh + gap)
        x = linear(v, lo, hi, bar_l, bar_r)
        w = abs(x - zero)
        if w < MIN_BAR_PX:                       # the 1.4 px bar the probe's guard is named for
            w = MIN_BAR_PX
        cls = "neg" if v < 0 else ("accent" if i == 0 else "quiet")
        o.append(rect(min(zero, x), y, w, bh, cls))
        o.append(text(L, y + bh - 12, name, "name", "start"))
        lx = (x + 14) if v >= 0 else (x - 14)
        o.append(text(lx, y + bh - 12, ("+" if v >= 0 else "−") + fmt(abs(v), 1),
                      "val t-accent" if i == 0 else ("val t-caution" if v < 0 else "val"),
                      "start" if v >= 0 else "end"))
    foot = top + len(CONTRIBUTION) * (bh + gap) + 34
    o.append(text(zero, foot, "0", "lab t-soft"))
    o.append(text(L, foot, "total +%s" % fmt(FY26_RETURN, 1), "val", "start"))
    o.append(text(L, foot + 40, "percentage points of the FY26 return",
                  "lab t-soft", "start"))
    return svg("Contribution to the FY26 return by sector, in percentage points: renewables plus "
               "8.1, digital plus 3.4, transmission plus 1.4, water plus 0.2, transport minus 0.7. "
               "They total plus 12.4.", "\n".join(o), "120 0 1728 480")


def fig_waterfall():
    """Slide 6. Two grounded bars, five floating, and the connectors that make it a waterfall."""
    hi = 2500.0
    xs = band(len(WATERFALL), 190, 1590, inset=0.0)
    bw = 140.0                               # so the first bar's left edge lands exactly on 120
    o, run, tops = [], 0.0, []
    for i, (name, v, kind) in enumerate(WATERFALL):
        x = xs[i] - bw / 2
        if kind == "total":
            y0, y1 = 0.0, float(v)
        else:
            y0, y1 = run, run + v
        run = y1 if kind != "total" else float(v)
        ytop, ybot = y_of(max(y0, y1), 0, hi), y_of(min(y0, y1), 0, hi)
        cls = {"total": "quiet", "up": "pos", "down": "neg"}[kind]
        if name == "revaluation":
            cls = "accent"
        o.append(rect(x, ytop, bw, max(ybot - ytop, MIN_BAR_PX), cls))
        tops.append((x, x + bw, ytop, ybot))
        # The two grounded bars are the deck's opening and closing NAV and are read as money,
        # so they carry a thousands separator; the five movements are read as deltas and do not.
        o.append(text(xs[i], ytop - 14, ("+" if v > 0 and kind != "total" else "") + fmt(abs(v))
                      if kind != "total" else fmt(v, 0, True),
                      "val t-accent" if cls == "accent" else "val"))
        o.append(text(xs[i], NAMES_Y, name, "name" if cls == "accent" else "name t-soft"))
    for i in range(len(tops) - 1):
        _, xr, ytop, ybot = tops[i]
        nxt = tops[i + 1]
        yy = ytop if WATERFALL[i][1] >= 0 or WATERFALL[i][2] == "total" else ybot
        yy = min(ytop, nxt[2]) if WATERFALL[i + 1][2] == "up" else max(ybot, nxt[3])
        yy = nxt[2] if WATERFALL[i + 1][2] in ("up", "total") else nxt[2]
        o.append('      <line class="grid" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                 % (xr, yy, nxt[0], yy))
    o.append('      <line class="axis" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>' % (L, BASE, R, BASE))
    o.append(text(L, TOP - 8, "$M", "lab t-faint", "start"))
    o.append(text(L, NOTE_Y, "$131M of the revaluation sits in renewables.", "val t-soft", "start"))
    return svg("NAV movement over FY26 in millions: opening 2,150, contributions plus 180, "
               "distributions minus 145, realised gains plus 95, unrealised revaluation plus 172, "
               "fees and carry minus 52, closing 2,400.", "\n".join(o))


def fig_scatter():
    """Slide 7. Five points, both axes, and one reference line so 'below' means something."""
    plot_l, plot_r = 280.0, 1460.0
    lo, hi = 0.0, 18.0
    o = ['      <line class="axis" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>' % (plot_l, BASE, R, BASE),
         '      <line class="axis" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>' % (plot_l, BASE, plot_l, TOP)]
    d0 = (linear(0, lo, hi, plot_l, plot_r), y_of(0, lo, hi))
    d1 = (linear(18, lo, hi, plot_l, plot_r), y_of(18, lo, hi))
    o.append('      <line class="grid" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
             'stroke-dasharray="6 8"/>' % (d0[0], d0[1], d1[0], d1[1]))
    o.append(text(d1[0] + 10, d1[1] + 26, "equal return per unit of risk", "lab t-faint", "start"))
    for name, irr, vol in RISK_RETURN:
        cx, cy = linear(vol, lo, hi, plot_l, plot_r), y_of(irr, lo, hi)
        below = irr < vol
        o.append('      <circle class="%s" cx="%.1f" cy="%.1f" r="%d"/>'
                 % ("caution" if below else "quiet", cx, cy, 13 if below else 11))
        guard_label(cx, cy - 24, 1728 - 120, 470, name, 22)
        o.append(text(cx, cy - 24, "%s  %s / %s" % (name, fmt(irr, 1), fmt(vol, 1)),
                      "val t-caution" if below else "val t-soft"))
    o.append(text(R, NAMES_Y, "volatility %", "lab t-soft", "end"))
    o.append(text(L, TOP + 12, "net IRR %", "lab t-soft", "start"))
    o.append(text(L, NOTE_Y, "Each point is labelled with its IRR and its volatility.",
                  "val t-soft", "start"))
    return svg("Net IRR against volatility by sector: digital 16.8 at 15.4, renewables 14.2 at "
               "12.1, transmission 9.1 at 6.2, water 7.4 at 4.8, transport 5.9 at 9.6. Transport "
               "sits below the equal-return line.", "\n".join(o))


def fig_top3():
    """Slide 8. The same grammar as slide 3, because it is the same kind of fact."""
    y, h = 62.0, 72.0
    hi = 40.0
    o, run = [], 0.0
    for i, (name, v) in enumerate(TOP3):
        x0, x1 = linear(run, 0, hi, L, R), linear(run + v, 0, hi, L, R)
        o.append(rect(x0, y, x1 - x0, h, "accent" if i == 0 else "quiet"))
        # The value sits with the name under the bar, not on it: a label on a data mark owes
        # two contrast ratios (DS-219) and two of these three could not pay the second.
        o.append(text((x0 + x1) / 2, y + h + 40, "%s  %d%%" % (name, v),
                      "name" if i == 0 else "name t-soft"))
        run += v
    xlim = linear(TOP3_LIMIT, 0, hi, L, R)
    xend = linear(run, 0, hi, L, R)
    o.append('      <line class="axis" x1="%.1f" y1="%.0f" x2="%.1f" y2="%.0f"/>'
             % (xlim, y - 22, xlim, y + h + 22))
    o.append(text(xlim, y - 34, "top-three ceiling 30%", "lab t-soft"))
    o.append(text(xend + 18, y + h / 2 + 10, "34%", "val t-accent", "start"))
    o.append(text(L, y + h + 96, "share of net asset value, three largest assets",
                  "lab t-soft", "start"))
    return svg("The three largest assets hold 34 percent of net asset value against a 30 percent "
               "policy limit: Calder wind 13, Norbeck solar 11, Aldis transmission 10.",
               "\n".join(o), "120 0 1728 220")


def fig_drawdown():
    """Slide 10, left column. The trough marked, and the part of it that is renewables shaded."""
    lo, hi = -8.0, 1.0
    base, top = 250.0, 60.0
    xs = band(len(DRAWDOWN), 120, 740, inset=0.0)
    zero_y = linear(0, lo, hi, base, top)
    o = ['      <line class="grid" x1="120" y1="%.1f" x2="740" y2="%.1f" stroke-dasharray="6 8"/>'
         % (zero_y, zero_y)]
    pts = [(xs[i], linear(v, lo, hi, base, top)) for i, (_, v) in enumerate(DRAWDOWN)]
    o.append('      <path class="accent-s" fill="none" stroke-width="4" d="%s"/>'
             % " ".join(("M" if i == 0 else "L") + "%.1f %.1f" % p for i, p in enumerate(pts)))
    trough_i = min(range(len(DRAWDOWN)), key=lambda i: DRAWDOWN[i][1])
    tx, ty = pts[trough_i]
    ry = linear(-5.1, lo, hi, base, top)
    o.append(rect(tx - 40, ty, 80, ry - ty, "caution"))
    o.append('      <circle class="caution" cx="%.1f" cy="%.1f" r="12"/>' % (tx, ty))
    o.append(text(tx, ty + 40, "−6.8%", "val t-caution"))
    o.append(text(tx, ty - 20, "5.1 pts renewables", "lab t-soft"))
    for i, (q, _) in enumerate(DRAWDOWN):
        o.append(text(xs[i], base + 46, q, "name t-soft",
                      "start" if i == 0 else ("end" if i == len(DRAWDOWN) - 1 else "middle")))
    return svg("FY26 drawdown by quarter: flat, minus 2.1, minus 6.8 at the trough, minus 1.4, "
               "flat at year end. Renewables carried 5.1 points of the 6.8.",
               "\n".join(o), "120 0 660 310")


def fig_tranches():
    """Slide 10, right column. Three bars, deliberately a different chart kind to its neighbour."""
    hi = 80.0
    base, top = 250.0, 60.0
    bw = 110.0
    xs = band(len(TRANCHES), 180.0, 690.0, inset=0.0)
    o = ['      <line class="axis" x1="120" y1="%.0f" x2="740" y2="%.0f"/>' % (base, base)]
    for i, (when, size, _) in enumerate(TRANCHES):
        ytop = linear(size, 0, hi, base, top)
        o.append(rect(xs[i] - bw / 2, ytop, bw, base - ytop, "accent" if i == 0 else "quiet"))
        o.append(text(xs[i], ytop - 14, "$%dM" % size, "val t-accent" if i == 0 else "val"))
        o.append(text(xs[i], base + 46, when, "name" if i == 0 else "name t-soft",
                      "start" if i == 0 else "middle"))
    return svg("The rebalancing programme in three tranches: $70M in Q1 2027, $60M in Q3 2027 "
               "and $40M in Q1 2028.", "\n".join(o), "120 0 660 310")


def fig_timeline():
    """Slide 11. Three step markers and one gate, and the gate must not look like a fourth step."""
    y = 200.0
    xs = [420.0, 1000.0, 1500.0]
    gate_x = 710.0
    o = ['      <line class="axis" x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>' % (240, y, 1620, y)]
    for i, ((when, size, to), x) in enumerate(zip(TRANCHES, xs)):
        o.append('      <circle class="%s" cx="%.0f" cy="%.0f" r="16"/>'
                 % ("accent" if i == 0 else "quiet", x, y))
        o.append(text(x, y - 44, when, "name" if i == 0 else "name t-soft"))
        o.append(text(x, y + 58, "$%dM" % size, "val t-accent" if i == 0 else "val"))
        o.append(text(x, y + 100, "to %d%%" % to, "lab t-soft"))
    # The gate carries its label inside itself (COMPONENT-CONTRACT 3.6), so the rhombus is sized
    # to the text rather than the text placed near a rhombus.
    hw, hh = 132.0, 74.0
    o.append('      <g class="decision">')
    o.append('        <path class="decision-shape" d="M%.0f %.0f L%.0f %.0f L%.0f %.0f L%.0f %.0f Z"/>'
             % (gate_x, y - hh, gate_x + hw, y, gate_x, y + hh, gate_x - hw, y))
    o.append('        <text class="decision-label" x="%.0f" y="%.0f" text-anchor="middle">gate</text>'
             % (gate_x, y - 6))
    o.append('        <text class="decision-label" x="%.0f" y="%.0f" text-anchor="middle">'
             'realised vs 4.5%%</text>' % (gate_x, y + 26))
    o.append('      </g>')
    o.append(text(240, NOTE_Y, "The committee reviews the realised discount before tranche two.",
                  "val t-soft", "start"))
    return svg("A timeline with three tranches and one gate: $70M in Q1 2027 to 49 percent, then "
               "a committee gate reviewing the realised discount against 4.5 percent, then $60M "
               "in Q3 2027 to 47 percent and $40M in Q1 2028 to 45 percent.",
               "\n".join(o), "240 0 1450 480")


# --- The self-test: the identities the deck's own quality bar promises --------------------------

def selftest():
    """Every total the deck states must be checkable against its parts on the same slide. That is
    this deck's added quality bar, and a bar nothing tests is a bar that passes everything."""
    fails = []

    def check(label, ok, detail=""):
        print("  %-4s %s%s" % ("ok" if ok else "FAIL", label, ("  - " + detail) if detail else ""))
        if not ok:
            fails.append(label)

    for i, yr in enumerate(YEARS):
        total = sum(s[i] for _, s in ALLOCATION)
        check("allocation %d sums to 100" % yr, total == 100, "got %d" % total)

    total = round(sum(v for _, v in CONTRIBUTION), 1)
    check("contributions sum to the FY26 return", total == FY26_RETURN,
          "got %s against %s" % (total, FY26_RETURN))

    run = 0.0
    for name, v, kind in WATERFALL:
        run = float(v) if kind == "total" else run + v
    check("the waterfall closes on 2,400", run == 2400, "got %s" % run)

    opening = WATERFALL[0][1]
    moves = sum(v for _, v, k in WATERFALL if k != "total")
    check("opening plus the movements is the close", opening + moves == WATERFALL[-1][1],
          "%d + %d" % (opening, moves))

    check("the top three sum to the stated 34%", sum(v for _, v in TOP3) == 34)
    check("the tranches take renewables to the 45% limit", TRANCHES[-1][2] == 45)
    check("the tranches sum to the $170M to be moved",
          sum(s for _, s, _ in TRANCHES) == 170, "got %d" % sum(s for _, s, _ in TRANCHES))

    # every figure builds, and every guard it calls is live
    for name, fn in FIGURES.items():
        try:
            out = fn()
            check("%s builds" % name, "<svg" in out and "</svg>" in out)
        except Exception as exc:                                     # noqa: BLE001
            check("%s builds" % name, False, "%s: %s" % (type(exc).__name__, exc))

    print("\n%d of %d checks passed." % (len(FIGURES) + 12 - len(fails), len(FIGURES) + 12))
    return 1 if fails else 0


FIGURES = {
    "curve": fig_curve, "limit": fig_limit_bar, "area": fig_area,
    "contribution": fig_contribution, "waterfall": fig_waterfall, "scatter": fig_scatter,
    "top3": fig_top3, "drawdown": fig_drawdown, "tranches": fig_tranches,
    "timeline": fig_timeline,
}


# --- The source documents, rendered into the deck's quick view ----------------------------------
# The quick view shows the source the slide rests on. Rendering it from `sources/*.md` rather than
# retyping it is the same rule the figure ledger follows: one home per fact (L-08). The subset is
# deliberately small - headings, paragraphs, tables and bold - because a source model is written in
# that subset and a fuller renderer would be a second markdown implementation to keep honest.

def md_to_html(md):
    out, rows, para = [], [], []

    def flush_para():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para)))
            del para[:]

    def flush_rows():
        if not rows:
            return
        cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
        body = ["<tr>%s</tr>" % "".join("<th>%s</th>" % inline(c) for c in cells[0])]
        for r in cells[1:]:
            if set("".join(r)) <= set("-: "):
                continue
            body.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r))
        out.append("<table>%s</table>" % "".join(body))
        del rows[:]

    def inline(s):
        s = esc(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        return s

    for line in md.splitlines():
        s = line.rstrip()
        if s.startswith("|"):
            flush_para()
            rows.append(s)
            continue
        flush_rows()
        if not s.strip():
            flush_para()
        elif s.startswith("### "):
            flush_para()
            out.append("<h3>%s</h3>" % inline(s[4:]))
        elif s.startswith("## "):
            flush_para()
            out.append("<h2>%s</h2>" % inline(s[3:]))
        elif s.startswith("# "):
            flush_para()
            out.append("<h1>%s</h1>" % inline(s[2:]))
        else:
            para.append(s.strip())
    flush_para()
    flush_rows()
    return "".join(out)


SOURCE_TITLES = {"portfolio-model": "Portfolio model", "market-outlook": "Market outlook"}


def quick_view(slug):
    with open(os.path.join(SOURCES, slug + ".md"), encoding="utf-8") as fh:
        return md_to_html(fh.read())


def provenance(slugs, box_id):
    """One source reads as the provenance line itself; two read as a disclosure (CONTRACT 3.2)."""
    items = []
    for slug in slugs:
        title = SOURCE_TITLES[slug]
        items.append(
            '<span class="sources-item">'
            + ('<svg class="sources-icon" aria-hidden="true"><use href="#i-source"></use></svg>'
               if len(slugs) > 1 else "")
            + '<button class="sources-open" type="button" data-qv="%s" data-file="%s.md">%s</button>'
              % (title, slug, title)
            + '<template class="qv-src" data-qv="%s">%s</template>' % (title, quick_view(slug))
            + "</span>")
    if len(slugs) == 1:
        return ('  <p class="provenance"><span class="sources sources--one">'
                '<svg class="sources-mark" aria-hidden="true"><use href="#i-source"/></svg>'
                '<span class="sources-box" id="%s">%s</span></span></p>' % (box_id, items[0]))
    return ('  <p class="provenance"><span class="sources">'
            '<button class="sources-btn" aria-expanded="false" aria-controls="%s">'
            '<svg class="sources-mark" aria-hidden="true"><use href="#i-sources"/></svg>'
            '<span class="sources-label">%d sources</span></button>'
            '<span class="sources-box" id="%s" hidden>%s</span></span></p>'
            % (box_id, len(slugs), box_id, "".join(items)))


def disclosure(kind, label, panel_id, rows):
    o = ['  <div class="disc" data-disc="%s">' % kind,
         '    <button class="disc-btn" aria-expanded="false" aria-controls="%s">' % panel_id,
         '      <span class="disc-mark" aria-hidden="true"></span>',
         '      <span class="disc-label">%s</span>' % esc(label),
         '    </button>',
         '    <div class="disc-panel" id="%s" hidden>' % panel_id]
    for k, v in rows:
        o.append('      <div class="row"><span class="k">%s</span><span>%s</span></div>'
                 % (esc(k), esc(v)))
    o += ['    </div>', '  </div>']
    return "\n".join(o)


def slide(n, stage, name, eyebrow, headline, body, bottom, slugs,
          standfirst=None, disc=None, body_cls="body"):
    o = ['<section class="slide" data-name="%s" data-stage="%s" aria-label="Slide %d">'
         % (esc(name), stage, n),
         '  <header>',
         '    <p class="eyebrow rise" style="--i:0"><span class="tick"></span>%s</p>' % esc(eyebrow),
         '    <h2 class="headline rise" style="--i:1">%s</h2>' % esc(headline)]
    if standfirst:
        o.append('    <p class="standfirst rise" style="--i:2">%s</p>' % esc(standfirst))
    o += ['  </header>',
          '  <div class="%s rise" style="--i:3">' % body_cls, body, '  </div>']
    if disc:
        o.append(disc)
    o.append('  <p class="bottom-line rise" style="--i:4"><b>%s</b></p>' % esc(bottom))
    o.append(provenance(slugs, "src%d" % n))
    o.append('</section>')
    return "\n".join(o)


def figure_body(fig):
    return "    " + fig


# --- The twelve slides ---------------------------------------------------------------------------
# Stage numbers are positions into STAGES, not names (CONTRACT 3.2).

STAGES = ["The position", "How it arrived", "What it costs to keep", "The fix, priced", "The ask"]
STAGE_ICON = ["i-position", "i-drift", "i-risk", "i-cost", "i-ask"]
ICON_SET = ("position=target,drift=trending-up,risk=circle-alert,cost=dollar-sign,"
            "ask=check,source=file-text,sources=library")


def build_slides():
    s = []

    s.append(slide(
        1, "0", "Concentration, not performance", "Meridian Infrastructure Fund · investment committee",
        "Concentration, not performance",
        '    <div class="two-fig">\n'
        '      <div class="two-fig-item"><p class="two-fig-val pulse">'
        '<span>52%</span></p><p class="two-fig-lab">share of the fund</p></div>\n'
        '      <div class="two-fig-item"><p class="two-fig-val pulse">'
        '<span>65%</span></p><p class="two-fig-lab">share of the return</p></div>\n'
        '      <p class="title-note">Meridian Infrastructure Fund is illustrative. It does not '
        'exist. Every figure here is an output of the assumptions in the source it names. '
        'None is drawn from a real fund, manager or transaction.</p>\n'
        '    </div>',
        "Renewables is 52% of the fund and produced 65% of the year's return.",
        ["portfolio-model"],
        standfirst="One sector holds the position and produced the year."))

    s.append(slide(
        2, "0", "The curve falls 22% by 2030", "Why this meeting",
        "The curve falls 22% by 2030",
        '    <div class="split">\n      <div class="split-fig">%s</div>\n'
        '      <div class="split-side">\n'
        '        <p class="side-val">39%%</p><p class="side-lab">of renewable revenue is uncontracted</p>\n'
        '        <p class="side-val">$310M</p><p class="side-lab">of NAV re-contracts before 2030</p>\n'
        '      </div>\n    </div>' % fig_curve(),
        "Our largest sector's uncontracted revenue basis falls a fifth while its NAV share peaks.",
        ["market-outlook"],
        disc=disclosure("derivation", "How the 22% was produced", "p2", [
            ("Curve", "Modelled calendar-year average, $78/MWh in 2026 falling to $61 in 2030."),
            ("Supply", "14.2 GW contracted to reach commercial operation between 2027 and 2029."),
            ("Demand", "Modelled growth of 3.1 GW over the same window."),
            ("Effect", "Weighted across the portfolio, renewables revenue moves −8.6% by 2030."),
        ])))

    s.append(slide(
        3, "0", "Renewables reached 52% of NAV", "Single-sector limit",
        "Renewables reached 52% of NAV",
        '    <div class="stat">\n'
        '      <div class="stat-left">\n'
        '        <p class="stat-scale">$2.40B net asset value</p>\n'
        '        <p class="stat-figure pulse"><span>52%%</span></p>\n'
        '        <p class="stat-unit">of the fund, above its own ceiling</p>\n'
        '      </div>\n'
        '      <div class="stat-right"><p class="stat-read">Seven points above the single-sector '
        'limit, on a position nobody bought.</p></div>\n'
        '    </div>\n    %s' % fig_limit_bar(),
        "The policy limit is 45%, and no purchase caused the breach.",
        ["portfolio-model"]))

    s.append(slide(
        4, "1", "Five years of quiet drift", "Allocation, 2022 to 2026",
        "Five years of quiet drift",
        figure_body(fig_area()),
        "Renewables rose 21 points in five years without a single allocation decision.",
        ["portfolio-model"], body_cls="body figwrap",
        standfirst="No allocation decision moved this. Revaluation did.",
        disc=disclosure("derivation", "What moved the share", "p4", [
            ("Purchases", "No renewable asset was bought in the window; two were bought in 2021."),
            ("Revaluation", "$131M of FY26's $172M revaluation sits in the sector."),
            ("Denominator", "Water and transport ran down through distribution, not sale."),
            ("Net effect", "31% to 52% with the allocation committee taking no decision on it."),
        ])))

    s.append(slide(
        5, "1", "Two sectors carried the year", "FY26 return by sector",
        "Two sectors carried the year",
        figure_body(fig_contribution()),
        "Renewables and digital produced 92% of FY26's 12.4% return, and transport subtracted.",
        ["portfolio-model"], body_cls="body figwrap",
        disc=disclosure("derivation", "How a contribution is computed", "p5", [
            ("Method", "Sector return weighted by its average share of NAV across the year."),
            ("Renewables", "16.2% sector return at a 50.0% average share is +8.1 points."),
            ("Transport", "−19.4% sector return at a 3.5% average share is −0.7 points."),
            ("Check", "The five contributions sum to the stated 12.4% total return."),
        ])))

    s.append(slide(
        6, "1", "The best year is a mark", "NAV movement, FY26",
        "The best year is a mark",
        figure_body(fig_waterfall()),
        "Unrealised revaluation is $172M of the movement, and $131M of it is renewables.",
        ["portfolio-model"], body_cls="body figwrap",
        standfirst="Six lines move the fund from 2,150 to 2,400. One of them is a valuation.",
        disc=disclosure("derivation", "What the $131M is", "p6", [
            ("Calder wind", "$58M, moved on a revised merchant tail beyond the contracted period."),
            ("Norbeck solar", "$44M, moved on a discount-rate change, not on operating performance."),
            ("Aldis transmission", "$29M, moved on the regulated asset base reset."),
            ("Realised", "None of the three was sold, refinanced or partially exited in the year."),
        ])))

    s.append(slide(
        7, "2", "Return does not track risk", "Net IRR against volatility",
        "Return does not track risk",
        figure_body(fig_scatter()),
        "Transport returns 5.9% at 9.6% volatility; water returns 7.4% at 4.8%.",
        ["portfolio-model"], body_cls="body figwrap",
        disc=disclosure("derivation", "How volatility is measured", "p7", [
            ("Measure", "Standard deviation of quarterly valuation movements, annualised."),
            ("Window", "The 36 quarters since inception, on the sector's own valuation series."),
            ("Excluded", "The two quarters around the 2023 valuation-policy change."),
            ("Caveat", "A private valuation series understates volatility against a traded one."),
        ])))

    s.append(slide(
        8, "2", "Top three assets hold 34%", "The second limit",
        "Top three assets hold 34%",
        '    <div class="stat">\n'
        '      <div class="stat-left">\n'
        '        <p class="stat-figure pulse"><span>34%%</span></p>\n'
        '        <p class="stat-unit">in three assets, above the second ceiling</p>\n'
        '      </div>\n'
        '      <div class="stat-right"><p class="stat-read">Two limits, both breached, and '
        'neither by a decision.</p></div>\n'
        '    </div>\n    %s' % fig_top3(),
        "The second limit is breached as well, against a 30% policy ceiling.",
        ["portfolio-model"],
        disc=disclosure("instances", "Which three assets", "p8", [
            ("Calder wind", "13% of NAV. Renewables. Acquired 2019, revalued twice since."),
            ("Norbeck solar", "11% of NAV. Renewables. Acquired 2021, the fund's largest single cheque."),
            ("Aldis transmission", "10% of NAV. Transmission. The only one of the three outside renewables."),
            ("Together", "34%, and two of the three are in the sector already over its own limit."),
        ])))

    s.append(slide(
        9, "3", "Rebalancing costs $22.5M", "What the recommendation costs",
        "Rebalancing costs $22.5M",
        '    <div class="sum">\n'
        '      <p class="sum-voice">This is what the recommendation costs, before anyone asks.</p>\n'
        '      <div class="sum-row"><span class="sum-lab">value forgone on sale</span>'
        '<span class="sum-val">$7.7M</span></div>\n'
        '      <div class="sum-row"><span class="sum-lab">redeployment drag</span>'
        '<span class="sum-val">$14.8M</span></div>\n'
        '      <div class="sum-row sum-total"><span class="sum-lab">total</span>'
        '<span class="sum-val pulse"><span>$22.5M</span></span></div>\n'
        '      <p class="sum-note">0.9% of net asset value, on $170M moved out of the sector.</p>\n'
        '    </div>',
        "Selling $170M forgoes $7.7M on discount and $14.8M idle, 0.9% of NAV.",
        ["portfolio-model"],
        disc=disclosure("condition", "What the total needs in order to hold", "p9", [
            ("Discount", "4.5% to carrying value. At 7% the first line becomes $11.9M."),
            ("Redeployment", "Nine months idle. At eighteen the second line becomes $29.6M."),
            ("Worst case", "Both moving together takes the total to $41.5M, 1.7% of NAV."),
            ("Where it fails", "If no buyer clears at under 8%, the programme returns to committee."),
        ])))

    s.append(slide(
        10, "3", "Holding is not the cheap option", "Hold against rebalance",
        "Holding is not the cheap option",
        '    <div class="ledger2">\n'
        '      <div class="col"><p class="col-head">Hold</p>%s\n'
        '        <p class="col-note">−6.8%% trough, 11 weeks to recover, 5.1 points renewables.</p></div>\n'
        '      <div class="col"><p class="col-head">Rebalance</p>%s\n'
        '        <p class="col-note">$22.5M one-off, spread over three tranches.</p></div>\n'
        '    </div>' % (fig_drawdown(), fig_tranches()),
        "Holding risks 5.1 points of renewables drawdown against a $22.5M one-off cost.",
        ["portfolio-model"],
        standfirst="Both columns are argued. Neither is free."))

    s.append(slide(
        11, "4", "Three tranches, one gate", "The programme",
        "Three tranches, one gate",
        figure_body(fig_timeline()),
        "Tranche one is $70M in Q1 2027, and the committee reviews the realised discount.",
        ["portfolio-model"], body_cls="body figwrap",
        disc=disclosure("condition", "What reopens the programme", "p11", [
            ("Trigger", "A realised discount above 4.5% on tranche one."),
            ("Then", "Tranches two and three are re-costed and return to this committee."),
            ("Not a trigger", "A power price inside the modelled curve. That is already assumed."),
            ("Held", "The 45% target itself, which is policy rather than this programme's choice."),
        ])))

    s.append(slide(
        12, "4", "Approve tranche one", "Tranche one, Q1 2027",
        "Approve tranche one",
        '    <div class="close">\n'
        '      <p class="close-ask">Approve tranche one — $70M, Q1 2027.</p>\n'
        '      <div class="close-cols">\n'
        '        <div><p class="close-head">This approves</p><p class="close-item">the $70M</p>'
        '<p class="close-item">the 4.5% discount assumption</p>'
        '<p class="close-item">the committee gate that follows</p></div>\n'
        '        <div><p class="close-head">This does not</p>'
        '<p class="close-item">tranches two and three, which return to this committee</p></div>\n'
        '      </div>\n    </div>',
        "Approve $70M in Q1 2027 and the gate that follows it.",
        ["portfolio-model"]))

    return "\n\n".join(s)


# --- This deck's own layout ----------------------------------------------------------------------
# Composition only. The look is the theme region's and the components are the shared block's; every
# value that could differ between themes is a token (DS-010).

COMPOSITION = """
/* this deck's own layout. The look is the theme region's; the components are the shared block's. */

/* 1 - the two figures that are the whole argument, side by side because they are read together */
.two-fig{display:grid;grid-template-columns:1fr 1fr;gap:var(--sp-5);align-content:end;
  align-self:end;padding-bottom:calc(24*var(--du))}
.two-fig-val{font-family:var(--font-display);font-size:var(--fs-figure);line-height:.9;
  color:var(--accent);display:inline-block;transform-origin:left center}
.two-fig-lab{font-family:var(--font-mono);font-size:var(--fs-small);letter-spacing:var(--track-mono);
  text-transform:uppercase;color:var(--ink-faint);margin-top:var(--sp-2)}
.title-note{grid-column:1 / -1;max-width:calc(1100*var(--du));color:var(--ink-soft);
  font-size:var(--fs-small);margin-top:var(--sp-4)}

/* 2 - a chart and two figures that qualify it. The chart is the claim; the figures are its size. */
.split{display:grid;grid-template-columns:1fr calc(460*var(--du));gap:var(--sp-5);align-items:center}
.split-fig{min-width:0}
.split-side{display:grid;gap:var(--sp-3);align-content:center;
  border-left:var(--rule) solid var(--accent);padding-left:var(--sp-4)}
.side-val{font-family:var(--font-display);font-size:var(--fs-title);line-height:1;color:var(--ink)}
.side-lab{font-family:var(--font-mono);font-size:var(--fs-mono);letter-spacing:var(--track-mono);
  text-transform:uppercase;color:var(--ink-faint)}

/* 3 and 8 - the same layout twice, on purpose: two limits, one grammar */
.stat{display:grid;grid-template-columns:calc(680*var(--du)) 1fr;gap:var(--sp-5);
  align-items:center;margin-bottom:var(--sp-4)}
.stat-scale{font-family:var(--font-mono);font-size:var(--fs-mono);letter-spacing:var(--track-mono);
  text-transform:uppercase;color:var(--ink-faint);margin-bottom:var(--sp-2)}
.stat-figure{font-family:var(--font-display);font-size:var(--fs-figure);line-height:.9;
  color:var(--accent);display:inline-block;transform-origin:left center}
.stat-unit{font-family:var(--font-mono);font-size:var(--fs-small);letter-spacing:var(--track-mono);
  text-transform:uppercase;color:var(--ink-faint);margin-top:var(--sp-2)}
.stat-right{display:grid;gap:var(--sp-3);align-content:center;
  border-left:var(--rule) solid var(--accent);padding-left:var(--sp-4)}
.stat-read{font-family:var(--font-display);font-size:var(--fs-subhead);line-height:1.3;
  max-width:var(--measure)}

.figwrap{position:relative}

/* 9 - three numbers that add up. The arithmetic is the layout, so there is no chart. */
.sum{display:grid;gap:var(--sp-2);align-content:center;max-width:calc(1180*var(--du))}
.sum-voice{font-family:var(--font-display);font-size:var(--fs-subhead);color:var(--ink-soft);
  margin-bottom:var(--sp-4);max-width:var(--measure)}
.sum-row{display:grid;grid-template-columns:1fr auto;align-items:baseline;gap:var(--sp-4);
  padding:var(--sp-2) 0}
.sum-total{border-top:var(--rule) solid var(--ink);margin-top:var(--sp-2);padding-top:var(--sp-3)}
.sum-lab{font-family:var(--font-mono);font-size:var(--fs-mono);letter-spacing:var(--track-mono);
  text-transform:uppercase;color:var(--ink-faint)}
.sum-val{font-family:var(--font-display);font-size:var(--fs-title);line-height:1;color:var(--ink)}
.sum-total .sum-val{font-size:var(--fs-figure);color:var(--accent);display:inline-block;
  transform-origin:right center}
.sum-note{font-size:var(--fs-small);color:var(--ink-soft);margin-top:var(--sp-3)}

/* 10 - two columns, both argued, drawn differently because they are not the same kind of claim */
.ledger2{display:grid;grid-template-columns:1fr 1fr;gap:var(--sp-5);align-items:start}
.ledger2 .col{display:grid;gap:var(--sp-3);align-content:start}
.ledger2 .col + .col{border-left:var(--hair) solid var(--line);padding-left:var(--sp-5)}
.col-head{font-family:var(--font-mono);font-size:var(--fs-mono);letter-spacing:var(--track-mono);
  text-transform:uppercase;color:var(--ink-soft)}
.col-note{font-size:var(--fs-small);color:var(--ink-soft);max-width:var(--measure)}

/* 12 - the close. One ask, and what it does not cover kept beside it rather than hidden. */
.close{display:grid;gap:var(--sp-5);align-content:center}
.close-ask{font-family:var(--font-display);font-size:var(--fs-subhead);line-height:1.2;
  color:var(--ink);max-width:var(--measure)}
.close-cols{display:grid;grid-template-columns:1fr 1fr;gap:var(--sp-5)}
.close-head{font-family:var(--font-mono);font-size:var(--fs-mono);letter-spacing:var(--track-mono);
  text-transform:uppercase;color:var(--ink-faint);margin-bottom:var(--sp-2)}
.close-item{font-size:var(--fs-body);color:var(--ink-soft);padding:var(--sp-1) 0;
  border-top:var(--hair) solid var(--line);max-width:var(--measure)}

/* the reading view reflows the composition; the components reflow themselves.
   Two things this half is for, and the second is the one that is easy to miss: every grid above
   collapses to a block, because a two-column track at 320 CSS px is DS-075's two-dimensional
   scroll; and every size above is restated in `--doc-*`, because the design unit is a different
   size here and a stage size carried into the document lands under DS-035's 16 du floor. */
.doc .two-fig,.doc .split,.doc .stat,.doc .ledger2,.doc .close-cols,.doc .sum-row{display:block}
.doc .two-fig{padding-bottom:0}
.doc .two-fig-val{font-size:var(--doc-fs-figure);display:block}
.doc .two-fig-lab,.doc .side-lab,.doc .sum-lab,.doc .col-head,.doc .close-head,
.doc .stat-unit,.doc .stat-scale{font-size:var(--doc-fs-mono)}
.doc .two-fig-item{margin-bottom:var(--doc-sp)}
.doc .title-note{font-size:var(--doc-fs);max-width:none;margin-top:var(--doc-sp-sm)}
.doc .split-side,.doc .stat-right{border-left:0;padding-left:0;margin-top:var(--doc-sp)}
.doc .side-val,.doc .sum-val{font-size:var(--doc-fs-lead)}
.doc .stat-read{font-size:var(--doc-fs-lead);max-width:none}
.doc .sum{max-width:none}
.doc .sum-voice{font-size:var(--doc-fs-lead);max-width:none;margin-bottom:var(--doc-sp)}
.doc .sum-row{padding:var(--doc-sp-2xs) 0}
.doc .sum-total{border-top:var(--doc-hair) solid var(--ink);padding-top:var(--doc-sp-sm)}
.doc .sum-total .sum-val{font-size:var(--doc-fs-figure);display:block}
.doc .sum-note{font-size:var(--doc-fs);margin-top:var(--doc-sp-sm)}
.doc .ledger2 .col + .col{border-left:0;padding-left:0;margin-top:var(--doc-sp)}
.doc .col-note{font-size:var(--doc-fs);max-width:none}
.doc .close-ask{font-size:var(--doc-fs-head);max-width:none}
.doc .close-cols > * + *{margin-top:var(--doc-sp)}
.doc .close-item{font-size:var(--doc-fs);max-width:none;
  border-top:var(--doc-hair) solid var(--line);padding:var(--doc-sp-2xs) 0}
"""


# --- Composing the deck ---------------------------------------------------------------------------

def compose():
    with open(DECK, encoding="utf-8", newline="") as fh:
        html = fh.read()

    marker = "<!-- slides go here, one section.slide each (COMPONENT-CONTRACT.md 3.2) -->"
    slides = build_slides()
    if marker in html:
        html = html.replace(marker, slides, 1)
    else:                              # a recompose: replace what a previous run wrote
        html = re.sub(r'(<main class="stage"[^>]*>\n).*?(\n<!-- =+ chrome -->)',
                      lambda m: m.group(1) + "\n" + slides + "\n" + m.group(2), html, count=1,
                      flags=re.S)

    html = re.sub(r'(<style id="slides">).*?(</style>)',
                  lambda m: m.group(1) + COMPOSITION + m.group(2), html, count=1, flags=re.S)
    html = re.sub(r"var STAGES = \[[^\]]*\];",
                  "var STAGES = [%s];" % ",".join("'%s'" % s for s in STAGES), html, count=1)
    html = re.sub(r"var STAGE_ICON = \[[^\]]*\];",
                  "var STAGE_ICON = [%s];" % ",".join("'%s'" % s for s in STAGE_ICON),
                  html, count=1)

    with open(DECK, "w", encoding="utf-8", newline="") as fh:
        fh.write(html)
    print("wrote %s - %d bytes, %d slides"
          % (os.path.relpath(DECK, ROOT).replace("\\", "/"), len(html.encode("utf-8")),
             html.count('<section class="slide"')))
    rel = os.path.relpath(DECK, ROOT).replace("\\", "/")
    print("next, in order:")
    print("  python tools/deck/shell.py icons %s --set %s" % (rel, ICON_SET))
    print("  python tools/deck/density.py write %s      # DS-239 derives the ranks" % rel)
    print("  python tools/deck/preflight.py %s --write  # DS-009 holds only this deck's rows" % rel)
    print("  python tools/deck/check.py %s --sources examples/portfolio-review/sources" % rel)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(selftest())
    rc = selftest()
    if rc:
        print("\nself-test failed - the deck was not written.")
        sys.exit(rc)
    print()
    compose()
