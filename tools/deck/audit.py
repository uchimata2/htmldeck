#!/usr/bin/env python3
"""Run the mechanical half of `docs/EVALUATION.md`'s pipeline over a deck.

Stage 1 is the **auto gate** — static analysis of the file. Stage 2 is the part of the **render
gate** a measurement can answer: the design-unit floor, continuous motion, the reflow view, tab
order, target size, and the 320 CSS px reflow requirement.

**This is necessary and nowhere near sufficient, and it says so.** Validating the rubric against a
seeded-defect deck showed that **five of the ten evaluation dimensions are invisible to any static
or measured check** — S1 Claim, S2 Evidence, S4 Density, D1 Spine and D4 Consistency are judgement,
and a pipeline stopping here ships a deck whose headline is a topic label and whose figures
contradict each other (**L-05**, DS-190, DS-191).

    python tools/deck/audit.py examples/reference-deck.html

Pure standard library (**L-07**), real Chrome offline via `render.py`.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render                                                       # noqa: E402
import contrast                                                     # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT

# ---------------------------------------------------------------------------- stage 1: static
# Each entry is (rule id, what it asserts, predicate). Only rules a file scan can actually
# decide - anything needing a render lives in stage 2, anything needing judgement is not here.
STATIC = [
    ("DS-001", "zero external references",
     lambda h: not [u for u in re.findall(
         r'(?:src|href|xlink:href)\s*=\s*["\']([^"\']+)["\']', h)
         if not u.startswith(("data:", "#", "blob:"))]),
    ("DS-003", "meta charset present",
     lambda h: '<meta charset="utf-8">' in h.lower()),
    ("DS-008", "latin script only",
     lambda h: not re.search(r"[Ͱ-ϿЀ-ӿ一-鿿぀-ヿ]", h)),
    ("DS-030", "three named type roles",
     lambda h: all(t in h for t in ("--font-display", "--font-text", "--font-mono"))),
    ("DS-031", "no Inter, Roboto, Arial or system-ui",
     lambda h: not re.search(r"font-family:[^;]*(Inter|Roboto|Arial|system-ui)", h)),
    ("DS-032", "faces embedded base64, licence travelling with them",
     lambda h: h.count("data:font/woff2;base64,") >= 1 and "Open Font License" in h),
    ("DS-033", "no vw/vh/clamp inside the stage",
     lambda h: not re.search(r"[:\s]\d[\d.]*v[wh]\b", h) and "clamp(" not in h),
    ("DS-061", "no width media query reshaping the stage",
     lambda h: not re.search(r"@media[^{]*max-width", h)),
    ("DS-088", "no speaker notes in the shipped deck",
     lambda h: "speaker-note" not in h and 'class="notes' not in h),
    ("DS-110", "no raster images",
     lambda h: not re.search(r"<img\b", h) and "data:image/png" not in h
     and "data:image/jpeg" not in h),
    ("DS-122", "no chart library",
     lambda h: not any(x in h.lower() for x in
                       ("chart.js", "d3.min", "plotly", "highcharts", "echarts"))),
    ("DS-100", "no rhetorical questions in slide copy",
     lambda h: not re.search(r"\?\s*<", h)),
    ("DS-106", "no banned terminology",
     lambda h: not re.search(r"\b(crucial|pivotal|seamless|leverage|synerg\w*|friction|"
                             r"genuinely|arguably|precisely|delve)\b", h, re.I)),
]

# ---------------------------------------------------------------------------- stage 2: rendered
PROBE = r"""
<script>
(function(){
  function tabbables(root){
    return Array.prototype.filter.call(
      root.querySelectorAll('a[href],button,input,select,textarea,[tabindex]'),
      function(el){
        if (el.disabled || el.closest('[inert]') || el.closest('[hidden]')) return false;
        var r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0;
      });
  }
  function run(){
    var out = {};
    var stage = document.getElementById('stage');
    var doc = document.getElementById('doc');
    var slides = stage.querySelectorAll('.slide');
    var k = parseFloat(getComputedStyle(stage).getPropertyValue('--k')) || 1;
    out.slideCount = slides.length;

    // DS-035 - nothing below 18 design units, anywhere
    out.underFloor = [];
    var all = stage.querySelectorAll('*');
    for (var i=0;i<all.length;i++){
      var el = all[i];
      if (el.children.length || !el.textContent || !el.textContent.trim()) continue;
      var fs = parseFloat(getComputedStyle(el).fontSize), du = fs;
      if (el.namespaceURI === 'http://www.w3.org/2000/svg'){
        var m = el.getScreenCTM(); if (!m) continue;
        du = fs * (Math.sqrt(Math.abs(m.a*m.d - m.b*m.c)) / k);
      }
      if (du < 17.5) out.underFloor.push([+du.toFixed(1),
        el.textContent.replace(/\s+/g,' ').trim().slice(0,32),
        (el.closest('.slide')||{dataset:{}}).dataset.name || '']);
    }

    // DS-140/142 - DS-140 sanctions exactly one looping motion, `Current`, for flows. Anything
    // else looping is continuous motion on static content, which DS-142 bans outright. 2.2.2
    // additionally needs a control for whatever does loop.
    out.infinite = []; out.ambient = [];
    for (var j=0;j<all.length;j++){
      var c = getComputedStyle(all[j]);
      if ((c.animationIterationCount||'').indexOf('infinite') < 0) continue;
      var row = [c.animationName, (all[j].closest('.slide')||{dataset:{}}).dataset.name || ''];
      out.infinite.push(row);
      if (!all[j].classList.contains('current')) out.ambient.push(row);
    }
    out.motionControl = !!document.getElementById('motion');

    // DS-091 - headline of six words or fewer. DS-085 - the last slide is a close.
    out.longHeadlines = [];
    for (var s=0;s<slides.length;s++){
      var h = slides[s].querySelector('.headline');
      if (h && h.textContent.trim().split(/\s+/).length > 6)
        out.longHeadlines.push([slides[s].dataset.name, h.textContent.trim().split(/\s+/).length]);
    }
    out.lastSlide = slides[slides.length-1].dataset.name;

    // DS-111 / DS-123 - figures present, and card rows standing in for a diagram
    out.figures = stage.querySelectorAll('svg.fig').length;

    // DS-132 - off-screen slides leave the tab order. DS-130 - the current one stays in it.
    var t = tabbables(document);
    out.tabbables = t.length;
    out.tabbablesOffscreen = t.filter(function(el){
      var sl = el.closest('.slide'); return sl && !sl.hasAttribute('data-current'); }).length;
    var curBtn = document.querySelector('.slide[data-current] .disc-btn');
    out.currentDiscReachable = curBtn ? t.indexOf(curBtn) >= 0 : null;

    // DS-168 / 2.5.8 - every target at least 24 CSS px
    out.smallTargets = t.filter(function(el){
      var r = el.getBoundingClientRect(); return r.width < 24 || r.height < 24; }).length;

    // DS-160/161 - closed by default. DS-137 - one panel at a time. DS-138 - it drops below.
    out.panelsOpenInitially = document.querySelectorAll('.stage .disc-panel:not([hidden])').length;
    var btns = document.querySelectorAll('.stage .disc-btn');
    if (btns.length){
      btns[0].click();
      document.getElementById('dots').children[4].click();
      var b2 = document.querySelector('.slide[data-current] .disc-btn');
      if (b2) b2.click();
      out.panelsOpenAfterTwo = document.querySelectorAll('.stage .disc-panel:not([hidden])').length;
      var p = document.querySelector('.slide[data-current] .disc-panel:not([hidden])');
      if (p) out.panelBelowControl =
        p.getBoundingClientRect().top >= p.parentNode.querySelector('.disc-btn').getBoundingClientRect().bottom - 1;
      document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape', bubbles:true}));
    }

    // DS-070..076 - the reflow view
    if (doc){
      document.getElementById('dots').children[6].click();
      document.getElementById('toDoc').click();
      out.docOn = doc.hasAttribute('data-on');
      out.docSections = doc.querySelectorAll('#docBody > section').length;
      var panels = doc.querySelectorAll('.disc-panel');
      out.docPanelsOpen = doc.querySelectorAll('.disc-panel:not([hidden])').length;
      out.docPanelsTotal = panels.length;
      // DS-073 - all content travels, tier two included. Compare text, not element counts.
      function norm(s){ return s.replace(/\s+/g,' ').trim(); }
      out.docShorterThanSlide = [];
      var secs = doc.querySelectorAll('#docBody > section');
      for (var q=0;q<slides.length && q<secs.length;q++){
        var a = norm(slides[q].textContent), b = norm(secs[q].textContent);
        if (b.length < a.length - 2) out.docShorterThanSlide.push([slides[q].dataset.name, a.length, b.length]);
      }
      // DS-075 / 1.4.10 - no two-dimensional scrolling at 320 CSS px
      var prev = doc.style.width;
      doc.style.width = '320px';
      doc.getBoundingClientRect();
      out.at320ScrollWidth = doc.scrollWidth;
      out.at320Overflowing = Array.prototype.filter.call(doc.querySelectorAll('#docBody *'),
        function(el){ return el.getBoundingClientRect().width > 321; }).length;
      doc.style.width = prev;
      out.switchVisibleInDoc = document.getElementById('toStage').getBoundingClientRect().width > 0;
      document.getElementById('toStage').click();
      out.backOnSlide = document.querySelector('.slide[data-current]').dataset.name;
    }

    // DS-143 - reduced motion keeps the semantics: the dashed arrows stay dashed
    var cur = document.querySelector('.current');
    if (cur) out.currentDasharray = getComputedStyle(cur).strokeDasharray;

    out.vw = window.innerWidth;
    document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,250); });
  else window.addEventListener('load', run);
})();
</script>
"""


def ok(flag):
    return "pass" if flag else "FAIL"


def main(deck):
    render.self_test()
    contrast.self_test()
    html = open(deck, "r", encoding="utf-8").read()
    print("browser: %s" % render.CHROME)
    print("deck:    %s" % os.path.relpath(deck, ROOT))

    print("\n=== stage 1  auto gate (static)")
    failures = []
    for rule, what, fn in STATIC:
        good = fn(html)
        if not good:
            failures.append(rule)
        print("  %-8s %-50s %s" % (rule, what, ok(good)))

    print("\n=== stage 2  contrast (WCAG 2.2 AA, DESIGN-SYSTEM §7)")
    cfails = contrast.audit(html, verbose=False)
    print("  %d failure(s)" % len(cfails))
    for theme, label, fg, bg, r, need in cfails:
        print("    %-6s %-32s %.2f:1 (needs %.1f)" % (theme, label, r, need))
        failures.append("contrast/%s" % label)

    probe = render.make_probe(deck, name="audit.html", extra=PROBE)
    data, err = render.read_result(render.file_url(probe), 1622, 1054)
    if not data:
        print("\n=== stage 3  render gate: NO RESULT\n%s" % err[:400])
        return 1

    print("\n=== stage 3  render gate (measured, viewport %d)" % data["vw"])
    rows = [
        ("DS-080/081/082", "sections: %d" % data["slideCount"], 6 <= data["slideCount"]),
        ("DS-035", "text below 18 design units: %d" % len(data["underFloor"]),
         not data["underFloor"]),
        ("DS-091", "headlines over six words: %d" % len(data["longHeadlines"]),
         not data["longHeadlines"]),
        ("DS-111", "inline SVG figures: %d" % data["figures"], data["figures"] > 0),
        ("DS-132", "tabbables from off-screen slides: %d" % data["tabbablesOffscreen"],
         data["tabbablesOffscreen"] == 0),
        ("DS-130", "current slide's disclosure reachable: %s" % data.get("currentDiscReachable"),
         data.get("currentDiscReachable") is not False),
        ("DS-168", "targets under 24 CSS px: %d" % data["smallTargets"], data["smallTargets"] == 0),
        ("DS-161", "panels closed by default: %d open" % data["panelsOpenInitially"],
         data["panelsOpenInitially"] == 0),
        ("DS-137", "panels open at once: %s" % data.get("panelsOpenAfterTwo"),
         data.get("panelsOpenAfterTwo", 0) <= 1),
        ("DS-138", "panel drops below its control: %s" % data.get("panelBelowControl"),
         data.get("panelBelowControl") is not False),
        ("DS-142", "looping motion on static content: %d" % len(data.get("ambient", [])),
         not data.get("ambient")),
        ("2.2.2", "control for motion over 5s: %s (%d looping)"
         % (data["motionControl"], len(data["infinite"])),
         len(data["infinite"]) == 0 or data["motionControl"]),
        ("DS-143", "reduced motion keeps the dashes: %s"
         % (data.get("currentDasharray") or "no dashed flow in this deck"),
         data.get("currentDasharray") != "none"),
        ("DS-070", "reflow view engages: %s" % data.get("docOn"), data.get("docOn") is True),
        ("DS-073", "sections carrying less text than their slide: %d"
         % len(data.get("docShorterThanSlide", [])), not data.get("docShorterThanSlide")),
        ("DS-073", "tier-two panels open in the reflow view: %s/%s"
         % (data.get("docPanelsOpen"), data.get("docPanelsTotal")),
         data.get("docPanelsOpen") == data.get("docPanelsTotal")),
        ("DS-075", "reflow scrollWidth at 320 CSS px: %s (overflowing: %s)"
         % (data.get("at320ScrollWidth"), data.get("at320Overflowing")),
         data.get("at320ScrollWidth", 999) <= 321 and data.get("at320Overflowing") == 0),
        ("DS-076", "position preserved returning from the reflow view: %r"
         % data.get("backOnSlide"), bool(data.get("backOnSlide"))),
    ]
    for rule, what, good in rows:
        if not good:
            failures.append(rule)
        print("  %-15s %-58s %s" % (rule, what, ok(good)))

    for du, text, slide in data["underFloor"][:6]:
        print("      %5.1f du  %-32s  [%s]" % (du, text, slide))
    for name, slide in data["infinite"][:6]:
        tag = "ambient" if [name, slide] in data.get("ambient", []) else "flow (DS-140)"
        print("      looping %-14s %-14s [%s]" % (name, tag, slide))

    print("\n%d mechanical failure(s): %s" % (len(failures), ", ".join(failures) or "none"))
    print("""
This gate covers the `auto` and `render` rules only. **Five of the ten evaluation dimensions -
S1 Claim, S2 Evidence, S4 Density, D1 Spine, D4 Consistency - are invisible to it**, and were
proven so against a seeded-defect deck. A clean run here is not a good deck; it is a deck with no
defect this gate was built to see (L-05, DS-191).""")
    return 1 if failures else 0


if __name__ == "__main__":
    deck = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(
        ROOT, "examples", "reference-deck.html")
    sys.exit(main(deck))
