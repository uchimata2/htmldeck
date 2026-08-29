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
      /* Whether the deck HAS a reflow view, which is a different question from whether it is
         showing one. DS-072 and DS-074 both judge that view, and with no view at all their
         measurements are vacuous rather than damning - see `verdicts` (T-075). */
      hasDoc: !!doc,
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
    probe = render.make_probe(deck, name="contract.html", extra=PROBE,
                              out=render.out_dir(deck))
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
    # **Paired by slide, never by position** (T-183). `zip` pairs the two runs by index, and the
    # two runs are two independent sets of Chrome launches: `render.measure` prints `!! no result`
    # and CONTINUES when one comes back empty, so a single dropped render shifts every pair after
    # it and the comparison silently reads slide n against slide n+1.
    #
    # **That does not degrade the measurement, it inverts it.** Measured on a real four-slide
    # sample, 2026-08-18: intact, 120 values and a worst disagreement of 0.00 du non-text and
    # 1.70 du of text. Drop one row from the smaller run and the same deck reports **314.14 du**
    # and **479.26 device px** against a 2.0 px bound - a catastrophic failure invented entirely
    # by the pairing. That is a red gate on a deck with nothing wrong with it, and re-running
    # clears it, which is the shape that teaches a reader to re-run until green.
    names_a, names_b = [r["slide"] for r in a], [r["slide"] for r in b]
    duplicated = sorted({n for n in names_a if names_a.count(n) > 1}
                        | {n for n in names_b if names_b.count(n) > 1})
    by_b = {r["slide"]: r for r in b}
    pairs = [(ra, by_b[ra["slide"]]) for ra in a if ra["slide"] in by_b]
    unpaired = sorted(set(names_a) ^ set(names_b))
    # Split by ELEMENT KIND, not by axis. Measured 2026-08-07 over the full 12-slide deck: a text
    # run's whole rect is glyph-derived, not only its width. `y` reached 0.62 du and `h` 0.42 on
    # SVG labels, against a worst width of 1.17 - so holding a text run's placement to the
    # non-text tolerance fails a deck whose layout is provably identical.
    worst = {"geom": (0.0, ""), "text": (0.0, "")}
    counted = {"geom": 0, "text": 0}
    for ra, rb in pairs:
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
            # **The pairing is a fact about the run, not about the deck**, so it is reported
            # beside the verdict rather than folded into it. `aligned` false means this run
            # measured two different sets of slides and no verdict it produced is about the deck.
            "paired": len(pairs), "unpaired": unpaired, "duplicated": duplicated,
            "aligned": not unpaired and not duplicated,
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
    # **`not off` over an empty list is a pass on nothing** - the L-44 shape, still live in this
    # module after three fixes to the one next door, because nothing had ever run this file's rows
    # against a measurement in which nothing was found (T-075). *Every viewport centres the stage*
    # with no viewport showing a stage is undecided.
    out.append(("DS-200", "scaled stage centred at %d viewport(s) showing a stage%s"
                % (len(on_stage), "" if not off else "; off by %.1f,%.1f px at %dx%d"
                   % (off[0][1], off[0][2], off[0][0]["vw"], off[0][0]["vh"])),
                None if not on_stage else not off))

    # DS-071 - the amended rule. Reported with k, because a bare pass/fail here is unreadable.
    wrong = [r for r in rows if r["docOn"] != r["want"]["engage"]]
    out.append(("DS-071", "reflow engages exactly when k < %.1f: %s"
                % (SCALE_THRESHOLD,
                   "%d/%d viewports" % (len(rows) - len(wrong), len(rows))
                   + ("" if not wrong else "; %dx%d k=%.3f gave doc=%s, wanted %s"
                      % (wrong[0]["vw"], wrong[0]["vh"], wrong[0]["k"],
                         wrong[0]["docOn"], wrong[0]["want"]["engage"]))),
                not wrong))

    # The guard is a claim about the auto-engage path, so a deck with no reflow view has no path
    # to guard: the probe fakes a small viewport and a fullscreen, the deck cannot hand over
    # because there is nowhere to hand over to, and `heldStill` comes back True on nothing.
    has_doc = any(r.get("hasDoc") for r in rows)
    guards = [r["fullscreenGuard"] for r in rows]
    out.append(("DS-072", "auto-engage consults fullscreenElement (tested against a double, "
                "not a real fullscreen): %s" % (guards[0] if has_doc else "no reflow view"),
                all(g is True for g in guards) if has_doc else None))

    # Every role, not the first one that answers. A role pinned to px is exactly what a reading
    # view must not have, and it hides behind any sibling that still scales.
    #
    # **With no reflow view there is no reading type to pin.** `bool(roles)` read that as a
    # failure, which is this file's copy of the defect T-051, T-065 and T-066 each removed from
    # `audit.py` - a rule failing a deck for not containing its subject. The absence itself is not
    # unreported: DS-071 fails, because two of the four viewports require the view to engage.
    roles = rows[0].get("remScaling") or []
    pinned = [r for r in roles if r[2] <= r[1] * 1.5]
    out.append(("DS-074", "reflow type follows the root font size: %d of %d role(s) scale%s"
                % (len(roles) - len(pinned), len(roles),
                   "" if not pinned else "; %s stays at %.1f px" % (pinned[0][0], pinned[0][2])),
                None if not has_doc else (bool(roles) and not pinned)))
    return out


# How many slides the two-resolution comparison samples. DS-063 is a claim about the whole stage,
# so a sample is a compromise and is named as one: four slides spanning the deck, at roughly 12
# Chrome launches. `--all` measures every slide.
SAMPLE_SIZE = 4


def sample_for(n):
    """`SAMPLE_SIZE` slide indices spread across a deck of `n` slides, 0-based.

    **The indices are derived from the deck, not fixed** (`PR-53`). They used to be
    `SAMPLE = [0, 4, 7, 11]`, and the probe reaches a slide by clicking `next`, which `deck.js`
    clamps at the last slide - so an eight-slide deck measured slides 1, 5, 8 and **8**, the
    duplicate guard correctly refused to compare it, and DS-063 read *undecided* while advising a
    re-run that would recur forever because nothing had been dropped. DS-082's default deck length
    is 8-12 and DS-081's floor is 6, so most of the legitimate band lost the rule on every run.

    **On a twelve-slide deck this returns `[0, 4, 7, 11]`** - the constant it replaces, which is
    the strongest evidence available that the derivation is the right one and not merely a
    different one. The self-test asserts it, so the two can never drift apart silently.

    A deck with fewer slides than `SAMPLE_SIZE` is sampled whole. The result is sorted and
    duplicate-free by construction at every length, which is what makes the duplicate the guard
    reports unambiguously the render's doing.
    """
    if n <= 0:
        return []
    k = min(SAMPLE_SIZE, n)
    if k == 1:
        return [0]
    return sorted({int(round(i * (n - 1) / float(k - 1))) for i in range(k)})


def scale_verdicts(deck, which=None, quiet=True):
    """DS-063 and DS-064 - measured by `render.py` since T-024, gated here for the first time."""
    if which is None:
        # `render.slide_count` reads the file and treats zero as fatal rather than rendering a
        # guess. Taking the length from there is the whole of the fix: four indices spread across
        # THIS deck cost the same renders and cannot fall off the end of it.
        which = sample_for(render.slide_count(deck))
    # **A duplicate the SAMPLER caused and one a dropped render caused need opposite fixes**, and
    # until now the message stated only the second. `sample_for` cannot produce one, so the only
    # way to get here is a caller passing a list with a repeat - and that is answered by fixing the
    # call, not by re-running. Said here, where the sample is known, rather than downstream where
    # only its consequence is.
    repeated = sorted({i for i in which if list(which).count(i) > 1})
    if repeated:
        return [("DS-063", "the sample asks for slide(s) %s twice, so the comparison is undecided "
                           "rather than failed. This is the sample and not the render: re-running "
                           "reproduces it exactly. Pass distinct indices, or none and let "
                           "`sample_for` derive them from the deck's own slide count"
                 % ", ".join(str(i + 1) for i in repeated), None),
                ("DS-064", "not measured: the sample DS-063 refused is the same sample", None)]
    return scale_verdicts_from(render.measure(deck, which, quiet=quiet))


def scale_verdicts_from(results):
    """The verdicts alone, given a measurement. **Split out of `scale_verdicts` by T-075** so the
    absent-subject fixture can run these rows against a measurement in which nothing was found;
    while the render was inside the function, no fixture could reach them without a browser and
    this file's rows sat outside the discipline `audit.py` has enforced since T-066."""
    out = []

    g = geometry(results)
    if not g:
        out.append(("DS-063", "the two-resolution comparison produced no result", False))
    elif not g["aligned"]:
        # **An unstable reading is reported as unstable** (T-183) - `None`, which this file already
        # means by *undecided, not failed*, and which the account keeps out of `checked` rather
        # than counting as a pass. Failing here would be the same wrong answer the misalignment
        # produced; passing would hide a run that measured nothing it claims to have measured.
        what = []
        if g["unpaired"]:
            what.append("only one run measured %s" % ", ".join(repr(s[:28]) for s in g["unpaired"]))
        if g["duplicated"]:
            what.append("a run measured %s twice"
                        % ", ".join(repr(s[:28]) for s in g["duplicated"]))
        out.append(("DS-063", "the two renderings measured different slides, so the comparison is "
                              "undecided rather than failed: %s. %d slide(s) paired. Re-run; if it "
                              "recurs the probe is dropping or repeating a slide, which is the "
                              "measurement to fix and not this deck"
                    % ("; ".join(what), g["paired"]), None))
    else:
        # `counted == 0` is the comparison finding nothing to compare, not the two renderings
        # disagreeing. It read as a failure until T-075: the same rule, judged against an empty
        # set. The loud message stays - *no non-text value measured is not a pass* is still true,
        # and undecided is not a pass.
        out.append(("DS-063", "non-text geometry across 3840x2000 and 1280x634: worst %.2f du of "
                    "%.2f allowed over %d values (%s)"
                    % (g["geom"][0], GEOM_TOLERANCE_DU, g["n_geom"],
                       g["geom"][1] if g["n_geom"] else "NO NON-TEXT ELEMENT MEASURED"),
                    g["geom_ok"] if g["n_geom"] else None))
        out.append(("DS-063", "text runs, whole rect, same pair: worst %.2f du = %.2f device px "
                    "of %.1f allowed (%.2f du at this k) over %d values (%s); k ratio %.4f"
                    % (g["text"][0], g["text_px"], TEXT_TOLERANCE_PX, g["text_tol_du"],
                       g["n_text"], g["text"][1] or "NO TEXT RUN MEASURED", g["k_ratio"]),
                    g["text_ok"] if g["n_text"] else None))

    b = body_floor(results)
    if not b:
        # **The row an outside project's deck failed on, reported 2026-08-10 (T-075).** A deck
        # whose body prose the probe cannot locate has not been evaluated against the 16 px floor,
        # and saying so is more useful than a verdict. The probe reached this state for two decks
        # in a row by looking for class names belonging to the reference deck; that half is fixed
        # in `render.py`, and this half is what stops the next probe gap being a failed release.
        out.append(("DS-064", "no body run measured at 720p - undecided, not failed", None))
    else:
        out.append(("DS-064", "smallest body run in a 720p capture: %.1f px (%.0f du) on %r, "
                    "floor %.0f, %d slide(s) sampled"
                    % (b["css"], b["du"], b["slide"][:28], BODY_FLOOR_CSS_PX, b["n"]), b["ok"]))
    return out


# **What this file's probes emit when they find nothing**, so the absent-subject fixture can run
# every row here against it without a browser. Written next to the probe it models on purpose:
# T-066's third defect was a fixture whose model of the probe was wrong, which made a rule with
# nothing wrong with it sit on the failing list and would have enshrined that in a declaration.
#
# The stage is present and unstyled rather than missing, because `PROBE` reads `#stage` before
# anything else and a deck without one returns no row at all - that is a render failure, and it is
# not what "found nothing" means.
PROBE_FOUND_NOTHING = {
    "k": 0.0,                       # `--k` unset, so `parseFloat(...) || 0`
    "layout": [0, 0],               # a stage with no size
    "rect": [0.0, 0.0, 0.0, 0.0],
    "transform": "none",
    "docOn": False,
    "hasDoc": False,                # no reflow view
    "stageHidden": False,           # `!!(viewport && ...)` with no #viewport
    "remScaling": [],               # filled only `if (doc)`
    "fullscreenGuard": True,        # `heldStill` is trivially true with nowhere to hand over to
    "fullscreenGuardTested": [False, 0, 300],
}


def nothing_found_rows():
    """The sweep `verdicts` sees when every probe found nothing - one row per viewport, since the
    rows are per-viewport and `want` is attached by `sweep` rather than by the probe."""
    rows = []
    for (w, h, k_expected, engage) in VIEWPORTS:
        row = dict(PROBE_FOUND_NOTHING, vw=w, vh=h)
        row["want"] = {"w": w, "h": h, "k": k_expected, "engage": engage}
        rows.append(row)
    return rows


def nothing_found_results():
    """The measurement `scale_verdicts_from` sees when both renderings SUCCEEDED and measured
    nothing - which is a different thing from a render that produced no result, and the reason
    `geometry`'s `produced no result` row is a real failure rather than an absent subject."""
    def at(k):
        return [{"slide": "a slide with nothing to measure", "k": k, "geom": {}, "type": {},
                 "vw": 0, "vh": 0, "overflow": []}]
    return {"3840x2000": at(2.0), "1280x634": at(0.5871), "720p": at(0.6667)}


def self_test():
    """Refuse to gate if the gate's own arithmetic is wrong (L-04)."""
    # **The sample is derived, and the derivation has to reproduce the constant it replaced.**
    # `[0, 4, 7, 11]` was `SAMPLE` for a twelve-slide deck; if a later edit to `sample_for` moves
    # it, that is a change to what DS-063 measures on every deck in this repository and it must
    # not happen quietly (`PR-53`).
    if sample_for(12) != [0, 4, 7, 11]:
        sys.exit("SELF-TEST FAILED: the derived sample for a 12-slide deck is %r, and the fixed "
                 "sample it replaced was [0, 4, 7, 11]. Every figure this repository quotes for a "
                 "routine run was measured on those four slides" % (sample_for(12),))
    # **Duplicate-free and in range at every length**, which is what makes a duplicate the pairing
    # guard reports unambiguously the RENDER's doing. The floor is DS-081's 6 and the band is
    # DS-082's 8-12; the range below covers both and the long decks T-178 tests at.
    for n in range(1, 61):
        got = sample_for(n)
        if len(got) != len(set(got)):
            sys.exit("SELF-TEST FAILED: the sample for a %d-slide deck repeats a slide - %r. The "
                     "pairing guard would refuse the comparison and advise a re-run that cannot "
                     "help, which is the defect PR-53 named" % (n, got))
        if any(i < 0 or i >= n for i in got):
            sys.exit("SELF-TEST FAILED: the sample for a %d-slide deck leaves the deck - %r. The "
                     "probe clamps at the last slide, so an index past the end silently measures "
                     "the last one again" % (n, got))
        if len(got) != min(SAMPLE_SIZE, n):
            sys.exit("SELF-TEST FAILED: a %d-slide deck was sampled at %d slide(s), not %d - %r"
                     % (n, len(got), min(SAMPLE_SIZE, n), got))
    if sample_for(0) != []:
        sys.exit("SELF-TEST FAILED: a deck with no slides returned a sample")

    # A caller passing a repeated index is the SAMPLER's fault and re-running cannot help, so it
    # reads differently from the render dropping one. The two need opposite fixes (T-230).
    rows = dict((r[0], (r[1], r[2])) for r in scale_verdicts("(never read)", which=[0, 4, 4, 7]))
    if rows["DS-063"][1] is not None or "not the render" not in rows["DS-063"][0]:
        sys.exit("SELF-TEST FAILED: a sample asking for one slide twice was not refused as the "
                 "sample's fault: %r" % (rows["DS-063"],))

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

    # T-183. **The pairing, watched failing.** Two runs of one two-slide deck, identical except
    # that the second run is missing a slide - which is exactly what `render.measure` leaves behind
    # when a read comes back empty and it continues. Built here rather than read off a real
    # measurement (**L-78**): a fixture that needs a browser is a fixture nothing runs.
    def _row(name, x):
        return {"slide": name, "k": 0.5, "geom": {"headline": [x, 0.0, 100.0, 20.0],
                                                  "rule": [x, 40.0, 200.0, 2.0]}}

    good = {"3840x2000": [_row("one", 10.0), _row("two", 900.0)],
            "1280x634": [_row("one", 10.0), _row("two", 900.0)]}
    g = geometry(good)
    if not g["aligned"] or g["paired"] != 2:
        sys.exit("SELF-TEST FAILED: two identical runs did not pair - %r" % g)
    if g["geom"][0] != 0.0:
        sys.exit("SELF-TEST FAILED: two identical runs disagreed by %.2f du" % g["geom"][0])

    dropped = {"3840x2000": good["3840x2000"], "1280x634": [_row("two", 900.0)]}
    g = geometry(dropped)
    if g["aligned"]:
        sys.exit("SELF-TEST FAILED: a run missing a slide was reported as aligned. Positional "
                 "pairing then compares slide n against slide n+1, and T-183 measured that "
                 "turning 0.00 du into 314.14 du on a deck with nothing wrong with it")
    if g["unpaired"] != ["one"]:
        sys.exit("SELF-TEST FAILED: the unpaired slide was not named - %r" % g["unpaired"])
    # and the pairing it DID make is still by name, so the surviving comparison is honest
    if g["paired"] != 1 or g["geom"][0] != 0.0:
        sys.exit("SELF-TEST FAILED: the surviving pair was mismatched - %d pair(s), worst %.2f du"
                 % (g["paired"], g["geom"][0]))

    twice = {"3840x2000": [_row("one", 10.0), _row("one", 10.0)],
             "1280x634": [_row("one", 10.0), _row("one", 10.0)]}
    if geometry(twice)["aligned"]:
        sys.exit("SELF-TEST FAILED: a run measuring one slide twice was reported as aligned - "
                 "that is the probe failing to advance, and it pairs cleanly by name while "
                 "measuring half of what it claims")

    # The verdict a broken pairing produces is `None`, not False: undecided, not failed.
    rows = [r for r in scale_verdicts_from(dropped) if r[0] == "DS-063"]
    if not rows or any(r[2] is not None for r in rows):
        sys.exit("SELF-TEST FAILED: a misaligned comparison did not report undecided - %r" % rows)
    if not any("different slides" in r[1] for r in rows):
        sys.exit("SELF-TEST FAILED: the undecided row does not say why - %r" % rows)
    # and an aligned one still decides
    rows = [r for r in scale_verdicts_from(good) if r[0] == "DS-063"]
    if not rows or any(r[2] is not True for r in rows):
        sys.exit("SELF-TEST FAILED: an aligned comparison stopped deciding - %r" % rows)
    return True


def audit(deck, which=None, quiet=False):
    """Every §2.4 / §2.5 row this module can decide, as (rule, measurement, pass) - the shape
    `audit.py` prints. Two Chrome sweeps: four viewports, then three resolutions."""
    rows = sweep(deck, quiet=quiet)
    # The deck's project, not this tool's (T-074).
    out = render.out_dir(deck)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "contract.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
    return verdicts(rows) + scale_verdicts(deck, which)


def main(deck, which=None):
    self_test()
    render.self_test()
    print("browser: %s" % render.CHROME)
    print("deck:    %s\n" % paths.display_path(deck, ROOT))
    print("=== viewport sweep")
    rows = audit(deck, which)
    failures, undecided = [], []
    print("\n=== §2.4 / §2.5 verdicts")
    for rule, what, good in rows:
        # `None` is undecided, not failing (T-065's third state, reaching this file in T-075).
        if good is False:
            failures.append(rule)
        elif good is None:
            undecided.append(rule)
        print("  %-8s %-78s %s"
              % (rule, what, "pass" if good else ("FAIL" if good is False else "undecided")))
    print("\n%d failure(s): %s" % (len(failures), ", ".join(failures) or "none"))
    if undecided:
        print("%d undecided, no subject: %s" % (len(undecided), ", ".join(sorted(set(undecided)))))
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
