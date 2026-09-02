---
id: T-229
title: Derive DS-106's banned-terminology list from the rule instead of restating it
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-229 — Derive DS-106's banned-terminology list from the rule instead of restating it

## 1. Specify

**Outcome**
No word DS-106's own sentence bans is missing from the check that decides it. Today `audit.ds106_no_banned_terminology` matches ten words and **`actually` is not among them**, while the rule names it - so `examples/measure-first/` uses it three times in slide copy and `examples/reference-deck.html` once, and both pass a `hard` rule the gate reports as checked.

**Closes** `PR-48` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the four instances in two shipped decks
- In: **deriving the fallback list from the rule's own row**, which is the register's hypothesis and is against the obvious fix: adding one word closes the instance and leaves the class, because the list is written twice and nothing compares them
- Out: the four categories DS-106 names that no check implements - that is DS-107's, and a category nobody has built is a different thing from a word the rule wrote down

**Inputs**
- `PR-48` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) DS-106 and DS-107
- `tools/deck/ruleset.py` - the precedent for deriving from a row

**Acceptance criteria**
- [ ] every word DS-106's sentence names is decided by the check, proved by seeding each
- [ ] the four instances are gone from both decks and the decks rebuild
- [ ] `python tools/check_all.py` green

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Count the instances the check would see before changing anything | **Not three and one.** `actually` appears **8** times in the reference deck and **9** in `measure-first` — and **7** of each are the shell's own CSS, script and HTML comments, present in every deck |
| 2 | Follow that where it leads: the subject is wrong before the list is | `copy_of()` — quick views, stylesheets, scripts and HTML comments cut. Adding the missing word without this would have failed **all five** tracked decks |
| 3 | Derive the list from DS-106's row rather than restating it | `banned_terms()` and `banned_pattern()`; **13** terms where the regex had 10 |
| 4 | Reconcile the two lists in both directions | `actually` was in the row and not the check; **`delve` was in the check and named by nothing**, so it is written into the row rather than dropped |
| 5 | Keep the reach the regex had. `synerg\w*` catches `synergies` and `\bsynergy\w*` does not | A single word matches from its **stem** — the word less a trailing `y` or `e` — which also gives `leveraging` and `delving`, and still does not reach `actual` |
| 6 | Seed every derived term and watch the check fire; seed each cut place and watch it stay quiet | Eight assertions in `audit.self_test`, including that the row must still name `actually` |
| 7 | Remove the three real instances and rebuild what derives from those decks | Reference deck ×1, `measure-first` ×2 and its spec; `seed_defects.py` and `presenter.py` re-run |

## 3. Implement

**Decisions & assumptions**
- **The subject was wrong before the list was, and that is the finding the register could not see.** 2026-08-29. The row predicted that adding one word would close the instance and leave the class. It was right and the class is bigger than it looked: the check read the **whole file**, so seven instances per deck came from `components.css`, `deck.js` and `shell.html`, which argue their own decisions in prose and are embedded in every deck. Adding `actually` alone would have failed all five tracked decks for words nobody wrote as copy — the obvious fix, one layer further down.
- **`delve` moves into the rule rather than out of the check.** 2026-08-29. Deriving strictly would have dropped it: it was matched by the check and named by nothing. A word worth catching belongs in the sentence that bans it.
- **The stem rule is the smallest one that keeps what the regex had.** 2026-08-29. `synerg\w*` catches `synergies`; `\bsynergy\w*` does not, because the inflection drops the `y`. Stripping a trailing `y` or `e` recovers it and gives `leverage` → `leveraging` and `delve` → `delving` for nothing. **It is deliberately not a stemmer**, and an inflection it misses is a term the row can name outright.
- **The italics in DS-106's row are the list, and the row says so.** 2026-08-29. A span carrying markup or running past six words is skipped, so an italicised aside does not silently become a banned word — which was measured rather than assumed: the first draft of this task's own amendment put `*synergy*` in the row's prose and it was parsed as a term.
- **The instance count in `PR-48` is corrected on the row.** `measure-first` had two in slide copy, not three; the third was the shell's prose. The register's figure is annotated where it sits rather than restated.
- **A look was owed, and it has been taken.** One SVG label changed from two lines to one — `What` / `actually sold` became `What sold` at the midpoint of the two — on `measure-first` **slide 4**, *The loop that never closes*, the four-node cycle diagram. Every measurement was green, including `figgrid`, `markhits` and `spec.py`, and none of them could decide whether the single line reads as well as the pair. **The owner looked on 2026-08-29 and confirmed it reads correctly.** Recorded in [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md). *This entry first said slide 7, which was neither the reader's number nor the element index — a position written from context rather than derived. Counting `<section>` elements gives 5, because the deck opens with a lobby and front matter is counted in no stage; the slide's `data-name` is the identifier that cannot be off by one.*

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `copy_of()`, `banned_terms()`, `banned_pattern()`, the DS-100 and DS-106 checks, and the self-test block
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-106` row: `delve`, and what the list and the subject are
- [`examples/reference-deck.html`](../examples/reference-deck.html), [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) and its `.slides.md` — the three instances
- [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html) — regenerated from the reference deck
- [`examples/README.md`](../examples/README.md) — both decks' byte figures re-derived, which `figures.py` caught: removing nine characters of copy from one deck and eighty-nine from another moves a number two documents quote
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-48` closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every word DS-106's sentence names is decided by the check, proved by seeding each | pass | Thirteen terms derived from the row and each seeded into copy in `audit.self_test`; the fixture also refuses a row that stops naming `actually`. Four negative cases prove the subject: a stylesheet comment, a script comment, an HTML comment and a quoted source each carry a banned word and none fires |
| The four instances are gone from both decks and the decks rebuild | pass | **Three, not four** — the register counted one of the shell's comments as slide copy. All three removed; `spec.py` green on `measure-first`, and the seeded-defect and presenter builds regenerated |
| `python tools/check_all.py` green | pass | Run at the end of B7, on a tree nothing was editing |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
| 2026-08-29 | → done | Batch **B7**. The list is derived from DS-106's own row and the subject is the deck's copy. **The register's hypothesis was right and its instance count was not**: seven of the eight hits per deck were the shell's own comments, so adding the missing word alone would have failed all five tracked decks. |
