---
id: T-121
title: The quick-view renderer flattens nested lists and renders indented code as paragraphs
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-070, T-107, T-110]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-13
updated: 2026-08-13
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

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised out of T-107's corpus audit, which counted every block construct across 355 source documents and fixed the three that were one branch each. These two change how the renderer holds state, so they are separated rather than bundled into an `xs` fix. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: a deck that hits this renders a quoted source flatter than it was, which is a fidelity loss rather than a broken deck, so it is not a defect that reopens `PH1`. |
