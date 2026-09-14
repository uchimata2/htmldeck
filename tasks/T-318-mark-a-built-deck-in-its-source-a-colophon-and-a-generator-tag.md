---
id: T-318
title: Mark a built deck in its source: a colophon and a generator tag
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-300, T-311, T-321]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-15
deliverables: [tools/deck/shell.py, shell/shell.html, shell/README.md, docs/COMPONENT-CONTRACT.md, docs/PUBLISHING.md, skills/htmldeck/references/build.md]
---

# T-318 — Mark a built deck in its source: a colophon and a generator tag

## 1. Specify

**Outcome**
A deck htmldeck builds says so in its source and nowhere a reader sees. Its head comment opens with a
colophon naming htmldeck and its repository, `https://github.com/uchimata2/htmldeck`, beside the font
and icon credits already there. Its head carries `<meta name="generator" content="htmldeck X.Y.Z">`,
the convention static-site generators use. **An author who deletes the colophon's repository line has
removed both marks for good**: a sync keeps the deletion and writes no tag.

**Ruled by the owner 2026-09-14**, each on the recommendation put to them. Where: the head comment and
the generator tag, not a console line and not a More-menu item. Tone: a colophon. Removal: it sticks.
Release: 1.0.0, in B29 ahead of `T-300`.

**Why nothing visible.** [`../docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) X-12 makes generator
branding a `hard` anti-pattern, from the corpus critique's finding of branding left in a corner
([`../docs/BRIEF.md`](../docs/BRIEF.md)). A mark in the source is not residue a recipient meets, so
X-12 stands unamended.

**Scope**
- In: `NOTE_DEFAULT` in `tools/deck/shell.py` rewritten as the colophon; the generator tag in
  `shell/shell.html`; `sync` writing the tag with the current version while the deck's head comment
  names the repository URL, and dropping it while it does not; self-test fixtures for both; the
  shipped example decks carrying the colophon; `shell/README.md` saying where the marks are and how to
  remove them; every other document that describes the head note, found by search.
- Out: anything rendered, printed, or shown in the degraded state; a console line; a menu item; a
  version number inside the head comment, which no sync touches and which would go stale (L-152).

**Inputs**
- `tools/deck/shell.py`: `SLOTS`, `head_note()`, `NOTE_DEFAULT`, `new()`, and sync
- `shell/shell.html`, and `shell/README.md`'s slot list
- `.claude-plugin/plugin.json`, the version's home
- [T-311](T-311-keep-a-decks-chart-engine-declaration-through-a-shell-sync.md): the head comment is the one place in the head a deck's own declaration survives a sync

**Acceptance criteria**
- [x] A deck built by `shell.py new` carries the colophon with the repository URL in its head comment,
      and the generator tag with the version read from `.claude-plugin/plugin.json`.
- [x] A sync writes the tag, at the current version, on a deck whose head comment names the repository
      URL. It writes no tag on a deck whose head comment does not. A self-test asserts both, and
      asserts that deleting the line and syncing leaves both marks absent.
- [x] Nothing renders differently: the reference deck's screen captures before and after the change
      are identical, so no look is owed.
- [x] The shipped example decks carry the colophon, and every document that describes the head note
      says where the marks are and how to remove them, with one home for the how.
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately.

**Open questions**
- none. The four above were the owner's and are ruled.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Search every file that describes, builds or tests the head note and the head's opening lines | the list of files the change reaches |
| 2 | Capture the reference deck's screens before any edit | the baseline |
| 3 | Rewrite `NOTE_DEFAULT` as the colophon; add the tag to `shell.html`; make sync write or drop it by the head comment's URL | the mechanism |
| 4 | Fixtures: a new deck, a synced deck with the line, a synced deck without it | the self-test |
| 5 | Add the colophon to the shipped examples' head comments, then sync them per `TOOLING.md` §1.14 | the examples |
| 6 | Capture the screens again and compare them with step 2 | criterion 3 |
| 7 | Write where the marks are and how to remove them in `shell/README.md`, and point the other documents there | criterion 4 |
| 8 | Lint, then the full gate | criterion 5 |

## 3. Implement

**Decisions & assumptions**
- The repository URL in the head comment is the switch for both marks, so an author has one line to delete and no new vocabulary to learn. Reversible. — 2026-09-14
- An existing adopter deck synced to 1.0.0 gains neither mark, because a sync cannot tell a removed colophon from one that never existed, and the owner ruled that removal sticks. Reversible. — 2026-09-14
- The tag is a thirteenth slot, `GENERATOR`, between the viewport line and `<title>`, not fixed markup in `shell.html`: `check` compares the skeleton byte for byte, so a fixed tag would fail every deck whose author removed the colophon. `new` and `sync` derive it from `NOTE`; `kept()` excludes it and `changes()` reports it. `head_note()` skips it, because the gates' fixtures build heads without a viewport line. Reversible. — 2026-09-15
- The colophon is one line, `Built with htmldeck: <URL>`, so deleting the line removes the name and the switch together. Reversible. — 2026-09-15
- `docs/PUBLISHING.md` §8 step 2 now syncs every shipped deck after the version bump, so no example ships with the outgoing version in its tag. A check that failed a deck on a stale tag was rejected: a plugin update with no shell change would turn every adopter deck red. Reversible. — 2026-09-15
- `measure-first` carries the colophon too: it was built with the published plugin. Reversible. — 2026-09-15

**Outputs produced**
- `tools/deck/shell.py` (`GENERATOR`, `REPO_URL`, `version()`, `generator_tag()`, five fixtures), `shell/shell.html`, `shell/README.md` (*The slots*: the one home for removal)
- Pointers: `docs/COMPONENT-CONTRACT.md`, `skills/htmldeck/references/build.md`; release step: `docs/PUBLISHING.md` §8 step 2
- The four shipped decks, the seeded-defect fixture and the three presenter builds, re-derived per `TOOLING.md` §1.14

| Measurement, 2026-09-15 | Result |
| :--- | :--- |
| `shell.py` self-test | 76 of 76 fixtures |
| Tags written by sync | `<meta name="generator" content="htmldeck 0.7.0">` on all four decks; regions changed per deck: `GENERATOR`, `NOTE` |
| Reference deck captures, 13 slides, before against after | 11 identical; slide 9 noise (matched on recapture); slide 11 stable difference, reproduced by padding the committed deck with neutral bytes, so it follows file length (T-321) |

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `new` carries both marks | pass | Fixture, and the version read from the manifest |
| Sync writes or drops the tag by the URL | pass | Three fixtures: written, dropped, deletion kept; both forms pass `check` |
| Nothing renders differently | pass | Nothing T-318 writes renders. Slide 11's difference is reproduced without T-318's content, by padding alone; raised as T-321. No look owed |
| Examples and documents | pass | Four decks carry the colophon; one home for removal in `shell/README.md`, pointed at from the contract and the build reference |
| Lint and full gate | pass | Run separately after the last edit |

**Child fix tasks raised**
- [T-321](T-321-make-a-decks-render-independent-of-its-file-length.md)

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | → proposed | Asked for by the owner: mark the decks htmldeck builds, without intruding and without marketing. `PH3`. |
| 2026-09-14 | → specified, planned | The owner ruled the four questions on their recommendations: the head comment and a generator tag, a colophon, removal sticks, 1.0.0 in B29 ahead of `T-300`. |
| 2026-09-15 | → implement, done | Built as a derived slot; examples synced; screen comparison raised T-321. |
