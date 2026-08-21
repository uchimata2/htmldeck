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

It self-tests against nineteen deliberately broken packages before it looks at this one, and *Run it*
below shows what a good result prints. That command is also the fastest way to tell whether a copied
skill directory is still wired up.

---

## Upgrade it

Refreshing the marketplace is not an upgrade. `/plugin marketplace update htmldeck` fetches the new
catalog and stops there, because third-party marketplaces have auto-update switched off by default.
The version you have installed does not move, and running `/plugin install` again only reports that
the plugin is already there.

The command that moves it runs in a terminal rather than inside Claude Code:

```bash
claude plugin update htmldeck@htmldeck
```

Restart Claude Code afterwards. The `@htmldeck` suffix names the marketplace and is not optional: the
bare name reports `Plugin "htmldeck" not found`.

If you would rather not run it yourself, open `/plugin`, go to the **Marketplaces** tab, select
`htmldeck` and choose **Enable auto-update**. Claude Code then refreshes the marketplace and updates
the installed plugin a few minutes after each session starts.

---

## What is actually here

| | |
| :--- | :--- |
| [`docs/DESIGN-SYSTEM.md`](docs/DESIGN-SYSTEM.md) | **The operative ruleset.** 176 rules, each with a stable `DS-nnn` ID, a hard/default/guidance label, and a statement of whether a check can reach it at all |
| [`docs/DESIGN-RATIONALE.md`](docs/DESIGN-RATIONALE.md) | Why each rule is what it is: what was measured, what was inherited, what was overruled, and the conflicts resolved by name |
| [`docs/EVALUATION.md`](docs/EVALUATION.md) | How a deck is scored, and **when it is good enough to stop** |
| [`tools/deck/check.py`](tools/deck/check.py) | The build check. A pass/fail per rule ID, **and an account of every rule it did not check, with a reason each** |
| [`examples/reference-deck.html`](examples/reference-deck.html) | A 12-slide deck built by hand against the ruleset. Open it offline |
| [`examples/`](examples/README.md) | Every shipped deck, with what was measured on each: the hand-built one above, one assembled through build mode, one an adopter built elsewhere, and a fixture carrying a deliberate defect per evaluation dimension |
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
  owned by a gate      121
  checked               91
  failing                0
  excused in the rules   3   DS-072 DS-210 DS-211
  excused here          27
  undecided, no subject  0
  SILENT                 0
  ------------------------
  buckets sum to       121   = owned, so the account is a partition

0 failure(s): none
```

**Read the account, not just the failure count.** A gate that checks 91 of 121 rules and says nothing
about the other 30 is making a claim it has not earned. Every rule in a gate's jurisdiction ends each
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
  rule rows in the table            176
  + declared in prose, not a row      1   DS-000 (guidance)
  = rule IDs the document declares  177   <- the figure that counts DS-000
```

**Which gate owns each `hard` rule.**

```bash
python tools/deck/ruleset.py --gates
```

```
  hard rules                        129
  gated mechanically (auto|render)   95   tools/deck/check.py
  gated by judgement (judge)         29   EVALUATION.md 1.1, the hard-judge checklist
  bind the checker, not the deck      5   DS-107 DS-190 DS-191 DS-220 DS-221
  ------------------------
  129 = hard, so every hard rule has an owner
```

**Every reference in every document.**

```bash
python tools/docs/refcheck.py
```

```
OK - 3060 document pointer(s) checked, 0 broken
     885 section reference(s) resolved, 0 dead; 2748 not bound to a document and skipped.
```

Every markdown link, every repo-relative path written in prose or printed by a tool, and every
`<named document> §n` reference in the repository, **including the ones on this page**. The third
one matters because a section number is a pointer whose target is printed in the document it points
at, so renumbering a heading silently falsifies every citation of it.

The task record is checked separately, by the `taskmd` plugin this project tracks its work with:

```bash
taskmd check
```

**The plugin package.**

```bash
python tools/plugin/check_scaffold.py
```

```
19 of 19 fixtures behaved as specified.
OK - manifest valid, components at the root, every ${CLAUDE_PLUGIN_ROOT} pointer resolves,
```

`check.py` drives **real Chrome or Edge**, headless, with a throwaway profile and every DNS lookup
black-holed. A preview pane is not a faithful `file://` environment, and it has given this project
confident wrong answers: it allowed a local `fetch()` that a real restricted origin denies, which is
the failure that puts the defect in the recipient's copy rather than the console, and it drew a
diagram as broken whose DOM geometry was correct to the pixel. The other three commands read files
and need nothing but Python.

---

## The reference deck

[`examples/reference-deck.html`](examples/reference-deck.html) is 12 slides and a colophon, **307 KB
in one file, zero external references**, three embedded typefaces, eleven icons and eight hand-written
SVG figures. Download it, disconnect, double-click it. Every measurement behind it, and how to
reproduce each, is in [`examples/README.md`](examples/README.md).

It also ships with [`examples/reference-deck-seeded-defects.html`](examples/reference-deck-seeded-defects.html),
the same deck with **one deliberate defect per evaluation dimension**, generated from its parent so
the only difference is the defect. Until it existed, the scoring rubric had never been run against a
deck known to be bad, so nothing showed it could fail one. Running the gate over it catches three of
the ten dimensions; the other seven are what the judgement pass is for, and `examples/README.md`
names every one it misses.

---

## The deck nobody authored by hand

[`examples/sort-window/`](examples/sort-window) holds *Move the window, not the fleet*: 12 slides,
**307 KB in one file, zero external references**, six hand-written SVG figures and ten disclosure
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

The judgement half is 29 `hard` rules that need a person. The worksheet is generated, not recalled,
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

- **It has been installed and used by one project other than this one**, which found six defects in
  two days: a manifest the installer rejected, a crash on any deck outside the plugin's own drive, a
  gate failing decks for not containing what its rules judge, upgrade instructions that upgraded
  nothing, a documented command with a flag the tool did not have, and a rule that looked for the
  reference deck's own class names and failed any deck not using them. All six are fixed. The third
  took three goes. The first fix searched for other instances with a throwaway script that read only
  part of what it claimed to have read; the second replaced that script with a fixture, and the
  fixture could see one file of the eight that needed it. The sample is one project.
- **That project's deck is now the third example here, and running the gates over it found four more
  defects**, none of which either deck written in this repository could have exposed. Two further
  faults came out of somebody opening the deck and clicking: a control that reopened at the previous
  document's scroll position, and a colophon filed as an argument slide. The pattern is the point.
  A ruleset tested only by its authors is tested against what its authors already knew.
- **The gate names seven glitch-free conditions it does not check**, and there is no frame-rate
  figure. Both are PH3, not oversights.

The whole backlog is in [`tasks/`](tasks/README.md), one Markdown file per task with its own log. It
is split into three phases, and a phase is not a version. **PH1** is what a first working plugin
needs; it shipped as 0.1.0 and took five patches. **PH2** is the minor and moderate fixes already
known. It shipped as 0.2.0 with two of its tasks open behind it. Both have since closed. The
second was the printed contents page, which now continues onto another sheet for decks past the
length one sheet holds. 0.2.3 carried three fixes to the published plugin. Two of them came
from looking at a rendered deck rather than from any command, and both turned out to be in this
repository's own example deck as well as in the deck that reported them. 0.2.4 changed nothing you
install; it was the project's own record. 0.3.0 was the first release shaped by a deck somebody else
built. **PH3** is the
larger work, including 3D visuals, the frame-rate figure and those seven conditions.
[`docs/BRIEF.md`](docs/BRIEF.md) says what is in each and why.

The current release is 0.5.1. Most of it came from watching somebody else build a deck with 0.4.0
and writing down everything that got in their way. The .1 is a check that shipped in 0.5.0
unable to see the thing it was written to catch, found a few hours later by looking at a slide.

The controls answer faster. Pressing the back or forward arrow used to take most of half a second to
show anything, which is long enough to wonder whether the button works. The back arrow never
showed anything at all, because one style rule quietly outranked another. Both are fixed, and a
control now runs on a shorter clock than the slides do.

Every slide says what it is about. The line above the headline used to repeat the slide number and the section name, and the bar along the bottom was already showing you
both. Now it names the thing on the slide, so a presenter glancing up learns something. Two of the
three example decks here had the old habit, and both are rewritten.

A deck can open on a lobby slide, the one an audience looks at while the room fills, carrying the
topic, who is presenting and what the occasion is. It is optional, like the sources page at the
end, and neither of them counts towards the slide numbers any more. They are covers, not content.

A quoted source finally reads like a document rather than like a slide. Its headings were smaller
than its own body text, which nobody had noticed.

The commands in the instructions now run. They were all written against a variable that turns out
to be empty in a shell, so anyone following them had to work out the paths themselves.

A deck built on an earlier version will fail several checks until you run `shell.py tokens` and
`shell.py sync`. The release notes say what fails and what fixes it. One of them, the line above
each headline, needs a sentence from you rather than a command.

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
