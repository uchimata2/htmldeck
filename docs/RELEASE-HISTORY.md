# Release history — htmldeck

**What shipped when, which release carried which fix, and which task found which defect.** Dated
narrative, in date order, kept because a project that cannot say when a rule started binding cannot
tell a regression from a decision.

**Tier 3. Nothing loads this document.** No skill, workflow or instruction file pulls it in, and
none should: it is read when somebody asks a question about the past, which is rarely, and it grows
by a paragraph per release. It was [`../CLAUDE.md`](../CLAUDE.md)'s *What this is* section until
2026-08-14, where it was **6,980 of 15,630 bytes — 45% of a file paid for on every turn of every
session** — measured at the context audit on 2026-08-13, moved here by
[T-143](../tasks/T-143-split-the-release-chronology-out-of-claude-md.md) for finding `CE-01`
([`CONTEXT-AUDIT.md`](CONTEXT-AUDIT.md) §6).

**Where the boundary falls against the other three release documents.** Four documents touch
releases and each answers a different question. Nothing here is copied from the other three; where
they already hold a fact, this document points.

| Question | Document |
| :--- | :--- |
| **What shipped when, and which task found which defect** | this document |
| Which release phase a task belongs to, and why | [`RELEASE-PHASES.md`](RELEASE-PHASES.md) — one row per task |
| What a release newly requires of an adopter's deck | [`PUBLISHING.md`](PUBLISHING.md) §8.1 |
| The steps of a release, in order | [`PUBLISHING.md`](PUBLISHING.md) §8 |

**The rules that were embedded in this narrative stayed in tier 1.** A paragraph written over time
carries real rules, and a section moved wholesale takes them out of the file that binds. T-143 §1
lists all fourteen and where each ended.

---

## 1. What shipped when

**Eleven releases over six days.** The authority is `shipped_in` on each task, and the two counted
columns below are derived from it rather than kept by hand — re-derive them, do not trust these:

```bash
git for-each-ref --sort=creatordate --format='%(refname:short) %(creatordate:short)' refs/tags
grep -h "^shipped_in:" tasks/*.md | sort | uniq -c
```

**The third column is not the second.** `0.2.1` is remembered for three defect fixes and carries ten
tasks; a patch release closes whatever was open, and only some of it is what the release was *for*.
Counted 2026-08-14.

| Version | Date | Tasks | What it is remembered for |
| :--- | :--- | ---: | :--- |
| `0.1.0` | 2026-08-09 | 50 | **PH1** — a working plugin someone can install. The repository went public at `github.com/uchimata2/htmldeck` the same day |
| `0.1.1` | 2026-08-09 | 2 | [T-061](../tasks/T-061-the-scaffold-check-passed-a-manifest-the-installer-rejects.md) — `0.1.0` did not install at all. The first release anyone could use |
| `0.1.2` | 2026-08-10 | 4 | [T-064](../tasks/T-064-the-tools-crash-when-the-deck-is-on-another-drive.md) — every tool crashed on a deck held on another drive |
| `0.1.3` | 2026-08-10 | 1 | [T-066](../tasks/T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md). The adopting project returned two defects against it |
| `0.1.4` | 2026-08-10 | 6 | The release after which [`PUBLISHING.md`](PUBLISHING.md) §8 was written down: four releases had each re-derived the same sequence from the last one's commits |
| `0.1.5` | 2026-08-10 | 12 | [T-083](../tasks/T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md) and [T-085](../tasks/T-085-the-reference-deck-does-not-carry-the-shell-it-defines.md) — **the first patch nobody reported.** Both were found by running §8's gate list rather than by an adopter, which is the argument for having written that list down |
| `0.2.0` | 2026-08-11 | 4 | **PH2** — [T-086](../tasks/T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md) and [T-087](../tasks/T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md) |
| `0.2.1` | 2026-08-11 | 10 | Three defect fixes: [T-090](../tasks/T-090-spec5-cannot-parse-a-descriptive-slide-label.md), [T-091](../tasks/T-091-build-md-documents-icons-set-as-a-single-pair.md), [T-094](../tasks/T-094-render-py-shots-out-with-a-relative-path-writes-nothing.md) |
| `0.2.2` | 2026-08-12 | 8 | Four defect fixes, all four from the adopting project: [T-101](../tasks/T-101-theme-py-self-test-fails-for-every-plugin-install.md), [T-102](../tasks/T-102-data-stage-is-an-index-and-the-contract-does-not-say-so.md), [T-103](../tasks/T-103-build-md-drops-ds-105s-link-clause-for-a-single-source-slide.md), [T-105](../tasks/T-105-fig-pos-neg-caution-are-vocabulary-so-a-real-deck-fails-for-using-them.md) |
| `0.2.3` | 2026-08-13 | 8 | Three defect fixes: [T-116](../tasks/T-116-the-printed-contents-page-collides-at-thirteen-entries.md), [T-108](../tasks/T-108-a-deck-has-no-back-matter-stage-so-the-colophon-is-labelled-with-the-last-argument-stage.md), [T-120](../tasks/T-120-printpages-standalone-defaults-the-slide-count-to-a-hardcoded-twelve.md) |
| `0.2.4` | 2026-08-14 | 1 | **Nothing an adopter loads** — PH3 record work only, and the version moved because the published line takes the next patch number rather than because the plugin did. [`PUBLISHING.md`](PUBLISHING.md) §8.1 carries the row, which is what makes an absent row distinguishable from a forgotten one |
| `0.3.0` | 2026-08-17 | 53 | **The first release shaped by an adopter's deck, and the first minor since `0.2.0`.** [T-128](../tasks/T-128-publish-the-adopter-deck-as-a-worked-example.md) published a deck somebody else built with the published skill, and running the gates over it found four `PH1` defects nothing written here could expose: [T-166](../tasks/T-166-shell-sync-leaves-an-upgraded-deck-failing-the-theme-gate.md), [T-167](../tasks/T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md), [T-168](../tasks/T-168-sources-open-ships-with-no-minimum-target-size.md), [T-169](../tasks/T-169-the-figure-binder-cannot-bind-a-value-split-across-table-cells.md). Two more, [T-174](../tasks/T-174-the-quick-view-reopens-at-the-previous-documents-scroll-offset.md) and [T-175](../tasks/T-175-the-published-example-colophon-is-not-back-matter.md), came from opening that deck and clicking. Also the commands an upgrade always needed: `shell.py sync`, `shell.py tokens`, and [T-096](../tasks/T-096-one-command-that-runs-every-checker-and-says-what-it-skipped.md)'s `check_all.py` |
| `0.3.1` | 2026-08-18 | 4 | [T-109](../tasks/T-109-one-source-reference-component-rendered-in-three-places.md) makes a source reference **one component wherever it renders** — the corner mark, the list behind a multi-source mark, and the colophon — and it is the only change here an existing deck has to answer; [`PUBLISHING.md`](PUBLISHING.md) §8.1's row names the two commands and the two hand edits. [T-119](../tasks/T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md) examined all 165 rules, changed four, removed none, and named thirteen no instrument could apply. [T-159](../tasks/T-159-gate-the-text-a-reader-follows-and-no-checker-reads.md) and [T-176](../tasks/T-176-shell-py-s-self-test-blocks-the-command-that-fixes-what-it-fails-on.md) are this repository's own tooling and never reach a deck. **Step 4 earned its keep again**: the README still said one of PH2's two trailing tasks was open and named the printed contents sheet, which [T-036](../tasks/T-036-the-second-contents-page-for-long-decks.md) had closed in `0.3.0` — a false sentence with every pasted figure on the page correct (**L-05**) |
| `0.4.0` | 2026-08-18 | 2 | **The chrome row rebuilt, and the first release whose digit came from a written rule.** [T-114](../tasks/T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md) gives the ruler, the counter and the pager one drawn box and fills the pager, on the principle that the box is for navigation — *Read* and *Motion* leave it. `.chrome` gains a twelfth slot so *Motion* can sit outside the menu in a deck that loops, which DS-218 requires and a static gate can now decide. **What finished it was a look, not a gate**: the `More` menu had never been rendered **open**, and drawing it found a menu item drawn as a button inside a box — a shut disclosure is `display:none`, so no measurement could reach it (**[L-117](lessons/L-117.md)**). The same pass rendered the row in dark at 25 slides and found [T-178](../tasks/T-178-dense-mode-drops-the-position-mark-below-the-section-marks.md), filed rather than fixed. [`PUBLISHING.md`](PUBLISHING.md) §8 gained the patch-versus-minor rule it never had, moving the subject off **scale** — what `0.3.0` was ruled on — and onto whether the deck contract changed shape |
| `0.5.0` | 2026-08-20 | 14 | **The release an outside build wrote.** Somebody built a 16-slide deck with `0.4.0` in their own project, and reading that session's transcript afterwards produced eight defects; the owner added four more from using the result. Four were in the published plugin and are the reason this is not a patch. **The documented commands could not run** — every one interpolated `${CLAUDE_PLUGIN_ROOT}`, which Claude Code puts into a plugin manifest and never into a shell, so that build hardcoded a version-pinned cache path 87 times instead ([T-189](../tasks/T-189-resolve-the-plugin-root-in-every-documented-command.md)). **Every deck ever shipped here had a control that could not answer a press**: the back pager's hover rule carried three classes and outranked a two-class `:active`, so it drew its lean and never its pinch, invisible to every gate because nothing here can watch an animation play ([T-199](../tasks/T-199-the-back-pager-button-never-plays-its-press-animation.md)). DS-240 gives a control its own clock and DS-241 makes the eyebrow name the slide's subject instead of repeating the number and the stage the chrome already prints — 23 slides across two shipped decks had that habit. DS-242 adds an optional lobby and moves the counter onto the argument rather than the file. **Three checks written this release found nothing on their first run and were wrong**: two matched on the wrong relation, one had an assertion that could not fail, and all three were caught by seeding the defect back in before the green was believed (**L-04**) |
| `0.5.1` | 2026-08-20 | 1 | **The check `0.5.0` shipped could not see the defect it was written for.** DS-241 reads an eyebrow through `content.runs()`, which decodes `&nbsp;` and `&amp;` and nothing else - so `07 &middot; Structure` arrived as that literal string and a digit followed by an ampersand is not a digit followed by a separator. The gate reported **`0` offending eyebrows on a deck where all fifteen were the defect**, hours after shipping. **Found by looking at a rendered slide after the gate had already called the deck clean** (rule 6), which no instrument here would have done. The fourth check in one day to find nothing on its first run; the other three were caught by seeding the defect first, and this one was not seeded - which is the entire difference and now the entry in [T-201](../tasks/T-201-ds-241s-check-misses-an-eyebrow-written-as-an-entity.md) |
| `0.6.0` | 2026-08-22 | 20 | **The release the gate stopped reading the file and started watching it run.** `GF-2` to `GF-8` ([T-041](../tasks/T-041-implement-the-nine-glitch-free-conditions.md)) decide seven of R6's nine glitch-free conditions from one browser walk, and six of the seven are facts no markup states: which faces loaded, which family the text rendered in, whether a canvas drew. `DS-244` ([T-204](../tasks/T-204-an-instrument-for-mark-collisions.md)) measures diagram label against diagram label after the portfolio-review deck passed every gate here carrying fifteen chart defects that only people found. Two instruments stopped reading a name and started reading a claim: DS-141's licence to run past 500 ms ([T-187](../tasks/T-187-open-the-motion-vocabulary-into-a-style-guide.md)) and DS-142's subject ([T-214](../tasks/T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md)), which was an allow-list of the single class name `.current` and failed any other looping motion for a design the ruleset permits. **T-187 carried no `shipped_in` from the day it closed until this release wrote one**, which is how it nearly missed the set. |

---

## 2. The phases, as they actually ran

**PH1 shipped 2026-08-09 as `0.1.0` and has reopened on every release since that carried a defect
fix.** A defect in the published plugin is a `PH1` **phase** task, not a later improvement, so the
phase reopens rather than the fix waiting for a later one. **No total is stated here, and that is the
same ruling made twice.** *`CLAUDE.md` carried the counts **nine reopenings** and **seven PH1
patches** until 2026-08-14; neither was re-derivable from the record, so they were not carried over.*
This document then carried **nine** in their place until 2026-08-22 — by which time `0.5.0` and
`0.5.1` had each reopened the phase again, so the figure that replaced two unmaintained ones was
unmaintained too. §1's table is one row per release and `work_package: PH1` in the task front matter
is countable.
*[T-216](../tasks/T-216-the-ph1-reopening-count-contradicts-the-prose-below-it.md), which removed the
same figure from [`RELEASE-PHASES.md`](RELEASE-PHASES.md) in the same pass.*

**PH2 shipped 2026-08-11 as `0.2.0` and the phase stayed open behind it for two days.** T-080 and
T-036 kept the `PH2` label by the owner's decision, so a shipped release and an open phase were not a
contradiction here ([`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) §3). T-080 closed
2026-08-12 and
[T-036](../tasks/T-036-the-second-contents-page-for-long-decks.md) closed 2026-08-13, which emptied
the phase.

**PH3 is the main line since 2026-08-13.** The three phases were set by the owner — `PH1` and `PH2`
on 2026-08-09, `PH3` split off PH2 on 2026-08-10 — and
[`RELEASE-PHASES.md`](RELEASE-PHASES.md) is the decision, including why the second split was needed
and why the line fell at an effort estimate of `l`. **T-089, T-092 and T-093 sit in PH3 against
their size**, because reopening a shipped phase is reserved for defects in the published plugin.

---

## 3. Which task found which defect

**`0.2.1`'s three were the first raised from outside this repository.** T-090 and T-091 were hit on
the published `0.2.0` by the first adopting project and moved here from the `PH3` they arrived
labelled with. T-094 is the project's own, found while rendering a deck to look at it.

**`0.2.2`'s four all came from the adopting project, and T-105 is the first this project took over
its filer's own classification.** It arrived as feedback because the contract behaves as written, and
a published gate that fails a deck for using a class the contract defines is a defect in the check
whatever the report calls it.

**Two of `0.2.3`'s three were found by looking at a rendered deck rather than by a command, and both
were in this repository's own reference deck as well as in the adopter's.** The printed contents page
collided at 13 entries in both, and the colophon drew a mark that referenced nothing in both, **with
every gate green the whole time**. T-120 is the exception and came from `check_all.py`'s first run.

**What that first run found is [`PUBLISHING.md`](PUBLISHING.md) §8**, which also records the
hand-kept list of sixteen commands it replaced on 2026-08-13
([T-096](../tasks/T-096-one-command-that-runs-every-checker-and-says-what-it-skipped.md)) and the
three red checks that list had missed the day it was written.

---

## 4. How the deck length target moved

**12 slides was the target until 2026-08-13 and is the floor after it.** The first adopting project
presented a 13-slide deck and reported the constraint as the problem: the material needed far more
room than 12 slides, a peer presented **43**, and the next deck from the same sources would be much
longer.

**One thing has been built and printed at 17, 25 and 43** — the contents page continues onto `k`
sheets past 16 entries and the printed page count is `n` + `k`
([T-036](../tasks/T-036-the-second-contents-page-for-long-decks.md), 2026-08-13). Nothing else has
been measured above 13.

**Nothing could see a print-only fault until 2026-08-13.** The contents page collided at 13 entries
in a presented deck *and* in this repository's own reference deck, while every gate stayed green and
the tool aimed at that page reported it clean — the fault lives only in paged layout, which no screen
measurement reaches
([T-116](../tasks/T-116-the-printed-contents-page-collides-at-thirteen-entries.md), **L-76**). The
gap closed the same day: `tools/deck/printgeom.py` reads the card rectangles out of the printed PDF
([T-123](../tasks/T-123-nothing-can-see-a-print-only-layout-fault.md)).

---

## 5. How the plugin got built

**The research finished and the scaffold followed, both by 2026-08-09.** The build check, the theme
contract, the component contract, the editorial split rule and build mode were all built that day;
the humanizer rule landed the same day as [`PUBLISHING.md`](PUBLISHING.md).
[`../examples/sort-window/`](../examples/sort-window) is the first deck nobody authored by hand.

**`reference/` was described as working prior art until 2026-08-09, which it never was.** It is one
1.2 KB file and it is a prompt: nothing in it is code to copy or behaviour to verify. The correction
is kept because the description had been acted on.
