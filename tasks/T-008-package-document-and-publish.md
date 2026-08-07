---
id: T-008
title: Package, document and publish
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-002, T-004, T-005]
related: []
work_package: final
owner: maintainer
created: 2026-08-04
updated: 2026-08-07
deliverables: []
---

# T-008 — Package, document and publish

## 1. Specify

**Outcome**
An installable plugin with an honest README and a fresh example deck.

**Why this one**
The example deck must be written new on a neutral topic — the corpus is real training work for named scenarios and none of its content may be copied here.

**Acceptance criteria**
- [ ] Install instructions end with a command that proves it runs
- [ ] Example deck written fresh, on a neutral topic
- [ ] Renders offline
- [ ] No personal, client or machine data anywhere
- [ ] Installs from a clean clone

**Open questions**
- ~~Marketplace plugin, plain skill package, or both?~~ **Answered 2026-08-07 by the owner: both,
  as one artifact.** Publish the plugin — [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json)
  and the marketplace entry — **and** keep [`skills/htmldeck/`](../skills/htmldeck/SKILL.md)
  self-contained enough that copying the directory alone works. It is one build, not two: the
  scaffold [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md) stood up is already a
  plugin, and the marketplace listing is the only route that ends in *"a command that proves it
  runs"* — criterion 1 above. **What the second half costs is a rule, not a package**: every path
  the skill resolves goes through `${CLAUDE_PLUGIN_ROOT}`, so a copied directory finds its own
  references. That is testable from a clean clone and belongs in the criteria below when this task
  is planned.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | (no change) | **The packaging question is answered: both, as one artifact** — plugin plus marketplace entry, with the skill directory kept self-contained. It adds no second package and one testable rule: every path resolves through `${CLAUDE_PLUGIN_ROOT}`, which a clean clone can check. **One thing this makes concrete for the example deck.** Criterion 2 asks for a fresh deck on a neutral topic; [`examples/reference-deck.html`](../examples/reference-deck.html) is exactly that and is **183 KB**, so whichever form ships, the package carries it — worth measuring against the marketplace listing rather than discovering at publish time. |
| 2026-08-07 | (no change) | **The release gate is clear: [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) closed and its `blocked_by` edge is removed.** `BRIEF.md`'s seventh criterion is met — all twelve slides of the reference deck carry a bottom line, and DS-202/203/205/216/217 are gated rather than asserted. **Two blockers remain, both about modes this repository does not have yet** — T-005's build check and T-004's critique mode — so publishing is no longer waiting on the example deck, only on the plugin's own two halves. One thing to carry into packaging: the deck is **183 KB**, not the 178 KB `BRIEF.md` recorded before the rewrite. |
| 2026-08-07 | (no change) | **Two blockers added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md), both taken from [`BRIEF.md`](../docs/BRIEF.md)'s own definition of done.** [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) is the *Release gate*, settled by the owner 2026-08-06 and until now recorded **in prose with no edge representing it** — the precise drift `blocked_by` exists to prevent, and the strongest finding of the audit. [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) is criterion 2 on the same list, equally open and equally a gate on shipping; it was `related`, which does not gate. Both bind publishing and nothing else, which is what this task is. `related` is now empty because its only entry became a blocker. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
