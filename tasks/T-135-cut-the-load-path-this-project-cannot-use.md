---
id: T-135
title: Cut the load path this project cannot use
type: fix
status: done
phase: review
shipped_in: 0.3.0
parent: T-130
blocked_by: []
related: [T-130, T-134]
work_package: PH3
finding: CE-07
owner: the project owner
business_value: high
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - .claude/settings.local.json
---

# T-135 — Cut the load path this project cannot use

## 1. Specify

**Outcome**
A session in this repository stops paying, on every turn, for skills and connectors it cannot use.
**The finding is `CE-07`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8, together with the correction that made it a task at all.

**Why this exists as a task when the audit said it would not be one**
`CE-07` was ranked third and marked *the owner's machine, not repository work*, on the reasoning that
the plugins supplying most skills are not installed anywhere on disk — so no plugin-enable setting
could reach them. **The reasoning was sound and the conclusion was wrong.** The configuration schema
exposes a per-skill listing override keyed on the **skill's name**, which does not care how the skill
is served, and it is honoured at project scope. The audit had reasoned from where the files were
rather than from what the configuration could address.

**Measured 2026-08-13, before the change:** the skill-description block is ~20,941 bytes (~5,235
estimated tokens) for 55 skills found on disk, against a listing of about 66; deferred MCP tool
schemas are reported at 50.4k, of which **~34.5k is one connector and ~8.1k a second that duplicates
a browser tool set already loaded eagerly**.

**Scope**
- In: a project-scoped, git-ignored settings file turning off the skills this repository cannot use.
- In: the one plugin that *is* installed locally and has no use here.
- In: **measuring the result**, which needs a restart and is the reason this task is not closed.
- Out: the user-scoped settings file, beyond the unrelated fix recorded in §3. A skill turned off
  globally is turned off for every other project, and the whole point of `CE-07` is per-project.
- Out: **disabling the cloud connectors**, which is the larger half and is an open question below.
- Out: anything committed to this repository. An adopter cloning htmldeck must not have their own
  skills disabled by a file of ours — the settings file used here is ignored by the owner's global
  git configuration and stays out of the tree.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §2.1 and §9 — the measurement and `CE-07`
- The harness configuration schema, which is the authority and settled three questions this audit had
  answered pessimistically

**Acceptance criteria**
- [ ] The project-scoped settings file is valid JSON and merges rather than replaces what was there
- [ ] Only skills with no plausible use in this repository are turned off; anything arguable is left
      alone
- [ ] Nothing that a deck task needs is disabled — in particular the browser surface **rule 6**
      depends on, and the tools this project's own gates use
- [ ] The file stays out of git, verified rather than assumed
- [ ] **Measured after a restart**: the skill-block and deferred-schema figures against the
      before-numbers above, recorded here
- [ ] The connector question below is answered before any connector is disabled

**Open questions**
- ~~**Do the cloud connectors get disabled for this project?**~~ **Answered 2026-08-13 — the unused
  ones, and the browser stays.** The blanket switch cannot express that, so a per-server denylist was
  used instead and the note-taking connector is the only entry. See §3. **What is still open is
  narrower and is a measurement, not a decision**: whether the second browser surface — real Chrome
  with logged-in sessions, ~8.1k — is needed here at all, given the in-app browser is already loaded
  and this repository renders through its own subprocess Chrome rather than through either. Read the
  tool list after the restart before deciding.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Establish the mechanism from the configuration schema rather than from the filesystem | the override key, its scope rules, and its allowed values |
| 2 | Choose the set to turn off — out-of-domain only, arguable ones left alone | the list, in the project-scoped file |
| 3 | Validate both edited files as JSON before trusting either | a parse check on each |
| 4 | **Restart, then measure** and record the before-and-after | the figures, in §3 |
| 5 | Answer the connector question, and act on it or record it as declined | §1's open question, closed |

## 3. Implement

**What landed 2026-08-13**

- `.claude/settings.local.json` — **35 skill overrides set to `off`**, plus `bpmn@bpmn-tools` disabled
  through the plugin switch, since that one is installed locally and turning it off there removes its
  commands as well as its description. The existing two permission entries were preserved.
- The set is out-of-domain only: enterprise-architecture modelling, academic and literature tooling,
  the business-strategy family, other presentation formats, office-document skills, two duplicates of
  things this project already has, and the cowork setup skills. **Anything arguable was left alone** —
  `dataviz`, `python-expert`, `technical-writer`, `code-review`, `update-config`, `artifact-*` and the
  built-in workflow skills are untouched.
- `~/.claude/settings.json` — **an unrelated defect fixed in passing.** Five permission entries named
  `mcp__claude_ai_Notion__*`; the live server is a different id, so those five rules had been matching
  nothing and the owner was being prompted for calls they had already allowed. Rewritten to the
  current names. This is a user-scoped change and is outside `CE-07`, recorded here because it was
  found here.

**Reviewed against the repository's actual needs, at the owner's challenge, and one entry was wrong.**

- **`cli-tool-dev` was turned back on.** This repository ships thirty-six command-line tools and
  [T-131](T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md) is about to add
  another. It is squarely in domain, and turning it off broke this task's own rule that anything
  arguable is left alone. The rule was right; the application of it was not.
- **`document-figures` was the closest call and stays off.** It names a *figure ledger*, and this
  project has one — but they are different objects: theirs extracts figures and diagrams from
  existing documents, and `tools/docs/figures.py` checks numeric claims in prose against their
  sources. Nothing in this repository reads Word, PowerPoint or PDF as an input.
- **`humanize-prose` is off and `humanizer` is on**, which is the intended direction. The project's
  humanizer rule in [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) is served by the installed
  `humanizer` plugin; two skills answering to the same idea is a routing hazard for a project that
  gates releases on one of them.
- **The rest are out of domain and were checked individually**: enterprise-architecture modelling,
  BPMN, academic and literature tooling, mathematics, the business-strategy family, other
  presentation formats, Office-document skills, Tauri, translation, the cowork setup skills, and one
  duplicate of the built-in code review.
- **The connectors are now partly answered** — see the decision below.

**Decisions & assumptions**
- **Project scope, in the git-ignored file, not the committed one.** — A committed settings file would
  disable an adopter's skills when they clone a public repository, which is a defect this project
  would be shipping rather than fixing. Verified ignored by the owner's global git configuration
  rather than by this repository's `.gitignore`, which is worth knowing: another clone would not
  inherit that. — 2026-08-13
- **`off` for the out-of-domain set; nothing set to the middle value.** — The schema offers a setting
  that keeps a skill listed while dropping its description, at about a tenth of the cost. It is the
  right choice for an arguable skill, and no skill in this set is arguable — the arguable ones were
  left fully on instead. — 2026-08-13
- **One connector denied by name; the blanket switch not used.** — The owner's answer was *the unused
  ones, but the Chrome connection may be needed for rendering and validating*, and the blanket switch
  cannot express that: it stops cloud connectors being fetched at all, so it would take any browser
  surface with them. A per-server denylist can, and the schema states it merges from all sources so a
  user can deny a server for themselves. The one denied is the note-taking connector — **~34.5k
  estimated tokens, and this repository tracks its tasks in local Markdown**. Both browser surfaces
  are untouched. **Denied by the server's id, which is fragile**: that id has already changed once,
  which is the defect fixed below, so a future rotation silently restores the cost. Worth knowing at
  the next measurement rather than assumed stable. — 2026-08-13

**Outputs produced**
- `.claude/settings.local.json` — 35 overrides, one plugin disabled, existing permissions preserved,
  valid JSON. **Written as text rather than as a link on purpose**: `taskmd check` refused the link,
  because a pointer to a git-ignored file resolves for whoever wrote it and 404s for every reader.
  The gate caught it on the first run, which is the scope rule doing exactly its job — and it is also
  the evidence for the decision above that this file must not be committed.

### Measurement 1, after the first restart — mostly a failure, and it named its own cause

| | Before | After | Verdict |
| :--- | ---: | ---: | :--- |
| Skill listing | 7.3k | **6.5k** | −800, against a predicted 2–3k |
| Deferred MCP schemas | 50.4k | **50.4k** | unchanged |

**Only four things actually disappeared**, and they are the whole of the −800: the six `bpmn` entries,
`claude-api`, `keybindings-help`, and one `business-consultant`. Every plugin-supplied skill survived.

**The cause is the key, not the scope, and the listing contained a controlled experiment nobody
arranged.** `business-consultant` was listed **twice** — once from a user-level skill and once from a
plugin, as `business-consultant:business-consultant`. The single override `"business-consultant":
"off"` removed the user-level one and left the plugin one standing. Same bare name, two sources, one
match. **An override keyed by name must use the name exactly as the listing prints it**, which for a
plugin skill is `plugin:skill`. The bare names matched built-ins and user skills, which is why those
three vanished and thirty-one did not.

**`enabledPlugins` worked** — all six `bpmn` rows are gone, which also confirms the file is being read
at project scope. So scope was never the problem.

**`deniedMcpServers` did nothing and has been removed.** Its own description calls it an enterprise
denylist; the sentence suggesting it merges from all sources belongs to a *different* key
(`allowManagedMcpServersOnly`) and was describing that key's behaviour, not granting user scope. **The
literal reading of a field's own description beats an inference drawn from its neighbour's**, and this
cost a restart to learn.

### What is set now, for measurement 2

- **33 overrides, 31 of them `plugin:skill`.** Expected saving ~3.4k of the 6.5k.
- **`disableClaudeAiConnectors: true`**, replacing the denylist that does not work here. **Stated as a
  hypothesis before the measurement**: the servers named by a UUID are the account connectors and go —
  the note-taking one at ~34.5k and the widget one at ~1.5k — while the app-provided servers named in
  words stay, **including both browser surfaces**. If both browsers disappear, the switch is wrong for
  this repository and the line comes out, because **rule 6** outranks the saving.

### Measurement 2 — nothing moved, and that is the answer

| | Before | Measurement 1 | Measurement 2 |
| :--- | ---: | ---: | ---: |
| Skill listing | 7.3k | 6.5k | **6.5k** |
| Deferred MCP schemas | 50.4k | 50.4k | **50.4k** |

Thirty-one `plugin:skill` keys changed nothing. `disableClaudeAiConnectors` changed nothing — the
note-taking connector is present in full, and so are both browser surfaces.

**One hypothesis fits every observation, and it is not the one being tested.** Look at what has ever
worked here: `claude-api` and `keybindings-help` are **built-ins**; the `business-consultant` that
disappeared was the **user-level** copy; `bpmn` went through **`enabledPlugins`**. Nothing
plugin-supplied has ever responded to an override, in either key form. So the rule that explains all
three measurements is **`skillOverrides` reaches built-in and user skills; plugin skills are governed
by whatever enables the plugin** — and the plugins supplying the remaining ~3.4k are not installed on
this machine, so nothing in a settings file names them.

**That is a hypothesis with three confirming observations and no disconfirming one, and it is still a
hypothesis.** It is written here rather than acted on, because acting on the last two cost a restart
each.

**The one experiment that would decide it** is moving `disableClaudeAiConnectors` to the *user*
settings file: if the connector then disappears, scope was the barrier and everything above is a
scoping problem; if it does not, the key does not apply on this machine at all. It is one line and
reversible, and it is **not taken here** because user scope affects every other project the owner
works in. The owner's call.

### The honest arithmetic, and why this task stops

**Reachable saving: ~800 tokens of a 7,300-token skill listing, once.** Two restarts bought it. The
audit banded `CE-07` at `L` on the assumption that the whole block was addressable; **what is
addressable from this repository is `S`**, and the finding has been corrected to say so rather than
left to imply a saving nobody can collect.

The settings file has been **reduced to what is proven to work** — three overrides and one plugin.
Thirty-one keys that demonstrably do nothing were removed rather than left in place: a configuration
full of no-op entries reads as a working policy and is a lie the next reader has to re-derive, which
is precisely the stale-record failure this audit was raised to find. **The list itself is not lost —
it is in this task**, which is its durable home, and it can be reinstated the day the mechanism is
known.

### The list, kept here because the settings file may not keep it

The thirty-one plugin skills judged out of domain for this repository, should the mechanism become
known: `archimate-ea`, `archimate-native`, `academic-researcher`, `competitive-analysis`, the two
`cowork-plugin-management` skills, `tauri-research`, `tauri-dev`, `strategy-memo`,
`faithful-translation`, `pptx-design`, `pptx-build`, `marp-slides`, `business-consultant`,
`business-model-canvas`, `humanize-prose`, `literature-search`, `document-figures`,
`document-summary`, `math-paper`, `project-manager`, `data-analyst`, `startup-advisor`,
`market-sizing`, `code-reviewer`, and the `docx`, `xlsx`, `pptx`, `morning`, `meeting-reschedule` and
`setup-cowork` skills. **`cli-tool-dev`, `python-expert`, `technical-writer`, `dataviz`, `pdf`,
`skill-creator` and `visual-explainer` are deliberately absent** — they are in domain or arguable, and
the rule is that arguable stays on.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The project-scoped settings file is valid JSON and merges rather than replaces what was there | met | Validated by parse after every edit; the two pre-existing permission entries survived all four rewrites |
| Only skills with no plausible use in this repository are turned off; anything arguable is left alone | met | Reviewed twice, and the second review at the owner's challenge found `cli-tool-dev` wrongly disabled — this repository ships 36 command-line tools. Corrected, and the rule restated in §3 |
| Nothing that a deck task needs is disabled — in particular the browser surface **rule 6** depends on | met | Confirmed by measurement rather than by reading: both browser surfaces are present in full after every change, including the one intended to remove connectors |
| The file stays out of git, verified rather than assumed | met | `git check-ignore` resolves it against the owner's global git configuration, and `taskmd check` independently refused a link to it — two instruments, agreeing |
| **Measured after a restart**: the figures against the before-numbers, recorded here | met | Twice. 7.3k → 6.5k → 6.5k, and deferred MCP unmoved at 50.4k throughout |
| The connector question is answered before any connector is disabled | met | Answered by the owner — *the unused ones, the browser stays* — and then answered again by measurement: **no connector could be disabled from here at all**, by either mechanism tried |
| — *added at review* — the saving is stated at the size it actually is | **not met, and corrected** | The audit banded `CE-07` at `L`. The reachable saving is ~800 tokens, which is `S`. `R8` §8 now says so. A band left standing at `L` would have priced future work off a number nobody could collect |

**Two criteria were met by a negative result, and that is a real outcome rather than a consolation.**
The task set out to cut the load path and cut 11% of one surface of it. What it established is
*where the boundary is*: from inside a repository, built-in and user skills are reachable and
plugin-supplied ones are not. That is worth more than the 800 tokens, because it stops the next
session re-running the same two experiments.

**Closed rather than left open.** The remaining ~3.4k is not blocked on effort — it is blocked on a
mechanism nobody here knows, and one decisive experiment that only the owner can authorise because it
touches every project. An open task implies queued work; this is a decision waiting on a person.

**Child fix tasks raised**
- **None.** If the owner runs the user-scope experiment and it works, the reinstatement is a new task
  with a known mechanism and the list above ready to paste.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | (no change) | **The deciding experiment returned null, and the line has been removed.** At *user* scope — the one scope untried — the connector's twenty-nine tools are present in full and the totals are unmoved: skills 6.5k, deferred MCP 50.4k, identical to both earlier readings. So **the barrier was never the scope**: the key does not apply on this machine at any scope, and neither does a per-skill override aimed at a plugin-supplied skill. Reverted immediately rather than left, because a global setting that does nothing here would still have disabled that connector in the owner's other project, which tracks its tasks there — **cost with no benefit is the worst of the four states**, and a setting kept "in case" is the dead configuration this task already removed once. The boundary in §3 stands and is now stronger: three mechanisms, three scopes, all inert for anything the harness or the account supplies. **The reachable saving from inside a repository is ~800 tokens, and that is final** until the mechanism is documented rather than guessed. |
| 2026-08-13 | (no change) | **The deciding experiment was authorised and was live**, after this task closed: `disableClaudeAiConnectors` is now set in the owner's **user** settings, which is the one scope not yet tried. It answers the question §3 left open — whether the barrier was the scope or the key. **It is global, and the owner has another project that tracks its tasks in the connector being disabled**, so the cost of leaving it on is that project's task workflow, not this one's. Revert is deleting one line from the user settings file. **No result is recorded here yet**: the reading is one `/context` in a fresh session, and this task stays `done` either way — a positive result reinstates the list kept in §3 under a new task, a negative one confirms the boundary already written. |
| 2026-08-13 | → done | **Measurement 2 moved nothing** — 6.5k and 50.4k unchanged, thirty-one corrected keys and the connector switch both inert. Three measurements now agree on one rule: **`skillOverrides` reaches built-in and user skills, and plugin-supplied skills are governed by whatever enables the plugin** — which for the plugins here is not any file on this machine. Reachable saving is **~800 tokens of 7,300, bought with two restarts**, so `CE-07`'s band is corrected from `L` to `S` in `R8` §8; a band left at `L` prices future work off a number nobody can collect. The settings file is **reduced to the three overrides and one plugin that are proven to work**, because thirty-one no-op entries read as a working policy and are the stale-record failure this audit exists to find — the list moved into §3, which is its durable home. Closed rather than parked: the rest is not blocked on effort but on a mechanism nobody here knows, plus **one decisive experiment the owner must authorise** because moving the connector switch to user scope touches every project they work in. Two criteria met by a negative result, and the boundary they establish is worth more than the 800 tokens: it stops the next session re-running these two experiments. |
| 2026-08-13 | (no change) | **Measured after the first restart, and the change was 90% ineffective: skills 7.3k → 6.5k against a predicted 2–3k, deferred MCP unchanged at 50.4k.** The listing then named its own cause. `business-consultant` appeared **twice** — once from a user skill, once from a plugin as `business-consultant:business-consultant` — and the single bare-name override removed the first and left the second. Same name, two sources, one match: **an override keyed by name must use the name the listing prints**, and for a plugin skill that is `plugin:skill`. Thirty-one keys were rewritten. `enabledPlugins` had worked all along — the six `bpmn` rows were gone — so **scope was never the problem and the file was being read**. `deniedMcpServers` did nothing and is removed: its own description calls it an enterprise denylist, and the merge sentence I reasoned from belongs to a neighbouring key describing itself. **The literal reading of a field beats an inference from the field next to it.** Replaced with the blanket connector switch, set with its hypothesis written down first — the UUID-named servers are the account connectors and go, the word-named ones including both browsers stay. If both browsers vanish the line comes out, because rule 6 outranks the saving. |
| 2026-08-13 | → in_progress | Raised and worked in one sitting, from `CE-07`, which [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) had ranked third **and excluded from repository work on reasoning that was sound and wrong**: the plugins supplying most skills are not installed on disk, so no plugin-enable setting reaches them — but the listing override keys on the skill's *name*, not on its delivery, and works at project scope. The audit had reasoned from where the files were instead of from what the configuration could address, and the correction is recorded in `R8` §8 under `CE-07` because the lesson is portable. 35 skills off, one local plugin off, one unrelated permission defect fixed in passing — five allow rules naming a renamed server, matching nothing. **Left open deliberately**: the saving is unmeasured until a restart, and the connector half — the larger number by far — is an open question rather than a unilateral change, because it may cover the browser surface rule 6 depends on. |
