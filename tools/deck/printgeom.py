#!/usr/bin/env python3
"""The printed *geometry* of the contents sheet - the one fault class no screen measurement reaches.

**Why this exists at all.** `contents_bound.py` measures the printed contents page by lifting the
deck's own `@media print` rules onto screen through the CSSOM. That is careful and it is still a
different surface: on the same deck on the same day it read a +26.0 du gap where the paper had
-49.2 pt, and reported clean while rows printed through each other (T-116, **L-76**). The fault
reached three printed decks - this repository's reference deck, and two built elsewhere - with every
gate green throughout. Chrome's paged layout gives a grid item its own content height rather than its
track, and no screen reading can see that, whatever the fixture holds.

**What it asserts, and nothing wider.** The owner's ruling, 2026-08-13: *no card overlaps another and
none reaches the footnote*. Both are a `>` between numbers. DS-222 to DS-226 as **judgements** stay
with the person who prints under CLAUDE.md rule 6, which is the 2026-08-08 ruling in T-038 and is
untouched here - this narrows that ruling only where the property is arithmetic.

**Contents sheets only.** A naive *do any two drawn boxes intersect* over a whole deck reports a
collision on any slide carrying a decision diamond: the diamond's bounding box overlaps its
neighbour's while nothing visually touches. The subject here is siblings in one grid, which is what
makes plain rectangle intersection the right test rather than a nuisance.

    python tools/deck/printgeom.py examples/reference-deck.html

Pure standard library (**L-07**), including the PDF reading. The reader is a graphics-state stack and
a bounding box: Chrome draws the rounded cards as beziers rather than `re`, and nests `q`/`cm` two
deep, so a reader that ignores the nesting returns coordinates in the tens of thousands. That is the
whole of the cost, and it is why no dependency was taken for a gate an adopter has to be able to run.
"""

import os
import re
import sys
import tempfile
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import printpages                                                   # noqa: E402
import render                                                       # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT

# Two rectangles that share a hairline are not a collision. The stroked outline and the clip path of
# one card already differ by 0.3 pt, and the gaps this is looking for are tens of points, so the
# tolerance costs nothing and stops float noise reading as a defect.
EPS = 0.5

# A card outline is a large stroked path. The thresholds exclude rules and dividers - a footnote rule
# is a stroked path too, and it is a few points tall.
MIN_W, MIN_H = 60.0, 30.0


# --- the PDF ---------------------------------------------------------------------------------

def objects(data):
    """`{number: body}` for every indirect object. Chrome writes them one per line at column 0."""
    out = {}
    for m in re.finditer(rb"(?m)^(\d+)\s+0\s+obj\b", data):
        end = data.find(b"endobj", m.end())
        out[int(m.group(1))] = data[m.end():end]
    return out


def stream_of(obj):
    """An object's stream, inflated if it carries one. Chrome Flate-compresses content streams -
    `zlib` is standard library, so this costs nothing."""
    m = re.search(rb"stream\r?\n", obj)
    if not m:
        return None
    raw = obj[m.end():obj.rfind(b"endstream")]
    return zlib.decompress(raw) if b"FlateDecode" in obj[:m.start()] else raw


def page_order(OBJ, data):
    """Page object numbers in **document** order, walked from the catalogue.

    Not scanned for in file order, and not read off the first `/Kids` array: the page tree is
    nested, and the first array on this repository's own printed deck holds 8 of its 14 pages. A
    reader that took that array would measure the wrong sheet and say nothing about it.
    """
    root = re.search(rb"/Root\s+(\d+)\s+0\s+R", data)
    if not root:
        return []
    cat = OBJ.get(int(root.group(1)), b"")
    top = re.search(rb"/Pages\s+(\d+)\s+0\s+R", cat)
    if not top:
        return []
    order = []

    def walk(num, seen):
        if num in seen or num not in OBJ:
            return
        seen.add(num)
        body = OBJ[num]
        if re.search(rb"/Type\s*/Page(?![sA-Za-z])", body):
            order.append(num)
            return
        kids = re.search(rb"/Kids\s*\[(.*?)\]", body, re.S)
        if kids:
            for k in re.findall(rb"(\d+)\s+0\s+R", kids.group(1)):
                walk(int(k), seen)

    walk(int(top.group(1)), set())
    return order


# --- the content stream ----------------------------------------------------------------------

NUM = rb"[-+]?(?:\d+\.?\d*|\.\d+)"
TOK = re.compile(rb"(%s)|/([^\s/<>\[\]()]+)|(<[0-9A-Fa-f]*>)|\((?:[^()\\]|\\.)*\)|([A-Za-z'\"*]+)"
                 % NUM)


def mul(a, b):
    """Matrix `a` concatenated onto `b`, both in PDF's six-number form."""
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]


def apply(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


PAINT = ("f", "f*", "F", "S", "s", "B", "B*", "b", "b*", "n")


def read_page(stream, height):
    """`(paths, texts)` for one page, in **page points measured down from the top**.

    `paths` are `(x0, top, x1, bottom, op)`; `texts` are `(x, baseline, size)` in paint order.

    The y flip is done here rather than left to callers because every number this module compares is
    a distance down a printed sheet, and two conventions in one file is how a sign error survives.
    """
    ctm = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    stack, nums, pts = [], [], []
    out, texts = [], []
    size = 0.0

    def down(y):
        return height - y

    for m in TOK.finditer(stream):
        num, _name, _hexs, op = m.groups()
        if num is not None:
            nums.append(float(num))
            continue
        if op is None:                       # a name, a hex string or a literal string
            continue
        o = op.decode("latin-1")
        if o == "q":
            stack.append(list(ctm))
        elif o == "Q":
            if stack:
                ctm = stack.pop()
        elif o == "cm" and len(nums) >= 6:
            ctm = mul(nums[-6:], ctm)
        elif o == "Tf" and nums:
            size = nums[-1]
        elif o == "Tm" and len(nums) >= 6:
            tm = mul(nums[-6:], ctm)
            # The text matrix carries the flip Chrome applies to every run, so the glyph size on
            # paper is the nominal size scaled by |d| - not the `Tf` operand on its own.
            texts.append((tm[4], down(tm[5]), abs(tm[3]) * size))
        elif o == "m" and len(nums) >= 2:
            pts.append(apply(ctm, nums[-2], nums[-1]))
        elif o == "l" and len(nums) >= 2:
            pts.append(apply(ctm, nums[-2], nums[-1]))
        elif o == "c" and len(nums) >= 6:
            # Both control points as well as the end point. For a rounded rectangle every control
            # point lies inside the corner it turns, so the hull is the box - which is the quantity
            # wanted, and it needs no bezier evaluation.
            for i in (0, 2, 4):
                pts.append(apply(ctm, nums[-6 + i], nums[-5 + i]))
        elif o in ("v", "y") and len(nums) >= 4:
            for i in (0, 2):
                pts.append(apply(ctm, nums[-4 + i], nums[-3 + i]))
        elif o == "re" and len(nums) >= 4:
            x, y, w, h = nums[-4:]
            for cx, cy in ((x, y), (x + w, y), (x + w, y + h), (x, y + h)):
                pts.append(apply(ctm, cx, cy))
        elif o in PAINT:
            if pts:
                xs = [p[0] for p in pts]
                ys = [down(p[1]) for p in pts]
                out.append((min(xs), min(ys), max(xs), max(ys), o))
            pts = []
        nums = []
    return out, texts


def sheet_geometry(pdf, sheet_index):
    """`(cards, footnote, problem)` for one printed contents sheet, counting from 1.

    `cards` are `(x0, top, x1, bottom)` in reading order. `footnote` is `(top, bottom)` or `None`.
    """
    data = open(pdf, "rb").read()
    OBJ = objects(data)
    order = page_order(OBJ, data)
    if len(order) < sheet_index:
        return None, None, ("the PDF has %d pages, so there is no sheet %d to read"
                            % (len(order), sheet_index))
    body = OBJ[order[sheet_index - 1]]
    mb = re.search(rb"/MediaBox\s*\[([^\]]*)\]", body)
    cs = re.search(rb"/Contents\s+(\d+)\s+0\s+R", body)
    if not mb or not cs:
        return None, None, "sheet %d declares no MediaBox or no content stream" % sheet_index
    height = float(mb.group(1).split()[3])
    stream = stream_of(OBJ.get(int(cs.group(1)), b""))
    if not stream:
        return None, None, "sheet %d's content stream did not inflate" % sheet_index

    drawn, texts = read_page(stream, height)
    cards = [(x0, t, x1, b) for x0, t, x1, b, op in drawn
             if op in ("S", "s", "B", "B*", "b", "b*")
             and (x1 - x0) > MIN_W and (b - t) > MIN_H]
    cards.sort(key=lambda c: (round(c[1], 1), c[0]))

    # **The footnote is the last text run painted, not the lowest one.** Paint order follows DOM
    # order and the deck appends `.contents-foot` after the grid, so the last run is the footnote by
    # construction. Taking the lowest instead would pick a card's own description on exactly the
    # broken page this gate exists for - the card that has overflowed its row is the one printing
    # text furthest down.
    foot = None
    if texts:
        _x, base, size = texts[-1]
        foot = (base - size, base)
    return cards, foot, None


# --- what the deck says the sheet holds --------------------------------------------------------

SHEET_PROBE = r"""
<script>
(function(){
  function run(){
    var out = [];
    var sheets = document.querySelectorAll('main.stage > section.contents');
    for (var i = 0; i < sheets.length; i++){
      out.push({cards: sheets[i].querySelectorAll('.cbox').length,
                feet: sheets[i].querySelectorAll('.contents-foot').length});
    }
    document.title = 'RESULT' + JSON.stringify({sheets: out}) + 'ENDRESULT';
  }
  if (document.readyState === 'complete') run();
  else window.addEventListener('load', run);
})();
</script>
"""


def expected_sheets(deck):
    """`(rows, problem)` - what each contents sheet carries, asked of the deck.

    **Never recomputed here.** The split rule lives in the deck and a copy of it in this file would
    agree until the day one of them changed, which is the day this gate exists to notice (**L-08**,
    and the same rule `printpages.py` follows for `k`).
    """
    probe = render.make_probe(deck, name="printgeom-sheets-probe.html", extra=SHEET_PROBE)
    data, err = render.read_result(render.file_url(probe), 1280, 800)
    if not data:
        return None, "the deck did not report its contents sheets\n%s" % err[:300]
    rows = data.get("sheets") or []
    if not rows:
        return None, "the deck builds no contents sheet - there is no printed geometry to read"
    return rows, None


# --- the verdicts ------------------------------------------------------------------------------

def sheet_problem(index, found, declared):
    """Why sheet `index` cannot be judged, or `None`.

    **A reader that found nothing must not report no overlaps.** This is `printpages.py`'s two-way
    page count one level up (**L-36**): the deck's own card count is the independent answer, and a
    disagreement is a failure of this gate rather than a clean deck. It is a function of its own so
    the self-test can put a wrong number in front of it without launching a browser.
    """
    if found != declared:
        return ("sheet %d: read %d card outline%s, the deck says it carries %d"
                % (index, found, "" if found == 1 else "s", declared))
    return None


def overlaps(a, b):
    """Do two card rectangles intersect, by more than a hairline, in both directions?"""
    return (min(a[2], b[2]) - max(a[0], b[0]) > EPS and
            min(a[3], b[3]) - max(a[1], b[1]) > EPS)


def verdicts(deck, pdf=None):
    """`(rule, what, ok)` rows.

    `PRINT-2` and `PRINT-3` are their own IDs rather than DS numbers, for the reason `PRINT-1` is:
    no rule in the ruleset states a coordinate. DS-226 states the contents page's shape, and *cards
    do not overlap* is the arithmetic that follows from it.
    """
    if not deck:
        return [("PRINT-2", "no deck to print - the geometry gate has no subject", False),
                ("PRINT-3", "no deck to print - the geometry gate has no subject", False)]

    sheets, problem = expected_sheets(deck)
    if problem:
        return [("PRINT-2", problem, False), ("PRINT-3", problem, False)]

    pdf = pdf or printpages.print_to_pdf(
        deck, os.path.join(render.out_dir(deck), "printgeom.pdf"))
    if not pdf:
        return [("PRINT-2", "Chrome produced no PDF - the printed geometry is unmeasured", False),
                ("PRINT-3", "Chrome produced no PDF - the printed geometry is unmeasured", False)]

    collisions, reaches, unread, footless = [], [], [], []
    for i, want in enumerate(sheets, start=1):
        cards, foot, problem = sheet_geometry(pdf, i)
        if problem:
            unread.append("sheet %d: %s" % (i, problem))
            continue
        problem = sheet_problem(i, len(cards), want["cards"])
        if problem:
            unread.append(problem)
            continue
        for a in range(len(cards)):
            for b in range(a + 1, len(cards)):
                if overlaps(cards[a], cards[b]):
                    collisions.append("sheet %d: cards %d and %d intersect (%.1f-%.1f pt and "
                                      "%.1f-%.1f pt)" % (i, a + 1, b + 1, cards[a][1], cards[a][3],
                                                         cards[b][1], cards[b][3]))
        if want["feet"] and not foot:
            # The deck says this sheet carries a footnote and the reader found none. Passing
            # here would report *every card ends above it* about a line nothing measured -
            # `sheet_problem` refuses the same shape one condition up (`PR-60`).
            unread.append("sheet %d: a footnote is declared and none was read" % i)
            continue
        if not want["feet"]:
            footless.append(i)
        if foot and want["feet"]:
            for n, c in enumerate(cards, start=1):
                if c[3] > foot[0] + EPS:
                    reaches.append("sheet %d: card %d ends at %.1f pt, the footnote starts at "
                                   "%.1f pt" % (i, n, c[3], foot[0]))

    if unread:
        why = "the printed sheets could not be read: " + "; ".join(unread)
        return [("PRINT-2", why, False), ("PRINT-3", why, False)]

    # **A truncated list says how long it is.** Three named pairs out of four reads as four faults
    # fixed once three are, and the seeded run this was measured against had exactly that shape.
    def some(items, clean):
        if not items:
            return clean
        head = "; ".join(items[:3])
        return head if len(items) <= 3 else "%d found, first three: %s" % (len(items), head)

    n = sum(s["cards"] for s in sheets)
    return [
        ("PRINT-2", "printed contents cards: %d over %d sheet%s, %s"
                    % (n, len(sheets), "" if len(sheets) == 1 else "s",
                       some(collisions, "no two intersect")),
         not collisions),
        ("PRINT-3", "footnote clearance: %s%s"
                    % (some(reaches, "every card ends above it"),
                       "" if not footless else " (%d sheet%s declare none)"
                       % (len(footless), "" if len(footless) == 1 else "s")),
         not reaches),
    ]


# --- self-test ----------------------------------------------------------------------------------

def _fixture(second_y):
    """A one-page PDF with two rectangles and one text run, built in memory (**L-04**).

    Deliberately not built out of anything in the repository: a fixture assembled from a tracked
    file's current contents blocks the commit that changes that file, which is a self-test asserting
    repository state rather than tool behaviour.

    The page is 200 pt tall. Card A occupies y 20-60 from the top; card B starts at `second_y`. The
    text run sits at the bottom and stands in for the footnote.
    """
    content = ("1 0 0 -1 0 200 cm\n"
               "10 20 100 40 re S\n"
               "10 %g 100 40 re S\n"
               "BT /F1 10 Tf 1 0 0 -1 10 190 Tm (x) Tj ET\n" % second_y).encode("latin-1")
    body = (b"%PDF-1.4\n"
            b"1 0 obj<</Type /Catalog /Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type /Pages /Count 1 /Kids[3 0 R]>>endobj\n"
            b"3 0 obj<</Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] "
            b"/Contents 4 0 R>>endobj\n"
            b"4 0 obj<</Length " + str(len(content)).encode() + b">>stream\n" + content +
            b"\nendstream endobj\n"
            # The trailer is not decoration. `page_order` starts at `/Root`, so a fixture without
            # one reads as a nought-page document - which is exactly what the first run of this
            # self-test reported, and it is the failure mode L-36 is about.
            b"trailer<</Size 5 /Root 1 0 R>>\n%%EOF\n")
    fd, tmp = tempfile.mkstemp(prefix="htmldeck-printgeom-", suffix=".pdf")
    with os.fdopen(fd, "wb") as fh:
        fh.write(body)
    return tmp


def self_test():
    """Read a clean fixture and a colliding one, and require **different** answers.

    A reader is only trusted here if it says no to a page that is wrong, so both directions are
    measured rather than the correct one alone (**L-05**). One fixture proves a parser runs; two
    prove it decides.
    """
    for second_y, want_cards, want_hit in ((80.0, 2, False), (40.0, 2, True)):
        tmp = _fixture(second_y)
        cards, foot, problem = sheet_geometry(tmp, 1)
        os.remove(tmp)
        if problem:
            sys.exit("SELF-TEST FAILED: the in-memory fixture did not read - %s" % problem)
        if len(cards) != want_cards:
            sys.exit("SELF-TEST FAILED: read %d card outlines from a fixture holding %d"
                     % (len(cards), want_cards))
        hit = any(overlaps(cards[a], cards[b])
                  for a in range(len(cards)) for b in range(a + 1, len(cards)))
        if hit != want_hit:
            sys.exit("SELF-TEST FAILED: two cards %g pt apart reported overlap=%s, wanted %s - a "
                     "reader that cannot tell the two apart cannot gate either"
                     % (second_y - 60.0, hit, want_hit))
        if not foot:
            sys.exit("SELF-TEST FAILED: the fixture's text run was not found, so no footnote band "
                     "would ever be located on a real sheet")

    # The count guard, put in front of a wrong number directly. Without this the branch that stops a
    # reader passing a page it never read is the one branch nothing exercises - which is the shape of
    # defect it exists to prevent.
    if sheet_problem(1, 2, 2) is not None:
        sys.exit("SELF-TEST FAILED: two cards read against two declared reported a problem")
    if sheet_problem(1, 0, 13) is None:
        sys.exit("SELF-TEST FAILED: nought cards read against thirteen declared reported no "
                 "problem - a reader that found nothing would report a clean page")
    return True


def main(deck):
    self_test()
    render.self_test()
    print("browser: %s" % render.CHROME)
    print("deck:    %s" % paths.display_path(deck, ROOT))
    rows = verdicts(deck)
    for rule, what, ok in rows:
        print("  %-8s %-70s %s" % (rule, what, "pass" if ok else "FAIL"))
    print("\nThis is the printed GEOMETRY. DS-222 to DS-226 as judgements are still asserted by "
          "printing and looking.")
    return 0 if all(ok for _r, _w, ok in rows) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(main(os.path.abspath(a[0]) if a else os.path.join(
        ROOT, "examples", "reference-deck.html")))
