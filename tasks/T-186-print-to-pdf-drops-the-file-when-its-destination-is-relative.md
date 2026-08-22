---
id: T-186
title: print_to_pdf drops the file when its destination is relative, and reports nothing
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-074, T-094, T-123]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-08-19
updated: 2026-08-22
shipped_in: 0.5.0
deliverables: [tools/deck/printpages.py]
---

# T-186 — print_to_pdf drops the file when its destination is relative, and reports nothing

## 1. Specify

**Outcome**
`printpages.print_to_pdf` puts the PDF where the caller asked, whether that path is absolute or
relative, or says why it could not — instead of returning `None` from a run that printed a real PDF
into somebody else's directory.

**The defect, measured**
2026-08-19, while building a print check for
[T-111](T-111-a-named-slide-transition-chosen-per-deck.md):

```
rel deck, abs dest:  C:\...\.assets-cache\t112d\x1.pdf
abs deck, rel dest:  None
```

The deck path is fine either way. **A relative `dest` is the one that fails**, and it fails the way
this repository has seen twice before: `--print-to-pdf=` is handed to Chrome verbatim, Chrome
resolves it against **its own** working directory, and the existence check afterwards looks where
the caller meant. The PDF exists; the function says it does not.

**It is the same defect T-094 fixed, in the module nobody swept.** T-094 found `--screenshot=` doing
exactly this in `render.py` and moved every path resolution into `out_dir` so there would be one
place to keep right. `printpages.print_to_pdf` builds its own destination and was not part of that
change — `os.makedirs` is called on `os.path.abspath(dest)`'s parent, so the *directory* is
resolved and the path handed to Chrome is not. Half of the fix is already in the function.

**Why it is `PH3` and not a `PH1` reopening.** No shipped command can reach it. `printpages.py`'s
own entry point takes a deck and nothing else, and every in-repo caller gets its destination from
`render.out_dir`, which returns an absolute path by T-074's design. It bites a programmatic caller
that passes a relative path — which is how it was found — so no adopter is affected through the
published surface and `../CLAUDE.md`'s rule keeps `PH1` shut.

**Scope**
- In: resolving `dest` where it is built, so Chrome is handed an absolute path.
- In: a fixture that hands the function a relative destination and requires the file back.
- Out: `render.py`. T-094 already fixed it there and the fix held.
- Out: any change to what is printed, to the flags, or to the page count.

**Inputs**
- [`tools/deck/printpages.py`](../tools/deck/printpages.py) — `print_to_pdf`.
- [T-094](T-094-render-py-shots-out-with-a-relative-path-writes-nothing.md) — **the same defect under
  its own name**: *render.py shots --out with a relative path writes nothing*. Same cause, same one-line
  fix, and the reasoning for keeping path resolution in one place.

**Acceptance criteria**
- [ ] A relative destination produces the PDF at that path, relative to the caller's working
      directory
- [ ] An absolute destination behaves exactly as it does today
- [ ] The self-test hands it a relative path and fails if the file does not come back
- [ ] `python tools/check_all.py` green

**Open questions**
- None. The fix is the one T-094 already made next door.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Resolve `dest` once, where it is built | `print_to_pdf` |
| 2 | A fixture that would have caught it | `self_test` |
| 3 | The gate | green |

## 3. Implement

**Decisions & assumptions**
- **One `abspath`, where the destination is built** — 2026-08-19. It was already in the function,
  on the *directory* being created, and the path handed to Chrome went out unresolved beside it.
  Resolving `dest` once at the top makes both correct and leaves one place to keep right, which is
  T-094's reasoning applied to the module it did not reach.
- **The fixture reads the source rather than printing a PDF** — 2026-08-19. `print_to_pdf` needs
  a browser and the self-test runs before every command, so a fixture that printed would put a
  Chrome start in front of every page count. What can be held without one is the line that carries
  the defect: the destination is resolved before it reaches the flag. **Checked against the
  pre-fix source and it fires**, so it is a fixture rather than a comment.

**Measured, before and after** — an absolute deck with a relative destination:

| | returned |
| :--- | :--- |
| before | `None`, from a run that had printed a real PDF into Chrome's working directory |
| after | `C:\...\.assets-cache\t112d\x3.pdf` |

An absolute destination is unchanged, which is every caller in this repository.

**Outputs produced**
- [`tools/deck/printpages.py`](../tools/deck/printpages.py) — `print_to_pdf`'s destination, and the
  fixture.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A relative destination produces the PDF at that path, relative to the caller's working directory | **pass** | §3's table |
| An absolute destination behaves exactly as it does today | **pass** | `abspath` of an absolute path is itself; every in-repo caller passes one and the gate is unchanged |
| The self-test hands it a relative path and fails if the file does not come back | **adapted, and stated** | It holds the *line* rather than the file — a fixture that printed would put a Chrome start in front of every page count, and the self-test runs before every command. Verified to fire against the pre-fix source, so it is not a fixture that has only ever passed |
| `python tools/check_all.py` green | **pass** | |

**Child fix tasks raised**
- none.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **`shipped_in` set to `0.5.0`, back-filled.** The field was never written, so this task read as belonging to no release while being closed. **Derived, not assumed**: the commit that set `status: done` is an ancestor of `v0.5.0`, which `git tag --contains` answers. Found while reading the unreleased set for `0.6.0` — eight tasks closed 2026-08-19 all carried an empty field, and a ninth ([T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md)) closed after the tag and belonged to `0.6.0` instead. |
| 2026-08-19 | → proposed | Found while building [T-111](T-111-a-named-slide-transition-chosen-per-deck.md)'s print check, which handed the function a relative destination and got `None` from a run that had printed a real PDF. Raised rather than fixed in place because this project's method has no work without a task file, and closed in the same session under the owner's standing instruction — it needs no ruling and reaches no shipped command. |
| 2026-08-19 | → done | One `abspath`, where the destination is built. The function already had one on the directory it creates and handed Chrome the unresolved path beside it — **T-094's defect in the module that change did not sweep**. The fixture reads the source rather than printing, because the self-test runs before every command and a print there would cost a browser start every time; it was checked against the pre-fix source and fires. |
