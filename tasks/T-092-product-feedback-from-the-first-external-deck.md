---
id: T-092
title: Product feedback from the first external deck — six needs, all against tasks that already exist
type: admin
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-004, T-016, T-069, T-070, T-082, T-088]
work_package: v0.3
owner: the project owner
business_value: high
effort: s
created: 2026-08-11
updated: 2026-08-11
deliverables: []
---

# T-092 — Product feedback from the first external deck — six needs, all against tasks that already exist

## 1. Specify

**Outcome**
The six things a real deck owner found wanting, after presenting-quality review of a finished
twelve-slide board deck, are routed to the tasks they belong to — as **needs**, not as fixes, and
not as new work.

**Read this first: none of these is a defect.** Every one is htmldeck doing exactly what it says
while failing the reader. The same project's defect reports are `T-090`, `T-091` and the two fixed in
0.2.0; they are deliberately kept apart from this, because filed together the interesting half gets
triaged as bugs and closed by making code match documentation.

**Nothing here proposes an implementation as required.** Where satisfying a need collides with an
existing rule, the collision is **named and left**. Resolving htmldeck's internal contradictions is
this repository's work; the adopter's job is to say what a reader cannot do.

**The constraint over all six**, from the same review: *the simplicity of the entire deck, the vibe
in general, is just perfect.* A feature that makes the deck busier has failed even if it closes the
need.

**The six, and where each lands**

| # | The need | Belongs to | That task's status |
| :-- | :--- | :--- | :--- |
| N-1 | A source line that says what the document is and can be opened — not `D5 §2` | **T-070** as a scoping input, **T-069** as the origin | `proposed` / `done` |
| N-2 | `Ctrl+R` should not be bound; it takes the browser's reload from a presenter mid-talk | **T-016** | `done` |
| N-3 | Disclosure attached to **part of a figure**, not only to the slide | **T-016** | `done` |
| N-4 | A green build reads as a finished deck; nothing in the run asks the X-08 question | **T-004**, critique mode | `done` |
| N-5 | The T-082 ledger-omission pattern recurring independently in an unrelated deck | **T-088** | open |
| N-6 | DS-091's six-word cap pulls an author toward the allusive headline — the X-08 failure itself | **T-004** | `done` |

**Four of the six belong to tasks that are `done`**, and that is the most useful thing this report
says. Each of those tasks built exactly what it specified. These are what real use found afterwards.

**Two collisions, named and not ruled on**
- **DS-105 forbids a `file://` link in a shipped deck.** A deck whose sources are files beside it has
  no conformant way to reach them (N-1).
- **DS-092 makes a descriptive source line impossible.** The mark is one `<p>`, so its items are
  counted together: give each a full stop and the paragraph exceeds four sentences; leave them
  without one and they concatenate into a single sentence over twenty words. Five sources cannot
  carry titles either way (N-1).

**The full statement of each need**, with what a reader gets today and why it does not serve them, is
the adopting project's own `HTMLDECK-FEEDBACK.md`, under its `docs/` and not reachable from this
repository. The directory prefix is left off on purpose: a slashed path written in prose is a pointer
`refcheck` resolves against this repository, and it reported this one dead the first time the task was
indexed here. This task carries the routing and the collisions; it does not restate the document.

**The lesson that comes with them, and it is the reusable half.** Two of the six — N-1's bare slugs
and N-3's single disclosure — had already been hit, resolved and written into the adopting project's
build log as its own *deviations*, weeks and hours before the review, and **neither was recognised as
product feedback** until the owner read the finished deck and said the sources were useless. The
recognisable form is a log entry reading *built X instead of Y, because rule Z*: it already names the
rule and the worse outcome, which is most of a report. **A workaround recorded as a local deviation
is a product finding nobody has reported yet**, and only the adopter is positioned to notice, because
the maintainer never sees the log.

**Scope**
- In: routing each need to the task that owns it, and recording the two collisions.
- Out: deciding any of them. Every item is an input to another task's specify.
- Out: filing any of these as new work. If a need survives triage and needs its own task, that is
  this repository's call to make, not the reporter's.

**Acceptance criteria**
- [ ] Each of N-1 to N-6 is recorded against the task named above, so a person opening that task sees
      the need without knowing this one exists
- [ ] Both collisions are recorded where the rules live, not only here
- [ ] Nothing from this task is filed as a defect
- [ ] Whatever is decided, the deviation-log lesson survives somewhere a future adopter reads

## 2. Plan

_not started_

## 3. Implement

_not started_

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- _none yet_

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (specify) | **Kept at `v0.3`, and against the size rule** — `s` would put it in v0.2 on effort alone. It follows [T-089](T-089-a-withdrawn-task-was-deleted-rather-than-cancelled.md), placed the same way a day earlier: v0.2 has shipped, and reopening a shipped phase is reserved for adopter defects. This report's own first line is that none of the six is a defect, which is exactly what disqualifies it. Its two companions, [T-090](T-090-spec5-cannot-parse-a-descriptive-slide-label.md) and [T-091](T-091-build-md-documents-icons-set-as-a-single-pair.md), *are* defects and went to `v0.1` — the three arrived together and split across two phases, which is the point of filing them apart. |
| 2026-08-11 | → proposed | Raised by the AI Training 06 (DentalPro) project, htmldeck's first adopter outside this repository, after its owner reviewed a finished twelve-slide board deck. Kept separate from that project's defect reports (`T-090`, `T-091`) on purpose and on its owner's instruction: these are the tool behaving as designed and failing the reader, and a need filed under a title saying *defect* gets triaged as a bug. N-6 was added last, from rewriting that deck's headlines to answer N-4 — the two rules pull in opposite directions and only one of them is checkable. |
