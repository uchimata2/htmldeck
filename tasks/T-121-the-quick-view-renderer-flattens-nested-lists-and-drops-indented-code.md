---
id: T-121
title: The quick-view renderer flattens nested lists and renders indented code as paragraphs
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-070, T-107, T-110, T-179]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-13
updated: 2026-08-18
shipped_in: 0.5.0
deliverables: [tools/deck/quickview.py]
---

# T-121 — The quick-view renderer flattens nested lists and renders indented code as paragraphs

# 1. Specify

**Outcome**
A nested list keeps its nesting and an indented code block stays code, in a quoted source read
inside a deck.

**The mechanism, measured**
[T-107](T-107-quickviews-markdown-renderer-drops-thematic-breaks.md) audited `markdown()` against
the 355 markdown documents in the source corpus — counts only, no content copied. Two constructs
are used and unhandled:

| Construct | Lines | Documents | What `markdown()` does |
| :--- | ---: | ---: | :--- |
| nested list item | 995 | 125 | matched by the item branch and appended to the flat list, so two levels render as one |
| indented code block | 958 | 124 | falls through to the paragraph case and renders as prose |

**Both are state, not a branch.** A thematic break, an ordered list and front matter were each one
branch and landed in T-107. Nesting needs the renderer to hold a stack rather than one list, and an
indented block needs it to distinguish a continuation line inside a list item from a code block —
which is why the same audit fixed three constructs and left these two.

**The indented-code count is an upper bound.** The pattern also matches a wrapped list continuation,
which is legitimately not code. Part of this task is separating them; a fix that turns every
continuation line into a `<pre>` is worse than the defect.

**Scope**
- In: nested lists, to the depth the corpus uses.
- In: indented code blocks, distinguished from list continuations.
- In: a self-test fixture per construct, as T-107 established — one fixture per construct the corpus
  uses, not per construct someone remembered.
- Out: adopting a Markdown library. **L-07** stands and the gap was never conversion quality.
- Out: setext headings. The corpus uses `===` zero times and `---`-under-text once in 355
  documents, which is why T-107 reads `---` as a thematic break with no ambiguity to resolve.
- Out: link reference definitions and footnotes — zero occurrences in the corpus.
- Out: what any of it looks like — [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md).

**Inputs**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `markdown()` and its self-test, whose
  docstring already names both gaps and their counts.
- [T-107](T-107-quickviews-markdown-renderer-drops-thematic-breaks.md) §3 — the full audit table.

**Acceptance criteria**
- [ ] A two-level list renders as a nested `<ul>`/`<ol>`, not as one flat list
- [ ] An indented code block renders as `<pre>`, and a wrapped list continuation does not
- [ ] The self-test covers both and fails if either branch is removed
- [ ] The count in `markdown()`'s docstring is removed or restated, not left describing a fixed gap

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Separate real indented code from list continuations in the corpus count | the true number |
| 2 | Hold a list stack rather than one list | `quickview.py` |
| 3 | The indented-block branch, guarded by whether a list is open | `quickview.py` |
| 4 | A fixture per construct, and each proven to fail without its branch | self-test |

## 3. Implement

**Step 1's answer: the upper bound, split**
Counted 2026-08-18 over the same tree T-107 read, excluding `_export/` and backup folders. **Counts
only: nothing was copied, quoted or written to disk** (`CLAUDE.md`, *Publishing constraints*). The
scan reads **357** documents where T-107 read 355, and reproducing T-107's own definitions gives
1093 and 810 against its 995 and 958 — near enough to be the same population, not near enough to
quote as the same number, so both are stated.

| | Lines | Documents |
| :--- | ---: | ---: |
| matches the indented pattern (T-107's upper bound, reproduced) | 810 | 111 |
| — of those, inside a fence, so already handled | 146 | — |
| — **real indented code** | **435** | 81 |
| — **wrapped list continuation, which must not become `<pre>`** | **229** | 27 |
| nested list items (T-107's definition, reproduced) | 1093 | 110 |
| deepest nesting the corpus uses | 4 levels | — |

**34% of everything the pattern matches is not code.** That is the number §1 asked for, and it is
what makes the guard the fix rather than a refinement of it: the naive branch §1 warned against
would have been wrong about a third of its own population.

**Decisions & assumptions**
- **A blank line no longer ends a list; the line after it does** — 2026-08-18. Not in §1's scope and
  taken anyway, for two reasons. The measurement above treats a blank line as not ending the list,
  so leaving the renderer disagreeing would have made the 34% a fact about the counting script and
  not about `markdown()` — a number with no home, which is worse than no number. And code indented
  *inside* a list item was unreachable without it: the item was already closed by the time the block
  arrived, so it landed at top level with its indentation half-stripped. A side effect worth naming:
  a loose list now renders as one `<ul>` instead of one `<ul>` per item.
- **A changed marker at the same indent starts a new list** rather than continuing the open one, so
  a `-` list followed by a `1.` list stays two lists — 2026-08-18.
- **The self-test's guarantee is proven by removing each branch, not asserted** — 2026-08-18. Four
  mutants, each disabling one branch, plus an unmutated control. The control is not ceremony: the
  first run of the harness reported 4 of 4 caught while **every mutant was dying at import**, and
  only the control exposed it (**audit with a second instrument**). Corrected, the control survives
  and all four mutants are caught by a real `SELF-TEST FAILED`.
- **The two shipped decks keep the old rendering, and that is a tool gap, not an oversight** —
  2026-08-18. See §4.

**Outputs produced**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `markdown()` holds a list stack and an
  indented-code buffer; four new self-test fixtures.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A two-level list renders as a nested `<ul>`/`<ol>`, not as one flat list | met | Fixtures cover three levels and an `<ol>` inside an `<ol>`; the corpus's deepest is 4 and renders correctly. Looked at in the deck, below |
| An indented code block renders as `<pre>`, and a wrapped list continuation does not | met | The 229-line population is what the guard is written against; both fixtures fail if either branch is removed |
| The self-test covers both and fails if either branch is removed | met | 4 of 4 mutants caught, control survives — §3 |
| The count in `markdown()`'s docstring is removed or restated, not left describing a fixed gap | met | Restated as the split, with the 357-vs-355 denominator named so it cannot be misread as T-107's figure |

**Looked at, offline** — `CLAUDE.md` rule 6, `TASK-WORKFLOW.md` §7 step 3. A probe source carrying
all four constructs was embedded in a throwaway copy of the reference deck and captured in real
Chrome through `tools/deck/render.py`, with L-110's re-arming opener because a shut disclosure is
`display:none` and a capture that walks to a slide closes the view. Both halves read correctly:
three-level nesting indents and keeps its markers, the nested `<ol>` numbers, the indented block is
a themed `<pre>` that keeps its internal blank line and its relative indentation, code inside a list
item sits inside the item at the text column, and the wrapped continuation is one bullet rather than
a code block. Nothing was written back to the repository.

**What this fix does not reach, and why it is a separate record.** Rendering the 8 sources the
shipped decks already carry through the old and new renderer shows **4 of 8 render differently** —
and the old output is materially wrong, not merely plainer: a wrapped list item came out as
`<li>first line</li></ol><p>the rest of the sentence</p><ol>`, one sentence split across an item and
a paragraph, one `<ol>` shattered into three. `measure-first` carries four of those; `sort-window`'s
three sources are unaffected and render byte-identically. The fix cannot be delivered to them,
because `quickview.py add` refuses a source already wired — `item_pattern` matches only a bare
provenance item — and no verb refreshes one. Proved by running it, not inferred from the regex.
That is a gap in the tool rather than in this fix, and every future renderer change meets it again,
so it is [T-179](T-179-a-quick-view-cannot-be-refreshed-after-the-renderer-changes.md).

**Child fix tasks raised**
- [T-179](T-179-a-quick-view-cannot-be-refreshed-after-the-renderer-changes.md) — a quick view
  cannot be refreshed after the renderer changes.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → done | Specified, planned, implemented and reviewed in one sitting; §1 was already complete and carried no open question, which is why it was first on the unattended list. The corpus split that §1 asked for came back **34% continuations**, which decided the shape of the fix rather than confirming it. Two things were not in §1 and are recorded in §3: a blank line no longer ends a list, without which the measurement and the renderer would have disagreed; and the branch coverage is proven by mutation rather than asserted, after the first harness reported a clean sweep it had never made. The fix does not reach the two shipped decks — [T-179](T-179-a-quick-view-cannot-be-refreshed-after-the-renderer-changes.md). |
| 2026-08-13 | → proposed | Raised out of T-107's corpus audit, which counted every block construct across 355 source documents and fixed the three that were one branch each. These two change how the renderer holds state, so they are separated rather than bundled into an `xs` fix. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: a deck that hits this renders a quoted source flatter than it was, which is a fidelity loss rather than a broken deck, so it is not a defect that reopens `PH1`. |
