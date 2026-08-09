#!/usr/bin/env python3
"""Gate the resolution contract - `docs/DESIGN-SYSTEM.md` §2.4 and §2.5.

`audit.py` covers the rules one render can decide. **These cannot be decided from one render**:
they are claims about what happens *between* viewports - the stage is identical up to a uniform
scale, it letterboxes rather than reflows, it stays centred, and the reflow view engages at the
right moment. So this sweeps several viewports and compares.

Two things it does that are worth stating, because both were the difference between a check that
works and one that flatters:

- **The sweep includes a short, wide viewport.** 1280 x 400 scales to 0.37 and puts body text at
  8.9 CSS px, and **a width test cannot see it** - which is the case that amended DS-071 from
  "below 960 CSS px" to "scale below 0.5" (T-021, 2026-08-07). A sweep of progressively narrower
  16:9 windows agrees with the old rule and the new one everywhere, and proves nothing.
- **DS-063 and DS-064 were already measured and never gated.** `render.py` has printed both
  numbers since T-024. Printing a number nothing fails on is not enforcement, so the thresholds
  live here and `render.py`'s report reads them from the same place (L-08 - one home per fact).

    python tools/deck/contract.py examples/reference-deck.html

Pure standard library (**L-07**), real Chrome offline via `render.py`.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                        # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT

# The tolerance DS-063 states, and the reason it is not zero: glyph advances round to device
# pixels, so any deck containing text fails an equality check. Measured over 384 values in
# DESIGN-RATIONALE.md §2 - worst case 0.09 non-text and 1.17 text.
GEOM_TOLERANCE_DU = 0.25          # DS-063, non-text geometry

# DS-063, text runs - **in device pixels at the smaller rendering, not in design units.**
#
# It was 2.0 design units, a number measured over one deck in one theme with headroom above its
# worst case of 1.17. T-007's second theme reached 2.23 du and failed a resolution contract it
# does not break: a tighter type scale fits more glyphs on a line, and every one of them rounds.
# **A design-unit threshold was the wrong shape for a device-pixel effect** - it silently encodes
# the scale factor of the deck it was measured on.
#
# Two is the mechanism's own number, not a fitted one: a whole-rect comparison folds two
# independent roundings, the run's edge and its extent, each up to one device pixel. At the
# sweep's smaller viewport k is 0.587, so the bound lands at 3.41 du - which the reference deck
# (1.07 du = 0.63 px) and `lattice` (2.23 du = 1.31 px) both clear with room.
TEXT_TOLERANCE_PX = 2.0
BODY_FLOOR_CSS_PX = 16.0          # DS-064, in a 720p capture
SCALE_THRESHOLD = 0.5             # DS-071, amended 2026-08-07: k below this hands over
CENTRE_TOLERANCE_PX = 1.5         # DS-200, half a device pixel each side plus rounding

# Which measured keys are text runs, for DS-063's two tolerances. Everything else is geometry.
TEXT_KEYS = {"headline", "standfirst", "body", "eyebrow", "discLabel", "monoLab",
             "svgLab", "svgVal", "svgName"}

# The sweep. `engage` is what DS-071 requires of the reflow view at that viewport.
#
#   k = min(vw/1920, vh/1080)
#
#   1280 x 720   k = 0.667   stage      - a 720p share, the case DS-064 is written for
#   1600 x 900   k = 0.833   stage      - an ordinary laptop
#   1280 x 400   k = 0.370   reflow     - short and wide; a width test keeps this on the stage
#    800 x 700   k = 0.417   reflow     - narrow; both the old rule and the new one agree
VIEWPORTS = [
    (1280, 720, 0.6667, False),
    (1600, 900, 0.8333, False),
    (1280, 400, 0.3704, True),
    (800, 700, 0.4167, True),
]

# Passive on purpose: it clicks nothing. Every other probe in this repository drives the deck
# through its controls; this one must observe what the deck does on its own, because that is what
# auto-engage means.
PROBE = r"""
<script>
(function(){
  function run(){
    var stage = document.getElementById('stage');
    var viewport = document.getElementById('viewport');
    var doc = document.getElementById('doc');
    var cs = getComputedStyle(stage);
    var k = parseFloat(cs.getPropertyValue('--k')) || 0;
    var r = stage.getBoundingClientRect();
    var out = {
      vw: window.innerWidth, vh: window.innerHeight,
      k: +k.toFixed(6),
      /* DS-060: the design space is 1920x1080 BEFORE the transform. offsetWidth is the layout
         box, which transform: scale() does not change - that is the whole point of DS-200. */
      layout: [stage.offsetWidth, stage.offsetHeight],
      rect: [+r.left.toFixed(2), +r.top.toFixed(2), +r.width.toFixed(2), +r.height.toFixed(2)],
      transform: cs.transform,
      /* DS-071: did the deck hand over to the reflow view by itself? */
      docOn: !!(doc && doc.hasAttribute('data-on')),
      stageHidden: !!(viewport && viewport.hasAttribute('hidden')),
      /* DS-074: does the reading view honour the user's font size? Double the root and the
         document rendering must double with it; a stage-like layout will not. WCAG 1.4.4.
         **Several roles, not one.** A single probe passed a variant that had pinned three of
         four reading-view roles to px, because the one element it sampled was not among them. */
      remScaling: [],
      /* DS-072: the auto-engage path must consult fullscreenElement. Verified against DOUBLES -
         a faked fullscreenElement and a faked viewport height - never a real fullscreen, because
         headless has no user gesture to request one with. The check says so in its own output
         rather than implying it saw the real thing. */
      fullscreenGuard: null
    };
    if (doc){
      var roles = ['.doc .headline', '.doc .standfirst', '.doc-head .t', '#docBody p'];
      var wasRoot = document.documentElement.style.fontSize;
      for (var i=0;i<roles.length;i++){
        var el = doc.querySelector(roles[i]) || document.querySelector(roles[i]);
        if (!el) continue;
        var before = parseFloat(getComputedStyle(el).fontSize);
        document.documentElement.style.fontSize = '32px';
        var after = parseFloat(getComputedStyle(el).fontSize);
        document.documentElement.style.fontSize = wasRoot;
        out.remScaling.push([roles[i], +before.toFixed(2), +after.toFixed(2)]);
      }
    }
    /* The guard only does anything when the environment says "switch" and fullscreen says "no".
       Asserting that nothing changes while the deck is ALREADY in the right state tests nothing
       - the first version of this check passed a deck with the guard deleted. So: fake a
       viewport the deck would hand over at, claim fullscreen, and require it to stay put. */
    try {
      var wasOn = !!(doc && doc.hasAttribute('data-on'));
      var realH = window.innerHeight;
      Object.defineProperty(window, 'innerHeight', { configurable: true, get: function(){ return 300; } });
      Object.defineProperty(document, 'fullscreenElement',
                            { configurable: true, get: function(){ return document.body; } });
      window.dispatchEvent(new Event('resize'));
      var heldStill = !!(doc && doc.hasAttribute('data-on')) === wasOn;
      delete document.fullscreenElement;
      delete window.innerHeight;
      out.fullscreenGuard = heldStill;
      out.fullscreenGuardTested = [wasOn, realH, 300];
      window.dispatchEvent(new Event('resize'));       /* let the deck settle back */
    } catch (e) { out.fullscreenGuard = 'not testable: ' + e.message; }
    document.title = 'RESULT' + JSON.stringify(out) + 'ENDRESULT';
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ setTimeout(run,250); });
  else window.addEventListener('load', run);
})();
</script>
"""


def sweep(deck, quiet=False):
    """Render the deck at each viewport in VIEWPORTS and read the geometry back."""
    probe = render.make_probe(deck, name="contract.html", extra=PROBE)
    rows = []
    for (w, h, k_expected, engage) in VIEWPORTS:
        cw, ch = render.calibrate(probe, w, h)
        data, err = render.read_result(render.file_url(probe), cw, ch)
        if not data:
            print("  !! no result at %dx%d\n%s" % (w, h, err[:300]))
            continue
        data["want"] = {"w": w, "h": h, "k": k_expected, "engage": engage}
        rows.append(data)
        if not quiet:
            print("  %4dx%-4d  k=%.4f  layout=%sx%s  doc=%-5s  (wanted k=%.4f doc=%s)"
                  % (data["vw"], data["vh"], data["k"], data["layout"][0], data["layout"][1],
                     data["docOn"], k_expected, engage))
    return rows


def geometry(results):
    """DS-063, split by DS-063's own two tolerances rather than one number for everything.

    `results` is what `render.cmd_measure` produced: {label: [per-slide measurement]}.
    """
    a, b = results.get("3840x2000", []), results.get("1280x634", [])
    if not (a and b):
        return None
    # Split by ELEMENT KIND, not by axis. Measured 2026-08-07 over the full 12-slide deck: a text
    # run's whole rect is glyph-derived, not only its width. `y` reached 0.62 du and `h` 0.42 on
    # SVG labels, against a worst width of 1.17 - so holding a text run's placement to the
    # non-text tolerance fails a deck whose layout is provably identical.
    worst = {"geom": (0.0, ""), "text": (0.0, "")}
    counted = {"geom": 0, "text": 0}
    for ra, rb in zip(a, b):
        for key in sorted(set(ra["geom"]) & set(rb["geom"])):
            bucket = "text" if key in TEXT_KEYS else "geom"
            for i, axis in enumerate("x y w h".split()):
                d = abs(ra["geom"][key][i] - rb["geom"][key][i])
                counted[bucket] += 1
                if d > worst[bucket][0]:
                    worst[bucket] = (d, "%s / %s / %s" % (ra["slide"], key, axis))
    # The text bound is device pixels at the SMALLER rendering, converted here because that is
    # where the scale factor is known. A fixed design-unit number encodes one deck's k.
    text_tol_du = TEXT_TOLERANCE_PX / b[0]["k"]
    return {"counted": counted["geom"] + counted["text"],
            "n_geom": counted["geom"], "n_text": counted["text"],
            "geom": worst["geom"], "text": worst["text"],
            "k_ratio": a[0]["k"] / b[0]["k"],
            "text_tol_du": text_tol_du,
            "text_px": worst["text"][0] * b[0]["k"],
            # No non-text value measured is not a pass. Until 2026-08-07 the probe carried nine
            # text keys and nothing else, so this tolerance had a number and zero coverage.
            "geom_ok": counted["geom"] > 0 and worst["geom"][0] <= GEOM_TOLERANCE_DU,
            "text_ok": counted["text"] > 0 and worst["text"][0] <= text_tol_du}


def body_floor(results):
    """DS-064: the smallest body run in a 720p capture, against the 16 CSS px floor."""
    rows = [(r["slide"], r["type"]["body"]["css"], r["type"]["body"]["du"])
            for r in results.get("720p", []) if "body" in r["type"]]
    if not rows:
        return None
    slide, css, du = min(rows, key=lambda t: t[1])
    return {"slide": slide, "css": css, "du": du, "ok": css >= BODY_FLOOR_CSS_PX,
            "n": len(rows)}


def verdicts(rows):
    """Turn the sweep into (rule, what it measured, pass/fail) - the shape audit.py prints."""
    out = []
    if not rows:
        return [("DS-060", "no viewport rendered - the sweep produced nothing", False)]

    bad_k = [r for r in rows if abs(r["k"] - r["want"]["k"]) > 0.002]
    out.append(("DS-060", "stage scale matches min(vw/1920, vh/1080) at %d viewports%s"
                % (len(rows), "" if not bad_k else "; off at %dx%d" % (bad_k[0]["vw"], bad_k[0]["vh"])),
                not bad_k))

    # Only where the stage is actually shown. A handed-over deck hides `.viewport`, and a hidden
    # stage measures 0x0 - which is R7 §3's finding arriving from the other direction: measuring
    # a stage the deck has switched away from reports a defect that is the deck working.
    on_stage = [r for r in rows if not r["docOn"] and r["rect"][3] > 0]

    bad_layout = [r for r in on_stage if tuple(r["layout"]) != (1920, 1080)]
    out.append(("DS-060", "design space stays 1920x1080 before the transform, at %d stage "
                "viewport(s): %s" % (len(on_stage),
                                     "yes" if not bad_layout else "%sx%s at %dx%d"
                                     % (bad_layout[0]["layout"][0], bad_layout[0]["layout"][1],
                                        bad_layout[0]["vw"], bad_layout[0]["vh"])),
                bool(on_stage) and not bad_layout))

    # DS-062 - letterbox, never reflow. The rendered stage keeps 16:9 whatever the window is,
    # which is only meaningful because the sweep contains a 3.2:1 window and a 1.14:1 one.
    ratios = [(r, r["rect"][2] / r["rect"][3]) for r in on_stage]
    bad_ratio = [(r, x) for r, x in ratios if abs(x - 16 / 9) > 0.01]
    out.append(("DS-062", "rendered aspect stays 16:9 across %d stage viewports%s"
                % (len(ratios), "" if not bad_ratio else "; %.3f at %dx%d"
                   % (bad_ratio[0][1], bad_ratio[0][0]["vw"], bad_ratio[0][0]["vh"])),
                bool(ratios) and not bad_ratio))

    # DS-200 - the rule instructs measuring the stage's rect against the viewport at several
    # widths, and says the bug is invisible at full size. This is that measurement.
    off = []
    for r in on_stage:
        left, top, w, h = r["rect"]
        dx = abs(left - (r["vw"] - w) / 2)
        dy = abs(top - (r["vh"] - h) / 2)
        if dx > CENTRE_TOLERANCE_PX or dy > CENTRE_TOLERANCE_PX:
            off.append((r, dx, dy))
    out.append(("DS-200", "scaled stage centred at every viewport%s"
                % ("" if not off else "; off by %.1f,%.1f px at %dx%d"
                   % (off[0][1], off[0][2], off[0][0]["vw"], off[0][0]["vh"])),
                not off))

    # DS-071 - the amended rule. Reported with k, because a bare pass/fail here is unreadable.
    wrong = [r for r in rows if r["docOn"] != r["want"]["engage"]]
    out.append(("DS-071", "reflow engages exactly when k < %.1f: %s"
                % (SCALE_THRESHOLD,
                   "%d/%d viewports" % (len(rows) - len(wrong), len(rows))
                   + ("" if not wrong else "; %dx%d k=%.3f gave doc=%s, wanted %s"
                      % (wrong[0]["vw"], wrong[0]["vh"], wrong[0]["k"],
                         wrong[0]["docOn"], wrong[0]["want"]["engage"]))),
                not wrong))

    guards = [r["fullscreenGuard"] for r in rows]
    out.append(("DS-072", "auto-engage consults fullscreenElement (tested against a double, "
                "not a real fullscreen): %s" % guards[0],
                all(g is True for g in guards)))

    # Every role, not the first one that answers. A role pinned to px is exactly what a reading
    # view must not have, and it hides behind any sibling that still scales.
    roles = rows[0].get("remScaling") or []
    pinned = [r for r in roles if r[2] <= r[1] * 1.5]
    out.append(("DS-074", "reflow type follows the root font size: %d of %d role(s) scale%s"
                % (len(roles) - len(pinned), len(roles),
                   "" if not pinned else "; %s stays at %.1f px" % (pinned[0][0], pinned[0][2])),
                bool(roles) and not pinned))
    return out


# Which slides the two-resolution comparison samples. DS-063 is a claim about the whole stage, so
# a sample is a compromise and is named as one: four slides spanning the deck's archetypes, at
# roughly 12 Chrome launches. `--all` measures every slide.
SAMPLE = [0, 4, 7, 11]


def scale_verdicts(deck, which=None, quiet=True):
    """DS-063 and DS-064 - measured by `render.py` since T-024, gated here for the first time."""
    results = render.measure(deck, which or SAMPLE, quiet=quiet)
    out = []

    g = geometry(results)
    if not g:
        out.append(("DS-063", "the two-resolution comparison produced no result", False))
    else:
        out.append(("DS-063", "non-text geometry across 3840x2000 and 1280x634: worst %.2f du of "
                    "%.2f allowed over %d values (%s)"
                    % (g["geom"][0], GEOM_TOLERANCE_DU, g["n_geom"],
                       g["geom"][1] if g["n_geom"] else "NO NON-TEXT ELEMENT MEASURED"),
                    g["geom_ok"]))
        out.append(("DS-063", "text runs, whole rect, same pair: worst %.2f du = %.2f device px "
                    "of %.1f allowed (%.2f du at this k) over %d values (%s); k ratio %.4f"
                    % (g["text"][0], g["text_px"], TEXT_TOLERANCE_PX, g["text_tol_du"],
                       g["n_text"], g["text"][1] or "NO TEXT RUN MEASURED", g["k_ratio"]),
                    g["text_ok"]))

    b = body_floor(results)
    if not b:
        out.append(("DS-064", "no body run measured at 720p", False))
    else:
        out.append(("DS-064", "smallest body run in a 720p capture: %.1f px (%.0f du) on %r, "
                    "floor %.0f, %d slide(s) sampled"
                    % (b["css"], b["du"], b["slide"][:28], BODY_FLOOR_CSS_PX, b["n"]), b["ok"]))
    return out


def self_test():
    """Refuse to gate if the gate's own arithmetic is wrong (L-04)."""
    for (w, h, k, _engage) in VIEWPORTS:
        computed = min(w / 1920.0, h / 1080.0)
        if abs(computed - k) > 0.0005:
            sys.exit("SELF-TEST FAILED: %dx%d scales to %.4f, table says %.4f" % (w, h, computed, k))
    engaging = [v for v in VIEWPORTS if v[3]]
    if not any(v[0] >= 960 for v in engaging):
        sys.exit("SELF-TEST FAILED: no engaging viewport is 960 CSS px or wider, so the sweep "
                 "cannot tell the scale rule from the width rule it replaced")
    for (w, h, k, engage) in VIEWPORTS:
        if engage != (k < SCALE_THRESHOLD):
            sys.exit("SELF-TEST FAILED: %dx%d expects engage=%s against k=%.4f" % (w, h, engage, k))
    if "click()" in PROBE:
        sys.exit("SELF-TEST FAILED: the probe drives the deck; auto-engage must be observed")
    return True


def audit(deck, which=None, quiet=False):
    """Every §2.4 / §2.5 row this module can decide, as (rule, measurement, pass) - the shape
    `audit.py` prints. Two Chrome sweeps: four viewports, then three resolutions."""
    rows = sweep(deck, quiet=quiet)
    with open(os.path.join(render.OUT, "contract.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
    return verdicts(rows) + scale_verdicts(deck, which)


def main(deck, which=None):
    self_test()
    render.self_test()
    print("browser: %s" % render.CHROME)
    print("deck:    %s\n" % paths.display_path(deck, ROOT))
    print("=== viewport sweep")
    rows = audit(deck, which)
    failures = []
    print("\n=== §2.4 / §2.5 verdicts")
    for rule, what, good in rows:
        if not good:
            failures.append(rule)
        print("  %-8s %-78s %s" % (rule, what, "pass" if good else "FAIL"))
    print("\n%d failure(s): %s" % (len(failures), ", ".join(failures) or "none"))
    if UNCHECKED:
        print(UNCHECKED)
    print("\nWhat this stage does NOT check is not listed here any more - "
          "`python tools/deck/check.py` derives the whole account from the ruleset's `Reach` "
          "column and names every rule it did not decide, with a reason (T-005).")
    return 1 if failures else 0


# **Retired by T-005, and the reason is that it was answering a question this file cannot answer.**
# It listed four rules as "not gated here", and only one of the four was a REACHABILITY statement:
# DS-061 and DS-065 are *checked in another stage*, which is a fact about how the gate is arranged
# today, and DS-033 was never a rule this file could reach in the first place. Conflating the two
# is what T-037 found and what the ruleset's `Reach` column now records per rule, and `check.py`
# derives the whole account from that column at run time rather than from a paragraph here.
#
# DS-065 in particular is no longer unchecked at all: T-021 reworded the rule so it could be false,
# and T-005 built the check `audit.ds065_units_ride_the_transform` the rewording made possible.
#
# The constant is kept, empty, because `audit.py` prints it and a caller that expects a string
# should get one. Its content lives in `check.py`'s coverage account and in `DESIGN-SYSTEM.md`.
UNCHECKED = ""


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = os.path.abspath(args[0]) if args else os.path.join(
        ROOT, "examples", "reference-deck.html")
    sys.exit(main(target, list(range(12)) if "--all" in sys.argv else None))
