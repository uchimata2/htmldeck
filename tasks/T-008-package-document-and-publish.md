---
id: T-008
title: Package, document and publish
type: deliverable
status: done
phase: review
parent: null
blocked_by: [T-002, T-004, T-005, T-056]
related: [T-050]
work_package: PH1
shipped_in: 0.1.1
owner: maintainer
created: 2026-08-04
updated: 2026-08-12
deliverables:
  - .claude-plugin/marketplace.json
  - README.md
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
- [ ] **Human-facing text has been humanized, and nothing agent-facing has been** — `CLAUDE.md`
      *Publishing constraints*, and [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) for the
      covered-set test, the exclusions and the owner's verbatim exception. **This criterion belongs
      to every release, not to this task**: closing T-008 retires the blocker edge and not the rule.
      For the first release it is already satisfied for `README.md`, by
      [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md)
- [ ] **The repository description is set to the drafted text, not written at the console.** It is in
      [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) §3, humanized and
      recorded with its draft and audit. It is covered by the rule above, so a description typed
      fresh into the GitHub field at push time is an **unhumanized human-facing text** and fails this
      task's own criterion. Copy it; do not retype it

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
| 1 | Settle what `master` becomes, by measuring rather than trusting the log below | The measurement, in §3 |
| 2 | Scan the tracked tree for personal, client and machine data, and decide the author identity **before** the first push | The scan, and the owner's answer, in §3 |
| 3 | Write the marketplace entry, without which the install route does not exist | `.claude-plugin/marketplace.json` |
| 4 | Humanize the two listing descriptions, which `PUBLISHING.md` §2 covers and nothing had applied to them | The edited `plugin.json`, recorded in §3 |
| 5 | Add install instructions ending in a command that proves the package | The new `README.md` section |
| 6 | Re-derive the README figures the preceding steps moved | `task.py check` output, in §3 |
| 7 | Create the repository, push `master`, set the description from [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) §3 | The remote |
| 8 | Tag `v0.1.0` and cut the GitHub release | The tag and the release |
| 9 | `task.py index`, `check --closing`, `check_scaffold.py`, and a clean-clone run | The output of each |

**Decisions — shape**

- **The description is copied from T-056 §3, never retyped.** It is human-facing text by
  `PUBLISHING.md` §2's own test, so typing a fresh one at the console publishes an unhumanized
  document and fails this task's criteria while looking like it passed.

## 3. Implement

**Decisions & assumptions**

- **`master` was never divergent, and the log below was wrong — 2026-08-09.** The 2026-08-09 row
  says *"`master` is 96 commits divergent and sits at the line-endings scaffold"*. Measured:
  `git rev-list --left-right --count` returns **0 119**, and the merge base **is** `master`'s HEAD.
  Master had **zero** commits the work lacked, so it was a strict ancestor and the publish is a
  plain `--ff-only` fast-forward. Nothing was discarded, no history was rewritten for this, and no
  force was needed. **The feared decision did not exist**; it was a misreading of "96 commits
  behind" recorded once and then cited as fact three times.

- **119 of 121 commits carried the owner's personal email, and it was rewritten before the first
  push — 2026-08-09.** The owner chose the GitHub noreply address. This is irreversible after
  publication: GitHub caches commits that force-pushes remove, and a fork keeps them regardless.
  Doing it while the repository was still local cost one command and no coordination. The two
  `maintainer@localhost` commits were left alone, being generic rather than personal.

- **The tracked tree is clean of personal, client and machine data — 2026-08-09.** Scanned for
  absolute paths, home directories, usernames and email addresses. Every hit was a false positive:
  the `Home`/`End` **keyboard keys** in DS-131 and the research notes, and one `/home/user/` string
  inside `check_scaffold.py` that is a fixture asserting absolute paths are *rejected*. The corpus
  knowledgebase, the live handoff and printed PDFs are all gitignored by construction.

- **The marketplace entry did not exist, and without it the install route did not either —
  2026-08-09.** `.claude-plugin/plugin.json` alone makes a plugin that can be copied, not one that
  can be installed by name. The 2026-08-07 answer above promised *"the plugin and the marketplace
  entry"* and only the first half had been built. `marketplace.json` now declares one plugin at
  `source: "./"`, which is where the components already sit.

- **`PUBLISHING.md` §2 caught its first real defect the day after it was written — 2026-08-09.** The
  `plugin.json` description is *marketplace listing text*, which §2 names explicitly, and it
  contained an em dash. It had never been through the humanizer because nothing had thought of a
  JSON string as prose. **This is the covered-set test working as designed**: a list of filenames
  would have said `README.md` and missed it, and the test asks where the reader is standing instead.
  Both descriptions are now clean.

- **The install section points at the existing output block rather than pasting a second copy —
  2026-08-09.** *Run it* already prints what `check_scaffold.py` says. Pasting it again would create
  two copies of one derived fact updated at different times, which is **L-13** and the mechanism
  behind **L-52**, in a document that had just been cured of exactly that.

**Outputs produced**
- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json` (description only)
- `README.md` (the *Install it* section)

## 4. Review

Verified against a clone of the **published** repository rather than the working tree, because
"installs from a clean clone" is a claim about what GitHub serves, not about what is on this machine.

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Install instructions end with a command that proves it runs | **met** | `README.md` *Install it*, ending in `check_scaffold.py`. Run from a fresh clone of the public repo: 10 of 10 fixtures, manifest valid, every `${CLAUDE_PLUGIN_ROOT}` pointer resolves |
| Example deck written fresh, on a neutral topic | **met** | Two of them. Riverbend and Marnfield are both illustrative and both say so on the deck; no corpus content was copied |
| Renders offline | **met** | `check.py` drives real Chrome headless with a throwaway profile and **every DNS lookup black-holed**, which is the offline test rather than a proxy for it. Both decks: `0 failure(s)`. Human inspection of the rendered decks was done under [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) and [T-002](T-002-build-mode-the-self-contained-deck-generator.md); **this task changed no deck**, so it inherits that rather than re-claiming it |
| No personal, client or machine data anywhere | **met, and it was not free** | The tracked tree scanned clean. The **history was not**: 119 of 121 commits carried the owner's personal email, and were rewritten to the GitHub noreply address before the first push. Confirmed on the published tip through the API, and in a clone from GitHub: the only two addresses in the published history are the noreply one and `maintainer@localhost` |
| Installs from a clean clone | **met** | Cloned from `https://github.com/uchimata2/htmldeck.git`; `check_scaffold.py` and `task.py check` both pass with no path editing |
| Human-facing text humanized, nothing agent-facing | **met** | `README.md` under [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md); the two listing descriptions and the release notes under this task, all three at zero em dashes. `SKILL.md` is untouched at 5 206 bytes |
| The description is the drafted text, not retyped | **met** | Passed to `gh repo create --description` as the exact string from [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) §3 |

**What is published**

| | |
| :--- | :--- |
| Repository | `https://github.com/uchimata2/htmldeck`, public, default branch `master` |
| Release | `v0.1.0`, not a draft, not a prerelease |
| Install | `/plugin marketplace add uchimata2/htmldeck` then `/plugin install htmldeck@htmldeck` |

**One thing the tag does not contain.** `v0.1.0` was cut before this section was written, so the
released tree carries T-008 at `in_progress`. That is the honest ordering: several criteria above are
claims about the published artifact and could not be verified until it existed. The tag marks the
released code, and the task record catches up behind it rather than being back-dated into it.

**Child fix tasks raised**
- none. [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md) already
  covers the one standing risk, which is that the README's pasted figures drift again.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Published: `https://github.com/uchimata2/htmldeck`, public, `master` as default, released as `v0.1.0`.** Three things were not what the record said. **`master` was never divergent** — the row below says 96 commits divergent at the line-endings scaffold and it was cited three times as a decision to be taken; measured, `rev-list --left-right` returns `0 119` and the merge base is `master`'s own HEAD, so it was a strict ancestor and publishing was a fast-forward that discarded nothing. **The marketplace entry did not exist**, so the install route promised on 2026-08-07 was half-built: `plugin.json` alone makes a plugin that can be copied, not one installable by name. **And 119 of 121 commits carried the owner's personal email**, which was rewritten to the GitHub noreply address before the first push, on the owner's decision — irreversible afterwards, because GitHub caches commits that force-pushes remove and forks keep them regardless. `PUBLISHING.md` §2 also caught its first live defect: the `plugin.json` description is marketplace listing text, it carried an em dash, and a covered set written as a list of filenames would have missed it. Every criterion verified against a clone of the published repository rather than the working tree. |
| 2026-08-09 | → in_progress | Unblocked: all four blockers closed. Planned in nine steps, opening with two measurements rather than two assumptions — what `master` actually is, and what the tracked tree and the history actually contain — because both were about to become irreversible. |
| 2026-08-09 | (no change) | **The fourth blocker is cleared and it left this task an artifact.** [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) closed, so **publishing now waits on nothing** — all four blockers are done and the only open PH1 task is this one. Two things landed here rather than being described. The **repository description is drafted, humanized and recorded** in T-056 §3, which closes the gap the row below identified: an output this task needs at publication that nothing here produced. It is now a criterion, worded so that retyping it at the console is a visible failure rather than a quiet one, because a description typed fresh into the GitHub field is an unhumanized human-facing text by the rule's own test. And the humanizing criterion now points at [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) rather than at T-056: the rule outlives the task, and a criterion pointing at a closed task is the spent-edge failure one level up. |
| 2026-08-09 | (no change) | **Gained a fourth blocker, [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md)** — the humanizing rule for the documents a stranger reads before installing anything, adapted from the taskmd project at the owner's request. A blocker rather than a follow-up, on the source task's reasoning: after publishing, the first impression has been made. It also lands one output *inside* this task's step list — T-056 step 4 drafts the repository description, which is text this task needs at publication and which nothing here currently produces. |
| 2026-08-09 | (no change) | **Publishing is deliberately held until there is a first publishable version** — the owner's decision, 2026-08-09, taken when [T-050](T-050-write-the-repository-readme.md) made the repository presentable and the question *push it now?* became live. It changes no edge: this task's two remaining blockers are already **T-002** and **T-004**, the two modes the README names as unbuilt, and *mature enough to publish* is that same line seen from the other side. **Three facts about the repository state that whoever publishes will need, none of them obvious from the task record.** There is **no git remote configured at all** — every commit of this project is local, so publishing is a create-and-push, not a push. The work lives entirely on `build/wp2-design-system-and-reference-deck`; **`master` is 96 commits divergent and sits at the line-endings scaffold**, so publishing without deciding what `master` becomes lands a visitor on a repository with no README and none of the ruleset. And the deck's own *Example deck written fresh, on a neutral topic* criterion is **already met** by [`examples/reference-deck.html`](../examples/reference-deck.html) — Riverbend is illustrative and the README says so — which is worth noticing before it is re-planned as outstanding work. |
| 2026-08-09 | (no change) | **The deck is 214 KB, not the 183 KB the two 2026-08-07 rows below state.** Those rows are left as written — they record what was measured on the day, before [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md), [T-034](T-034-a-contents-page-for-the-printed-deck.md) and [T-035](T-035-the-ruler-navigator.md) added the print mode, the contents page and the ruler — and this row is where a reader picking up packaging finds the current figure. Re-measured by [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md): 219 083 bytes, still zero external references. **The packaging argument is unchanged**: whichever form ships, the package carries one file, and 214 KB is no more of an obstacle than 183 KB was. |
| 2026-08-09 | (no change) | **One blocker cleared and one criterion split out.** [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) closed 2026-08-09, so of the three blockers only build mode and critique mode remain — publishing now waits on the two modes and nothing else. **The README leaves this task** as [T-050](T-050-write-the-repository-readme.md), raised by [T-042](T-042-audit-the-whole-repository-against-itself.md): the outcome above asks for *"an installable plugin with an honest README"*, and a README depends on neither blocker — it describes what exists and names the two modes as unbuilt, which is a sentence rather than a gate. What stays here is install, the marketplace entry and the publish itself, all of which genuinely do wait. `related` gains T-050. |
| 2026-08-07 | (no change) | **The packaging question is answered: both, as one artifact** — plugin plus marketplace entry, with the skill directory kept self-contained. It adds no second package and one testable rule: every path resolves through `${CLAUDE_PLUGIN_ROOT}`, which a clean clone can check. **One thing this makes concrete for the example deck.** Criterion 2 asks for a fresh deck on a neutral topic; [`examples/reference-deck.html`](../examples/reference-deck.html) is exactly that and is **183 KB**, so whichever form ships, the package carries it — worth measuring against the marketplace listing rather than discovering at publish time. |
| 2026-08-07 | (no change) | **The release gate is clear: [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) closed and its `blocked_by` edge is removed.** `BRIEF.md`'s seventh criterion is met — all twelve slides of the reference deck carry a bottom line, and DS-202/203/205/216/217 are gated rather than asserted. **Two blockers remain, both about modes this repository does not have yet** — T-005's build check and T-004's critique mode — so publishing is no longer waiting on the example deck, only on the plugin's own two halves. One thing to carry into packaging: the deck is **183 KB**, not the 178 KB `BRIEF.md` recorded before the rewrite. |
| 2026-08-07 | (no change) | **Two blockers added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md), both taken from [`BRIEF.md`](../docs/BRIEF.md)'s own definition of done.** [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) is the *Release gate*, settled by the owner 2026-08-06 and until now recorded **in prose with no edge representing it** — the precise drift `blocked_by` exists to prevent, and the strongest finding of the audit. [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) is criterion 2 on the same list, equally open and equally a gate on shipping; it was `related`, which does not gate. Both bind publishing and nothing else, which is what this task is. `related` is now empty because its only entry became a blocker. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
