---
id: T-292
title: The docs gate is four fifths one render — decide what figures.py's coverage account binds to
type: fix
status: done
phase: review
parent: T-287
blocked_by: []
related: [T-285, T-234]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
finding: CE-18
created: 2026-09-02
updated: 2026-09-02
shipped_in: 0.7.0
deliverables: []
---

# T-292 — The docs gate is four fifths one render — decide what figures.py's coverage account binds to

## 1. Specify

**Outcome**
`python tools/check_all.py --docs` no longer spends most of its time rendering a deck. Measured
2026-09-02 on the frozen tree: **`figures.py` was 22.5 s of the 27.6 s** the docs gate spent in
commands (81.4%), because it resolves the README's *coverage of the ruleset* account by running
`check.py` on the reference deck — a render inside the documents gate, which `T-285` §3 named for this
audit rather than fixed. The finding is `CE-18` in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3. **The gain is seconds, not tokens** —
the run prints one line either way — and it ranks because the owner's question was about the cost of
a batch.

**The remedy is a hypothesis, and L-152 bounds it**: a count is bound or deleted, never refreshed. So
a cached figure is not an answer. Candidates to measure: bind the account to the ruleset table that
`check.py` itself reads, which is a document and not a render; or let `--docs` skip that one binding
with a printed reason, since the full gate still resolves it.

**Scope**
- In: one binding in `figures.py`; the docs-mode timing table re-taken after.
- Out: the full gate's behaviour; any figure other than the coverage account.

**Inputs**
- `../tools/docs/figures.py`, `T-285` §3, `../docs/lessons/L-152.md`

**Acceptance criteria**
- [ ] The docs gate's command time re-measured, before and after, on one tree.
- [ ] The coverage account is still bound to something live, or its deletion is argued from L-152.
- [ ] Full gate green.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the binding; find what `check.py` reads to produce the count | `owned by a gate` is in the ruleset; **`checked` is a run result and is in no document** |
| 2 | Before rebinding anything, ask whether the account is what forces the run | **Empty `ACCOUNTS`; `check.py` runs anyway.** The premise fails here |
| 3 | Find what does force it | `README.md` pastes the command's output in a fence, and `figures.py` compares the paste against a live run |
| 4 | Time the tool by command, not by mode | `figures.py` 33.2 s; `check.py` 28.7 s of it; the other five 4 s together |
| 5 | Refuse the remedy, keep the binding, raise the reshaped one | [T-296](T-296-the-readmes-deck-gate-fence-is-what-the-docs-gate-pays-for.md) |

## 3. Implement

**Decisions & assumptions**
- **The coverage account stays exactly where it is, and that is this task's answer.** `CE-18` says `figures.py` *resolves the README's coverage account by running `check.py` on the reference deck*. Empty `ACCOUNTS`, run the tool, and `check.py` still runs — so the account is a **second reader of a run that happens for another reason**. Rebinding it saves no seconds and trades a live binding for a weaker one — 2026-09-02
- **The first candidate was impossible anyway, for a reason worth writing down.** *Bind the account to the ruleset table `check.py` reads* cannot work: the whole, `owned by a gate`, is printed by `ruleset.py --counts`, and the part, `checked`, is a **result of a run over a deck** that appears in no document. An account whose two halves live at different altitudes has no document to bind to — 2026-09-02
- **What costs the time is a fence on the front page.** `README.md` pastes `check.py examples/reference-deck.html`'s output, and `figures.py` compares every pasted block against a live run. `figures.py` alone is **33.2 s**; `check.py` is **28.7 s** of it and the other five commands 4 s together — 2026-09-02
- **The reshaped remedy is raised, not absorbed.** §4's elastic says a batch finishes what it found, and B11's precedent says a batch may judge the elastic too long and record it. Every candidate removes something the front page guarantees on every documentation commit, which is a ruling rather than a fix — 2026-09-02

**Outputs produced**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — `CE-18`'s mechanism refuted where it is stated, and pointed at its true subject
- [`T-296`](T-296-the-readmes-deck-gate-fence-is-what-the-docs-gate-pays-for.md) — the decision the measurement produced
- **No change to `../tools/docs/figures.py`.** The binding this task existed to move is the one thing that should not move

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| the docs gate's command time re-measured, before and after, on one tree | **partly met** | The **before** is measured per command, which is finer than the row had it: `figures.py` 33.2 s, `check.py` 28.7 s of that, five other commands 4 s together. There is no *after*, because the change this task was scoped to make is the one the measurement says not to make |
| the coverage account is still bound to something live, or its deletion argued from **L-152** | pass | Still bound, to the same command, and the argument is stronger than the row's: the run is not this binding's to pay for. **L-152** does not reach it — nothing here is a count being refreshed |
| full gate green | pass | Run separately from `lint.py`, on the frozen tree, at the batch's landing |

**Child fix tasks raised**
- [T-296](T-296-the-readmes-deck-gate-fence-is-what-the-docs-gate-pays-for.md) — what a documentation commit may skip on the front page. Raised rather than absorbed: each candidate removes a guarantee, which is the owner's to give up

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | proposed → done | B20. **The remedy is refused on the measurement, and the binding this task existed to move is the one thing that should not move.** `CE-18` names the coverage account as what runs the deck gate inside `figures.py`. Empty `ACCOUNTS` and `check.py` still runs, because `README.md` pastes its output in a fence that is compared against a live run — the account is a second reader, and rebinding it buys nothing. The row's other candidate was impossible for its own reason: the account's whole is in the ruleset and its part, `checked`, is a run result appearing in no document. Timed per command rather than per mode: **33.2 s, of which 28.7 s is the one render**. The remedy that would work removes a guarantee from the front page on every documentation commit, so it went to [T-296](T-296-the-readmes-deck-gate-fence-is-what-the-docs-gate-pays-for.md) rather than into this batch. |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-18`, the cost `T-285` §3 named for it. `PH3`. |
