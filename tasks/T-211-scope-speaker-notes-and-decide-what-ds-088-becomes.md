---
id: T-211
title: Scope speaker notes, and decide what DS-088 becomes
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-213]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-21
updated: 2026-08-21
shipped_in: 0.6.0
deliverables: [docs/DESIGN-SYSTEM.md, docs/BRIEF.md, docs/research/R1-rules-candidate.md]
---

# T-211 — Scope speaker notes, and decide what DS-088 becomes

## 1. Specify

**Outcome**
Speaker notes have a written scope: what they are, where they live in a shipped `.html`, what a
presenter does with them, and what the gate says about them. Today the project holds two statements
that cannot both stand. **DS-088** forbids speaker notes, presenter markers and script in the
shipped deck, `auto` and gated. **R1's candidate rule A10** carries the marker *amend — BRIEF Q4*
and has since it was written. `docs/BRIEF.md` open question 4 said *scope now, build later* and was
never revisited. The owner ruled on 2026-08-21 that speaker notes get a task; this is it. What comes
out is a scope and a decision on DS-088 — **not** an implementation.

**Why it is a decision rather than a fix.** DS-088 is not wrong. It is a rule the corpus supports:
R1 measured *no speaker notes, no presenter markers, no script — decided explicitly*. Amending it is
a ruleset change with a stated reason under DS-000, and the reason has to survive the thing DS-088
was protecting: a deck that ships with a presenter's private text inside it, readable by anyone the
file reaches. **Self-containment cuts both ways here** — rule 1 says the file carries everything,
which is exactly why notes inside it are not private.

**Scope**
- In: what a speaker note is, and whether it ships inside the deck at all.
- In: what DS-088 becomes — unchanged, narrowed, or amended — and the reason, per DS-000.
- In: clearing R1's A10 marker either way, so the candidate rule stops pointing at an open question.
- In: closing the speaker-notes half of `docs/BRIEF.md` open question 4.
- Out: building it. A scope that names the mechanism is the deliverable; the mechanism is a later
  task.
- Out: PDF export, the other half of BRIEF Q4. The owner left it deferred on 2026-08-21.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-088, and DS-000 for what amending costs.
- [`docs/BRIEF.md`](../docs/BRIEF.md) open question 4 — the scope-now-build-later statement.
- [`docs/research/R1-corpus-conventions.md`](../docs/research/R1-corpus-conventions.md) — the
  measurement behind A10, and the 2026-08-21 ruling that a stated rule beats the artefacts.
- [`docs/research/R1-rules-candidate.md`](../docs/research/R1-rules-candidate.md) — A10 and its
  marker.
- [`docs/research/R7-printable-mode.md`](../docs/research/R7-printable-mode.md) — it scoped speaker
  notes out alongside PDF export, and says why.

**Acceptance criteria**
- [ ] A written scope exists saying what a speaker note is and where it lives, or a written decision
      that speaker notes stay out — either is a pass, an unresolved *maybe* is not.
- [ ] DS-088 is either unchanged with the reason restated, or amended under DS-000 with the reason
      recorded in its row.
- [ ] The privacy consequence is addressed explicitly: a self-contained file carries its notes to
      whoever receives it, and the scope says what that means for the presenter.
- [ ] R1's A10 marker no longer says *amend — BRIEF Q4*, whichever way it went.
- [ ] `docs/BRIEF.md` open question 4's speaker-notes half is struck through and points here.
- [ ] `python tools/check_all.py` is green, since DS-088 is gated and a rule edit moves counts six
      documents quote.

**Open questions**
- ~~Whether a note that never ships — a sidecar the generator emits and the deck does not carry —
  satisfies what was wanted.~~ **Decided in §3: neither a sidecar nor an in-deck note, but a second
  build.** A sidecar is a file the presenter has to keep beside the deck and cannot present from; an
  in-deck note ships. A presenter build is one self-contained file that opens by double-clicking —
  which is what the presenter needs — and carries a marker that makes it fail a gate, which is what
  stops it being the file that goes out.
## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read DS-088's actual words before deciding what to amend | the finding, as it turned out |
| 2 | Decide where a note lives, against the three candidates: in the deck, in a sidecar, in a second build | the scope |
| 3 | State the privacy consequence explicitly, since rule 1 is what creates it | the reason DS-088 exists, restated |
| 4 | Restate DS-088's reason in its row without changing its force | the ruleset |
| 5 | Clear R1's A10 marker and close BRIEF Q4's speaker-notes half | no dangling pointer |
| 6 | Raise the build as its own task, sized honestly | a child |
| 7 | `python tools/check_all.py` | green |

## 3. Implement

**The scope: notes live in a presenter build, and the gate is what keeps them there.**

**1 — What a speaker note is.** Text attached to a slide in the **specification**, addressed to the
person presenting rather than to the audience: what to say, what to watch for, what the slide is
answering. It is authored where the slide is authored, and it is not slide copy — DS-106's
terminology gate and DS-100's rhetorical-question rule are about what an audience reads, and a note
is not that.

**2 — Where it lives.** In a **presenter build**: a second artifact from the same specification,
which is itself one self-contained file that opens by double-clicking. Not a sidecar — a presenter
cannot present from a Markdown file beside the deck, and a file that has to travel with another file
is the failure rule 1 exists to prevent, one participant along. Not in the shipped deck — see 4.

**3 — What the presenter does with it.** Opens the presenter build instead of the shipped one. Both
are the same deck; only one of them can pass a gate.

**4 — What stops it shipping.** The presenter build carries a marker DS-088's own check fails on, so
**the only build that can pass a gate is the one with no notes in it**. This is the safety property
the whole scope rests on, and it is structural rather than procedural: nobody has to remember which
file to send, because the wrong one is red.

**The privacy consequence, stated because rule 1 is what creates it.** A deck is one self-contained
file. A note inside the shipped file therefore travels to **everyone the file reaches**, and is
readable by anyone who presses `Ctrl+U` — no tooling, no intent required. That is not a tidiness
concern and it is not what a presenter expects when they write *they will push back on the number —
concede the range*. **The corpus decided the same thing explicitly** (R1 A10, *no speaker notes, no
presenter markers, no script — decided explicitly*). Two builds is the only arrangement where the
presenter gets the note and the recipient cannot.

**Decisions & assumptions**
- **DS-088 needed no amendment, and reading it is what settled that.** The row says *in the shipped
  deck*. It was being read as a ban on notes existing; it is a ban on their shipping, and a presenter
  build does not ship. **The task was raised on the premise that scoping notes makes DS-088
  amendable, and that premise was wrong** — reported here rather than worked around. — 2026-08-21
- **Permission was never the missing thing either.** DS-088 is `default`, and DS-000 licenses
  departure from `default` with a stated reason. Anyone could already have shipped notes with a
  reason. What was missing was a **scope** — what a note is, where it lives, and what stops it
  shipping by accident — which is why the answer is a design rather than a rule change. — 2026-08-21
- **A sidecar was the open question's proposal and it loses on the presenter's side.** It keeps notes
  out of the shipped file, which is the whole of what it buys, and costs the presenter the one
  property this project sells: double-click and present. A second build keeps both. — 2026-08-21
- **Building it is [T-213](T-213-build-the-presenter-build-and-the-marker-that-keeps-it-unshippable.md),
  sized `l`.** It touches a build path, the shell, the component contract and a gate at once, and
  introduces a second output artifact where the repository has always had one. — 2026-08-21

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-088 reviewed, kept, and its reason
  restated in the row with the presenter build named as outside it.
- [`docs/research/R1-rules-candidate.md`](../docs/research/R1-rules-candidate.md) — A10 reads
  **keep**; the *amend — BRIEF Q4* marker it carried from the day it was written is resolved.
- [`docs/BRIEF.md`](../docs/BRIEF.md) — open question 4's speaker-notes half closed and pointing
  here; the PDF-export half untouched, as the owner left it.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A written scope saying what a speaker note is and where it lives, or a written decision that they stay out — an unresolved *maybe* is not a pass | **met** | §3, in four numbered parts: what a note is, where it lives, what the presenter does, and what stops it shipping. It is a scope, not a deferral: the mechanism has a task and a size. |
| DS-088 is either unchanged with the reason restated, or amended under DS-000 with the reason recorded in its row | **met** — **unchanged** | And the reason it needed no amendment is the finding: the row already said *in the shipped deck*, and it is `default`, so DS-000 already licensed a stated departure. **The task's own premise — that scoping notes makes DS-088 amendable — was wrong**, and is reported rather than worked around. |
| The privacy consequence is addressed explicitly | **met** | §3 states it as the reason the row exists: rule 1 makes the deck one self-contained file, so a note inside it travels to everyone the file reaches and is readable with `Ctrl+U`. Two builds is the only arrangement where the presenter gets the note and the recipient cannot. |
| R1's A10 marker no longer says *amend — BRIEF Q4* | **met** | It reads **keep**, with the resolution dated and its reason beside it. |
| `docs/BRIEF.md` open question 4's speaker-notes half is struck through and points here | **met** | Struck, closed, and pointing at this task and at T-213. The PDF-export half is untouched. |
| `python tools/check_all.py` is green | **met** | **0 failure(s), 0 unclassified, 0 stale.** DS-088 is `auto` and its check is unchanged, so no count moved; the row's text grew and nothing that quotes a count reads it. |
| *(closing checklist step 3)* | **n/a** | This task produced no rendered artifact. Its output is a scope and three document edits. |

**Child fix tasks raised**
- [T-213](T-213-build-the-presenter-build-and-the-marker-that-keeps-it-unshippable.md) — build the
  presenter build and the marker. `PH3`, `l`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-21 | → proposed | Raised on the owner's ruling against `docs/BRIEF.md` open question 4, which had said *scope now, build later* and was never revisited. The question was surfaced by a resume sweep asking every remaining open question in the project rather than only the ones a handoff named. `PH3` because PH2 has shipped and this is not a defect in the published plugin. The PDF-export half of Q4 was left deferred in the same ruling and is not in this task. |
| 2026-08-21 | proposed → done | Scoped, and **DS-088 needed no amendment** — which is the finding rather than a non-decision. The row already read *in the shipped deck*, and it is `default`, so DS-000 already licensed a stated departure; **this task was raised on the premise that scoping notes makes DS-088 amendable and that premise was wrong.** What was missing was a scope, and it is: notes live in a **presenter build**, a second self-contained artifact from the same specification, carrying a marker DS-088's own check fails on — so the only build that can pass a gate is the one with no notes in it. The privacy argument is stated as the reason the row exists: rule 1 makes the deck one file, so a note inside it is readable by everyone it reaches. A sidecar was the open question's proposal and loses on the presenter's side. R1's A10 marker reads **keep**; BRIEF Q4's speaker-notes half is closed and its PDF half untouched. Building it is [T-213](T-213-build-the-presenter-build-and-the-marker-that-keeps-it-unshippable.md), `l`. |
