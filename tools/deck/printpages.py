#!/usr/bin/env python3
"""The printed page count — the one print check the owner ruled worth automating.

**The failure it catches is silent.** A print stylesheet that does not assert `display` prints
thirteen blank pages (DS-222), and nothing on the presentation list can see that: every rule about
the stage still holds, because the stage is still there — it just did not reach the paper. The page
count is the smallest measurement that makes it loud.

**`n` + `k` for `n` slides and `k` contents sheets**, since [T-034] put a generated contents page in
front and [T-036] let it continue onto further sheets past 16 entries. The count is what makes an
off-by-one visible in *either* direction: `n` means the contents page never rendered, and one more
than expected means the trailing blank page DS-222's corollary removed has come back.

**`k` is read out of the deck's own DOM, never recomputed here** - the same rule as the slide count
below it (T-120, **L-08**). A copy of the split rule in this file would agree with the deck until
the day one of them changed, and the check exists to notice exactly that kind of day. `k` is 1 for
every deck at or under the bound, which is every deck this repository ships.

DS-222 to DS-226 themselves are **not** asserted here. The owner's ruling, 2026-08-08: automate the
count and only the count; *disclosure content dropped, slides clip* stays with the print a person
does anyway under CLAUDE.md rule 6. A gate that claimed those five would be claiming a judgement it
cannot make, which is the whole of T-038.

    python tools/deck/printpages.py examples/reference-deck.html

Pure standard library (**L-07**) - including the PDF reading, which is a page count and no more.
"""

import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths                                                        # noqa: E402
import render                                                       # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = render.ROOT


def print_to_pdf(deck, dest=None):
    """Print the deck through real Chrome, offline, exactly as a reader would. Headers and footers
    off: Chrome's default prints the file's full local path across every page, which is someone
    else's directory layout on paper and is not reachable from CSS."""
    # The deck's project, not this tool's - see `paths.output_root` and T-074.
    out = render.out_dir(deck)
    dest = dest or os.path.join(out, "pagecount.pdf")
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or out, exist_ok=True)
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


SHEET_PROBE = r"""
<script>
(function(){
  function run(){
    var n = document.querySelectorAll('main.stage > section.contents').length;
    document.title = 'RESULT' + JSON.stringify({sheets:n}) + 'ENDRESULT';
  }
  if (document.readyState === 'complete') run();
  else window.addEventListener('load', run);
})();
</script>
"""


def sheet_count(deck):
    """`(k, problem)` - how many contents sheets the deck builds, counted in its own DOM.

    The sheets are generated at start-up, so a file scan cannot see them; this asks the deck. Zero
    is a problem rather than an answer: a deck that builds no contents page would otherwise make
    `n` + 0 the expectation and pass while missing the page this check exists for."""
    probe = render.make_probe(deck, name="pagecount-sheets-probe.html", extra=SHEET_PROBE)
    data, err = render.read_result(render.file_url(probe), 1280, 800)
    if not data:
        return None, "the deck did not report a contents-sheet count\n%s" % err[:300]
    k = data.get("sheets")
    if not k:
        return None, "the deck builds no contents sheet - there is no `n` + k to compare against"
    return k, None


def verdicts(deck, slide_count):
    """`(rule, what, ok)` rows. `PRINT-1` is its own ID rather than a DS number: no rule in the
    ruleset states a page count - §5.4 states the *shape* of the printed artifact, and `n` + `k` is
    the arithmetic that follows from it."""
    if not slide_count:
        return [("PRINT-1", "no slide count to compare against - the render gate produced none",
                 False)]
    sheets, problem = sheet_count(deck)
    if problem:
        return [("PRINT-1", problem, False)]
    pdf = print_to_pdf(deck)
    if not pdf:
        return [("PRINT-1", "Chrome produced no PDF - the print path is unmeasured", False)]
    declared, objects = page_count(pdf)
    want = slide_count + sheets
    agree = declared is not None and declared == objects
    return [
        ("PRINT-1", "printed pages: %s declared, %s counted, wanted %d (%d slides + %d contents "
                    "sheet%s)" % (declared, objects, want, slide_count, sheets,
                                  "" if sheets == 1 else "s"),
         agree and declared == want),
    ]


def self_test():
    """A minimal PDF with a known page count, built in memory (**L-04**). If the reader cannot
    count two pages here it cannot be trusted to count thirteen there."""
    fake = (b"%PDF-1.4\n1 0 obj<</Type /Pages /Count 2 /Kids[2 0 R 3 0 R]>>endobj\n"
            b"2 0 obj<</Type /Page /Parent 1 0 R>>endobj\n"
            b"3 0 obj<</Type /Page /Parent 1 0 R>>endobj\n")
    # A temporary file, in the place the platform keeps temporary files. It used to be written
    # under the tool's own directory, which is the installed package once htmldeck is a plugin -
    # and a self-test that writes into its own install fails on any read-only one (T-074).
    fd, tmp = tempfile.mkstemp(prefix="htmldeck-pagecount-", suffix=".pdf")
    with os.fdopen(fd, "wb") as fh:
        fh.write(fake)
    declared, objects = page_count(tmp)
    os.remove(tmp)
    if (declared, objects) != (2, 2):
        sys.exit("SELF-TEST FAILED: a two-page PDF read as %s declared, %s counted"
                 % (declared, objects))
    return True


def main(deck):
    self_test()
    render.self_test()
    # Derived from the deck, never passed in and never defaulted (T-120). It used to be
    # `int(a[1]) if len(a) > 1 else 12` - a stored copy of a fact the file states (**L-08**) - and it
    # went wrong the day the reference deck gained its colophon: this entry point reported FAIL on a
    # deck printing 14 correct pages while `check.py`, calling `verdicts` with a rendered count,
    # reported pass on the same file. Two callers, one number, and only one of them was reading it.
    #
    # The override argument went with the constant rather than being kept. Its only purpose was to
    # correct the constant by hand, and an override is a second way to be wrong about something the
    # deck already says.
    slides = render.slide_count(deck)
    print("browser: %s" % render.CHROME)
    print("deck:    %s" % paths.display_path(deck, ROOT))
    print("slides:  %d, counted in the deck" % slides)
    rows = verdicts(deck, slides)
    for rule, what, ok in rows:
        print("  %-8s %-70s %s" % (rule, what, "pass" if ok else "FAIL"))
    print("\nThis is the page COUNT. DS-222 to DS-226 are asserted by printing and looking.")
    return 0 if all(ok for _r, _w, ok in rows) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(main(os.path.abspath(a[0]) if a else os.path.join(
        ROOT, "examples", "reference-deck.html")))
