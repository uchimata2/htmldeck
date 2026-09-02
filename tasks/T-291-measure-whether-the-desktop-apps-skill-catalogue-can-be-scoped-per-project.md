---
id: T-291
title: Measure whether the desktop app's skill catalogue can be scoped, and disable what no project uses
type: fix
status: done
phase: review
parent: T-287
blocked_by: []
related: [T-135]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
finding: CE-17
created: 2026-09-02
updated: 2026-09-02
shipped_in: unreleased
deliverables: []
---

# T-291 — Measure whether the desktop app's skill catalogue can be scoped, and disable what no project uses

## 1. Specify

**Outcome**
The catalogue of skills a session here is offered on every turn is measured as **60 entries,
15,024 bytes of name and description, about 3,800 estimated tokens per turn**, of which five serve
this repository. Forty-one come from the desktop app's own skill store under the user's roaming
profile and fourteen are the harness's built-ins; `CE-07`'s per-project enabling reached the
`~/.claude` plugins and none of these. This task finds whether the app's store can be scoped or
disabled per skill, does so for what no project on this machine uses, and records the boundary where
it cannot. The finding is `CE-17` in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3.

**The change lands outside the repository.** The controller is the user; no clone inherits it. The
task exists so the measurement and the boundary have a home, which is the ecoctx rule for a
user-controlled item.

**Scope**
- In: the app's skill settings; one setting written, one restart, one re-measurement — the ecoctx
  rule, and *two failed attempts is the signal to stop*.
- Out: anything under `~/.claude/plugins`, which `T-135` already scoped; the built-ins.

**Inputs**
- `../docs/CONTEXT-AUDIT.md` §11.1, `CE-17`

**Acceptance criteria**
- [ ] The catalogue re-measured after the change, by the same script, with the before and after figures in §3.
- [ ] Where a skill could not be scoped, the boundary is one line here rather than a retry.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-count the catalogue as received, by group | **61** entries: 5 this repository's, 15 built-ins, 41 in between |
| 2 | Find where the 41 live, before assuming a store can be pruned | **40 of the 41 are on no disk in this profile**; the one that is sits in `~/.claude/skills` |
| 3 | Ask the CLI what it can toggle, rather than the documentation | `enabledPlugins` yes; `disabledSkills`, `enabledSkills`, `allowedSkills`, `deniedSkills`, `skillSettings` all absent |
| 4 | Ask the account what it can toggle | `ListSkills` returns each account skill with its own `enabled` flag |
| 5 | Record the boundary rather than retry | §3, and one line for the owner in §4 |

## 3. Implement

**Decisions & assumptions**
- **The finding's size is right and its mechanism is wrong.** `CE-17` says the 41 are *installed by the desktop app in the user's roaming profile*. Searching the whole profile finds a directory for **one** of them — `business-consultant`, in `~/.claude/skills` — and none for `marp-slides` or `archimate-ea` at any depth. They arrive with the account. The counts do re-derive: 5 this repository's, 41 others, and **15** built-ins where the row says 14 — 2026-09-02
- **Per-skill scoping exists, and no file on this machine reaches it.** `ListSkills` returns each account skill with its own `enabled` flag, so the control is per skill and belongs to the account interface. The CLI binary carries `enabledPlugins` and `disabledMcpjsonServers` and knows **none** of `disabledSkills`, `enabledSkills`, `allowedSkills`, `deniedSkills`, `skillSettings`. That check is what the memory entry *the config schema is the authority* exists to force; this time the schema says no — 2026-09-02
- **The change is not made here, and that is the boundary rather than a failure.** It changes the owner's account settings, through an interface this session cannot drive, and no session can restart itself to take the after-reading — `T-288`'s wall in a different place. **One attempt, not two**: the settings-key question was answered decisively, and retrying it is the retry §1's rule warns against — 2026-09-02
- **The byte figure is left at `CE-17`'s measurement rather than restated.** Re-deriving it means transcribing all 61 name-and-description pairs, which is the thing being measured; the counts already size the prize — 2026-09-02

**Outputs produced**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — `CE-17`'s row struck, and its finding block corrected where the mechanism is stated
- **No setting was written.** The one action that spends this band is the owner's, and §4 carries it

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| the catalogue re-measured after the change, by the same script, with the before and after in §3 | **not met** | No change was made, so there is no *after*. The **before** is re-derived and §3 carries it, including one figure the row had wrong. A session cannot restart itself, and the switch is in the owner's account interface — the wall `T-288` met, recorded rather than worked around |
| where a skill could not be scoped, the boundary is one line here rather than a retry | pass | It **can** be scoped, per skill, in the account interface; nothing on this machine reaches it. One pass settled it — the CLI either carries a per-skill settings key or it does not |

**What the owner does, if the band is worth spending.** Disable, in the account's skill settings, what no project on this machine uses — most of the 41 are for domains nothing here touches, the ArchiMate, Tauri, academic and PowerPoint families among them. **Nothing in this repository changes and no clone is affected.** The re-measurement is the next session's first turn, against §3's 61.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | proposed → done | B20, closing **not met** on the first criterion and recording why, which is what §1 asked for. **The counts re-derive; the mechanism does not.** `CE-17` reads *41 installed by the desktop app in the user's roaming profile*, and the profile holds a directory for **one** of the 41 and none for the rest at any depth — they arrive with the account. Per-skill scoping exists, since `ListSkills` reports an `enabled` flag on each, and no file on this machine reaches it: the CLI knows `enabledPlugins` and not one of five plausible per-skill keys. So the band is real, the controller is the owner's account interface, and §4 carries the single action that spends it. **One attempt, not two** — the schema answered decisively, and a retry is what §1's rule warns against. |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-17`. User-controlled; the task holds the measurement. `PH3`. |
