---
id: T-093
title: DS-005's check bans the one ESM route R6 measured as working
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-019, T-069]
work_package: v0.3
owner: maintainer
business_value: medium
effort: s
created: 2026-08-11
updated: 2026-08-11
deliverables: []
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
- Does `fetch('data:...')` belong on the permitted side too? R6 §2 measures it passing and it reads
  no file, but nothing in the repository needs it — deciding it now would be inventing a case.
  *Recommend: permit it, on the same argument, and say so in the check's docstring.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | State what DS-005 forbids as a predicate over the argument, not over the function name | the rule, in one line |
| 2 | Rewrite the predicate; fixtures for each side, both directions (**L-04**) | `audit.py` |
| 3 | Confirm a deck carrying the `esm` preflight row passes, and both example decks are unchanged | evidence |

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
| 2026-08-11 | → proposed | Created from [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) §3, which found it by writing a preflight row that probes `import()` and noticing the row could never ship. `v0.3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: it is not a defect an adopter hit in the published plugin — no deck can reach it — and v0.2 has shipped, so everything that is not such a defect goes to v0.3 whatever its size. |
