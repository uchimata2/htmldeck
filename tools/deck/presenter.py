#!/usr/bin/env python3
"""Derive a presenter build from a shipped deck and its specification's `Notes` fields.

**Two artifacts from one specification, and only one of them can pass a gate.** That sentence is
[T-211] §3's whole scope and this tool is the half that makes it true. A speaker note is addressed
to the person presenting; a deck is one self-contained file, so a note left inside the shipped file
travels to everyone the file reaches and is readable with `Ctrl+U`. DS-088 bans notes **in the
shipped deck** — not their existence — and the presenter build is where they live instead.

**The marker is the notes themselves, and that is the design rather than a shortcut.** DS-088's
check is `"speaker-note" not in h`, so a note carried in `class="speaker-note"` fails the gate by
*being a note*. A separate `data-presenter` flag would have been a second thing to keep in sync, and
a presenter build that lost its flag would pass — which is the safety property gone. Nothing here
adds a rule, a checker or a token.

**The shipped deck is never touched.** This reads a built deck and writes a **copy** with the notes
in it. So *the shipped artifact is byte-identical to what the same specification produces with no
notes authored* holds by construction and there is nothing to compare — the same shape
`seed_defects.py` derives its fixture with, and `fps.py` instruments a deck with.

**What the gate cannot reach.** A file that is never run through `check.py` is just a deck with an
extra panel, and the failure mode is a person attaching the wrong one. So the output is named
`<slug>-presenter.html` and carries a banner saying what it is. Neither replaces the gate; both are
for the case the gate is never run in.

    python tools/deck/presenter.py examples/sort-window/sort-window.html \\
                                   examples/sort-window/sort-window.slides.md

Notes are authored as an optional tenth field in `<slug>.slides.md`:

    - **Notes.** They will push back on the number - concede the range, hold the direction.

Pure standard library (**L-07**).

[T-211]: scope speaker notes and decide what DS-088 becomes.
"""

import html as html_mod
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ANCHOR = "</body>"
SLIDE_HEAD = re.compile(r"^##\s+Slide\s+(\d+)\b", re.M)
# A field runs from its own `- **Name.**` to the next one, so a note may wrap over several lines
# exactly as `Structure` and `Text` already do. Anchoring the end on the next field rather than on
# a blank line is what allows that.
FIELD = re.compile(r"^-\s+\*\*([A-Za-z][A-Za-z ]*)\.\*\*[ \t]*(.*?)(?=^-\s+\*\*|\Z)", re.M | re.S)
# The deck's own slides, in document order. `spec.py` cuts them the same way.
DECK_SLIDE = re.compile(r'<section[^>]*class="[^"]*\bslide\b[^"]*"', re.I)


def notes_of(spec_text):
    """`{slide number: note}` for every slide whose specification authors one.

    Absent and empty are the same answer — no note — and neither is an error. A `Notes` field is
    optional per slide, because a required one would put an empty `Notes.` on every slide of every
    deck and carry the word into specifications nobody wanted it in.
    """
    out, heads = {}, list(SLIDE_HEAD.finditer(spec_text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(spec_text)
        for name, value in FIELD.findall(spec_text[m.end():end]):
            if name.strip().lower() != "notes":
                continue
            text = " ".join(value.split())
            if text:
                out[int(m.group(1))] = text
    return out


def slide_count(deck_html):
    return len(DECK_SLIDE.findall(deck_html))


PANEL = """
<style>
/* The presenter build's own chrome. Scoped under two ids nothing in the shell uses, so it cannot
   collide with a theme, and injected rather than linked so this file is still one file.
   The banner below uses an HTML entity where the script uses a backslash-u escape, and that
   is not an inconsistency: JS parses those escapes and HTML does not. The first draft used
   a script-style escape in the banner and printed it literally across the top of the deck.

   **Every length here is one of the deck's own tokens, and that is not decoration.** The first
   draft used raw values and the presenter build then failed DS-033 and DS-010 as well as DS-088 -
   three failures where the design intends exactly one. A reader running `check.py` on this file
   should see the safety property and nothing else, and a future maintainer tidying the noise away
   is one careless edit from tidying away the notes. `max-height` is a percentage rather than `vh`
   for the same reason: on a fixed element it resolves against the viewport and DS-033 bans the
   viewport units. The colours stay literal - they must not vary with the theme, because a warning
   that restyles itself to match the deck is a warning that disappears into it. */
#pb-bar{position:fixed;top:0;left:0;right:0;z-index:99998;display:flex;gap:var(--sp-2);
  align-items:center;justify-content:space-between;padding:var(--sp-1) var(--sp-2);
  font-family:var(--font-mono);font-size:var(--fs-small);font-weight:600;
  background:#7A1020;color:#FFF3F2}
#pb-bar button{font:inherit;color:inherit;background:transparent;cursor:pointer;
  border:var(--hair) solid rgba(255,243,242,.5);border-radius:var(--radius-sm);
  padding:var(--sp-0) var(--sp-1)}
#pb-notes{position:fixed;left:0;right:0;bottom:0;z-index:99998;max-height:40%%;overflow:auto;
  padding:var(--sp-2);background:#14131A;color:#F2EFE6;
  font-family:var(--font-mono);font-size:var(--fs-small);
  border-top:var(--hair) solid #7A1020}
#pb-notes[hidden]{display:none}
#pb-notes .pb-slide{opacity:.6;text-transform:uppercase;margin-bottom:var(--sp-0)}
</style>
<div id="pb-bar">
  <span>PRESENTER BUILD &mdash; do not send. Carries speaker notes and fails the deck gate by design.</span>
  <button id="pb-toggle" type="button" aria-pressed="true">Hide notes</button>
</div>
<div id="pb-notes"><div class="pb-slide"></div><div class="speaker-note"></div></div>
<script>
(function(){
  var NOTES = %(notes)s;
  var bar = document.getElementById('pb-notes');
  var slot = bar.querySelector('.speaker-note'), lab = bar.querySelector('.pb-slide');
  var btn = document.getElementById('pb-toggle'), on = true;

  /* Follow the deck's own `[data-current]` rather than counting clicks. Anything that keeps its
     own idea of where the deck is drifts the first time somebody uses the ruler, and `audit.py`
     records what happens when a helper assumes a piece of chrome instead of reading state. */
  function slides(){ return document.querySelectorAll('.stage .slide'); }
  function show(){
    var all = slides(), cur = document.querySelector('.slide[data-current]');
    var at = Array.prototype.indexOf.call(all, cur);
    var n = at + 1, note = NOTES[n];
    lab.textContent = 'Slide ' + (at < 0 ? '?' : n) +
      (cur && cur.dataset.name ? ' \\u00b7 ' + cur.dataset.name : '');
    slot.textContent = note || 'No note for this slide.';
    slot.style.opacity = note ? '1' : '.5';
    bar.hidden = !on;
  }
  btn.addEventListener('click', function(){
    on = !on; btn.textContent = on ? 'Hide notes' : 'Show notes';
    btn.setAttribute('aria-pressed', String(on)); show();
  });
  new MutationObserver(show).observe(document.getElementById('stage') || document.body,
                                     {subtree: true, attributes: true,
                                      attributeFilter: ['data-current']});
  if (document.readyState !== 'loading') show();
  else window.addEventListener('DOMContentLoaded', show);
})();
</script>
</body>"""


def build(deck_html, notes):
    """The deck with the presenter chrome injected. Raises if the anchor is not there."""
    if ANCHOR not in deck_html:
        raise ValueError("no %s in this file - it does not look like a deck" % ANCHOR)
    safe = {n: html_mod.escape(t, quote=False) for n, t in notes.items()}
    return deck_html.replace(ANCHOR, PANEL % {"notes": json.dumps(safe, ensure_ascii=True)}, 1)


def self_test():
    """The parse, the injection, and the property the whole scope rests on."""
    spec = ("## Slide 1 - a\n\n- **Title.** A\n- **Notes.** first note\n"
            "  wrapped over two lines\n- **Sources.** none\n\n"
            "## Slide 2 - b\n\n- **Title.** B\n- **Sources.** none\n\n"
            "## Slide 3 - c\n\n- **Notes.** \n- **Sources.** none\n")
    got = notes_of(spec)
    assert got == {1: "first note wrapped over two lines"}, got
    assert 2 not in got, "a slide with no Notes field must not get an entry"
    assert 3 not in got, "an empty Notes field is no note, not an empty one"

    out = build("<html><body><section class=\"slide\"></section></body></html>", got)
    # **The safety property, asserted here as well as in the gate.** DS-088's check is this string.
    assert "speaker-note" in out, "the artifact must carry the token DS-088 fails on"
    assert out.count("</body>") == 1, "the anchor was duplicated rather than replaced"
    assert "first note wrapped over two lines" in out, "the note did not reach the page"

    esc = build("<body></body>", {1: 'push back <b>hard</b> & "concede"'})
    assert "<b>hard</b>" not in esc, "note text must be escaped, not injected as markup"

    assert slide_count('<section class="slide x"></section><section class="slide"></section>') == 2
    try:
        build("<html><p>no body close</p></html>", {})
    except ValueError:
        pass
    else:
        raise AssertionError("a file with no </body> must be refused, not silently returned")


def main(argv):
    if not argv or argv[0] in ("--help", "-h", "help"):
        print(__doc__.strip())
        return 0
    self_test()
    if len(argv) < 2:
        sys.exit("usage: presenter.py <deck.html> <slug>.slides.md [--out DIR]")

    deck, spec = argv[0], argv[1]
    out_dir = None
    rest = argv[2:]
    while rest:
        a = rest.pop(0)
        if a == "--out":
            out_dir = rest.pop(0)
        else:
            sys.exit("unknown argument: %s" % a)

    for f in (deck, spec):
        if not os.path.isfile(f):
            sys.exit("no such file: %s" % f)
    with open(deck, "r", encoding="utf-8") as fh:
        deck_html = fh.read()
    with open(spec, "r", encoding="utf-8") as fh:
        notes = notes_of(fh.read())

    n_deck = slide_count(deck_html)
    highest = max(notes) if notes else 0
    if highest > n_deck:
        sys.exit("the specification authors a note on slide %d and the deck has %d slides - "
                 "notes are attached by position, so this would silently land on nothing"
                 % (highest, n_deck))

    out_dir = out_dir or os.path.dirname(os.path.abspath(deck))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir,
                       os.path.splitext(os.path.basename(deck))[0] + "-presenter.html")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write(build(deck_html, notes))

    print("deck:      %s  (%d slides, unchanged)" % (paths.display_path(deck, ROOT), n_deck))
    print("spec:      %s  (%d slide(s) carry a note)"
          % (paths.display_path(spec, ROOT), len(notes)))
    print("presenter: %s  (%d KB)"
          % (paths.display_path(out, ROOT), os.path.getsize(out) // 1024))
    if not notes:
        print("\n  No `Notes` field is authored anywhere in that specification, so this build "
              "carries\n  none. It still fails DS-088, because the panel that would hold them is "
              "in it.")
    print()
    print("  This file is NOT shippable and is meant not to be. It fails DS-088 by carrying the")
    print("  notes DS-088 forbids in a shipped deck - run `check.py` on it and it goes red, which")
    print("  is the safety property rather than a defect. Send the deck above, present from this.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
