---
id: T-107
title: quickview.py's Markdown renderer drops thematic breaks, shipping "---" as body text
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-070, T-110, T-121, T-122]
work_package: PH1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-12
updated: 2026-08-13
shipped_in: 0.2.3
deliverables:
  - tools/deck/quickview.py
  - shell/components.css
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

**The audit, and its verdicts**
Every block construct counted across **355 markdown documents** in the source corpus — the real
population, not this repository's seven example sources, which use headings and tables and nothing
else. **Counts only: nothing was copied, quoted or written to disk** (CLAUDE.md, *Publishing
constraints*).

| Construct | Lines | Documents | `markdown()` before | Verdict |
| :--- | ---: | ---: | :--- | :--- |
| ATX heading | 3647 | 350 | `<h1>`–`<h3>` | ok |
| unordered list item | 6707 | 324 | `<ul>` | ok |
| table row | 6222 | 196 | `<table>` | ok |
| **ordered list item** | **1994** | **161** | matched, emitted as `<ul>` | **fixed here** |
| **YAML front matter** | — | **130** | rendered as body text | **fixed here** |
| **thematic break** | **721** | **119** | `<p>---</p>` — the reported defect | **fixed here** |
| nested list item | 995 | 125 | flattened to one level | [T-121](T-121-the-quick-view-renderer-flattens-nested-lists-and-drops-indented-code.md) |
| indented code block | 958 | 124 | rendered as paragraphs | [T-121](T-121-the-quick-view-renderer-flattens-nested-lists-and-drops-indented-code.md) |
| fence | 446 | 91 | `<pre>` | ok |
| blockquote | 497 | 83 | `<blockquote>` | ok |
| HTML block | 23 | 12 | made inert | deliberate (T-070 test 2) |
| setext heading, `---` under text | **1** | **1** | read as a thematic break | ok — see below |
| setext heading, `===` | 0 | 0 | not handled | no subject |
| link reference definition | 0 | 0 | not handled | no subject |
| footnote definition | 0 | 0 | not handled | no subject |

**The `---` ambiguity is measured away rather than argued about.** A `---` directly under a line of
text is a setext H2 in CommonMark, so a naive thematic-break branch could turn headings into rules.
The first count said 131 documents did that — and all 131 were the *closing* line of YAML front
matter, one per document. Excluding front matter, the whole corpus contains **one** setext underline,
in one document. So `---` is read as a thematic break, and front matter is consumed before the body
is scanned.

**Front matter was not optional once the break branch landed.** Before this task a leading `---`
block rendered as a paragraph of `key: value` runs; after a break branch and nothing else it would
have rendered as *two rules around* that paragraph, which is worse than the defect. It renders as a
key/value table instead — dropping content out of a quoted source is the one thing a surface
carrying a fidelity claim must not do.

**Decisions & assumptions**
- **Three constructs fixed here, two split out.** A thematic break, an ordered list and front matter
  are each one branch. Nested lists need a stack and indented code needs the renderer to tell a
  continuation line from a code block; both change how it holds state, which is not an `xs` fix —
  2026-08-13.
- **`<hr>` and the list markers get the plainest themed value the theme allows**, not a considered
  one. The global reset carries `list-style:none`, so an `<ol>` was rendering without the numbers
  that made it ordered; restored inside `.qv-doc` only. What any of it should look like is
  [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md)'s, and that task
  names `<hr>` in its scope already — 2026-08-13.
- **The self-test now carries one fixture per construct the corpus uses**, each naming the construct
  and its corpus count in the failure message. That is the actual lesson: the renderer's coverage was
  honest and its self-test was narrower, so **L-04**'s guarantee was narrower than it read —
  2026-08-13.

**Outputs produced**
- [`tools/deck/quickview.py`](../tools/deck/quickview.py) — `front_matter()`, the thematic-break
  branch, `<ol>` versus `<ul>`, and the widened self-test.
- [`shell/components.css`](../shell/components.css) — `.qv-doc hr`, `.qv-doc ul`, `.qv-doc ol`, and
  the same block in both shipped decks and the seeded fixture.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `markdown("a\\n\\n---\\n\\nb")` produces an `<hr>` and no paragraph of hyphens | met | `<p>a</p><hr><p>b</p>`. `***` and `- - -` give the same, and the self-test asserts `<p>---</p>` is absent |
| The self-test covers `---` and fails if the branch is removed | met | Branch deleted, tool run: **exit 1**, `SELF-TEST FAILED: the Markdown renderer dropped a thematic break, in 119 of 355 corpus documents`. Restored, exit 0 |
| The audit is written down with a verdict per construct | met | The fifteen-row table above, counted across 355 corpus documents rather than asserted |
| `<hr>` inside `.qv-body` renders themed, and has a contract row if it needed one | met | Measured in real Chrome: `1px rgb(215, 209, 194)` — `--line`, not the browser's grey. No new contract row: these are element selectors under a class that already has one. **It took [T-122](T-122-the-quick-views-contracted-article-is-never-created-so-seventeen-rules-are-dead.md) to get there** — the rule was themed all along and matched nothing |
| `quickview.py` self-test green; `check.py` green | met | Both, inside `python tools/check_all.py` on both shipped decks |
| Opened and looked at, offline | met | A probe deck carrying a source with every construct, `file://`, DNS black-holed, at 1920 and 1280: front matter as a table, numbered steps, bullets, a hairline rule where `---` was |

**Child fix tasks raised**
- [T-121](T-121-the-quick-view-renderer-flattens-nested-lists-and-drops-indented-code.md) — nested
  lists and indented code, the two constructs the audit found that are not one branch each. `PH3`.
- [T-122](T-122-the-quick-views-contracted-article-is-never-created-so-seventeen-rules-are-dead.md) —
  found while verifying *renders themed*, and closed here because this task could not meet that
  criterion without it. `PH1`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | The reported construct plus two more the audit found in the same class, all three one branch each: thematic breaks (119 of 355 corpus documents), ordered lists rendered as `<ul>` (161), and YAML front matter rendered as body text (130). Two that are not one branch went to T-121. **The audit was the deliverable, not the `<hr>`** — it also settled the `---`-versus-setext ambiguity by counting it: one setext underline in 355 documents, and the 131 that looked like more were all front-matter closers. Verifying *renders themed* found T-122, without which the criterion could not be met. |
| 2026-08-12 | → proposed | Created. Reported by the first adopting project against published `0.2.2`: 7 literal `<p>---</p>` and 0 `<hr>` in its deck. Scoped past the one construct to the self-test's coverage, which is what let it through. |
| 2026-08-13 | (no change) | **Shipped in `0.2.3`.** `shipped_in` read `unreleased` until this sweep: the closing commit `788742a` is contained in `v0.2.3`, which is what the field holds (TASK-WORKFLOW.md §3). Found by reconciling the board after the `0.2.3` release rather than by a check - nothing validates the field against the tags. |
