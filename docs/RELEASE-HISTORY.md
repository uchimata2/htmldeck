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

---

## 2. The phases, as they actually ran

**PH1 shipped 2026-08-09 as `0.1.0` and has reopened nine times.** A defect in the published plugin
is a `PH1` **phase** task, not a later improvement, so the phase reopens rather than the fix waiting
for a later one. Every patch in §1's table above `0.1.0` is one of those reopenings. *`CLAUDE.md`
carried the counts **nine reopenings** and **seven PH1 patches** until 2026-08-14; neither was
re-derivable from the record and §1's table is countable, so they were not carried over.*

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
