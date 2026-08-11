---
id: T-092
title: Product feedback from the first external deck — six needs, all against tasks that already exist
type: admin
status: done
phase: review
parent: null
blocked_by: []
related: [T-004, T-016, T-069, T-070, T-082, T-088]
work_package: v0.3
owner: the project owner
business_value: high
effort: s
created: 2026-08-11
updated: 2026-08-12
deliverables:
  - docs/DESIGN-RATIONALE.md
  - docs/LESSONS.md
  - skills/htmldeck/references/build.md
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

| # | The need | Belongs to | At routing, 2026-08-11 | Today |
| :-- | :--- | :--- | :--- | :--- |
| N-1 | A source line that says what the document is and can be opened — not `D5 §2` | **T-070** as a scoping input, **T-069** as the origin | `proposed` / `done` | `done` / `done` |
| N-2 | `Ctrl+R` should not be bound; it takes the browser's reload from a presenter mid-talk | **T-016** | `done` | `done` |
| N-3 | Disclosure attached to **part of a figure**, not only to the slide | **T-016** | `done` | `done` |
| N-4 | A green build reads as a finished deck; nothing in the run asks the X-08 question | **T-004**, critique mode | `done` | `done` |
| N-5 | The T-082 ledger-omission pattern recurring independently in an unrelated deck | **T-088** | open | `done` |
| N-6 | DS-091's six-word cap pulls an author toward the allusive headline — the X-08 failure itself | **T-004** | `done` | `done` |

**Four of the six belonged to tasks that were already `done`** when this was written, and that is the
most useful thing this report says. Each of those tasks built exactly what it specified. These are
what real use found afterwards.

**All six are `done` now.** T-070 and T-088 both closed on 2026-08-11 — the same day this table was
written, which is why the routing column needed two of them. The snapshot column is kept rather than
overwritten: *four of six landed on already-finished work* is the finding, and a column edited to
today's answer would erase it.

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
- [x] Each of N-1 to N-6 is recorded against the task named above, so a person opening that task sees
      the need without knowing this one exists
- [x] Both collisions are recorded where the rules live, not only here
- [x] Nothing from this task is filed as a defect
- [x] Whatever is decided, the deviation-log lesson survives somewhere a future adopter reads

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Route each need into the task that owns it, at that task's own altitude — §1 for a task still specifying, a log row for one already closed | Five task files |
| 2 | Record both collisions where the rules' tensions live, not in a task | `docs/DESIGN-RATIONALE.md` |
| 3 | Write the deviation-log lesson twice: once for this project, once where an adopter will read it | `docs/LESSONS.md`, `skills/htmldeck/references/build.md` |
| 4 | Close without filing anything as a defect | This record |

## 3. Implement

**Decisions & assumptions**
- **A need against a `done` task is a log row, not a reopening.** Four of the six land on tasks that
  built exactly what they specified, so there is no criterion to add and nothing to un-close. The row
  is dated, says where it came from, and says it is recorded rather than reopened — which is what
  makes it findable by someone opening that task without knowing this one exists, the whole of
  criterion 1.
- **A need against a task still in `specify` goes into §1**, where it can affect scope. T-070 and
  T-088 both took one, and in both cases it changed the *justification* rather than the deliverable:
  T-070 learns which half of the quick view is load-bearing, T-088 learns that its expensive
  false-alarm measurement is worth paying for.
- **The collisions became `U-01` and `U-02` in their own subsection**, not rows in
  [`../docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2's table. That table's column is
  *Resolution* and these have none; a row in it would have to invent one, and §1 put ruling on them
  out of scope. The subsection also carries what makes them a third kind: §2 came from reading and
  §2.1 from building, and these two came from a reader saying a green deck did not serve them.
- **The lesson is written in two registers.** **L-66** is the project's own record, addressed to
  whoever next receives a report. The `build.md` §4 obligation is the adopter-facing half: it does
  not ask anyone to file anything, it asks a build to say which of its own deviations are candidates
  — because the whole finding is that a closed workaround stops looking like a question.

**Outputs produced**
- [T-070](T-070-the-quick-view-for-a-source-document.md) §1 (N-1), [T-088](T-088-a-figure-in-a-sentence-naming-no-field-goes-stale-unwatched.md) §1 (N-5) — scoping inputs.
- [T-016](T-016-the-interaction-and-motion-layer.md) (N-2, N-3), [T-004](T-004-critique-mode-blunt-section-by-section-review.md) (N-4, N-6), [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) (N-1's origin) — log rows against closed tasks.
- [`../docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2.2 — U-01 and U-02.
- [`../docs/LESSONS.md`](../docs/LESSONS.md) — L-66.
- [`../skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) §4 — a third
  obligation on deviation authority.

**What N-4 and N-6 turned out to be, and it is one need rather than two.** N-4 says a green build
reads as a finished deck; N-6 says DS-091's six-word cap pulls an author toward the allusive headline
X-08 forbids. Both are the same mechanism seen from opposite ends: **where a checkable rule and a
judged rule point in different directions, the deck goes where the check points**, because that is
the one that answers back. Recorded on T-004 as a pair for that reason.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each of N-1 to N-6 is recorded against the task named above | met | Five tasks, six needs. Each entry names the need, where it came from and what it is for, and reads without this task — the log rows say *recorded, not reopened* in as many words so a reader does not go looking for a reopening that did not happen. |
| Both collisions are recorded where the rules live | met | `DESIGN-RATIONALE.md` §2.2, as **U-01** (DS-105 against a source a reader can open) and **U-02** (DS-092's bound against five sources carrying titles), both marked open with an owner or the absence of one. Cross-referenced from T-069, where the mark's shape was decided, and T-070, which owns U-01. |
| Nothing from this task is filed as a defect | met | No task raised, no rule changed, no code touched. The one behaviour change is an obligation in `build.md` §4, and it obliges a build to *say* something, not to work differently. |
| The deviation-log lesson survives somewhere a future adopter reads | met | Twice. **L-66** for this project's own intake, and `build.md` §4's third obligation for the adopter's — the shipped skill is the only document in this repository an adopter is certain to read, which is why the lesson could not live in `LESSONS.md` alone. |

**Child fix tasks raised**
- none, by §1's scope. Whether any need earns its own task is this repository's call and remains
  open; every one of them is now sitting in the record of the task that would make it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | (reconciled) | **The routing table's status column had gone stale within hours of being written.** It recorded T-070 as `proposed` and T-088 as `open`; both closed on 2026-08-11, the same day. Split into two columns rather than corrected in place — *four of six landed on already-finished work* is this report's finding, and a column edited to today's answer erases the evidence for it. **All six are `done` now**, which is the answer to the question that surfaced it: whether a second project rebuilding a deck should wait for anything the first one asked for. It should not. |
| 2026-08-11 | (shipped) | **Shipped in `0.2.1`.** The six findings and their routing are public from here; four of the six went to tasks that were already `done`. |
| 2026-08-11 | → done | All four criteria met, and the report was right that **four of the six belong to closed tasks**. Routing them cost five task files, one rationale subsection and two copies of one lesson, and changed no rule - which is the outcome §1 asked for and the one a defect-shaped intake would not have produced. Two things worth carrying: **N-4 and N-6 are one need, not two** - where a checkable rule and a judged rule disagree the deck follows the check, because that is the one that answers back - and **N-5 is what makes T-088 worth its price**, since a pattern found twice in decks this repository wrote could be a house habit and a third in an adopter's deck could not. The collisions are `U-01` and `U-02`, open and owned or explicitly unowned. |
| 2026-08-11 | (specify) | **Kept at `v0.3`, and against the size rule** — `s` would put it in v0.2 on effort alone. It follows [T-089](T-089-a-withdrawn-task-was-deleted-rather-than-cancelled.md), placed the same way a day earlier: v0.2 has shipped, and reopening a shipped phase is reserved for adopter defects. This report's own first line is that none of the six is a defect, which is exactly what disqualifies it. Its two companions, [T-090](T-090-spec5-cannot-parse-a-descriptive-slide-label.md) and [T-091](T-091-build-md-documents-icons-set-as-a-single-pair.md), *are* defects and went to `v0.1` — the three arrived together and split across two phases, which is the point of filing them apart. |
| 2026-08-11 | → proposed | Raised by the AI Training 06 (DentalPro) project, htmldeck's first adopter outside this repository, after its owner reviewed a finished twelve-slide board deck. Kept separate from that project's defect reports (`T-090`, `T-091`) on purpose and on its owner's instruction: these are the tool behaving as designed and failing the reader, and a need filed under a title saying *defect* gets triaged as a bug. N-6 was added last, from rewriting that deck's headlines to answer N-4 — the two rules pull in opposite directions and only one of them is checkable. |
