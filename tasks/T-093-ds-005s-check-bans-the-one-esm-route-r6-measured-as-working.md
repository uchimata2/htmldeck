---
id: T-093
title: DS-005's check bans the one ESM route R6 measured as working
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-019, T-069]
work_package: v0.3
owner: maintainer
business_value: medium
effort: s
created: 2026-08-11
updated: 2026-08-11
deliverables:
  - tools/deck/audit.py
---

# T-093 — DS-005's check bans the one ESM route R6 measured as working

## 1. Specify

**Outcome**
`audit`'s DS-005 predicate decides the rule DS-005 states rather than a wider one, so a deck that
inlines an ESM library the way [R6](../docs/research/R6-portability-contract.md) §6 measured can pass
the gate.

**Why this one**
The predicate is

```
("DS-005", "no fetch, XHR or dynamic import - element access, not file reads",
 lambda h: not re.search(r"\bfetch\s*\(|XMLHttpRequest|\bimport\s*\(", h)),
```

and the rule is *script may not read a local file's bytes; the renderer may consume them.* **A
`import(blob:)` of source already inlined into the page reads no local file** — R6 §6 measured it
working, at 703 KB for three.js, and DS-006 exists **only** to say how to make it work. So the check
forbids the route two other rules assume.

**This is [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md)'s shape one rule
along**: a predicate reading wider than the rule it implements, and an excusal elsewhere resting on
the wider reading. It is latent rather than live — no build path emits an ESM deck — and it was found
because [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md)'s preflight has an `esm`
row whose probe parses `import("")` to test the syntax. **A deck emitting that row fails DS-005
today**, and the row is the deck asking whether the capability is present, not the deck reading a
file.

**Scope**
- In: narrowing the predicate to what DS-005 forbids — a fetch-like read of a **local file**.
- In: deciding what the narrowed form permits by argument (a `data:`/`blob:` URL) rather than by
  pattern-matching what happens to be in a deck today.
- In: the preflight's `esm` row passing the gate once it can be emitted.
- Out: building an ESM path in build mode. Nothing here asks for one; this is about the gate not
  forbidding it in advance.

**Inputs**
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §5, §6 —
  what is refused, what the substitute is, and the one route that works.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) DS-005, DS-006.
- [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) — the same defect on DS-001,
  and the shape of the fix: cut the exemption exactly as wide as the rule that covers it.

**Acceptance criteria**
- [ ] `fetch('./x')`, `XMLHttpRequest` on a sibling and `import('./x.mjs')` still fail
- [ ] `import(blob:...)` and `import(data:...)` pass, with a fixture for each
- [ ] A deck emitting the preflight's `esm` row passes DS-005
- [ ] Both example decks still pass the whole gate unchanged

**Open questions**
- ~~Does `fetch('data:...')` belong on the permitted side too?~~ **Answered in §4, 2026-08-11:
  yes, and it needed no decision in the end.** The predicate is about the argument rather than the
  call, so one rule covers both kinds and the answer falls out instead of being added.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | State what DS-005 forbids as a predicate over the argument, not over the function name | the rule, in one line |
| 2 | Rewrite the predicate; fixtures for each side, both directions (**L-04**) | `audit.py` |
| 3 | Confirm a deck carrying the `esm` preflight row passes, and both example decks are unchanged | evidence |

## 3. Implement

**Decisions & assumptions**

- **The rule was right and the check was wrong**, so `DESIGN-SYSTEM.md` is unamended — 2026-08-11.
  DS-005 already says *script may not read a local file's bytes*; nothing in it mentions a function
  name. Amending a correct rule to match an over-wide predicate is the failure this repository keeps
  a lesson about, one direction over.
- **Two narrowings, and each is one of the rule's own words** — 2026-08-11. *Script*: only `<script>`
  bodies are read, so a slide saying *import (see the appendix)* is prose rather than a call site
  (**L-67**, and this is the third instance in two days). *Local file*: a file is named by a path, so
  a `data:` or `blob:` URL is not one — those are bytes the page already carries, which is exactly
  what DS-005 permits.
- **A call site whose argument is not a literal is reported and not failed** — 2026-08-11. It cannot
  be decided statically: the working ESM route builds its blob URL into a variable first, which is
  R6 §6's own measured shape. Guessing either way would be the check inventing a verdict, so the row
  prints the count and says how many it could not read. What catches a path arriving through a
  variable is the deck being one file with no siblings to read.
- **Two rows instead of a boolean**, so the count travels in the text — DS-105's reason: *0 naming a
  path, of 0 sites* and *of 12* are the same boolean and not the same fact.
- **The `esm` preflight row now probes a `data:` URL** rather than an empty string. That is an
  improvement rather than a concession: the form R6 §6 measured as working is the form worth asking
  a browser about.

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `fetch_verdicts`, DS-005 out of `STATIC`, the
  absent-subject declaration, and seven fixtures.
- [`tools/deck/check.py`](../tools/deck/check.py) — the producer wired into `gather`.
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `fetch_verdicts` added to
  the static half.
- [`tools/deck/preflight.py`](../tools/deck/preflight.py) — the `esm` row's probe.

**Evidence**

A deck that reaches for an ESM library the way R6 §6 measured, built from the shell:

```
  preflight rows emitted : custom-properties, grid, esm
  the esm row is there   : True

  DS-005   no XMLHttpRequest: script reads bytes the page already carries, never a fi pass
  DS-005   every fetch-like call names an inline URL: 4 site(s), 2 not a literal, 0 n pass

  shell.py check         : clean
  the old predicate      : FAIL - it matched 'import('
```

**And the seeded-defect suite is what caught the one thing this could have broken.** Moving DS-005
out of `STATIC` took it out of `static_variants.static_failures`, which builds the static half from a
list of producers rather than from `check.py`:

```
MISSED - the gate does not check what it says it checks:
  script-reads-a-file          DS-005 not among []
```

With the producer added, `24 of 24 static variants caught`, and the seeded `fetch('data.json')` is
named by its own site:

```
  script-reads-a-file          breaks DS-005  -> CAUGHT
      DS-005   every fetch-like call names an inline URL: 1 site(s), 0 no FAIL
```

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `fetch('./x')`, `XMLHttpRequest` on a sibling and `import('./x.mjs')` still fail | met | Three fixtures, plus the seeded `script-reads-a-file` variant caught end to end by the suite that runs the real static half. |
| `import(blob:...)` and `import(data:...)` pass, with a fixture for each | met | Both, and a fourth for the variable argument — the shape R6 §6 actually measured, which is reported rather than failed. |
| A deck emitting the preflight's `esm` row passes DS-005 | met | Built and run above: three rows emitted including `esm`, both DS-005 rows pass, and the predicate this replaced fails the same deck on the characters `import(`. |
| Both example decks still pass the whole gate unchanged | met | 0 failures, 0 silent, 114-rule partition intact on each, and both DS-005 rows now print `0 site(s)` rather than a bare pass. |

**Open question, answered here**
`fetch('data:...')` is permitted, on the same argument as `import`: R6 §2 measures it passing and it
reads no file. It is not a special case in the code — the predicate is about the argument, so one
rule covers both call kinds and the answer falls out rather than being added.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → done | **The rule was right and the check was wrong, so `DESIGN-SYSTEM.md` is unamended.** DS-005 is about the argument now — only `<script>` bodies are read, and a `data:` or `blob:` URL is bytes the page already carries rather than a local file. A call site whose argument is not a literal is reported and not failed, because R6 §6's own working shape builds the blob URL into a variable and a check cannot decide that statically; the row prints how many it could not read. **The seeded-defect suite caught the one thing this could have broken**: moving DS-005 out of `STATIC` took it out of `static_variants`, whose static half is a hand-kept list of producers rather than `check.py`'s own gather — it reported `MISSED` and named the rule. 24 of 24 static variants caught after wiring it back. The open question dissolved instead of being decided: a predicate over the argument covers `fetch('data:...')` without a case for it. |
| 2026-08-11 | → planned | Three steps: state the rule as a predicate over the argument, rewrite with fixtures in both directions, and confirm a deck carrying the `esm` preflight row passes. |
| 2026-08-11 | → proposed | Created from [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) §3, which found it by writing a preflight row that probes `import()` and noticing the row could never ship. `v0.3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: it is not a defect an adopter hit in the published plugin — no deck can reach it — and v0.2 has shipped, so everything that is not such a defect goes to v0.3 whatever its size. |
