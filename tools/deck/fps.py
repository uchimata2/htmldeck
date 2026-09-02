#!/usr/bin/env python3
"""Measure the frame rate a deck actually holds — in a browser a person is looking at.

**This is the one measurement in this repository the harness cannot take, and the reason is not
convenience.** `render.py` drives headless Chrome, and headless never produces a frame: measured
2026-08-19 under [T-185], `document.timeline.currentTime` stays at 0, no `animationstart` fires, and
a 420 ms animation reads `currentTime: 0` after 900 ms of real timers. **The clock a CSS animation
runs on is frame production, not time** (**L-26**). So `render.py motion` *seeks* the timeline and
reads the computed style at each point, which measures every intermediate state exactly and says
nothing whatsoever about how fast the frames arrive — because there are none.

So this tool splits the work at the only place it can be split. It does everything that can be
automated: injects a measuring overlay, finds the heaviest slide, gathers the machine's capability
fields, and formats the row. **A person supplies the machine that draws.** The output is a card on
screen with a table row ready to paste into `docs/EVALUATION.md`.

**It is not a gate and it must never become one.** Nothing here fails a deck. A frame-rate threshold
is a claim about hardware this project has no corpus for, and inventing one from a single machine is
the reasoning **L-05** refuses and the scope warning in `docs/upstream/harness.md` refuses again.
`check_all.py` lists it under `NOT_RUN` for exactly that reason.

**Two numbers, never one.** A frame rate is bounded by the display, so *58* means nothing until you
know the ceiling was 60 and not 144. The overlay measures the refresh ceiling first, on an idle
burst before any slide is shown, and reports *held against ceiling*.

**Two counts, and only one of them is in the measurement.** A slide's *entry* animations run once
when it arrives — 340 ms, staggered 60 ms apart — then hold their end state and never replay, so a
six-second window that opens afterwards never sees them. Its *looping* animations run for all of it.
The reference deck's slide 8 carries six animated elements and **one** of them is moving while the
figure is taken: five `rise` entrances and the dashed `Current` flow. Reporting a single *animated*
count invites the reader to look for six moving things and find one — asked, and rightly, on the
first good reading. So both numbers are printed and the looping one leads.

**Finding the heaviest slide takes a walk, and ranking it takes the right axis.** Both halves were
wrong in the first build and the first real reading found them. `.rise` is declared
`.slide[data-played] .rise`, so a slide nobody has visited has no animation to count — counting from
a standing start reports the opening slide and nothing else, while looking like a derivation. And an
entry animation is over 340 ms in, so across a six-second window it costs nothing: what has to be
ranked is **looping** motion, with the total only breaking ties. Ranking on the raw count picks the
slide with the most *finished* animations.

**What it collects about the machine, and what it does not.** OS and browser, browser version, core
count, device memory, screen size, device pixel ratio, display refresh, and the WebGL renderer
string. That is a class of hardware — the thing that makes the figure interpretable. It reads no
hostname, no user name, no path, and no account. `CLAUDE.md`'s publishing rule keeps machine data out
of this repository, and this tool keeps it by not gathering it rather than by remembering to redact.

    python tools/deck/fps.py examples/reference-deck.html
    python tools/deck/fps.py examples/reference-deck.html --seconds 10
    python tools/deck/fps.py examples/reference-deck.html --slide 8 --no-open

Pure standard library (**L-07**).

[T-185]: no instrument here can watch an animation play.
"""

import os
import sys
import webbrowser

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ANCHOR = "</body>"

# The overlay. Kept as one string rather than a file so the tool stays a single artifact an adopter
# can copy, and injected rather than linked so the measured deck is still one self-contained file
# (rule 1 - a deck that needs a second file to be measured is not the deck that ships).
#
# `%%` is a literal percent; the template is applied with `%`.
OVERLAY = """
<div id="fps-card" style="position:fixed;left:50%%;top:50%%;transform:translate(-50%%,-50%%);
  z-index:99999;max-width:44rem;padding:1.4rem 1.6rem;border-radius:10px;
  font:14px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  background:#14131A;color:#F2EFE6;box-shadow:0 18px 60px rgba(0,0,0,.45)">
  <div id="fps-state">Measuring the display's refresh ceiling…</div>
</div>
<script>
(function(){
  var SECONDS = %(seconds)s, FORCED = %(forced)s, DECK_NAME = '%(deck)s';
  var card = document.getElementById('fps-card'), state = document.getElementById('fps-state');
  function say(t){ state.textContent = t; }

  /* Count rAF callbacks over `ms`, and report frames per second over the interval actually
     observed rather than over the interval asked for - the last frame lands past the deadline and
     dividing by the nominal window quietly inflates every figure. */
  function count(ms, done){
    var n = 0, t0 = performance.now();
    (function tick(){
      var t = performance.now();
      if (t - t0 >= ms) return done(n, t - t0);
      n++; requestAnimationFrame(tick);
    })();
  }

  /* The heaviest slide, counted rather than guessed - and **the count has to walk the deck first**.
     `.rise` is declared `.slide[data-played] .rise`, so a slide nobody has visited has NO animation
     to see. Counting from a standing start therefore reports the opening slide and zero everywhere
     else, and the instrument picks slide 1 every time while looking like it derived something.
     Measured 2026-08-22 on the first real reading: slide 1, 5 animated, 144 of 144 - a correct
     measurement of an idle page.

     **Ranked on LOOPING animations first, and that is the substantive half.** An entry animation
     runs for 340 ms and is over long before a six-second window starts, so it costs nothing for the
     interval actually being measured; an infinite one costs for all of it. Ranking on the raw count
     picks the slide with the most finished animations, which is the same wrong answer arrived at
     more slowly. Total breaks ties, because a slide with more to composite is the better bet when
     nothing loops. */
  function weigh(){
    var slides = document.querySelectorAll('.stage .slide'), out = [];
    for (var i = 0; i < slides.length; i++){
      goTo(i);                       /* visiting is what makes the slide's motion exist to count */
      var all = slides[i].querySelectorAll('*'), n = 0, inf = 0;
      for (var j = 0; j < all.length; j++){
        var c = getComputedStyle(all[j]);
        if (!c.animationName || c.animationName === 'none') continue;
        n++;
        if ((c.animationIterationCount || '').indexOf('infinite') >= 0) inf++;
      }
      out.push({i: i, n: n, inf: inf, name: slides[i].dataset.name || ('slide ' + (i + 1))});
    }
    return out;
  }

  /* Drive the deck with its own controls and never by assuming an index - the helper in audit.py
     used to call a chrome element by id and returned a null dereference when T-028 deleted it. */
  function goTo(i){
    var slides = document.querySelectorAll('.stage .slide');
    var prev = document.getElementById('prev'), next = document.getElementById('next');
    if (!prev || !next) throw new Error('no prev/next control to drive the deck with');
    for (var guard = 0; guard < slides.length + 2; guard++){
      var cur = document.querySelector('.slide[data-current]');
      var at = Array.prototype.indexOf.call(slides, cur);
      if (at === i || at < 0) return;
      (at < i ? next : prev).click();
    }
  }

  function gpu(){
    try {
      var c = document.createElement('canvas');
      var gl = c.getContext('webgl') || c.getContext('experimental-webgl');
      if (!gl) return 'no WebGL context';
      var e = gl.getExtension('WEBGL_debug_renderer_info');
      return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : 'renderer string withheld';
    } catch (err) { return 'unavailable: ' + err.message; }
  }

  /* Capability, not identity. Nothing here names the machine, its owner or any path. */
  function machine(){
    var ua = navigator.userAgent, m = {};
    var b = ua.match(/(Edg|Chrome|Firefox|Safari)\\/([\\d.]+)/);
    m.browser  = b ? (b[1] === 'Edg' ? 'Edge' : b[1]) + ' ' + b[2] : 'unknown';
    m.os       = (ua.match(/\\(([^)]*)\\)/) || [, 'unknown'])[1].split(';')[0].trim();
    m.cores    = navigator.hardwareConcurrency || 'unreported';
    m.memory   = navigator.deviceMemory ? navigator.deviceMemory + ' GB' : 'unreported';
    m.screen   = screen.width + '\\u00d7' + screen.height + ' @ ' + (devicePixelRatio || 1) + '\\u00d7';
    m.gpu      = gpu();
    return m;
  }

  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }

  /* **A window that draws no frames must say so, not sit at `Measuring...` looking busy.** Found
     2026-08-22 while checking this overlay for script errors in a hidden preview pane: the card
     rendered, the script ran, `requestAnimationFrame` never fired once, and the page stayed on its
     first message indefinitely. That is T-185's finding arriving through a second door, and without
     this watchdog it is indistinguishable from a slow machine - which is the reading most likely to
     be written down as a number. */
  var done_ = false, stage = 'ceiling';
  function bail(why){
    if (done_) return;
    done_ = true;
    card.innerHTML =
      '<div style="font-size:1.5rem;margin-bottom:.6rem">No frames.</div>' +
      '<div style="opacity:.85;margin-bottom:.8rem">' + why + '</div>' +
      '<div style="opacity:.7">A frame rate can only be measured where frames are produced. A ' +
      'hidden tab, a minimised or background window, a preview pane and a headless browser all ' +
      'produce exactly this - the animation clock is frame production, not time. Bring this ' +
      'window to the front in Chrome or Edge and reload.</div>';
  }
  setTimeout(function(){ if (stage === 'ceiling') bail('The display never drew a frame to measure ' +
    'the refresh ceiling with.'); }, 5000);
  setTimeout(function(){ bail('The run did not finish.'); }, (SECONDS + 8) * 1000);

  function report(held, ceiling, slide, mc){
    if (done_) return;
    done_ = true;
    var pct = ceiling ? Math.round(held / ceiling * 100) : 0;
    var row = '| ' + [new Date().toISOString().slice(0, 10),
                      DECK_NAME,
                      (slide.i + 1) + ' \\u00b7 ' + slide.name,
                      slide.inf + ' looping + ' + (slide.n - slide.inf) + ' entry',
                      held.toFixed(1),
                      ceiling.toFixed(0),
                      mc.os + ', ' + mc.browser + ', ' + mc.cores + ' cores, ' + mc.gpu
                     ].join(' | ') + ' |';
    card.innerHTML =
      '<div style="font-size:2.6rem;line-height:1;margin-bottom:.2rem">' + held.toFixed(1) +
      '<span style="font-size:1rem;opacity:.7"> fps held</span></div>' +
      '<div style="opacity:.75;margin-bottom:1rem">against a ' + ceiling.toFixed(0) +
      ' fps display ceiling \\u2014 ' + pct + '%% of what this screen can draw</div>' +
      '<div style="opacity:.85">slide ' + (slide.i + 1) + ' \\u00b7 ' + esc(slide.name) +
      ' \\u00b7 ' + SECONDS + 's</div>' +
      '<div style="opacity:.85">' + slide.inf + ' looping \\u2014 running for the whole window' +
      '<br>' + (slide.n - slide.inf) + ' entry \\u2014 played when the slide arrived and finished ' +
      'before the window opened, so they cost this figure nothing</div>' +
      (slide.inf === 0 ? '<div style="opacity:.85;margin-bottom:.6rem;color:#F0C878">Nothing on ' +
        'this slide loops, so the interval measured is an idle page holding the refresh rate. ' +
        'That is a real result and not a fault - this deck has no sustained motion outside its ' +
        'flow.</div>' : '') +
      '<div style="opacity:.85;margin-bottom:1rem">' + esc(mc.os) + ' \\u00b7 ' + esc(mc.browser) +
      ' \\u00b7 ' + mc.cores + ' cores \\u00b7 ' + esc(mc.memory) + ' \\u00b7 ' + esc(mc.screen) +
      '<br>' + esc(mc.gpu) + '</div>' +
      '<div style="opacity:.6;margin-bottom:.3rem">paste this row into docs/EVALUATION.md</div>' +
      '<textarea readonly style="width:100%%;height:4.5rem;background:#0C0B10;color:#F2EFE6;' +
      'border:1px solid #34313E;border-radius:6px;padding:.5rem;font:inherit">' +
      esc(row) + '</textarea>';
  }

  /* The ceiling first, and BEFORE any slide is shown. It is a property of the display, and
     measuring it while the deck animates folds the two numbers into one. */
  function start(){
    count(1000, function(n, ms){
      stage = 'measuring';
      var ceiling = n / (ms / 1000);
      say('Walking the deck to see what each slide animates\\u2026');
      var weights = weigh();
      var ranked = weights.slice().sort(function(a, b){
        return (b.inf - a.inf) || (b.n - a.n) || (a.i - b.i);
      });
      var slide = FORCED !== null ? weights[FORCED - 1] : ranked[0];
      if (!slide) { say('no slides found - is this a deck?'); return; }
      say('Slide ' + (slide.i + 1) + ' carries ' + slide.n + ' animated element(s), ' +
          slide.inf + ' looping. Measuring for ' + SECONDS + 's\\u2026');
      goTo(slide.i);
      requestAnimationFrame(function(){
        count(SECONDS * 1000, function(n2, ms2){
          report(n2 / (ms2 / 1000), ceiling, slide, machine());
        });
      });
    });
  }

  if (document.readyState === 'complete') setTimeout(start, 300);
  else window.addEventListener('load', function(){ setTimeout(start, 300); });
})();
</script>
</body>"""


def instrument(html, seconds=6, slide=None, name=None):
    """The deck with the overlay injected. Raises if the anchor is not there.

    `name` is the deck's own name, and it has to come from here: `deck.js` rewrites
    `document.title` to the current slide on every navigation, so a page reading its own title
    reports the slide it is standing on and never the deck. Found on the first good reading -
    both columns said *One transfer disappears*.
    """
    if ANCHOR not in html:
        raise ValueError("no %s in this file - it does not look like a deck" % ANCHOR)
    body = OVERLAY % {"seconds": int(seconds),
                      "forced": "null" if slide is None else int(slide),
                      "deck": (name or "this deck").replace("\\", "").replace("'", "")}
    return html.replace(ANCHOR, body, 1)


def self_test():
    """The injection, and the two ways it can silently do nothing."""
    out = instrument("<html><body><p>x</p></body></html>", seconds=3)
    if not ("fps-card" in out):
        sys.exit("SELF-TEST FAILED: %s" % ("the overlay did not land",))
    if not (out.count("</body>") == 1):
        sys.exit("SELF-TEST FAILED: %s" % ("the anchor was duplicated rather than replaced",))
    if not ("var SECONDS = 3," in out):
        sys.exit("SELF-TEST FAILED: %s" % ("--seconds did not reach the page",))
    if not ("FORCED = null" in out):
        sys.exit("SELF-TEST FAILED: %s" % ("an unforced run should pick the slide itself",))
    if not ("FORCED = 4" in instrument("<body></body>", slide=4)):
        sys.exit("SELF-TEST FAILED: %s" % ("--slide did not reach the page",))
    if not ("DECK_NAME = 'my-deck'" in instrument("<body></body>", name="my-deck")):
        sys.exit("SELF-TEST FAILED: %s" % ("the deck name did not",))
    if not ("DECK_NAME = 'this deck'" in out):
        sys.exit("SELF-TEST FAILED: %s" % ("a missing name must not leave the template unfilled",))
    # A percent sign in the template that is not doubled would raise here rather than at run time.
    if not ("%(seconds)s" not in out):
        sys.exit("SELF-TEST FAILED: %s" % ("the template was not applied",))
    try:
        instrument("<html><p>no body close</p></html>")
    except ValueError:
        pass
    else:
        raise AssertionError("a file with no </body> must be refused, not silently returned")


def main(argv):
    if not argv or argv[0] in ("--help", "-h", "help"):
        print(__doc__.strip())
        return 0
    self_test()

    deck, seconds, slide, open_it = argv[0], 6, None, True
    rest = argv[1:]
    while rest:
        a = rest.pop(0)
        if a == "--seconds":
            seconds = int(rest.pop(0))
        elif a == "--slide":
            slide = int(rest.pop(0))
        elif a == "--no-open":
            open_it = False
        else:
            sys.exit("unknown argument: %s" % a)

    if not os.path.isfile(deck):
        sys.exit("no such deck: %s" % deck)
    with open(deck, "r", encoding="utf-8") as fh:
        html = fh.read()

    out_dir = os.path.join(paths.output_root(deck), ".assets-cache", "deck")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, os.path.splitext(os.path.basename(deck))[0] + "-fps.html")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write(instrument(html, seconds, slide,
                            os.path.splitext(os.path.basename(deck))[0]))

    print("deck:    %s" % paths.display_path(deck, ROOT))
    print("built:   %s  (%d KB)" % (paths.display_path(out, ROOT), os.path.getsize(out) // 1024))
    print()
    print("  This measures nothing on its own. It needs a window that draws frames, so open the")
    print("  file above in Chrome or Edge, leave it in the foreground, and do not switch tabs -")
    print("  a background tab is throttled and the figure it produces is about the throttling.")
    print()
    print("  It measures the display's refresh ceiling, picks the slide carrying the most animated")
    print("  elements, runs for %ds, and prints a table row to paste into docs/EVALUATION.md." % seconds)
    if open_it:
        webbrowser.open("file:///" + os.path.abspath(out).replace(os.sep, "/"))
        print("\n  Opened in the default browser. If that is not Chrome or Edge, open it there instead.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
