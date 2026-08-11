---
id: T-091
title: build.md documents shell.py icons --set as a single pair, and it takes one comma-separated argument
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-090]
work_package: v0.1
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-11
updated: 2026-08-11
deliverables:
  - tools/deck/shell.py
  - skills/htmldeck/references/build.md
---

# T-091 — `build.md` documents `shell.py icons --set` as a single pair, and it takes one comma-separated argument

## 1. Specify

**Outcome**
`build.md` §2 shows the invocation that works for more than one icon, and the error a wrong one
produces names the cause rather than a symptom two steps downstream.

**What is wrong**
`build.md` §2 documents

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py icons <slug>.html --set <concept>=<lucide-name>
```

and shows a single pair. `--set` in fact takes **one comma-separated argument** —
`--set a=x,b=y,c=z`. An author with three icons follows the documentation, passes three `--set`
pairs, and the run fails with

```
icon `i-analysis` is used and nothing says which Lucide glyph it is
```

which is true, and names the symptom rather than the cause: the earlier pairs were parsed and the
later ones were not, so the message points at the icon rather than at the argument shape that lost
it.

**Why it is worth a task at all.** It is small and it cost a wrong diagnosis before the usage string
was read — the same shape as the `--out` flag this project reported earlier: **a documented procedure
nobody had executed.** Both are cheap to fix and both are found only by an adopter, because the
maintainer's own runs use the form that works.

**Scope**
- In: `build.md` §2's example, and the failure message when `--set` is given more than once.
- Out: changing `--set` to accept repetition. That is a defensible design and this task does not
  argue for it; if it were taken, the documentation fix is still needed for the version already
  shipped.

**Inputs**
- `skills/htmldeck/references/build.md` §2.
- `tools/deck/shell.py`, the `icons` subcommand's argument parsing.

**Acceptance criteria**
- [x] `build.md` §2 shows a multi-icon example in the form that works
- [x] Passing `--set` more than once either works or fails with a message naming the argument, not
      the icon
- [x] The single-pair form still works, so the documented case does not regress

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the parser before rewording anything, since where the value is lost decides where the message belongs | The mechanism, in §3 |
| 2 | Refuse a repeated option where it is read, and name the argument in the message | `tools/deck/shell.py` |
| 3 | Show the multi-icon form in §2, and say what the flag takes | `skills/htmldeck/references/build.md` |
| 4 | Run all three shapes — one pair, several in one flag, the flag repeated | The runs, in §4 |

## 3. Implement

**Decisions & assumptions**
- **The refusal goes in `option()`, not in the `icons` branch.** `option` reads `argv.index(name)`,
  which takes the first occurrence — so **every** flag this parser reads drops a repeat in silence,
  not only `--set`. Fixing it where the value is lost covers `--title`, `--theme`, `--stage-icons`
  and `--sheet` by construction, and a fix in the subcommand would have left the same defect in four
  places for the next adopter to find one at a time.
- **`--set` still takes one comma-separated value.** §1 put repetition out of scope and this task does
  not argue for it: the shipped version needs the documentation to match the parser, and that is true
  whichever way a later task rules.
- **The message names the argument and the shape.** `--set was given 2 times and this parser reads
  the first only … It takes ONE comma-separated value: --set a=x,b=y,c=z` — the count is in it
  because a message that describes the rule without saying what was received leaves the author
  checking whether it applies to them.

**Outputs produced**
- [`../tools/deck/shell.py`](../tools/deck/shell.py) — `option()` refuses a repeated flag; two
  fixtures in `self_test` hold both shapes.
- [`../skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) — §2's example is
  the multi-icon form, with a sentence saying what the flag takes and what the old shape looked like
  when it failed.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `build.md` §2 shows a multi-icon example in the form that works | met | The fence now carries two pairs in one `--set`, and the paragraph under it names the constraint rather than leaving it to be inferred from an example. |
| A repeated `--set` works or fails naming the argument, not the icon | met | `shell.py icons <deck> --set when=clock --set where=map` → `--set was given 2 times and this parser reads the first only … It takes ONE comma-separated value`, exit 1. Before this it wired `when` and said nothing about `where`. |
| The single-pair form still works | met | Both `--set when=clock` and `--set when=clock,where=map` wrote the sprite and exited 0, on a copy of the shipped deck. `shell.py --self-test`: **20 of 20 fixtures**, the two new ones included. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (shipped) | **Shipped in `0.2.1`.** **One of the three fixes this release is for**, and the second raised from outside the repository. |
| 2026-08-11 | → done | All three criteria met, and **the fix is one level up from the report**. `option()` reads `argv.index`, so every flag this parser takes drops a repeat in silence - `--set` is the one an adopter happened to repeat, because it is the one the documentation showed a single pair of. Refusing the repeat where the value is lost covers `--title`, `--theme`, `--stage-icons` and `--sheet` at the same time, which is the difference between fixing this report and fixing its family. Awaiting a `v0.1.6` patch release with [T-090](T-090-spec5-cannot-parse-a-descriptive-slide-label.md). |
| 2026-08-11 | (specify) | **Moved to `v0.1`** with [T-090](T-090-spec5-cannot-parse-a-descriptive-slide-label.md), for the same rule and by the same route: an adopter following the shipped `build.md` hit it on `0.2.0`. The precedent is [T-074](T-074-the-documented-render-command-does-not-exist.md), a documented command that did not exist, shipped as `v0.1.4` — a procedure the plugin ships is part of the plugin. |
| 2026-08-11 | → proposed | Raised by the AI Training 06 (DentalPro) project alongside [T-090](T-090-spec5-cannot-parse-a-descriptive-slide-label.md), found in the same build. Kept as its own task rather than folded into that one: they share a discovery session and nothing else, and a finding fixed inside another task's record makes that record claim a criterion it never had. |
