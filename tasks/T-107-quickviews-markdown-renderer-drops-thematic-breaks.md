---
id: T-107
title: quickview.py's Markdown renderer drops thematic breaks, shipping "---" as body text
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-070, T-110]
work_package: PH1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - tools/deck/quickview.py
---

# T-107 — quickview.py's Markdown renderer drops thematic breaks, shipping "---" as body text

## 1. Specify

**Outcome**
A `---` in a source document becomes a rule in the quick view. Today it becomes a paragraph
containing three hyphens, and the deck ships it.

**The mechanism, measured**
In the first deck built on the published plugin:

```
7    <p>---</p>
0    <hr
```

[`tools/deck/quickview.py`](../tools/deck/quickview.py) `markdown()` states its own coverage in its
docstring — *"Headings, paragraphs, lists, tables, quotes and fences"*. Thematic breaks are not on
that list and there is no branch for them, so `---` falls through to the paragraph case and is
emitted as literal text. The renderer is doing exactly what it says; what it says is short by one
construct that every source document in the corpus uses.

**Why it survived.** The self-test at the foot of the same file exercises headings, bold, code,
lists and tables. It does not exercise `---`, so the gap was never a failure — which is the
interesting half of this defect. **L-04** makes the tool refuse to report if its self-test fails; a
self-test that omits a construct makes that guarantee narrower than it reads.

**Scope**
- In: a thematic-break branch in `markdown()`, emitting `<hr>`.
- In: the self-test gains a `---` case, so the construct cannot silently regress.
- In: **an audit of `markdown()` against the constructs the corpus source documents actually use**,
  because one omission found by an adopter is evidence about the self-test's coverage, not about
  this one construct (**record the rule, not the instance**). Anything else missing is fixed here or
  raised as a child task with a reason.
- In: `<hr>` gets a style rule if it does not already have one — `.qv-body` is required by contract
  to style every element it may contain.
- Out: how the rule *looks* beyond being visible and themed —
  [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md).

**Inputs**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `markdown()` and its self-test.
- [`shell/components.css`](../shell/components.css) — the `.qv-body` block, which claims to style
  every element a source may contain.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — DS-229's completeness half: every
  class the shared style block styles has a contract row.
- [T-070](T-070-the-quick-view-for-a-source-document.md) — the feature and its three admission tests.

**Acceptance criteria**
- [ ] `markdown("a\n\n---\n\nb")` produces an `<hr>` and no paragraph of hyphens.
- [ ] The self-test covers `---` and fails if the branch is removed.
- [ ] The audit of `markdown()` against corpus constructs is written down in §3, with a verdict per
      construct — not a claim that it was done.
- [ ] `<hr>` inside `.qv-body` renders themed, and has a contract row if it needed one.
- [ ] `python tools/deck/quickview.py` self-test green; `python tools/deck/check.py` green.
- [ ] Opened and looked at, offline.

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | List the block constructs used across the corpus source documents | the coverage target |
| 2 | Diff that list against `markdown()`'s branches | the real gap, `---` included |
| 3 | Implement the missing branches | `quickview.py` |
| 4 | Extend the self-test to every construct in step 1 | `quickview.py` |
| 5 | Style and contract-row anything newly emitted | `components.css`, contract |
| 6 | Re-render a source quick view and look at it offline | verdict |

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created. Reported by the first adopting project against published `0.2.2`: 7 literal `<p>---</p>` and 0 `<hr>` in its deck. Scoped past the one construct to the self-test's coverage, which is what let it through. |
