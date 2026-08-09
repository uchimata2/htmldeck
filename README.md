# htmldeck

**Single-file HTML presentations that don't look generated.** One `.html` you double-click. It opens
with the network off, carries its own fonts, icons and diagrams, and renders identically on a
projector, a laptop and a share window. There is nothing to install, no build step and no CDN.

This repository is the **design system, the evaluator and the build check** behind that, plus two
decks built strictly to them. It is a Claude Code plugin, and all four parts run today: the standard,
the gate, the mode that writes a deck and the mode that reviews one. What is still outstanding has
its own section, *What does not exist yet*.

---

## Install it

Both lines are typed inside Claude Code, not in a terminal:

```
/plugin marketplace add uchimata2/htmldeck
/plugin install htmldeck@htmldeck
```

Copying [`skills/htmldeck/`](skills/htmldeck/) into a plugin of your own works as well. Every path
the skill resolves goes through `${CLAUDE_PLUGIN_ROOT}`, which is what lets a copied directory find
its own references.

To check the package rather than assume it, clone the repository and run:

```bash
git clone https://github.com/uchimata2/htmldeck
cd htmldeck
python tools/plugin/check_scaffold.py
```

It self-tests against ten deliberately broken packages before it looks at this one, and *Run it*
below shows what a good result prints. That command is also the fastest way to tell whether a copied
skill directory is still wired up.

---

## What is actually here

| | |
| :--- | :--- |
| [`docs/DESIGN-SYSTEM.md`](docs/DESIGN-SYSTEM.md) | **The operative ruleset.** 163 rules, each with a stable `DS-nnn` ID, a hard/default/guidance label, and a statement of whether a check can reach it at all |
| [`docs/DESIGN-RATIONALE.md`](docs/DESIGN-RATIONALE.md) | Why each rule is what it is: what was measured, what was inherited, what was overruled, and the conflicts resolved by name |
| [`docs/EVALUATION.md`](docs/EVALUATION.md) | How a deck is scored, and **when it is good enough to stop** |
| [`tools/deck/check.py`](tools/deck/check.py) | The build check. A pass/fail per rule ID, **and an account of every rule it did not check, with a reason each** |
| [`examples/reference-deck.html`](examples/reference-deck.html) | A 12-slide deck built by hand against the ruleset. Open it offline |
| [`docs/research/`](docs/research/) | Seven notes the rules are derived from: a corpus study, external principles, exemplar decks, prior art, asset licences, a `file://` capability matrix, printing |
| [`skills/htmldeck/`](skills/htmldeck/) | The plugin skill: the pipeline, the artifacts it passes between stages, and the two questions it asks |

The tooling is **pure Python standard library plus real Chrome**, so there are no packages to install
either.

---

## Run it

Clone, then run any of these. Output below is from a clean clone at
[`examples/reference-deck.html`](examples/reference-deck.html).

**The gate, and what it admits it did not check.**

```bash
python tools/deck/check.py examples/reference-deck.html
```

```
  owned by a gate      113
  checked               81
  failing                0
  excused in the rules   4   DS-042 DS-072 DS-210 DS-211
  excused here          28
  SILENT                 0
  ------------------------
  buckets sum to       113   = owned, so the account is a partition

0 failure(s): none
```

**Read the account, not just the failure count.** A gate that checks 81 of 113 rules and says nothing
about the other 32 is making a claim it has not earned. Every rule in a gate's jurisdiction ends each
run **checked**, **excused in writing** (with what would close the excusal), or **failing**, and a
rule in none of those three states *fails the run*. So a rule added to the ruleset with nothing behind
it is a red run the same afternoon, not a discovery two months later.

**A check that runs and finds nothing to judge lands there too.** A rule of the form *every X is Y*,
on a deck with no X, is **undecided** rather than passing, and the account separates the two, because
a rule with no check behind it and a rule whose check found no subject need opposite fixes. The gate
passed on its own absence three times before that distinction existed
([`docs/LESSONS.md`](docs/LESSONS.md) L-44).

**Every count the documents state, derived rather than re-typed.**

```bash
python tools/deck/ruleset.py --counts
```

```
  rule rows in the table            163
  + declared in prose, not a row      1   DS-000 (guidance)
  = rule IDs the document declares  164   <- the figure that counts DS-000
```

**Which gate owns each `hard` rule.**

```bash
python tools/deck/ruleset.py --gates
```

```
  hard rules                        117
  gated mechanically (auto|render)   87   tools/deck/check.py
  gated by judgement (judge)         25   EVALUATION.md 1.1, the hard-judge checklist
  bind the checker, not the deck      5   DS-107 DS-190 DS-191 DS-220 DS-221
  ------------------------
  117 = hard, so every hard rule has an owner
```

**The task record, its links and its section references.**

```bash
python tools/tasks/task.py check
```

```
OK - 60 tasks, vocabulary valid, task references resolve, 1002 document pointer(s) checked, 0 broken
     496 section reference(s) resolved, 0 dead; 1146 not bound to a document and skipped.
```

Every markdown link, every repo-relative path written in prose, and every `<named document> §n`
reference in the repository, **including the ones on this page**.

**The plugin package.**

```bash
python tools/plugin/check_scaffold.py
```

```
10 of 10 fixtures behaved as specified.
OK - manifest valid, components at the root, every ${CLAUDE_PLUGIN_ROOT} pointer resolves,
```

`check.py` drives **real Chrome or Edge**, headless, with a throwaway profile and every DNS lookup
black-holed. A preview pane is not a faithful `file://` environment, and it has given this project a
confident wrong answer four times. The other three commands read files and need nothing but Python.

---

## The reference deck

[`examples/reference-deck.html`](examples/reference-deck.html) is 12 slides, **221 KB in one file,
zero external references**, three embedded typefaces, nine icons and seven hand-written SVG figures.
Download it, disconnect, double-click it. Every measurement behind it, and how to reproduce each, is
in [`examples/README.md`](examples/README.md).

It also ships with [`examples/reference-deck-seeded-defects.html`](examples/reference-deck-seeded-defects.html),
the same deck with **one deliberate defect per evaluation dimension**, generated from its parent so
the only difference is the defect. Until it existed, the scoring rubric had never been run against a
deck known to be bad, so nothing showed it could fail one. Running the gate over it catches three of
the ten dimensions; the other seven are what the judgement pass is for, and `examples/README.md`
names every one it misses.

---

## The deck nobody authored by hand

[`examples/sort-window/`](examples/sort-window) holds *Move the window, not the fleet*: 12 slides,
**212 KB in one file, zero external references**, five hand-written SVG figures and ten disclosure
panels. It was built through the pipeline rather than written, assembled from
[`shell/`](shell), which is the reference deck with its content cut out, then authored three slides
at a time with the gate run per batch.

The directory holds all four artifacts a run leaves behind: the deck, the foundation spec with its
outline, the slide-by-slide specification, and the three source documents its figures were
reconciled against. The specification files exist so that when a deck turns out wrong, there is
something to open.

```bash
python tools/deck/check.py examples/sort-window/sort-window.html --sources examples/sort-window/sources
```

**Marnfield, the parcel network in it, does not exist**, and neither do the source documents outside
this repository. Every figure is an output of the assumptions written down beside it.

---

## Reviewing a deck

```bash
python tools/deck/critique.py <deck> [--sources <dir>]
```

The review has a half a program can do and a half it cannot, and this prints the first so a reader
spends their attention on the second. It says which passes ran, what the gate already decided, the
figure ledger, and the five dimensions (Claim, Evidence, Density, Spine, Consistency) that no check
in this repository reaches.

The judgement half is 25 `hard` rules that need a person. The worksheet is generated, not recalled,
and **a rule left unanswered fails the run**:

```bash
python tools/deck/critique.py <deck> --worksheet > sheet.txt
python tools/deck/critique.py --answers sheet.txt
```

Run over the seeded-defect deck, the mode found **all ten** of its deliberate defects; run over the
parent, none. Two of the ten needed something the worksheet alone does not give: the reordered
argument was found by reading the stage order, and the contradicted figure only surfaced once
sources were supplied. That is why the report always says which half it checked.

---

## What does not exist yet

Listed here rather than left to be inferred, so nobody has to work out which parts of this page
describe a plan.

- **Nothing is published yet.** [T-008](tasks/T-008-package-document-and-publish.md) is the deploy,
  and this repository has no remote.

The whole backlog is in [`tasks/`](tasks/README.md), one Markdown file per task with its own log.
It is split into two releases. **v0.1** is what a first working plugin needs, and it is now down to
publishing. **v0.2** is everything else already known, including 3D visuals, a frame-rate figure, and
the seven glitch-free conditions the gate names and does not yet check.
[`docs/BRIEF.md`](docs/BRIEF.md) says what is in each and why.

**Both halves of the gate are green.** Two `hard` rules failed the reference deck on the judgement
half's first run and were settled the same day in
[T-052](tasks/T-052-two-hard-judge-failures-in-the-reference-deck.md), one by amending the rule and
one by editing the deck. The mechanical gate was green throughout, which is the point of having a
second half.

---

## Where to go next

| If you want to | Read |
| :--- | :--- |
| Use the plugin | [`skills/htmldeck/SKILL.md`](skills/htmldeck/SKILL.md) |
| Judge the design position | [`docs/DESIGN-SYSTEM.md`](docs/DESIGN-SYSTEM.md), then [`docs/DESIGN-RATIONALE.md`](docs/DESIGN-RATIONALE.md) for why |
| Know what a deck is scored on | [`docs/EVALUATION.md`](docs/EVALUATION.md) |
| See the evidence | [`docs/research/`](docs/research/); every rule traces to a note there |
| Continue the work | [`CLAUDE.md`](CLAUDE.md) for the rules, [`docs/BRIEF.md`](docs/BRIEF.md) for the specification, [`tasks/README.md`](tasks/README.md) for the board |

---

## Licence

**MIT**, in [`LICENSE`](LICENSE).

The three typefaces embedded in the reference deck are under the **SIL Open Font License 1.1**,
which permits redistribution and embedding provided the licence travels with the font. It does: the
deck carries the OFL notice next to the faces themselves, so a deck you send someone is complete and
correctly licensed on its own. The reasoning and the per-family verification are in
[`docs/research/R5-assets-and-licences.md`](docs/research/R5-assets-and-licences.md).

**Riverbend, the city in the reference deck, does not exist.** Every figure in it is an output of
assumptions printed on the slide that uses it; none is attributed to a real agency, study or place.
