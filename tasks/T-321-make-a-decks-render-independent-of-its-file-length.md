---
id: T-321
title: Make a deck's render independent of its file length
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-318]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-09-15
updated: 2026-09-15
deliverables: []
---

# T-321 — Make a deck's render independent of its file length

## 1. Specify

**Outcome**
A deck renders the same whatever bytes sit in places that do not render. Today the reference deck's
slide 11 does not: the threshold figure's labels come out narrower, and the bar label loses its inset,
when the file grows by a comment.

**Found by T-318, 2026-09-15.** Captured with `python tools/deck/render.py shots <deck> 11`, compared
pixel by pixel:

| Deck | Slide 11 against the committed deck's capture |
| :--- | :--- |
| committed deck, captured twice | identical |
| committed deck + a 111-byte comment after `</html>` | differs, box (97, 433)–(1474, 847) |
| committed deck + a 111-byte line inside the head comment | differs, same box, same pixels as the row above |
| T-318's synced deck (colophon line and generator tag), captured twice | differs, same pixels as the two rows above |

Slide 9 differed once in one capture and matched on the next, so it is noise; slide 11 is stable in
both states. The difference therefore follows file length, not content.

**Scope**
- In: the mechanism (a font-load race, a scripted measurement, or the capture's virtual-time budget);
  whether a real browser shows it; the fix where it lives.
- Out: T-318, which changes nothing that renders.

**Acceptance criteria**
- [ ] The mechanism is named with the command that shows it.
- [ ] Slide 11 captures identically with and without padding bytes, or the difference is shown to be
      the capture's and not a reader's, with a note in `tools/deck/render.py` saying so.

**Open questions**
- Phase: `PH3` until the cause is known. If it is in `shell/`, it is a defect in the published plugin
  and becomes `PH1` by `CLAUDE.md`'s rule. — whoever takes the task.
- Does 1.0.0 wait for it? — the owner, 2026-09-15: no. It stays unbatched, outside B29.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- none yet

**Outputs produced**
- none yet

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-15 | → proposed | Raised by T-318's screen comparison. |
| 2026-09-15 | proposed | The owner ruled it out of B29; 1.0.0 does not wait for it. |
