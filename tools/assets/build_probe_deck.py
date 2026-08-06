#!/usr/bin/env python3
"""Build a real 12-slide deck out of the measured assets, and report what each one cost.

`measure.py` weighs assets one at a time. That is not the question T-013 asks. The question is
what a *finished deck* weighs once the fonts, icons, motion library and diagrams are all in the
same file - and whether that file still renders with the network off. A three-slide toy answers
neither; layout and pacing problems only appear at real size (L-02), so this builds twelve.

The deck is a measurement vehicle, not a product. It is written to `.assets-cache/` (gitignored)
rather than committed: the repository keeps the script and the numbers, never the artefact.
Topic is deliberately neutral - CLAUDE.md forbids corpus content in this repository.

Run `measure.py all` first to populate the cache; this script reads it and never fetches.

    python tools/assets/build_probe_deck.py

Pure standard library, by L-07. Writes LF (L-11) and UTF-8 (L-10).
"""

import base64
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, ".assets-cache")
OUT = os.path.join(CACHE, "probe-deck.html")

# One text face, one display face, one mono - the smallest set that can carry a visual identity.
# Chosen off measure.py's table for character rather than ubiquity: Instrument Serif and Space
# Grotesk are cheap *and* not the face every generated deck already uses.
FACES = [
    ("Space Grotesk", "display", "600"),
    ("Instrument Serif", "serif", "400"),
    ("JetBrains Mono", "mono", "400"),
]
ICON_SET = "lucide"
MOTION_LIB = "anime.js 4"

SLIDES = [
    ("How a Heat Pump Works", "title",
     "Moving heat instead of making it"),
    ("The idea in one line", "statement",
     "A heat pump does not create heat. It collects heat that already exists outside and "
     "carries it indoors, which is why it can deliver more energy than it consumes."),
    ("Why that is not a trick", "two-col",
     "Burning fuel converts chemical energy into heat, and it can never exceed 100% efficiency. "
     "A heat pump moves heat rather than making it, so the ceiling does not apply. The work it "
     "does is compression, not combustion."),
    ("The four-stage cycle", "diagram-cycle",
     "Refrigerant loops continuously through four states, absorbing heat outside and releasing "
     "it inside."),
    ("Stage one - evaporate", "detail",
     "Cold liquid refrigerant meets outdoor air. Even at -5 C the air holds enough heat to boil "
     "it, because the refrigerant boils far below the temperature of water."),
    ("Stage two - compress", "detail",
     "The compressor squeezes the vapour. Pressure rises and temperature rises with it - this "
     "is the only stage that consumes meaningful electricity."),
    ("Stage three - condense", "detail",
     "Hot vapour passes through the indoor coil, gives up its heat to the room, and returns to "
     "liquid."),
    ("Stage four - expand", "detail",
     "An expansion valve drops the pressure, the liquid cools sharply, and the loop begins "
     "again."),
    ("What the numbers look like", "chart",
     "Coefficient of performance falls as outdoor temperature drops, but stays above one across "
     "the working range."),
    ("Where it stops making sense", "two-col",
     "Below roughly -20 C most units fall back on resistive heating and the advantage "
     "disappears. Poor insulation has the same effect for a different reason: the heat arrives "
     "and then leaves."),
    ("What decides the outcome", "diagram-flow",
     "Three factors dominate, and only one of them is the appliance."),
    ("In short", "closing",
     "A heat pump is a heat mover. Judge it on the temperature range it will actually work in, "
     "and on the building around it."),
]

ICONS_WANTED = ["arrow-right", "thermometer", "wind", "zap", "snowflake", "flame",
                "gauge", "house", "settings", "trending-down", "check", "circle-alert"]


def read_cache(key):
    path = os.path.join(CACHE, key.replace("/", "_"))
    if not os.path.exists(path):
        return None
    with open(path, "rb") as fh:
        return fh.read()


def font_face_css(family, alias, weight, raw):
    """A woff2 as a data: URI. base64 costs a third extra, and there is no way around it for a
    binary in a single file - that surcharge is the real price of rule 1 for fonts."""
    b64 = base64.b64encode(raw).decode("ascii")
    return ("@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:block;"
            "src:url(data:font/woff2;base64,%s) format('woff2');}" % (family, weight, b64))


def icon_svg(raw):
    """Strip to the bare element and force currentColor, so one glyph themes with the deck."""
    svg = raw.decode("utf-8", "replace")
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    svg = re.sub(r"\s+", " ", svg)
    svg = re.sub(r">\s+<", "><", svg).strip()
    svg = re.sub(r'stroke="(?!none)[^"]*"', 'stroke="currentColor"', svg)
    svg = re.sub(r'\swidth="[^"]*"', "", svg)
    svg = re.sub(r'\sheight="[^"]*"', "", svg)
    return svg


def build():
    if not os.path.isdir(CACHE):
        print("No .assets-cache/. Run:  python tools/assets/measure.py all")
        return 1

    budget = {}

    # ---- fonts
    face_css, missing = [], []
    for family, alias, weight in FACES:
        raw = read_cache("font_" + family)
        if raw is None:
            missing.append(family)
            continue
        face_css.append(font_face_css(family, alias, weight, raw))
        budget["font: " + family] = len(base64.b64encode(raw))
    if missing:
        print("Missing fonts in cache: %s - run measure.py fonts" % ", ".join(missing))
        return 1

    # ---- icons. Only one was cached by measure.py; fetch-free, so reuse it under each name.
    # The deck needs a dozen distinct glyphs to be representative, and the *size* is what is
    # being measured, not the artwork, so a repeated glyph measures honestly.
    icon_raw = read_cache("icon_" + ICON_SET)
    if icon_raw is None:
        print("Missing icons in cache - run measure.py icons")
        return 1
    one = icon_svg(icon_raw)
    icons_markup = "".join(one for _ in ICONS_WANTED)
    budget["icons: %s x%d" % (ICON_SET, len(ICONS_WANTED))] = len(icons_markup.encode())

    # ---- motion
    lib_raw = read_cache("lib_" + MOTION_LIB)
    if lib_raw is None:
        print("Missing %s in cache - run measure.py libs" % MOTION_LIB)
        return 1
    budget["motion: " + MOTION_LIB] = len(lib_raw)

    slides_html = []
    for i, (title, kind, body) in enumerate(SLIDES, 1):
        slides_html.append(render_slide(i, title, kind, body, one))
    slides_markup = "\n".join(slides_html)

    html = TEMPLATE % {
        "faces": "".join(face_css),
        "slides": slides_markup,
        "motion": lib_raw.decode("utf-8", "replace"),
        "count": len(SLIDES),
    }

    os.makedirs(CACHE, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)

    total = os.path.getsize(OUT)
    budget["deck: markup, CSS, diagrams, script"] = total - sum(budget.values())

    print("\nPROBE DECK - %d slides, built at %s" % (len(SLIDES), os.path.relpath(OUT, ROOT)))
    print("-" * 72)
    for label in sorted(budget, key=lambda k: -budget[k]):
        share = 100.0 * budget[label] / total
        print("  %-38s %8.1f KB  %5.1f%%" % (label, budget[label] / 1024.0, share))
    print("-" * 72)
    print("  %-38s %8.1f KB" % ("TOTAL, one self-contained file", total / 1024.0))
    print("\n  Zero external references. Open it with the network off and look at it (L-01).")
    return 0


def render_slide(n, title, kind, body, icon):
    if kind == "title":
        return ('<section class="slide s-title" data-n="%d"><div class="stage">'
                '<h1>%s</h1><p class="lede">%s</p>'
                '<div class="rule"></div></div></section>' % (n, title, body))
    if kind == "closing":
        return ('<section class="slide s-closing" data-n="%d"><div class="stage">'
                '<h2>%s</h2><p class="lede">%s</p></div></section>' % (n, title, body))
    if kind == "statement":
        return ('<section class="slide" data-n="%d"><div class="stage">'
                '<h2>%s</h2><p class="statement">%s</p></div></section>' % (n, title, body))
    if kind == "diagram-cycle":
        return ('<section class="slide" data-n="%d"><div class="stage">'
                '<h2>%s</h2><p>%s</p>%s</div></section>' % (n, title, body, CYCLE_SVG))
    if kind == "diagram-flow":
        return ('<section class="slide" data-n="%d"><div class="stage">'
                '<h2>%s</h2><p>%s</p>%s</div></section>' % (n, title, body, FLOW_SVG))
    if kind == "chart":
        return ('<section class="slide" data-n="%d"><div class="stage">'
                '<h2>%s</h2><p>%s</p>%s</div></section>' % (n, title, body, CHART_SVG))
    if kind == "two-col":
        half = body.split(". ")
        a = ". ".join(half[: max(1, len(half) // 2)]) + "."
        b = ". ".join(half[max(1, len(half) // 2):])
        return ('<section class="slide" data-n="%d"><div class="stage"><h2>%s</h2>'
                '<div class="cols"><div class="col"><span class="ico">%s</span><p>%s</p></div>'
                '<div class="col"><span class="ico">%s</span><p>%s</p></div></div>'
                '</div></section>' % (n, title, icon, a, icon, b))
    return ('<section class="slide" data-n="%d"><div class="stage">'
            '<h2><span class="ico">%s</span>%s</h2><p>%s</p></div></section>'
            % (n, icon, title, body))


CYCLE_SVG = """<svg class="fig" viewBox="0 0 900 340" role="img"
 aria-label="Four-stage refrigerant cycle: evaporate, compress, condense, expand">
<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="3"
 orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="var(--line)"/></marker></defs>
<g class="fig-g">
<rect x="30"  y="120" width="170" height="96" rx="6"/>
<rect x="255" y="120" width="170" height="96" rx="6"/>
<rect x="480" y="120" width="170" height="96" rx="6"/>
<rect x="705" y="120" width="165" height="96" rx="6"/>
<text x="115" y="158">1 Evaporate</text><text x="115" y="186" class="sub">outdoor coil</text>
<text x="340" y="158">2 Compress</text><text x="340" y="186" class="sub">the only input</text>
<text x="565" y="158">3 Condense</text><text x="565" y="186" class="sub">indoor coil</text>
<text x="787" y="158">4 Expand</text><text x="787" y="186" class="sub">valve</text>
<path d="M200,168 L250,168" marker-end="url(#ah)"/>
<path d="M425,168 L475,168" marker-end="url(#ah)"/>
<path d="M650,168 L700,168" marker-end="url(#ah)"/>
<path d="M787,216 L787,270 L115,270 L115,216" marker-end="url(#ah)" fill="none"/>
<text x="451" y="296" class="sub">refrigerant returns cold and low-pressure</text>
</g></svg>"""

FLOW_SVG = """<svg class="fig" viewBox="0 0 900 300" role="img"
 aria-label="Three factors determining heat pump outcome">
<g class="fig-g">
<rect x="40"  y="60" width="230" height="80" rx="6"/>
<rect x="335" y="60" width="230" height="80" rx="6"/>
<rect x="630" y="60" width="230" height="80" rx="6"/>
<rect x="335" y="190" width="230" height="70" rx="6" class="accent"/>
<text x="155" y="95">Climate</text><text x="155" y="122" class="sub">how cold it gets</text>
<text x="450" y="95">Building fabric</text><text x="450" y="122" class="sub">how fast heat leaves</text>
<text x="745" y="95">The unit</text><text x="745" y="122" class="sub">what you can buy</text>
<text x="450" y="222">Delivered performance</text>
<text x="450" y="246" class="sub">two of the three are fixed before you choose</text>
<path d="M155,140 L155,170 L440,170 L440,188" fill="none" marker-end="url(#ah)"/>
<path d="M450,140 L450,188" fill="none" marker-end="url(#ah)"/>
<path d="M745,140 L745,170 L460,170 L460,188" fill="none" marker-end="url(#ah)"/>
</g></svg>"""

CHART_SVG = """<svg class="fig" viewBox="0 0 900 330" role="img"
 aria-label="Coefficient of performance against outdoor temperature">
<g class="fig-g chart">
<line x1="90" y1="270" x2="860" y2="270"/><line x1="90" y1="40" x2="90" y2="270"/>
<text x="70"  y="275" class="sub ar">1</text>
<text x="70"  y="160" class="sub ar">3</text>
<text x="70"  y="46"  class="sub ar">5</text>
<text x="120" y="295" class="sub">-20</text><text x="320" y="295" class="sub">-10</text>
<text x="520" y="295" class="sub">0</text><text x="720" y="295" class="sub">10</text>
<polyline class="series" fill="none"
  points="120,250 220,222 320,190 420,158 520,126 620,100 720,74 820,58"/>
<circle class="dot" cx="120" cy="250" r="5"/><circle class="dot" cx="520" cy="126" r="5"/>
<circle class="dot" cx="820" cy="58" r="5"/>
<text x="140" y="243" class="sub">1.2</text>
<text x="540" y="119" class="sub">3.4</text>
<text x="800" y="46" class="sub ar">4.6</text>
<text x="475" y="322" class="sub">outdoor temperature, C</text>
</g></svg>"""


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>How a Heat Pump Works</title>
<style>
%(faces)s
:root{
  --bg:#0f1113; --ink:#f2efe9; --dim:#9aa0a6; --accent:#e0b25f; --line:#4a5058;
  --stage-w:1600px; --stage-h:900px;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%%;background:var(--bg);color:var(--ink);
  font-family:'Space Grotesk',system-ui,sans-serif;overflow:hidden}
.deck{position:fixed;inset:0;display:grid;place-items:center}
.slide{position:absolute;inset:0;display:grid;place-items:center;opacity:0;
  pointer-events:none;transition:opacity .45s ease}
.slide.on{opacity:1;pointer-events:auto}
.stage{width:var(--stage-w);height:var(--stage-h);padding:96px 120px;
  display:flex;flex-direction:column;justify-content:center;gap:28px;
  transform-origin:center;transform:scale(var(--k,1))}
h1{font-family:'Instrument Serif',Georgia,serif;font-size:104px;font-weight:400;
  line-height:1.02;letter-spacing:-.01em}
h2{font-family:'Instrument Serif',Georgia,serif;font-size:64px;font-weight:400;
  line-height:1.08;display:flex;align-items:center;gap:20px}
p{font-size:30px;line-height:1.5;color:var(--dim);max-width:36ch}
.lede{font-size:34px;color:var(--dim);max-width:40ch}
.statement{font-size:40px;color:var(--ink);max-width:30ch;line-height:1.35}
.rule{width:180px;height:3px;background:var(--accent)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:64px;margin-top:12px}
.col p{font-size:28px;max-width:none}
.ico{display:inline-block;width:44px;height:44px;color:var(--accent);flex:0 0 auto}
.ico svg{width:100%%;height:100%%;stroke-width:1.6}
.fig{width:100%%;height:auto;margin-top:8px}
.fig-g rect{fill:none;stroke:var(--line);stroke-width:2}
.fig-g rect.accent{stroke:var(--accent)}
.fig-g path,.fig-g line{stroke:var(--line);stroke-width:2;fill:none}
.fig-g text{fill:var(--ink);font-family:'Space Grotesk',sans-serif;font-size:22px;
  text-anchor:middle}
.fig-g text.sub{fill:var(--dim);font-size:17px}
.fig-g text.ar{text-anchor:end}
.chart .series{stroke:var(--accent);stroke-width:3}
.chart .dot{fill:var(--accent)}
.hud{position:fixed;right:28px;bottom:22px;font-family:'JetBrains Mono',monospace;
  font-size:15px;color:var(--dim);letter-spacing:.04em}
.s-title h1,.s-closing h2{font-size:112px}
@media print{html,body{overflow:visible;background:#fff;color:#000}
  .slide{position:relative;opacity:1;page-break-after:always}}
</style></head>
<body>
<div class="deck">
%(slides)s
</div>
<div class="hud"><span id="pos">1</span> / %(count)d</div>
<script>%(motion)s</script>
<script>
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide')), i=0;
  function fit(){
    var k=Math.min(innerWidth/1600, innerHeight/900);
    document.documentElement.style.setProperty('--k', k);
  }
  function show(n){
    i=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach(function(s,j){ s.classList.toggle('on', j===i); });
    document.getElementById('pos').textContent=i+1;
    var el=slides[i].querySelectorAll('h1,h2,p,.fig,.col');
    if(window.anime){ anime.animate(el,{opacity:[0,1],y:[14,0],delay:anime.stagger(55),
      duration:520,ease:'outQuad'}); }
  }
  addEventListener('resize',fit); fit(); show(0);
  addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown') show(i+1);
    if(e.key==='ArrowLeft'||e.key==='PageUp') show(i-1);
    if(e.key==='Home') show(0);
    if(e.key==='End') show(slides.length-1);
  });
  addEventListener('click',function(e){ show(i + (e.clientX < innerWidth/3 ? -1 : 1)); });
})();
</script>
</body></html>
"""


if __name__ == "__main__":
    sys.exit(build())
