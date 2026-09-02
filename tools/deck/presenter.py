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
SLIDE_HEAD = re.compile(r"^##\s+Slide\s+(\d+)\b[^\n]*?(?:[-–—]\s*(.*))?$", re.M)
# The deck names its own slides. `data-name` is what the ruler and the contents page read, so it is
# the one string both documents already agree on and the only identity available without inventing
# a third.
DECK_NAME = re.compile(r'<section[^>]*\bclass="[^"]*\bslide\b[^"]*"[^>]*\bdata-name="([^"]*)"', re.I)
# A field runs from its own `- **Name.**` to the next one, so a note may wrap over several lines
# exactly as `Structure` and `Text` already do. Anchoring the end on the next field rather than on
# a blank line is what allows that.
FIELD = re.compile(r"^-\s+\*\*([A-Za-z][A-Za-z ]*)\.\*\*[ \t]*(.*?)(?=^-\s+\*\*|\Z)", re.M | re.S)
# A field runs to the next field or to the end of the slide's section - and a slide's section can
# end with a horizontal rule before the next heading. `measure-first` separates its slides that way,
# so the last field on a slide swallowed the `---` and a presenter read three hyphens at the end of
# their note. Found by looking at the render, 2026-08-22 (T-217).
HRULE = re.compile(r"^[ \t]*(?:-{3,}|\*{3,}|_{3,})[ \t]*$", re.M)
# **A slide section ends at the next heading of ANY level, not at the next `## Slide`.** The last
# slide of a specification is followed by `## Open - needs a decision` and its table, and bounding
# on the slide heading alone gave that slide a section running to end of file - so the final field
# swallowed the open-questions section whole. The presenter would have read it as their note.
# Found by reading the built note back, 2026-08-22 (T-217).
HEADING = re.compile(r"^#{1,6}[ \t]", re.M)
# The deck's own slides, in document order. `spec.py` cuts them the same way.
DECK_SLIDE = re.compile(r'<section[^>]*class="[^"]*\bslide\b[^"]*"', re.I)


def notes_of(spec_text):
    """`{slide number: (title, note)}` for every slide whose specification authors a note.

    Absent and empty are the same answer — no note — and neither is an error. A `Notes` field is
    optional per slide, because a required one would put an empty `Notes.` on every slide of every
    deck and carry the word into specifications nobody wanted it in.

    The **title** comes back with the note because the number cannot be trusted to locate anything;
    see `resolve`.
    """
    out, heads = {}, list(SLIDE_HEAD.finditer(spec_text))
    stops = [h.start() for h in HEADING.finditer(spec_text)]
    for m in heads:
        after = [x for x in stops if x > m.start()]
        end = after[0] if after else len(spec_text)
        for name, value in FIELD.findall(spec_text[m.end():end]):
            if name.strip().lower() != "notes":
                continue
            cut = HRULE.search(value)
            text = " ".join((value[:cut.start()] if cut else value).split())
            if text:
                out[int(m.group(1))] = ((m.group(2) or "").strip(), text)
    return out


def slide_count(deck_html):
    return len(DECK_SLIDE.findall(deck_html))


def deck_names(deck_html):
    """The deck's slide names, in document order."""
    return DECK_NAME.findall(deck_html)


def key(title):
    """Lowercase alphanumerics only.

    The deck's `data-name` is not the specification's heading character for character: the same
    slide is `€450k in, €1.2m a year out` in one and `450k in, 1.2m a year out` in the other,
    because the currency symbols do not survive into the attribute. An exact compare would refuse a
    match any reader would call obvious, and refusing is expensive here — it stops a build. So both
    sides are reduced to what they have in common.
    """
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())


def resolve(notes, names):
    """`({deck index: note}, [problem])` — attach each note by TITLE, never by position.

    **Position is not identity, and one example cannot show that.** `presenter.py` shipped
    attaching specification slide `n` to the deck's `n`th slide. It held on `sort-window`, whose two
    documents happen to number the same twelve slides, and broke on `measure-first`, whose deck
    opens with a title slide and closes with `Sources` and numbers neither in its specification — so
    every note landed one slide early, on a real slide, with nothing reporting it (**L-131**).

    **There is no position fallback.** Falling back is the defect; an unresolvable note stops the
    build and says what it looked for.
    """
    keyed = {}
    for i, nm in enumerate(names):
        keyed.setdefault(key(nm), []).append(i)
    out, problems = {}, []
    for n in sorted(notes):
        title, text = notes[n]
        if not title:
            problems.append("slide %d has a note and its heading states no title, so there is "
                            "nothing to match it on" % n)
            continue
        hits = keyed.get(key(title), [])
        if len(hits) == 1:
            out[hits[0]] = (n, title, text)
        elif not hits:
            problems.append("slide %d %r matches no slide in the deck" % (n, title))
        else:
            problems.append("slide %d %r matches %d slides in the deck (%s)"
                            % (n, title, len(hits), ", ".join(str(i + 1) for i in hits)))
    return out, problems


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


def build(deck_html, attached):
    """The deck with the presenter chrome injected.

    `attached` is `resolve`'s mapping — **deck index** to `(spec slide, title, note)` — so the
    numbers reaching the page are the deck's own positions and the panel needs to know nothing
    about how the specification numbered anything. Raises if the anchor is not there.
    """
    if ANCHOR not in deck_html:
        raise ValueError("no %s in this file - it does not look like a deck" % ANCHOR)
    safe = {str(i + 1): html_mod.escape(t, quote=False)
            for i, (_n, _title, t) in attached.items()}
    return deck_html.replace(ANCHOR, PANEL % {"notes": json.dumps(safe, ensure_ascii=True)}, 1)


def self_test():
    """The parse, the match, the injection, and the property the whole scope rests on."""
    spec = ("## Slide 1 - Two opposite problems\n\n- **Title.** A\n- **Notes.** first note\n"
            "  wrapped over two lines\n- **Sources.** none\n\n"
            "## Slide 2 - Nothing here measures it\n\n- **Title.** B\n- **Sources.** none\n\n"
            "## Slide 3 - Empty note\n\n- **Notes.** \n- **Sources.** none\n")
    got = notes_of(spec)
    if not (set(got) == {1}):
        sys.exit("SELF-TEST FAILED: %r" % (got,))
    if not (got[1] == ("Two opposite problems", "first note wrapped over two lines")):
        sys.exit("SELF-TEST FAILED: %r" % (got[1],))
    if not (2 not in got):
        sys.exit("SELF-TEST FAILED: %s" % ("a slide with no Notes field must not get an entry",))
    if not (3 not in got):
        sys.exit("SELF-TEST FAILED: %s" % ("an empty Notes field is no note, not an empty one",))

    # A slide section ending in a horizontal rule must not put it inside the note.
    ruled = notes_of("## Slide 1 - T\n\n- **Notes.** hold the range\n\n---\n\n## Slide 2 - U\n")
    if not (ruled[1] == ("T", "hold the range")):
        sys.exit("SELF-TEST FAILED: %r" % (ruled,))

    # The LAST slide is followed by the open-questions section, not by another slide. Bounding on
    # `## Slide` alone gave it a section running to end of file.
    tail = notes_of("## Slide 1 - T\n\n- **Notes.** make the ask\n\n"
                    "## Open - needs a decision\n\n| # | q |\n| - | - |\n| 1 | something |\n")
    if not (tail[1] == ("T", "make the ask")):
        sys.exit("SELF-TEST FAILED: %r" % (tail,))

    # **The offset case, which is the whole of T-217.** The deck opens with a title slide the
    # specification does not number, so specification slide 1 is the deck's slide 2. Attaching by
    # position puts the note on `Cover`; attaching by title puts it where it was written.
    names = ["Cover", "Two opposite problems", "Nothing here measures it", "Sources"]
    attached, problems = resolve(got, names)
    if not (not problems):
        sys.exit("SELF-TEST FAILED: %r" % (problems,))
    if not (list(attached) == [1]):
        sys.exit("SELF-TEST FAILED: %r" % (attached,))
    if not (attached[1][0] == 1 and attached[1][2].startswith("first note")):
        sys.exit("SELF-TEST FAILED: %r" % (attached,))

    # Punctuation and currency must not break an obvious match.
    money = notes_of("## Slide 9 - \u20ac450k in, \u20ac1.2m a year out\n\n- **Notes.** hold it\n")
    hit, probs = resolve(money, ["x", "450k in, 1.2m a year out"])
    if not (not probs and hit[1][2] == "hold it"):
        sys.exit("SELF-TEST FAILED: %r" % ((hit, probs),))

    # No match and ambiguity both stop the build rather than landing on a neighbour.
    _a, p_none = resolve(money, ["something else"])
    if not (p_none and "matches no slide" in p_none[0]):
        sys.exit("SELF-TEST FAILED: %r" % (p_none,))
    _a, p_many = resolve(money, ["450k in, 1.2m a year out", "450k in 1.2m a year out"])
    if not (p_many and "matches 2 slides" in p_many[0]):
        sys.exit("SELF-TEST FAILED: %r" % (p_many,))

    out = build("<html><body><section class=\"slide\"></section></body></html>", attached)
    # **The safety property, asserted here as well as in the gate.** DS-088's check is this string.
    if not ("speaker-note" in out):
        sys.exit("SELF-TEST FAILED: %s" % ("the artifact must carry the token DS-088 fails on",))
    if not (out.count("</body>") == 1):
        sys.exit("SELF-TEST FAILED: %s" % ("the anchor was duplicated rather than replaced",))
    if not ("first note wrapped over two lines" in out):
        sys.exit("SELF-TEST FAILED: %s" % ("the note did not reach the page",))
    if not ('"2":' in out):
        sys.exit("SELF-TEST FAILED: %s" % ("the note must be keyed by the DECK's index, not the specification's",))

    esc = build("<body></body>", {0: (1, "t", 'push back <b>hard</b> & "concede"')})
    if not ("<b>hard</b>" not in esc):
        sys.exit("SELF-TEST FAILED: %s" % ("note text must be escaped, not injected as markup",))

    if not (slide_count('<section class="slide x"></section><section class="slide"></section>') == 2):
        sys.exit("SELF-TEST FAILED: the assertion did not hold")
    if not (deck_names('<section class="slide" data-name="A"></section>' '<section class="slide" data-name="B"></section>') == ["A", "B"]):
        sys.exit("SELF-TEST FAILED: the assertion did not hold")
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

    names = deck_names(deck_html)
    n_deck = slide_count(deck_html)
    if len(names) != n_deck:
        sys.exit("%d slide(s) in this deck carry no data-name, so they cannot be matched by title"
                 % (n_deck - len(names)))
    attached, problems = resolve(notes, names)
    if problems:
        sys.exit("cannot place %d note(s), and this tool does not guess:\n  %s\n\n"
                 "The deck's slides are:\n  %s\n\n"
                 "A note is attached to the slide whose title it was written under, never to a "
                 "position - the two documents do not always number the same slides."
                 % (len(problems), "\n  ".join(problems),
                    "\n  ".join("%2d  %s" % (i + 1, nm) for i, nm in enumerate(names))))

    out_dir = out_dir or os.path.dirname(os.path.abspath(deck))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir,
                       os.path.splitext(os.path.basename(deck))[0] + "-presenter.html")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write(build(deck_html, attached))

    print("deck:      %s  (%d slides, unchanged)" % (paths.display_path(deck, ROOT), n_deck))
    print("spec:      %s  (%d slide(s) carry a note)"
          % (paths.display_path(spec, ROOT), len(notes)))
    # **Print what was decided, not only how much.** The defect T-217 fixed was invisible because
    # the tool reported a count and never its own choices; a mapping on screen can be read.
    for i in sorted(attached):
        n, title, _t = attached[i]
        print("  spec slide %-3d -> deck slide %-3d  %s" % (n, i + 1, title))
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
