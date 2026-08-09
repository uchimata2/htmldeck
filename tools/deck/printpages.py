#!/usr/bin/env python3
"""The printed page count — the one print check the owner ruled worth automating.

**The failure it catches is silent.** A print stylesheet that does not assert `display` prints
thirteen blank pages (DS-222), and nothing on the presentation list can see that: every rule about
the stage still holds, because the stage is still there — it just did not reach the paper. The page
count is the smallest measurement that makes it loud.

**`n` + 1 for `n` slides**, since [T-034] put a generated contents page in front. The count is what
makes an off-by-one visible in *either* direction: `n` means the contents page never rendered, and
`n` + 2 means the trailing blank page DS-222's corollary removed has come back.

DS-222 to DS-226 themselves are **not** asserted here. The owner's ruling, 2026-08-08: automate the
count and only the count; *disclosure content dropped, slides clip* stays with the print a person
does anyway under CLAUDE.md rule 6. A gate that claimed those five would be claiming a judgement it
cannot make, which is the whole of T-038.

    python tools/deck/printpages.py examples/reference-deck.html 12

Pure standard library (**L-07**) - including the PDF reading, which is a page count and no more.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render                                                       # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT


def print_to_pdf(deck, dest=None):
    """Print the deck through real Chrome, offline, exactly as a reader would. Headers and footers
    off: Chrome's default prints the file's full local path across every page, which is someone
    else's directory layout on paper and is not reachable from CSS."""
    dest = dest or os.path.join(render.OUT, "pagecount.pdf")
    os.makedirs(render.OUT, exist_ok=True)
    if os.path.exists(dest):
        os.remove(dest)
    render.chrome_run(render.file_url(deck), 1280, 800,
                      ["--print-to-pdf=" + dest, "--no-pdf-header-footer"])
    return dest if os.path.exists(dest) else None


def page_count(pdf):
    """Pages in a PDF, read two ways and required to agree.

    The page tree's `/Count` is the document's own answer; counting `/Type /Page` objects is the
    independent one. Chrome writes both uncompressed. **Requiring them to agree is what stops a
    parse that silently found nothing from reading as a count of zero** - and zero would otherwise
    be indistinguishable from a deck that printed nothing at all (L-36).
    """
    data = open(pdf, "rb").read()
    counts = [int(m.group(1)) for m in re.finditer(rb"/Count\s+(\d+)", data)]
    declared = max(counts) if counts else None
    objects = len(re.findall(rb"/Type\s*/Page(?![sA-Za-z])", data))
    return declared, objects


def verdicts(deck, slide_count):
    """`(rule, what, ok)` rows. `PRINT-1` is its own ID rather than a DS number: no rule in the
    ruleset states a page count - §5.4 states the *shape* of the printed artifact, and `n` + 1 is
    the arithmetic that follows from it."""
    if not slide_count:
        return [("PRINT-1", "no slide count to compare against - the render gate produced none",
                 False)]
    pdf = print_to_pdf(deck)
    if not pdf:
        return [("PRINT-1", "Chrome produced no PDF - the print path is unmeasured", False)]
    declared, objects = page_count(pdf)
    want = slide_count + 1
    agree = declared is not None and declared == objects
    return [
        ("PRINT-1", "printed pages: %s declared, %s counted, wanted %d (%d slides + contents)"
         % (declared, objects, want, slide_count),
         agree and declared == want),
    ]


def self_test():
    """A minimal PDF with a known page count, built in memory (**L-04**). If the reader cannot
    count two pages here it cannot be trusted to count thirteen there."""
    fake = (b"%PDF-1.4\n1 0 obj<</Type /Pages /Count 2 /Kids[2 0 R 3 0 R]>>endobj\n"
            b"2 0 obj<</Type /Page /Parent 1 0 R>>endobj\n"
            b"3 0 obj<</Type /Page /Parent 1 0 R>>endobj\n")
    tmp = os.path.join(render.OUT, "_selftest.pdf")
    os.makedirs(render.OUT, exist_ok=True)
    with open(tmp, "wb") as fh:
        fh.write(fake)
    declared, objects = page_count(tmp)
    os.remove(tmp)
    if (declared, objects) != (2, 2):
        sys.exit("SELF-TEST FAILED: a two-page PDF read as %s declared, %s counted"
                 % (declared, objects))
    return True


def main(deck, slides):
    self_test()
    render.self_test()
    print("browser: %s" % render.CHROME)
    print("deck:    %s" % os.path.relpath(deck, ROOT))
    rows = verdicts(deck, slides)
    for rule, what, ok in rows:
        print("  %-8s %-70s %s" % (rule, what, "pass" if ok else "FAIL"))
    print("\nThis is the page COUNT. DS-222 to DS-226 are asserted by printing and looking.")
    return 0 if all(ok for _r, _w, ok in rows) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(main(os.path.abspath(a[0]) if a else os.path.join(
        ROOT, "examples", "reference-deck.html"), int(a[1]) if len(a) > 1 else 12))
