---
id: T-303
title: Close a slidefacts element at its own tag, find every control on a slide, and make readability's ledger add up
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-299, T-258, T-259]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: high
effort: m
created: 2026-09-13
updated: 2026-09-14
deliverables: [tools/deck/slidefacts.py, tools/deck/readability.py]
---

# T-303 — Close a slidefacts element at its own tag, find every control on a slide, and make readability's ledger add up

## 1. Specify

**Outcome**
`slidefacts.py` reads the whole face of a slide, and `readability.py` reads all of the copy it says it
reads. Today `by_class` closes an element at the **first** matching close tag
(`tools/deck/slidefacts.py` `:97`, `section.find("</%s>" ...)`), so a `.body` whose first child is
the same tag stops at that child. `readability.py` takes its lines **and** its counted-out words
through `slidefacts.facts` (`tools/deck/readability.py` `:151` and `:162`), so the dropped words are on
neither side of a ledger that promises nothing goes missing quietly. And `controls()`
(`tools/deck/slidefacts.py` `:119`-`:130`) matches only `data-disc`, so a slide's real `<button>` is
reported as absent.

**From the adopter report** `10`, `13`, `14`.

**Re-run in triage, 2026-09-13, on this tree.** `by_class` on a nested fixture returned `['FIRST']`
where `['FIRST SECOND THIRD']` was expected, and the unnested control returned both of its words.
`slidefacts.py` on slide 2 of a copy of the reference deck printed the disclosure and omitted the
`sources-btn` button on the same slide.

**Scope**
- In: `by_class` tracks tag depth to the balanced close
- In: `readability.py` asserts that the words read plus the words counted out equal the words the
  slide carries, so a truncation of this kind cannot pass quietly again
- In: `controls()` finds `<button>`, `role="button"`, `role="tab"`, `role="switch"` and `[tabindex]`,
  and prints each control's accessible name
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the three records above, each with its command, its version and its own proposed fix
- [T-299](T-299-triage-the-third-adopters-report.md) section 3, where the three were ruled together

**Acceptance criteria**
- [ ] records `10`, `13` and `14` are each closed with the remedy measured, or deferred with the reason
      recorded in this task
- [ ] each fix is proved by seeding the defect and watching it fire, in both directions (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Each record carries its evidence and a proposed fix; the proposal is a hypothesis to measure
  before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | With the unchanged tools, snapshot every slide's facts and `readability.py`'s ledger on the four tracked decks, and reproduce `13` | the before direction, §3 |
| 2 | `13`: close an element at its balanced close tag | `tools/deck/slidefacts.py` |
| 3 | `10`: read controls from the accessibility contract, each with its accessible name, each printed once | `tools/deck/slidefacts.py` |
| 4 | `14`: count each slide's fields a second time with a different reader, and print the ledger short where the two differ | `tools/deck/readability.py` |
| 5 | Prove both directions in each self-test, then diff the snapshot taken after against step 1's | §3 |
| 6 | Lint, then the full gate | — |

## 3. Implement

**Decisions & assumptions**
- `13`: an element closes where the count of opens of its own tag returns to zero, and a void
  element opens none. Reversible. — 2026-09-14
- The same cause sat in the `<svg>` pattern and is fixed here, though no record names it:
  `readability.py`'s new ledger found it on its first run. On the reference deck's slide 13, a figure
  holding icon `<svg>`s printed 28 label words as body copy. Reversible. — 2026-09-14
- `10`: controls come from the accessibility contract, as the record proposes. A negative `tabindex`
  is left out, against the record's wording, because only a script can focus it and a reader cannot
  reach it. Reversible. — 2026-09-14
- Each control prints once, under the field that names it. The first control inside a `[data-disc]`
  element is that disclosure's trigger, and a control with `data-qv` is under `Quick views`.
  Otherwise every disclosure and quick view would print twice. Reversible. — 2026-09-14
- A control with no accessible name prints `(no accessible name)`, not an empty quote. Reversible.
  — 2026-09-14
- `14`: the carried side is counted by the standard library's HTML parser over the same fields and
  cuts, not by `slidefacts`, because a ledger counted by the reader it audits adds up whatever that
  reader drops. A difference prints as `LEDGER SHORT`, and the exit code stays 0 because the tool
  never gates. Reversible. — 2026-09-14
- Reading a `.body` whole moves the hardest-lines ranking. A body of stat cards is now one line with
  no sentence end, so slide 5 of the reference deck ranks first at Fog 32.5. That is outside the three
  records and is not changed here. Reversible. — 2026-09-14
- The first-close idiom is in five more tools. Nothing is raised: the three patterns whose tag can
  nest match 102 elements on the four tracked decks and none is unbalanced, and the rest match
  `script`, `style`, `p` or an empty `span`, which cannot nest ([L-167](../docs/lessons/L-167.md)).
  Reversible. — 2026-09-14

| Record | Case | Tool | Result |
| :--- | :--- | :--- | :--- |
| `13` | the record's fixture, a `.body` opening with a nested `<div>` | unchanged | `['FIRST']` |
| `13` | same | fixed | `['FIRST SECOND THIRD']` |
| `13` | body-copy words on the four tracked decks | unchanged, fixed | 92 → 185, 112 → 228, 363 → 504, 60 → 162; 27 of 51 slides changed |
| `13` | source words on `measure-first` | unchanged, fixed | 25 → 123 |
| `14` | the ledger with the first-close reading patched back into `slidefacts` | fixed `readability.py` | short on all four decks, by 121, 116, 239 and 102 words |
| `14` | the ledger before the `<svg>` fix | fixed | short on the reference deck only: slide 13 body copy carries 0 and is read as 28 |
| `14` | the ledger after it | fixed | adds up on all four: 986, 804, 1,353 and 585 words |
| `10` | slide 2 of the reference deck | unchanged | the disclosure only; the `sources-btn` button absent ([T-299](T-299-triage-the-third-adopters-report.md) §3) |
| `10` | same | fixed | `disclosure 'scope'` and `button '2 sources'` |
| `10` | controls on the four tracked decks | unchanged, fixed | 10 → 15, 10 → 17, 9 → 16, 8 → 8. Every added control is a sources button, and no disclosure trigger or quick-view control is printed twice |

**Outputs produced**
- `tools/deck/slidefacts.py`: `close_of` and `svg_spans` close at the balanced tag; `controls` reads
  the accessibility contract; four self-test cases, each also asserting its fixture reproduces the
  defect
- `tools/deck/readability.py`: `Carried` and `ledger`, the ledger line, and a self-test that hands
  the ledger a truncated reading and watches it go short
- [L-167](../docs/lessons/L-167.md): a defect in how a pattern closes an element is a class

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| records `10`, `13` and `14` each closed with the remedy measured, or deferred with the reason | **pass** | All three closed. The ledger `14` asked for found a second instance of `13`'s cause, fixed here |
| each fix proved by seeding the defect and watching it fire, in both directions | **pass** | Each self-test case asserts the fixed reading and that its fixture still reproduces the defect under the replaced arithmetic. On the decks, §3's table runs the ledger with the defect patched back in and without it |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree, since the diff reaches `tools/deck/` |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | All three records closed, each proved in both directions. The ledger found a second first-close defect, in the `<svg>` pattern, on its first run, and it was fixed here. No look is owed: no deck changed, and both tools print text. |
| 2026-09-14 | -> in_progress | Step 1 ran with the unchanged tools before any edit. |
| 2026-09-14 | -> planned | Six steps. |
| 2026-09-14 | -> specified | §1 was complete as raised. |
| 2026-09-13 | -> proposed | Raised by T-299 from the third adopter's records `10`, `13` and `14`, which share `slidefacts.py`. `PH1`: an adopter met all three in the published `0.7.0`. |
