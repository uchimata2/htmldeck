---
id: T-083
title: The generated example deck fails a hard rule and nothing recorded it
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-021, T-071, T-075]
work_package: PH1
shipped_in: 0.1.5
owner: the project owner
business_value: high
effort: s
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - examples/sort-window/sort-window.html
  - docs/THEME-CONTRACT.md
---

# T-083 — The generated example deck fails a hard rule and nothing recorded it

## 1. Specify

**Outcome**
`examples/sort-window/sort-window.html` passes the build check, or its failure is recorded as a known
and reasoned exception. Either way the repository stops shipping a red gate on the deck it points at
as proof the pipeline works.

**Why this one**
Found 2026-08-10 while working
[T-071](T-071-the-intermediate-specifications-carry-their-references.md). Run today:

    1 failure(s): DS-064
        DS-064   smallest body run in a 720p capture: 15.0 px (23 du) on 'Approve the slot by 19 Septe',
                 floor 16, 4 slide(s) sampled

**It is not new and it is not T-071's.** The same run against the file as it stood at `d80e0c3`
reports the identical row — same slide, same 15.0 px, same 23 du — so it predates that task and was
already true of the committed deck.

**Why `high`.** `CLAUDE.md` names this deck as **the first deck nobody authored by hand**, and the
repository is public. A generated example that fails a `hard` rule is the strongest available argument
against the generator, and it is sitting in the repository unremarked. The second half is worse than
the first: nothing in the task record says this was ever run, so the failure is not a known cost, it is
an unknown one.

**A second observation, which may be the more interesting half.** The reference deck passes the same
rule at 17.3 px on a four-slide sample. Both decks carry the **same shared component block**, so the
difference is either this deck's own composition or **which four slides the sample drew** — and if it
is the sample, a `hard` rule is being decided by a draw. Worth settling before the fix, because the two
answers lead to different fixes.

**Scope**
- In: what the 15.0 px run actually is — the ask lines on slide 12, the provenance mark, or something
  else. Read the element, do not infer it from the slide.
- In: whether DS-064's four-slide sample can return different verdicts for the same deck. If it can,
  that is a defect in the check and outranks the deck's.
- In: the fix, or the reasoned exception, and a line in the task record either way.
- In: why no task ran this check against this deck. The gate exists and is green elsewhere, so the gap
  is in when it runs, not in what it can see.
- Out: the reference deck, which passes.
- Out: DS-064's 16 px floor, which is settled ([T-021](T-021-the-reflow-view-and-the-resolution-contract.md)).

**Inputs**
- `python tools/deck/check.py examples/sort-window/sort-window.html --sources examples/sort-window/sources`
- [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) — where DS-064's floor and its 720p capture were
  settled, and the measurement it lifted into the gate.
- [T-075](T-075-ds-064-probes-for-the-reference-decks-own-class-names.md) — the last time this rule's
  own implementation was wrong, which is the reason to check the instrument before the deck.

**Acceptance criteria**
- [ ] The failing run is either green or recorded as a reasoned exception with the cost stated
- [ ] What the 15.0 px run is has been read off the deck, not inferred
- [ ] Whether the four-slide sample is deterministic is answered
- [ ] Whatever made this go unrun is named, and if it is a missing step it is written into the
      workflow rather than remembered

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the element off the deck, and answer whether the sample can vary | this file §3 |
| 2 | Decide whether the deck or the rule is wrong, and fix that one | the deck |
| 3 | Write down the token arithmetic, so the next author meets it before the gate does | [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) |
| 4 | Every deck gate green, and the slide looked at offline | this file §4 |
| 5 | Ship the patch, per [`PUBLISHING.md`](../docs/PUBLISHING.md) §8 | `v0.1.5` |

## 3. Implement

**What the 15.0 px run is — read off the deck, not inferred**

Slide 12 has no `.standfirst`, so DS-064's probe takes the first `<p>` of its `.body`. That is
`<p class="close-item">The 21:50 linehaul slot, requested this month</p>`, and the composition block
set it `font-size:var(--fs-small)`.

The arithmetic is exact and explains the number to the decimal: `--fs-small` is
`--fs-base / --type-ratio` = `26 / 1.155` = **22.51 du**, and a 720p capture scales by
`k = 0.6667`, giving **15.01 CSS px** against a 16 px floor. The gate reported 15.0 px, 23 du.

**The four-slide sample is deterministic.** `contract.SAMPLE = [0, 4, 7, 11]` — fixed indices, named
in the source as a compromise and documented as one. So the reference deck passing at 17.3 px and
this deck failing at 15.0 px is not a draw: both sample slide 12, and the two decks' slide 12
differ. The reference deck's close carries no body paragraph at all; this one's does.

**Decisions & assumptions**
- **The deck is wrong, not the rule** — 2026-08-10. DS-064's row already records the owner scoping
  the probe *against* widening it to every prose run, because the reference deck's smallest such run
  is a note at `--fs-small` and *"prose this rule was not written about"*. That reasoning does not
  cover this case and points the other way: the three `.close-item` lines are not marginalia, they
  are **what approval authorises**, on the slide the deck exists to reach. A board reading the ask at
  15 px on a shared screen is the exact failure the floor is for. So `--fs-small` → `--fs-body`.
- **The token arithmetic is the finding, not the instance** — 2026-08-10. `--fs-small` cannot clear
  DS-064's floor at any base size DS-034 allows but the very top: the band 24–28 du maps to
  **13.9–16.2 CSS px** at `k = 0.6667`. So the token is legitimate only where the probe will not read
  it — never a `.standfirst`, never the first `<p>` of a `.body`. Written into
  [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) beside the token, where an author choosing it
  looks, rather than into DS-064's row, which is already the longest in the ruleset and is read after
  a failure rather than before one.
- **Why it went unrun, named:** the deck gates are per-deck and the README prints five repository-wide
  commands, so the set someone runs by habit never included `check.py` against
  `examples/sort-window/`. That is not a memory failure to resolve with more care — it is the
  enumeration [T-078](T-078-write-down-the-release-sequence.md) declared the same day.
  [`PUBLISHING.md`](../docs/PUBLISHING.md) §8 now lists the per-deck gates **for both examples**, and
  names what would close its excusal. The step exists in writing; this task is the last of the three
  defects that writing it uncovered.

**Outputs produced**
- `examples/sort-window/sort-window.html` — `.close-item` at `--fs-body`, with the reason and the
  measured number beside it in the composition block.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — `--fs-small`'s row now says where it may
  not be used, and why, with the arithmetic.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The failing run is green, or a reasoned exception with the cost stated | met, green | `0 failure(s): none`. The smallest body run is now **17.3 px (26 du)**, the same figure the reference deck reports, because both are `--fs-base`. |
| What the 15.0 px run is has been read off the deck, not inferred | met | `.close-item`, the first `<p>` of slide 12's `.body`, at `--fs-small`. The arithmetic reproduces 15.01 px against a reported 15.0. |
| Whether the four-slide sample is deterministic is answered | met | It is. `SAMPLE = [0, 4, 7, 11]`, fixed in `contract.py` and documented there as a named compromise. The instrument was never in question. |
| Whatever made this go unrun is named, and written into the workflow rather than remembered | met | The gate list was five repository-wide commands; the per-deck gates are now in `PUBLISHING.md` §8 for both examples, with the condition that closes the excusal. |

**The runs.** `check.py --sources`: 113 rules owned, 82 checked, **0 failures**. `shell.py check`,
`component.py check` and `theme.py check`: green.

**Looked at, offline.** Slide 12 re-rendered at 720p. The three lines now sit at body size under the
headline and read as the ask rather than as a caption; nothing overflows and the block stays centred.
The slide is better for the change, which is the argument that it was a defect and not a tolerance.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | One token, and the deck reads better for it. **The instrument was never the suspect it looked like:** the sample is fixed indices, and the arithmetic reproduces the reported 15.0 px to the decimal from `--fs-base/1.155` at `k=0.667`. What made it worth a `PH1` patch is that DS-064's own row records the owner scoping the probe *away* from `--fs-small` prose — correctly, for marginalia — and this slide put the ask itself in that band, which is the one place the exemption must not reach. The transferable half is the token's, not the slide's, so it is written beside `--fs-small` in the theme contract where an author choosing it will meet it. Shipped in **`v0.1.5`**. |
| 2026-08-10 | → in_progress | Read the element before deciding anything: slide 12 has no `.standfirst`, so the probe takes the first `<p>` of its `.body`, which is `.close-item`. That also settled the sample question — `SAMPLE = [0, 4, 7, 11]` is fixed, so the reference deck passing and this one failing is a difference between the two decks' slide 12, not a draw. |
| 2026-08-10 | (no change) | **Moved from `PH2` to `PH1` by the owner.** The deck is in the published repository and `README.md` points at it; an adopter who runs the documented gate on the shipped example gets a red run today, which is exactly CLAUDE.md's test for reopening PH1 — *a defect an adopter hits in the published plugin is a `PH1` patch, not a PH2 improvement*. The rival, leaving it in `PH2` because nobody has reported it, is an argument that applies to every latent defect and is the one the rule exists to overrule. **This reopens PH1 for the fifth time.** |
| 2026-08-10 | → proposed | Raised from [T-071](T-071-the-intermediate-specifications-carry-their-references.md), which ran the build check on this deck as part of its own review and found a failure that task had not caused — confirmed against the committed file before recording, so the attribution is measured rather than assumed. `high` because the deck is the repository's own evidence that the generator works and it is public; `s` because the row names its slide and its number and the whole question is which of two things produced it. `PH2`: a fix, not a capability. |
