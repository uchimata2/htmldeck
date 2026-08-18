# Publishing

**Shipping a release: §8. The humanizing rule: §1 to §7.** Those two subjects are one document
because a release is where the rule binds, and splitting them is how the rule came to be cited from
three places.

§1 to §7 are the detail behind [`../CLAUDE.md`](../CLAUDE.md) *Publishing constraints*, fourth
bullet. That bullet is the rule; those sections are what it means in practice — the covered-set test,
the exclusions with their reasons, the owner's exception verbatim, and the boundary against
[`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §3.3. §8 is the sequence around it, which lived only in task
logs until 2026-08-10.

*The section numbers were not renumbered when §8 was added, and will not be: `PUBLISHING.md §2`,
`§3` and `§6` are cited from two task records, and renumbering silently falsifies every one of them
([`../tasks/TOOLING.md`](../tasks/TOOLING.md) §2). §8 goes at the end even though it is the part read first — the pointer
above is how that is resolved.*

**This document is agent-facing and is not covered by its own rule** — see §7.

---

## 1. The rule

**No release is published until the human-facing text has been through the humanizer, and no plugin
file has been.** The owner, 2026-08-09:

> No release can be published without humanizing human-facing information. Plugin files are not human
> facing and must be kept AI optimized.

Two halves, and the second is a requirement rather than a scope note. A humanizer pass over
[`../skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md), this file, `CLAUDE.md`, a tool docstring
or a commit message is a **defect**, not a courtesy.

**It binds every release, not the first.** [T-056](../tasks/T-056-humanize-the-human-facing-documents-before-publishing.md)
is `blocked_by` on [T-008](../tasks/T-008-package-document-and-publish.md), and that edge is spent the
moment T-008 closes — which is exactly why the rule does not live on the edge. The edge gates release
one. This document gates release two and everything after it.

---

## 2. What it covers — a test, not a list

> **What does a stranger read before they have installed anything?**

Anything that answers the question is covered. Anything that does not, is not.

Today the test resolves to three things:

- [`../README.md`](../README.md) — the front door.
- **The repository description and any marketplace listing text** — the one or two sentences shown
  beside the name, before a click. Drafted at [T-056](../tasks/T-056-humanize-the-human-facing-documents-before-publishing.md)
  §3 and used by T-008 at publication.
- [`../examples/README.md`](../examples/README.md) — **added by the owner on 2026-08-11**, after
  `v0.2.0` shipped. It is browsable on the forge without installing anything, and the front page
  sends a reader there for every measurement it asserts, so a stranger deciding whether to install
  can and does read it. It was outside the set for the first six releases; `v0.2.0` is therefore not
  a release that missed a gate, and the set widened after it rather than during it.

**The test is the rule; those two are only today's answer.** A list of filenames goes stale the first
time a document is added, and it goes stale *silently* — nothing fails, the new document simply is
not covered. This repository has already paid for that once: `reconcile_targets` in
`.handoff/config.md` is an enumeration, and what it had quietly stopped covering is what
[T-042](../tasks/T-042-audit-the-whole-repository-against-itself.md) found.

**Applying the test to a document that does not exist yet.** Ask where the reader is standing, not
what the file is called. A `CONTRIBUTING.md` is read after cloning by someone who has already decided:
not covered. A landing page, a launch post, a screenshot caption, an installation walkthrough: all
read before the decision, all covered.

---

## 3. What it excludes, and why

| Excluded | Why |
| :--- | :--- |
| **Everything agent-facing** — `SKILL.md` and its `references/`, `CLAUDE.md`, this file, tool docstrings | The owner's words: keep them efficient for AI parsing. The compression that reads as machine-written is the *feature*, and `SKILL.md` is under a byte budget on purpose |
| **Commit messages** | Same reason. They are read by tooling and by whoever bisects, not by a stranger deciding whether to install |
| **Task files** | Fifty-odd records of work already done are an audit trail. Rewriting their prose edits the history rather than the product |
| **The ruleset and the research notes** — `DESIGN-SYSTEM.md`, `DESIGN-RATIONALE.md`, `EVALUATION.md`, `LESSONS.md`, `research/` | Not read before installing, cited by ID from code, and their density is what makes them usable |
| **Deck copy** | DS-106's jurisdiction, and gated. See §4 |
| **Anything the humanizer would have to invent a fact to improve** | §6 |

---

## 4. Where this rule ends and DS-106 begins

Two instruments over one text would disagree, and the gated one would win anyway. So they do not
overlap:

| | This rule | DS-106 / DS-107 |
| :--- | :--- | :--- |
| **Jurisdiction** | Repository text a stranger reads before installing | **Deck copy** — the words on a slide |
| **Instrument** | The `humanizer` skill, run by a person, at release time | `tools/deck/check.py`, run per build; the categories are inlined in [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §3.3 and their owning skill is named in [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §8 |
| **On a violation** | The release does not ship | The build fails |
| **Scope of the artifact** | The repository | One deck |

A deck built by this plugin is **never** run through the `humanizer` skill, and the README is
**never** checked against DS-106. If a text seems to fall under both, it is deck copy: the gated
instrument takes it.

---

## 5. How to run it

**The skill.** `humanizer@humanizer`, **2.9.1**, from the `blader/humanizer` marketplace. Verified
present in this project's session 2026-08-09; nothing had to be enabled.

**Mode.** File mode for `README.md` — it rewrites in place and reports a summary. Pasted-text mode for
the repository description, which is short enough that the draft, the audit answers and the final text
should all be recorded.

**The exception, as given by the owner on 2026-08-09 — verbatim:**

> When humanizing docs: preserve tables, code blocks, heading hierarchy, and **Label:** value
> bullets. Skip patterns 15, 16, 18. Apply the rest.

The three skipped patterns are **15 Overuse of Boldface**, **16 Inline-Header Vertical Lists** and
**18 Emojis** — named as well as numbered so the instruction survives the skill being renumbered, and
**re-verified against the installed copy** rather than trusted. Each is load-bearing here: this
project carries its decisions in bolded labels and its rules in inline-header lists, and stripping
them would flatten the structure that makes a document skimmable rather than remove a tell.

**Pattern 14 applies: cut the em dashes.** The owner answered this directly on 2026-08-09.

**Where 14 stops: inside a table cell, the exception wins.** *Preserve tables* and *cut the em
dashes* meet in a measurement row, and the first one takes it. Settled 2026-08-11, on
[`../examples/README.md`](../examples/README.md)'s first pass: 43 em dashes went to 8, and all 8
survivors are in table cells, three of them in rows whose figures §6 requires to survive
byte-identical. Rewriting a cell to drop its punctuation means restructuring the sentence around a
protected number, which is the trade §6 already refuses. The prose is the jurisdiction; a cell is
the table's.

**The escape that is not being taken.** The skill's *Voice Calibration* section says a user-supplied
writing sample outranks its style rules, §14 included — so this repository's existing prose could be
handed over as a sample and its em dashes kept. It is recorded here because the next person to read
§14 will find that escape too, and the answer above forecloses it.

---

## 6. What must survive byte-identical

Beyond the exception's tables, code blocks, headings and label bullets:

**Every figure in the README is pasted from a run.** Counts, byte sizes, tool output. A rewrite that
rounds one, rephrases it, or re-derives it from memory is a **defect**, not a style improvement — a
correct number quietly becoming a plausible one (**L-03**).

So after any pass over the README, prove it rather than trusting the diff:

```bash
python tools/docs/figures.py
```

It runs each command the README prints and compares the block underneath it, and it partitions
**every** fence and every prose numeral on the page: compared, excluded with a reason, or a named
gap that fails the run. `--values` prints what to paste when something has moved. This replaces
diffing the five commands by eye, which is what this section said until 2026-08-10 — six figures had
already gone stale under that instruction, because a rule with nothing behind it is a claim
([T-060](../tasks/T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md)).

**A figure is bound to the field that produced it, not to the run as a whole.** The gate prints
`checked   84`, so a sentence saying `checks` names that field and one about the judgement half does
not — a correct number moved into the wrong sentence fails, and the report names the field behind
every figure it compared. **The same rule reaches five documents that paste no output at all**:
wherever a page states a part of a whole the gate prints — *"84 of the 114 rules a gate owns … the
other 30"* — the part must be a figure of that account and the remainder must be the subtraction.
That figure lived in five places and drifted to three different values; correcting it by hand is
[T-045](../tasks/T-045-sweep-the-stale-claims-across-the-live-documents.md)'s work, and this is why
it does not need doing again
([T-068](../tasks/T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md)). A row struck
through and dated is a record of what was true then, and is skipped.

**The account is declared, so a claim that has drifted still reports.** A sentence naming a declared
account is held to what that account prints, whatever value it states. Until
[T-154](../tasks/T-154-bind-the-measurements-that-five-live-documents-state-in-prose.md) the claim
was found by the *whole's value*, so the day the account moved `113 → 115` the four pages still
saying `113` left the watched set **because they were wrong** (**L-97**). An account whose label the
command stops printing fails the run rather than going quiet.

**Two figures the check does not treat alike.** A count of the *ruleset* is `compared` and a drift
fails the run. A count of the *repository* — `refcheck.py`'s pointer totals — is declared a `floor`,
because it moves on every documentation commit including the one that corrects it. **A floor may be
exceeded and never reddens; falling below it fails, and a pasted `0` is exact** — zero as a lower
bound asserts nothing, and `0 broken` and `0 dead` carry all of that block's evidence. Re-paste those
at release time from `--values`; do not chase them between releases.

**What it still cannot see.** It checks that a pasted figure matches its command. It does not check
that the sentence around the figure is true — the README's *"all three are fixed"* went false while
every figure on the page was correct, and no gate here would have caught it (**L-05**).

---

## 7. This document

Agent-facing, by §3, and therefore **not** covered by §2's test. It is a working rule read by whoever
prepares a release, not by a stranger choosing whether to install. Its density, its bolded labels and
its tables are deliberate, and a humanizer pass over it is a defect on exactly the same terms as one
over `SKILL.md`.

---

## 8. The release sequence

Eight steps, in order, each with what proves it was done. Written down on 2026-08-10 after `v0.1.4`
shipped: four releases had each re-derived the same sequence from the last one's commits, which works
until the person doing it is not the person who did it last. *Step 5 was added on 2026-08-12 by
[T-100](../tasks/T-100-a-release-adds-a-required-part-and-conforming-decks-fail-silently.md).*

| # | Step | What proves it |
| :-- | :--- | :--- |
| 1 | **`python tools/check_all.py` green** — the whole set, not the routine one. **It takes minutes, so run it in the background**; it prints its own elapsed time | Its own last line: `0 failure(s), 0 unclassified, 0 stale` and the seconds beside them. It replaced a list of sixteen commands on 2026-08-13 ([T-096](../tasks/T-096-one-command-that-runs-every-checker-and-says-what-it-skipped.md)) |
| 2 | **Bump the version** in `.claude-plugin/plugin.json`, `CLAUDE.md` and `README.md` — to the next number on the **published** line, per the rule below the table | Three files carry it; a grep for the outgoing version returns nothing outside `docs/BRIEF.md`'s history |
| 3 | **Humanize the human-facing set** (§2's test), then re-run `python tools/docs/figures.py` and re-paste the `floor` block from `--values` | `0 stale figure(s)`. §6 is why: a rewrite that re-derives a number from memory is a defect, not a style improvement |
| 4 | **Read the prose around the figures** | Nothing. **This is the step no gate covers** — `v0.1.4` found a spelled-out fixture count and a defect tally that had both gone false while every pasted figure was correct (**L-05**) |
| 5 | **Name what stops conforming** — §8.1. If this release adds or tightens a required part, write the row before you tag — or **fill in the `*next*` row** the work already left there, replacing it with the number step 2 bumped to | A row in §8.1's table, naming the rule ids that will newly fail and the smallest edit that satisfies them, under a version and not under `*next*` |
| 6 | **Commit, tag `vX.Y.Z`, push both** | `git push origin master --tags`, and the tag on the remote |
| 7 | **`gh release create`**, with a note written to §2's test, **carrying §8.1's row verbatim** | The published release page. A release note is read before installing, so §2 covers it — it is not an exception to the rule, it is an instance of it |
| 8 | **Record the shipping version** in each closed task's `shipped_in` and log, and in **both** chronology homes — [`RELEASE-PHASES.md`](RELEASE-PHASES.md) and [`RELEASE-HISTORY.md`](RELEASE-HISTORY.md), which carries one row per release | The version appears in the record without anyone reconstructing it later, which is the failure this whole section exists for. *It said `BRIEF.md` until 2026-08-14; [T-145](../tasks/T-145-move-brief-mds-release-phases-to-its-own-document.md) moved the chronology out that morning and `BRIEF.md` now holds no version string at all, so the step named a file that could not satisfy it. `RELEASE-HISTORY.md` was added 2026-08-18 for the same reason one step further on: the step named one of the two homes the same move created, and `0.4.0` shipped with the chronology missing its row until the next session's sweep found it* |

**Which number step 2 bumps to: the next one on the published line, whatever phase the tasks in the
release belong to.** `0.2.0` plus three `PH1`-phase fixes is `0.2.1`. **Read the published version
before tagging** — `plugin.json` and the newest tag — because the phase label is not evidence about
either, and a tag below the installed version is offered to nobody. The tell in a record is *awaiting
`vX.Y.Z`* where `X.Y.Z` is not greater than what is installed; it is worth a grep at release time.
**L-69** is the release it nearly broke, and why no gate here can see the failure. *Stated here since
2026-08-14 ([T-144](../tasks/T-144-give-each-cumulative-rule-one-operative-home.md)). It lived in
`../CLAUDE.md` from 2026-08-11, beside the release status, which `L-69` §4 records as the cheap fix
that protected this sequence and did nothing for the reading cost.*

**Which digit moves: the shape of the deck contract, not the size of the diff.** *Written
2026-08-18, because §8 had a rule for the next number on the line and none for which digit it
lands on.*

- **Minor** — the contract a deck must satisfy **changes shape**: a contracted part added or
  removed, a `.chrome` slot added, a required rule tightened, a measured bound moved. The adopter
  has to read §8.1's row before upgrading.
- **Patch** — everything else, **including a shared-shell edit that `shell.py sync` settles**. The
  shell moving is not by itself a shape change: what a deck must *contain* is unchanged and the
  repair is mechanical.

The test is §8.1's *What it newly required* column, which is already written by the time step 2
runs: a row naming a new or deleted part is minor, a row whose whole content is *the shared shell
moved* is patch, and **`Nothing`** is patch.

**This rule is prospective, and it replaces a criterion that was stated rather than absent.**
`0.3.0` took its minor on **scale** — 53 closed tasks — and `0.3.1` took its patch by following
that precedent, both recorded in
[`RELEASE-PHASES.md`](RELEASE-PHASES.md). Scale is the wrong subject, and the table below is the
demonstration: `0.3.0` was the larger release and required **nothing** of an existing deck, while
`0.2.1`, `0.2.2` and `0.3.1` were each smaller and each added a required part that failed decks
already built. All three shipped as patches. **The digit is read by the adopter deciding whether to
upgrade, so it has to encode their cost, not this project's effort** — which is what moves the
subject from how much was done to whether the contract changed shape.

No row above is restated to match. What shipped, shipped, and the rule starts here.

**The gate list was an enumeration for three days, and is now one command.**

```
python tools/check_all.py
```

It discovers what to run rather than listing it: every `tools/**/*.py` that `git` says a clone
receives, and every deck this repository ships, with the per-deck five run against each. It ends
with the partition [`check.py`](../tools/deck/check.py) keeps over rules and
[`figures.py`](../tools/docs/figures.py) over fences, one altitude up — each checker **ran**, **was
skipped with a stated reason**, or **failed**. **A tool in none of those three fails the run**, so a
checker added and left unwired goes red instead of going unnoticed, and an entry naming a deleted
file goes red too. `--list` prints what it would run without running it; `--verbose` lets every
child write its own account to the console.

**Its first run found what a list cannot.** Three checkers the sixteen never ran are green and are
now gates — `deliverable_variants.py`, `contract_variants.py` and `content_variants.py`, siblings of
the `static_variants.py` that was already in the list. And **`PRINT-1`, the printed page count, was
reached by nothing**: `check.py` evaluates it only under `--print-pages` and the list never passed
that flag, while `printpages.py`'s own entry point defaulted the slide count to a hardcoded 12 and
failed a deck that prints correctly. The per-deck `check.py` line now passes `--print-pages`, and
that entry point derives its count from the deck — the two callers agreed on both shipped decks on
2026-08-13
([T-120](../tasks/T-120-printpages-standalone-defaults-the-slide-count-to-a-hardcoded-twelve.md)).

**The first checker ends with one advisory that is expected**, and a release run meets it before
anything else: `taskmd check` reports `DUPLICATE INDEX` against
[`RELEASE-PHASES.md`](RELEASE-PHASES.md), because the phase
tables name a majority of the board's ids. It is a true reading of a document that is not a duplicate
index, it fires on every run, and the decision behind ignoring it is
[`../tasks/TOOLING.md`](../tasks/TOOLING.md) §1. **A `DUPLICATE INDEX` naming any other
document is not covered by it and stops the release.** *It named `docs/BRIEF.md` until 2026-08-14,
when the tables moved; the advisory followed them, which is what the file-name form of the excusal is
for.*

**`--sources` is the one argument that cannot be guessed from the deck's path**, and guessing wrong
does not error — it reports `FIG-0 … source files this reader cannot open` and fails the run, which
reads exactly like a defect in the deck. So it is **declared per deck** in `check_all.py`'s manifest,
and a deck with no declaration is refused rather than run against a guess. Adding a deck to this
repository means adding its `--sources` directory there; the run says so if you forget.

**The per-deck five are where every defect this list was written from was hiding**, and the reason is
structural: the README prints repository-wide commands, so the set anyone runs by habit never reaches
a deck. That is now the command's job rather than the reader's — it runs them against **every** deck
it discovers, not the one being worked on.

**The last of the five is the exception, and it is one deck rather than two — permanently.**
`spec.py` reads a specification pair, and `examples/reference-deck.html` ships without one: it was
built by hand before the two documents existed, so there is no `.foundation.md` to hand it.
[T-087](../tasks/T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md)
settled on 2026-08-11 that it owes a provenance record but **not that one**, and **rejected
retrofitting a `.foundation.md`** — it would make a hand-built deck claim to be a build-mode output,
buying a checkable `SPEC-5` at the cost of the only example showing what hand-built provenance looks
like. That deck's record is source-level instead (`examples/sources/` plus the colophon), so `spec.py`
runs on `sort-window` alone and always will. It is declared as a permanent exemption in
`check_all.py`'s manifest and **printed as a skip with that reason on every run**, so nobody reads a
command that cannot run as one that passed, or reopens a question that has an answer.

**It has already failed, which is why it is declared rather than trusted.** The README prints five
commands and that set was treated as the list. Writing this section meant running everything in it,
and **three checks outside the printed five were red on 2026-08-10**: the shared shell was stale on
`examples/sort-window/`, a `hard` rule was failing on the same deck
([T-083](../tasks/T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md)),
and `contents_bound.py` refused to start at all
([T-084](../tasks/T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md)). None of
the three would have been found by running the printed five, and each had been red since the day a
task changed a deck without running the checks that read it.

~~**What closes the excusal:** one command that runs every checker under `tools/` and reports which it
ran and which it skipped **with a reason** — the partition `figures.py` already applies to fences and
`check.py` to rules. Until that exists, a list kept by hand is what there is, and a list kept by hand
goes stale silently — which is §2's own argument about the covered set, one document over.~~

**Closed 2026-08-13** by
[T-096](../tasks/T-096-one-command-that-runs-every-checker-and-says-what-it-skipped.md), which built
that command. The excusal is kept struck through rather than deleted: it is the specification the
command was written to, and a paragraph that says what a step owes is worth more visible than gone.

### 8.1 What each release newly required

**A conforming deck is not edited by an upgrade, and can stop conforming anyway.** The requirement
arrives documented — `DESIGN-SYSTEM.md`, the two contracts and `build.md` all describe a new part
before a gate enforces it — and the adopter's first news of it is a wall of failures against a file
nobody touched. That has now happened twice running.

**The expensive half is not the reading.** An adopter who has not baselined the old build cannot
tell a new requirement from a regression, and the first reading of six failures after an upgrade is
that the upgrade broke something. Naming them here, and in the release note, is what makes
baselining unnecessary.

**A row may be written when the work lands, and it carries `*next*` until step 2 gives it a
number.** The two decisions are separate and have separate rules: *what stops conforming* is known
the day the change is built and is expensive to reconstruct later, while *which number* is read off
the published line at release time and off nothing else. Writing a version into this column early
would be the same conflation `../CLAUDE.md` forbids between a phase and a version — so the column
says `*next*`, and **step 2 replaces it with the number it bumped to**. A `*next*` row still in the
table after a tag is a release that skipped step 5's other half.

| Version | What it newly required | What newly fails | The smallest edit |
| :--- | :--- | :--- | :--- |
| `0.2.0` | A per-slide `Sources` field in the specification, and a provenance mark rendered from it (DS-105, T-069) | `spec.py` on every slide of a deck written before it | Add `Sources:` to each slide in the `.slides.md`, then rebuild the marks |
| `0.2.1` | The capability preflight and its degraded state (DS-009, T-019) | `check.py` — `DS-009` ×3, `DS-013`, `DS-229`; `shell.py check` — `NOT A SHELL`, no `<script id="preflight">`; `theme.py check` — `DS-013`, `--scrim` undeclared | `python tools/deck/shell.py preflight <deck>` writes the block and the anchor; declare `--scrim` in the theme region |
| `0.2.2` | `data-stage` decided as an index (T-102); `.fig` role classes usable (T-105); the one-source provenance mark (T-103); DS-232, cross-slide SVG references (T-104) | `component.py` on a deck whose `data-stage` carries a stage **name**; `check.py` — `DS-232` on a deck defining a `<marker>` in one slide and using it in another. **Nothing that passed 0.2.1 newly fails for the other two**: T-105 stops a gate failing a legal deck, and T-103 changes what `build.md` asks for on new work | `data-stage="2"` — the zero-based index into the deck's `STAGES`; move each `<marker>` into the slide that uses it |

| `0.2.3` | Nothing new is *required* of a deck's content. What changed is the **shared shell** — the component block (T-116) and the deck script (T-108) — plus a new `data-stage` value, `back`, which is additive | `shell.py check` on **every deck built before this release**: `COMPONENTS differs from shell/components.css` and `SCRIPT differs from shell/deck.js`. Also `STAGE TABLE` on a deck whose `STAGES` and `STAGE_ICON` differ in length, which is a real defect the gate could not see before. **Nothing that passed `0.2.2` newly fails for `back`**: it adds a legal value and takes none away | For `STAGE TABLE`, give every stage an icon, or move back matter to `data-stage="back"` and delete the stage invented for it. For the two region failures, `python tools/deck/shell.py sync <deck> --write` |
| `0.2.4` | **Nothing.** Not "nothing required of a deck's content" as in `0.2.3` — nothing at all. No file under `skills/`, `shell/` or `tools/` differs from `0.2.3` but the version string, so the shared shell is byte-identical and `shell.py check` has nothing new to say | **Nothing.** Any deck that passed `0.2.3` passes `0.2.4` unchanged, and a deck already behind on the shell is behind by exactly what `0.2.3` said | None. If `shell.py check` reports a difference, it is `0.2.3`'s row, not this one |
| `0.3.0` | **Nothing new of a deck's content.** The **shared shell** moved twice: `components.css` gives `.sources-open` a minimum target size ([T-168](../tasks/T-168-sources-open-ships-with-no-minimum-target-size.md)) and `deck.js` resets the quick view's scroll offset on open ([T-174](../tasks/T-174-the-quick-view-reopens-at-the-previous-documents-scroll-offset.md)). Separately, `shell.py check` gains a **`TOKENS`** row ([T-166](../tasks/T-166-shell-sync-leaves-an-upgraded-deck-failing-the-theme-gate.md)) | `shell.py check` on **every deck built before this release**: `COMPONENTS differs from shell/components.css` and `SCRIPT differs from shell/deck.js`. And **`TOKENS` on any deck built before `0.2.3`** that never declared `--qv-measure`. That requirement is `0.2.3`'s, arriving with the quick-view measure; what is new here is that a gate can finally see it, so an adopter reads it as this release's failure and it is the previous one's | `python tools/deck/shell.py sync <deck> --write`, then `python tools/deck/shell.py tokens <deck> --write`. Neither touches a per-deck region: `sync` rewrites only the shared blocks, and `tokens` adds only the declarations that are missing, at the shipped theme's value |
| `0.3.1` | **The four-kind source vocabulary** ([T-109](../tasks/T-109-one-source-reference-component-rendered-in-three-places.md)): a source reference is one component wherever it renders, typed by what the source is. New contracted parts — `.sources-id`, `.sources-icon`, `.sources--list`, `.qv-file` — and `.sources` may now sit anywhere in a `.slide` rather than only in its `.provenance`. `.sources-open` gains a required `data-file`. The **shared shell** moved in all three regions. **The release's other three tasks require nothing of a deck, and the row says so rather than leaving it inferred**: [T-119](../tasks/T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md)'s audit narrowed DS-138 and split DS-041 so the gate keeps only the half it can decide, which loosens what a deck must satisfy rather than tightening it; [T-159](../tasks/T-159-gate-the-text-a-reader-follows-and-no-checker-reads.md) and [T-176](../tasks/T-176-shell-py-s-self-test-blocks-the-command-that-fixes-what-it-fails-on.md) are this repository's own tooling and never reach an adopter's deck | `shell.py check` on **every deck built before this release**: `SKELETON`, `COMPONENTS` and `SCRIPT` all differ. `component.py check` — **`.qv-file: 0 per .qv-head`**, and **`.sources-open: N of N carry no data-file`** on any deck carrying a quick view. `check.py` — **`DS-105 marks wearing the wrong kind's glyph`** on any deck whose multi-source marks draw the single-source glyph, which was every such deck before this release. **Nothing fails for the identifier bound**: no deck written before this release has a `.sources-id` to exceed it | `python tools/deck/shell.py sync <deck> --write` settles the three regions and `.qv-file` with them, because `.qv-file` ships in the skeleton. The other two are per-deck markup and `sync` must not touch them: add `data-file="<the source's base name>"` to each `.sources-open`, and point every multi-source mark's `<use>` at a symbol drawn by Lucide `library` — `python tools/deck/shell.py icons <deck> --set sources=library --write` adds it |
| `0.4.0` | **The chrome row's shape** ([T-114](../tasks/T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md)). New contracted parts — `.navbox`, `.more`, `.more-menu` and the `.btn--pager` modifier — and `.controls` is gone. `.chrome` carries a **twelfth slot**, `CHROME_TAIL`, holding `More` and, in a deck whose motion loops, `Motion` beside it. DS-218 is tightened from *a control exists* to **a control not shut inside `.more-menu`**; DS-217's measured bound moves 17 → 16 because the container is drawn. One new token, `--more-menu-w`. The **shared shell** moved in all three regions, and then in `components.css` once more before the tag: a menu item is drawn as a row rather than as a button in a box, which is a look fixed after rendering the menu **open** for the first time and requires nothing of a deck beyond the `sync` this row already asks for. **[T-177](../tasks/T-177-tokens-write-carries-the-dark-value-into-the-light-band.md) requires nothing of a deck** and the row says so rather than leaving it inferred: it fixes `tokens --write` carrying a dual-band colour's dark value into the light band, which is this repository's own tooling | **`shell.py check` says `NOT A SHELL`, and that is the whole report** — the deck has no `CHROME_TAIL` anchor, so the cut stops there and the three region failures behind it are never printed. It reads as *your file is broken* rather than *your shell is one release behind*, and it is the second. Then, **after the repair below and because of it**, `audit.py` — **`DS-218`** on any deck whose motion loops or runs past 5 s, because the migration puts `Motion` in the menu and a control behind a click is not persistent. Also `theme.py` / `shell.py check` — **`TOKENS`, `--more-menu-w`** | Three commands, in order, and the third is not optional on a deck with looping motion: `python tools/deck/shell.py sync <deck> --write` installs the anchor and settles the three regions, announcing `MIGRATING` when it does; `python tools/deck/shell.py tokens <deck> --write` adds `--more-menu-w`; then, **if anything in the deck loops**, `python tools/deck/shell.py tail <deck> --loops --write` moves `Motion` out beside `More`. Verified in that order on a deck built before this change: `NOT A SHELL` → three regions synced → one token → `DS-218 pass` |

**The `0.2.3` row was the third in a row whose smallest edit was "rebuild it", and that was the
finding rather than the footnote — [T-124](../tasks/T-124-an-adopter-cannot-refresh-a-decks-shell-after-an-upgrade.md)
closed it on 2026-08-13 and the row above now names a command.** A byte-for-byte shell comparison is
what makes the shared half trustworthy (T-085), and its other edge is that every release touching
`shell/` fails every deck in the wild through no fault of the deck. Measured on this repository's own
deck at the `v0.2.2` tag, run against the tooling that followed it: three problems, of which one was
a genuine defect and two were the deck being one release behind. **`sync` takes the two and leaves
the one**, which is the division it exists to make.

**So a shell change is no longer a row this table struggles to write, and the rule for writing one
is now: name the command.** `sync` reports before it writes, because a deck one release behind and a
deck whose shell someone edited on purpose are the same bytes. What it cannot do is migrate authored
content — the `0.2.0` and `0.2.2` rows above are per-deck facts and stay hand edits.

**A release with nothing to say here says so** — the row is the evidence the question was asked, and
an absent row is indistinguishable from a forgotten one.
