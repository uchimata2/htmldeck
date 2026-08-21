---
id: T-213
title: Build the presenter build, and the marker that keeps it unshippable
type: deliverable
status: proposed
phase: specify
parent: T-211
blocked_by: []
related: [T-211]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-213 — Build the presenter build, and the marker that keeps it unshippable

## 1. Specify

**Outcome**
A specification carrying speaker notes produces **two** artifacts: the deck that ships, with no
notes in it, and a **presenter build** that carries them and cannot pass a gate. Today neither
exists; [T-211](T-211-scope-speaker-notes-and-decide-what-ds-088-becomes.md) scoped them and
explicitly did not build them.

**What T-211 settled, and what it left**
Settled: notes never ship; DS-088 is unchanged and governs the shipped deck; the presenter build is
a second artifact from the same specification; its safety property is that it carries a marker
DS-088's own check fails on, so **the only build that can pass a gate is the one with no notes in
it**. Left: all of the mechanism. The scope is T-211 §3 and this task does not re-derive it.

**Why it is `l` rather than `m`**
It touches a build path, the shell, the component contract and a gate at once, and it introduces a
second output artifact where the repository has always had one. Each of those is small; the
combination is not, and the one-file promise is the thing being qualified.

**Scope**
- In: the presenter build — how notes are authored in the specification, how the build emits them,
  and what the presenter sees.
- In: the marker, and proving by seeded defect that a presenter build cannot pass `check.py`.
- In: the component-contract row for however the notes are carried.
- Out: changing DS-088. T-211 settled that it stands.
- Out: PDF export, the other half of `docs/BRIEF.md` open question 4, which the owner left deferred
  on 2026-08-21.

**Inputs**
- [T-211](T-211-scope-speaker-notes-and-decide-what-ds-088-becomes.md) §3 — the scope, and the
  privacy argument the marker exists to enforce.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-088 and its restated reason.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — where the notes region's row goes.

**Acceptance criteria**
- [ ] One specification produces both artifacts, and the shipped one is byte-identical to what the
      same specification produces with no notes authored.
- [ ] A presenter build **fails** `python tools/deck/check.py`, proved by seeding one and running it.
- [ ] The shipped build passes every gate it passes today.
- [ ] The presenter build is still one self-contained file that opens by double-clicking, because a
      presenter is a recipient too.
- [ ] `python tools/check_all.py` green.

**Open questions**
- Whether the presenter build carries the audience deck as well, or only the notes. Carrying both
  is what a presenter actually wants and is also the version that most looks like the shipping file,
  which is the argument for making the marker loud.

## 2. Plan

*Not started.*

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- *Not started.*

**Outputs produced**
- *Not started.*

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised by [T-211](T-211-scope-speaker-notes-and-decide-what-ds-088-becomes.md), which scoped speaker notes and ruled that DS-088 stands unchanged because it governs the **shipped** deck. `PH3`, `l`: a build path, the shell, the contract and a gate at once, and a second output artifact where there has always been one. |
