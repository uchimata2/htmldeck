# htmldeck

**Single-file HTML presentations that don't look generated.** One `.html` you double-click. It opens
with the network off, carries its own fonts, icons and diagrams, and renders identically on a
projector, a laptop and a share window — no installation, no build step, no CDN.

This repository is the **design system, the evaluator and the build check** behind that, plus a
reference deck built strictly to them. It is a Claude Code plugin in progress: the standard and the
gate are built and run today; **the mode that writes a deck for you is not** — see *What does not
exist yet*.

---

## What is actually here

| | |
| :--- | :--- |
| [`docs/DESIGN-SYSTEM.md`](docs/DESIGN-SYSTEM.md) | **The operative ruleset** — 160 rules, each with a stable `DS-nnn` ID, a hard/default/guidance label, and a statement of whether a check can reach it at all |
| [`docs/DESIGN-RATIONALE.md`](docs/DESIGN-RATIONALE.md) | Why each rule is what it is: what was measured, what was inherited, what was overruled, and the conflicts resolved by name |
| [`docs/EVALUATION.md`](docs/EVALUATION.md) | How a deck is scored, and **when it is good enough to stop** |
| [`tools/deck/check.py`](tools/deck/check.py) | The build check — a pass/fail per rule ID, **and an account of every rule it did not check, with a reason each** |
| [`examples/reference-deck.html`](examples/reference-deck.html) | A 12-slide deck built by hand against the ruleset. Open it offline |
| [`docs/research/`](docs/research/) | Seven notes the rules are derived from — a corpus study, external principles, exemplar decks, prior art, asset licences, a `file://` capability matrix, printing |
| [`skills/htmldeck/`](skills/htmldeck/) | The plugin skill: the pipeline, the artifacts it passes between stages, and the two questions it asks |

Everything is **pure Python standard library plus real Chrome**. There is nothing to install.

---

## Run it

Clone, then run any of these. Output below is from a clean clone at
[`examples/reference-deck.html`](examples/reference-deck.html).

**The gate, and what it admits it did not check.**

```bash
python tools/deck/check.py examples/reference-deck.html
```

```
  owned by a gate      111
  checked               79
  failing                0
  excused in the rules   4   DS-042 DS-072 DS-210 DS-211
  excused here          28
  SILENT                 0
  ------------------------
  buckets sum to       111   = owned, so the account is a partition

0 failure(s): none
```

**The account is the point.** A gate that checks 79 of 111 rules and says nothing about the other 32
is making a claim it has not earned. Every rule in a gate's jurisdiction ends each run **checked**,
**excused in writing** — with what would close the excusal — or **failing**, and a rule in none of
those three states *fails the run*. So a rule added to the ruleset with nothing behind it is a red
run the same afternoon, not a discovery two months later.

**A check that runs and finds nothing to judge lands there too.** A rule of the form *every X is Y*,
on a deck with no X, is **undecided** — not passing — and the account separates the two, because a
rule with no check behind it and a rule whose check found no subject need opposite fixes. The gate
passed on its own absence three times before that distinction existed
([`docs/LESSONS.md`](docs/LESSONS.md) L-44).

**Every count the documents state, derived rather than re-typed.**

```bash
python tools/deck/ruleset.py --counts
```

```
  rule rows in the table            160
  + declared in prose, not a row      1   DS-000 (guidance)
  = rule IDs the document declares  161   <- the figure that counts DS-000
```

**Which gate owns each `hard` rule.**

```bash
python tools/deck/ruleset.py --gates
```

```
  hard rules                        114
  gated mechanically (auto|render)   85   tools/deck/check.py
  gated by judgement (judge)         24   EVALUATION.md 1.1, the hard-judge checklist
  bind the checker, not the deck      5   DS-107 DS-190 DS-191 DS-220 DS-221
  ------------------------
  114 = hard, so every hard rule has an owner
```

**The task record, its links and its section references.**

```bash
python tools/tasks/task.py check
```

```
OK - 52 tasks, vocabulary valid, task references resolve, 776 document pointer(s) checked, 0 broken
     430 section reference(s) resolved, 0 dead; 990 not bound to a document and skipped.
```

Every markdown link, every repo-relative path written in prose, and every `<named document> §n`
reference in the repository — **including the ones on this page**.

**The plugin package.**

```bash
python tools/plugin/check_scaffold.py
```

```
10 of 10 fixtures behaved as specified.
OK - manifest valid, components at the root, every ${CLAUDE_PLUGIN_ROOT} pointer resolves,
```

`check.py` drives **real Chrome or Edge**, headless, with a throwaway profile and every DNS lookup
black-holed — because a preview pane is not a faithful `file://` environment and has given this
project a confident wrong answer four times. The other three commands read files and need nothing
but Python.

---

## The reference deck

[`examples/reference-deck.html`](examples/reference-deck.html) — 12 slides, **214 KB in one file,
zero external references**, three embedded typefaces, nine icons and seven hand-written SVG figures.
Download it, disconnect, double-click it. Every measurement behind it, and how to reproduce each, is
in [`examples/README.md`](examples/README.md).

It also ships with [`examples/reference-deck-seeded-defects.html`](examples/reference-deck-seeded-defects.html)
— the same deck with **one deliberate defect per evaluation dimension**, generated from its parent
so the only difference is the defect. That file exists because *a rubric that has never been tested
is a rubric that passes everything*, and it is the evidence the scoring works. Running the gate over
it catches three of the ten dimensions; the other seven are what the judgement pass is for, and
`examples/README.md` names every one it misses.

---

## What does not exist yet

Stated here rather than left to be inferred, because a README describing the plan is not a README.

- **Build mode does not exist.** Nothing in this repository writes a deck. The reference deck was
  built by hand against the ruleset, which is how the ruleset was validated —
  [T-002](tasks/T-002-build-mode-the-self-contained-deck-generator.md).
- **Critique mode does not exist.** The rubric in `EVALUATION.md` is complete and can be applied by
  hand; nothing automates the report —
  [T-004](tasks/T-004-critique-mode-blunt-section-by-section-review.md).
- **Both halves of the gate are green.** Two `hard` rules failed the reference deck on the
  judgement half's first run and were settled the same day —
  [T-052](tasks/T-052-two-hard-judge-failures-in-the-reference-deck.md), one by amending the rule
  and one by editing the deck. The mechanical gate was green throughout, which is exactly the
  point of having a second half.

The whole backlog is in [`tasks/`](tasks/README.md), one Markdown file per task with its own log.

---

## Where to go next

| If you want to | Read |
| :--- | :--- |
| Use the plugin | [`skills/htmldeck/SKILL.md`](skills/htmldeck/SKILL.md) |
| Judge the design position | [`docs/DESIGN-SYSTEM.md`](docs/DESIGN-SYSTEM.md), then [`docs/DESIGN-RATIONALE.md`](docs/DESIGN-RATIONALE.md) for why |
| Know what a deck is scored on | [`docs/EVALUATION.md`](docs/EVALUATION.md) |
| See the evidence | [`docs/research/`](docs/research/) — every rule traces to a note there |
| Continue the work | [`CLAUDE.md`](CLAUDE.md) for the rules, [`docs/BRIEF.md`](docs/BRIEF.md) for the specification, [`tasks/README.md`](tasks/README.md) for the board |

---

## Licence

**MIT** — [`LICENSE`](LICENSE).

The three typefaces embedded in the reference deck are under the **SIL Open Font License 1.1**,
which permits redistribution and embedding provided the licence travels with the font. It does: the
deck carries the OFL notice next to the faces themselves, so a deck you send someone is complete and
correctly licensed on its own. The reasoning and the per-family verification are in
[`docs/research/R5-assets-and-licences.md`](docs/research/R5-assets-and-licences.md).

**Riverbend, the city in the reference deck, does not exist.** Every figure in it is an output of
assumptions printed on the slide that uses it; none is attributed to a real agency, study or place.
