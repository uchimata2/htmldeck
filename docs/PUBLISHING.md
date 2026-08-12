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
(`TASK-WORKFLOW.md` §6.1). §8 goes at the end even though it is the part read first — the pointer
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
`checked   82`, so a sentence saying `checks` names that field and one about the judgement half does
not — a correct number moved into the wrong sentence fails, and the report names the field behind
every figure it compared. **The same rule reaches five documents that paste no output at all**:
wherever a page states a part of a whole the gate prints — *"82 of the 113 rules a gate owns … the
other 31"* — the part must be a figure of that account and the remainder must be the subtraction.
That figure lived in five places and drifted to three different values; correcting it by hand is
[T-045](../tasks/T-045-sweep-the-stale-claims-across-the-live-documents.md)'s work, and this is why
it does not need doing again
([T-068](../tasks/T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md)). A row struck
through and dated is a record of what was true then, and is skipped.

**Two figures the check does not treat alike.** A count of the *ruleset* is `compared` and a drift
fails the run. A count of the *repository* — `refcheck.py`'s pointer totals — is declared `volatile`
and is **reported rather than failed**, because it moves on every documentation commit including the
one that corrects it, so it is stale the moment it is pasted. Re-paste those at release time from
`--values`; do not chase them between releases.

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
| 1 | **Every gate green** — the whole set, not the routine one | Each command's own verdict line. See *the gate list* below, which is the step that has already gone wrong |
| 2 | **Bump the version** in `.claude-plugin/plugin.json`, `CLAUDE.md` and `README.md` | Three files carry it; a grep for the outgoing version returns nothing outside `docs/BRIEF.md`'s history |
| 3 | **Humanize the human-facing set** (§2's test), then re-run `python tools/docs/figures.py` and re-paste the `volatile` block from `--values` | `0 stale figure(s)`. §6 is why: a rewrite that re-derives a number from memory is a defect, not a style improvement |
| 4 | **Read the prose around the figures** | Nothing. **This is the step no gate covers** — `v0.1.4` found a spelled-out fixture count and a defect tally that had both gone false while every pasted figure was correct (**L-05**) |
| 5 | **Name what stops conforming** — §8.1. If this release adds or tightens a required part, write the row before you tag | A row in §8.1's table, naming the rule ids that will newly fail and the smallest edit that satisfies them |
| 6 | **Commit, tag `vX.Y.Z`, push both** | `git push origin master --tags`, and the tag on the remote |
| 7 | **`gh release create`**, with a note written to §2's test, **carrying §8.1's row verbatim** | The published release page. A release note is read before installing, so §2 covers it — it is not an exception to the rule, it is an instance of it |
| 8 | **Record the shipping version** in each closed task's log and in [`BRIEF.md`](BRIEF.md) | The version appears in the record without anyone reconstructing it later, which is the failure this whole section exists for |

**The gate list is an enumeration, and it is declared as one.**

```
python tools/tasks/lint.py                                     # index, check, refcheck
python tools/docs/figures.py                                   # every figure the README pastes,
                                                               # and the same figures in five
                                                               # documents that paste none
python tools/deck/ruleset.py --counts                          # the ruleset's own arithmetic
python tools/plugin/check_scaffold.py                          # the plugin manifest
python tools/deck/static_variants.py                           # the seeded-defect suite
python tools/examples/seed_defects.py --check                  # the blindness fixture, still derived
python tools/deck/contents_bound.py                            # the contents-page bound
python tools/deck/shell.py check <deck>                        # the five below run PER DECK, and
python tools/deck/component.py check <deck>                    # this repository ships TWO:
python tools/deck/theme.py check <deck>                        #   examples/reference-deck.html
python tools/deck/check.py <deck> --sources <dir>              #   examples/sort-window/sort-window.html
python tools/deck/spec.py <deck>.foundation.md <deck>.slides.md <deck>.html
```

**The first command ends with one advisory that is expected**, and a release run meets it before
anything else: `taskmd check` reports `DUPLICATE INDEX` against `docs/BRIEF.md`, because the phase
tables name a majority of the board's ids. It is a true reading of a document that is not a duplicate
index, it fires on every run, and the decision behind ignoring it is
[`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) §6. **A `DUPLICATE INDEX` naming any other
document is not covered by it and stops the release.**

**`--sources` is the one argument that cannot be guessed from the deck's path**, and guessing wrong
does not error — it reports `FIG-0 … source files this reader cannot open` and fails the run, which
reads exactly like a defect in the deck. The two directories are not siblings of their decks in the
same way, so they are written out rather than left to `<dir>`:

```
examples/reference-deck.html              --sources examples/sources
examples/sort-window/sort-window.html     --sources examples/sort-window/sources
```

**The per-deck five are where every defect this list was written from was hiding**, and the reason is
structural: the README prints repository-wide commands, so the set anyone runs by habit never reaches
a deck. Run them against **both** examples, not the one being worked on.

**The last of the five is the exception, and it is one deck rather than two — permanently.**
`spec.py` reads a specification pair, and `examples/reference-deck.html` ships without one: it was
built by hand before the two documents existed, so there is no `.foundation.md` to hand it.
[T-087](../tasks/T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md)
settled on 2026-08-11 that it owes a provenance record but **not that one**, and **rejected
retrofitting a `.foundation.md`** — it would make a hand-built deck claim to be a build-mode output,
buying a checkable `SPEC-5` at the cost of the only example showing what hand-built provenance looks
like. That deck's record is source-level instead (`examples/sources/` plus the colophon), so the line
above runs on `sort-window` alone and always will. Stated here so nobody reads a command that cannot
run as one that passed, or reopens a question that has an answer.

**It has already failed, which is why it is declared rather than trusted.** The README prints five
commands and that set was treated as the list. Writing this section meant running everything in it,
and **three checks outside the printed five were red on 2026-08-10**: the shared shell was stale on
`examples/sort-window/`, a `hard` rule was failing on the same deck
([T-083](../tasks/T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md)),
and `contents_bound.py` refused to start at all
([T-084](../tasks/T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md)). None of
the three would have been found by running the printed five, and each had been red since the day a
task changed a deck without running the checks that read it.

**What closes the excusal:** one command that runs every checker under `tools/` and reports which it
ran and which it skipped **with a reason** — the partition [`figures.py`](../tools/docs/figures.py)
already applies to fences and [`check.py`](../tools/deck/check.py) to rules. Until that exists, a list
kept by hand is what there is, and a list kept by hand goes stale silently — which is §2's own
argument about the covered set, one document over.

### 8.1 What each release newly required

**A conforming deck is not edited by an upgrade, and can stop conforming anyway.** The requirement
arrives documented — `DESIGN-SYSTEM.md`, the two contracts and `build.md` all describe a new part
before a gate enforces it — and the adopter's first news of it is a wall of failures against a file
nobody touched. That has now happened twice running.

**The expensive half is not the reading.** An adopter who has not baselined the old build cannot
tell a new requirement from a regression, and the first reading of six failures after an upgrade is
that the upgrade broke something. Naming them here, and in the release note, is what makes
baselining unnecessary.

| Version | What it newly required | What newly fails | The smallest edit |
| :--- | :--- | :--- | :--- |
| `0.2.0` | A per-slide `Sources` field in the specification, and a provenance mark rendered from it (DS-105, T-069) | `spec.py` on every slide of a deck written before it | Add `Sources:` to each slide in the `.slides.md`, then rebuild the marks |
| `0.2.1` | The capability preflight and its degraded state (DS-009, T-019) | `check.py` — `DS-009` ×3, `DS-013`, `DS-229`; `shell.py check` — `NOT A SHELL`, no `<script id="preflight">`; `theme.py check` — `DS-013`, `--scrim` undeclared | `python tools/deck/shell.py preflight <deck>` writes the block and the anchor; declare `--scrim` in the theme region |
| `0.2.2` | `data-stage` decided as an index (T-102); `.fig` role classes usable (T-105); the one-source provenance mark (T-103); DS-232, cross-slide SVG references (T-104) | `component.py` on a deck whose `data-stage` carries a stage **name**; `check.py` — `DS-232` on a deck defining a `<marker>` in one slide and using it in another. **Nothing that passed 0.2.1 newly fails for the other two**: T-105 stops a gate failing a legal deck, and T-103 changes what `build.md` asks for on new work | `data-stage="2"` — the zero-based index into the deck's `STAGES`; move each `<marker>` into the slide that uses it |

**A release with nothing to say here says so** — the row is the evidence the question was asked, and
an absent row is indistinguishable from a forgotten one.
