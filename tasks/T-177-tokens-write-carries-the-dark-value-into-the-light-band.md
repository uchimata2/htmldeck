---
id: T-177
title: shell.py tokens carries a dual-band token's dark value into the light band
type: fix
status: done
phase: review
shipped_in: 0.4.0
parent: null
blocked_by: []
related: [T-166, T-114]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-18
updated: 2026-08-18
deliverables: []
---

# T-177 — `shell.py tokens` carries a dual-band token's dark value into the light band

## 1. Specify

**What happened, and how it was seen.**
[T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md) added `--nav-line` to draw
the chrome's navigation container, declared in **both** colour bands of both themes — light beside
`--ui-line` near the top, dark in the second band — which is how every colour token in
[`../docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) is declared. `shell.py tokens <deck>
--write` then added **one** declaration to each deck, in the deck's light `:root`, carrying the
**dark** value `#4A463C`. The light band got a near-black border and the dark band got nothing.

**Why nothing caught it.** `theme.py check` passed: DS-013 asks whether every contracted token is
*declared*, and it was. No rule asks whether it was declared at the right value in the right band,
and no gate compares a deck's declaration against the shipped theme's — which is the point of
`tokens` and also its blind spot.

**The mechanism.** `shipped_values()` in [`../tools/deck/shell.py`](../tools/deck/shell.py) is
`theme_mod.declarations(read(theme_css))`, a flat `{name: value}` map. A token declared twice
collapses to whichever declaration is read last, and the dark band is second in both
`themes/lattice.css` and `themes/quarto.css`. `declare_tokens()` then writes that single value into
the one block it knows about.

**Why it had never bitten.** `tokens` shipped with [T-166](T-166-shell-sync-leaves-an-upgraded-deck-failing-the-theme-gate.md)
and only writes tokens a deck is *missing*. Every dual-band token predates it, so every deck already
declared them all. `--nav-line` was the first new one, and it failed on its first use.

**What T-114 did instead, and why that is not the fix.** It dropped `--nav-line` and bordered the
box on `--line`, which is already contracted, already in both bands, and already in every deck — so
no deck needed a new declaration at all. That removes the instance. **The defect is still there and
the next dual-band token meets it**, which is why this is a task rather than a note.

**Candidate fixes, in the order they should be argued.**

1. **Refuse rather than guess.** `undeclared_tokens()` learns which tokens the shipped theme
   declares more than once, and `tokens --write` skips them with the message the tool already has
   for a value it cannot copy — *declare them by hand, THEME-CONTRACT.md gives each a band*. Small,
   honest, and it makes the tool say what it does not know.
2. **Carry both bands.** `declare_tokens()` writes the light value to the deck's light block and the
   dark value to its dark block. Better for an adopter, and it needs `theme.py` to expose bands
   rather than a flat map — which is the larger half of the work.

**Recommendation: 1, then 2 if an adopter meets it.** A tool that writes a wrong value silently is
worse than one that declines, and the decline costs one line of prose in the report.

## 2. Acceptance criteria

| # | Criterion | Met |
| :-- | :--- | :--- |
| 1 | A token declared in both bands of the shipped theme is never written at one value into one band | yes |
| 2 | The self-test seeds exactly this: a two-band token missing from a deck, and asserts what `--write` does with it | yes |
| 3 | The report names the token and says why it was not written, in the shape T-166's report already uses | yes |

## 3. Implement

**Both fixes, and they compose rather than compete.** The owner ruled **refuse *and* carry both**
on 2026-08-18, and the two are not alternatives: carrying handles the case the tool can settle, and
refusing handles the case it cannot. What decides which is whether **this deck** has a band to
receive each value the shipped theme declares.

**What was built**

| Where | What |
| :--- | :--- |
| [`../tools/deck/theme.py`](../tools/deck/theme.py) | `blocks()` — top-level rules with braces matched, comments stripped first; and `bands()` — `{band: {token: value}}` keyed `light` / `dark`. `declarations()` is untouched: flattening is right for *reading* a value and wrong for *carrying* one, and both questions now have a function |
| [`../tools/deck/shell.py`](../tools/deck/shell.py) | `shipped_bands()`; `undeclared_tokens()` returns `{band: value}` per token instead of one string; `declare_tokens()` returns `(html, added, refused)` and writes each band into the deck's own; `TOKEN_BLOCK_DARK`, appended after the deck's bands where `:root[data-theme="dark"]` outranks `:root`; `refusal_report()` |
| the `tokens` command | prints refusals, names the bands it wrote, and **exits non-zero when anything was declined** even though something else was written |

**Two things found while building it, both worth more than the fix**

- **The comment strip is load-bearing, not tidiness.** Everything between the previous `}` and the
  next `{` is the selector, so both theme files' opening banners landed *inside* the first selector
  and `:root` stopped matching `:root`. The first run of `bands()` returned `{}` on both themes and
  reported it plainly, which is the only reason it took a minute rather than an afternoon.
- **`TOKEN_MARK` was a prefix of `TOKEN_MARK_DARK`,** so `TOKEN_MARK in region` matched the dark
  block and the light insert would eventually have gone into it. Carrying the colon into the mark
  separates them and emits byte-identical text, so no deck changed.

**The fixtures were proven to discriminate, not just to pass.** The old flat-map path was
reconstructed and run against the new assertions: it puts `#3B382F` — the **dark** value — into the
light band and leaves the dark band empty, and fails them. The new path writes `#D7D1C2` light and
`#3B382F` dark and passes. A fixture that has only ever been green is a claim about the instrument
(**L-04**, **L-36**), and this one has now been seen red.

**No deck changed.** All three already declare every contracted token, so `tokens` is a no-op on
them; the mark change is byte-identical. The defect was latent for future tokens and is now closed
before one arrives.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| A dual-band token is never written at one value into one band | met | `declare_tokens` writes per band or declines; asserted both ways |
| The self-test seeds exactly this and asserts what `--write` does | met | Eleven new fixtures, 66 of 66 green, and the old path was reconstructed and shown to fail them |
| The report names the token and says why, in T-166's shape | met | `refusal_report()`, and the command exits non-zero when anything was declined |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Filed by [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md), which met the defect and sidestepped it by bordering on `--line`. Recommendation recorded: refuse first, carry both if an adopter meets it. |
| 2026-08-18 | proposed → review | **Owner ruled both, and both are built.** `theme.bands()` splits the two bands; `declare_tokens()` carries each into the deck's own and declines what the deck has no band for, naming the token and the reason. **The old path was reconstructed and shown to fail the new fixtures** — it writes the dark value into the light band and leaves dark empty — so the eleven fixtures have been seen red as well as green. Two incidental finds: stripping comments before scanning selectors is load-bearing (both themes' banners had swallowed `:root`), and the light mark was a prefix of the dark one. `check_all.py` 0 failures in 198 s; no deck changed, because all three already declare every contracted token. |
| 2026-08-18 | review → done | **Shipped in `0.4.0`.** Repository tooling only; it requires nothing of a deck and §8.1's row says so rather than leaving it inferred. |
