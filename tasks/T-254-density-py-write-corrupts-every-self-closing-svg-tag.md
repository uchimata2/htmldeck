---
id: T-254
title: Fix set_var's self-closing tag insertion, and have write verify what it wrote
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225, T-261]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables:
  - tools/deck/density.py
---

# T-254 — Fix set_var's self-closing tag insertion, and have write verify what it wrote

## 1. Specify

**Outcome**
`density.py write` produces valid markup on a deck containing self-closing SVG tags. Today `set_var` assumes a tag's last character is `>` and everything before it is attribute space, so `<circle ... />` becomes `<circle ... /  style="--dp:0">` — **seven invalid tags on one slide**. The browser reparents the broken subtree and `DS-035` then reports three labels at `0.0 du`, which names neither the tool nor the tag. **It is intermittent** — `0, 3, 3` over three runs — so it reads as a race in the author's own motion.

**From the adopter report** [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md).

**Scope**
- In: the one-line guard in `set_var`: insert before `/>` when the tag is self-closing
- In: **`write` verifying what it wrote** — it already parses the deck to find the tags, so re-parsing and refusing to save a file that gained a malformed tag would have caught this in the run that caused it
- In: whether `DS-035` should say a CTM is degenerate: `0.0 du` is not small type, it is no type
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md) — each carries its evidence, its version and its own proposed fix
- `tools/deck/density.py` `:179` — the branch that runs when the tag carries no `style=` yet
- the adopter's own repair, `re.subn(r'/ (style="[^"]*")>', r' \1/>', html)`, which is evidence of the shape rather than the fix to take

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- **Scope item 3 — should `DS-035` say a CTM is degenerate — is deferred to
  [T-261](T-261-ds-035-measures-a-text-run-through-its-transform.md), settled 2026-08-29.** That task
  already owns it in as many words: its scope reads *naming the transform as the cause when
  `sqrt(|det|)` is under 1*, which is the same measurement and the same row. Two tasks amending one
  probe is the rework the remediation order exists to avoid, and B1's three tasks are held to
  disjoint files on purpose. Nothing here is lost — `PR`-free, the record's item 3 is closed by
  `T-261` in B2, one batch later.
- Otherwise none. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce, at the function rather than at the deck. Four shapes through `set_var`: `/>`, ` />`, a self-closing tag that already carries `style=`, and an ordinary `<p …>` | The two broken shapes named, and the merge branch shown to be sound |
| 2 | Fix `set_var`: find the closing `/>` and insert before it, falling back to the last character when the tag is not self-closing | `tools/deck/density.py` — one branch, no change to the merge path |
| 3 | State the post-condition the fix restores, as a function: same element name, same self-closing form, the property present, still one tag | `written_ok`, which is what step 4 calls |
| 4 | Have `write` verify every tag it wrote and **refuse to save** when one fails, naming the tag | `write` fails loudly instead of writing invalid markup |
| 5 | Seed the defect in both directions (**L-125**): the old insertion must fail step 4, the new one must pass | The guard shown to fire, not merely to exist |
| 6 | Add the four shapes to `self_test`, so the next reader cannot lose the fix | `self_test` covers the self-closing tag it never had |
| 7 | `python tools/tasks/lint.py`, then `python tools/check_all.py`, separately | Both green |

## 3. Implement

**Decisions & assumptions**
- **The insertion point is found, not assumed** — `SELF_CLOSING` matches `\s*/\s*>$`, so ` />` is
  handled as well as `/>` and the original spacing survives. The adopter's own repair
  (`re.subn(r'/ (style="[^"]*")>', ...)`) fixes the output after the fact; it was read as evidence
  of the shape and not taken as the fix, because a writer that produces valid markup needs no
  repair pass and a repair pass has to be remembered — 2026-08-29.
- **The verification is a post-condition, not a search for this bug's shape.** `written_ok` asserts
  what an attribute edit cannot change: the element name, whether the tag closes on `/>` or `>`,
  that the result is still one tag with balanced quotes, and that the property asked for is in it.
  A guard written as *does the output contain `/ style=`* would pass the next insertion defect —
  2026-08-29.
- **Refusing to save is the whole value.** `write` returns 1 and prints each tag before and after;
  the deliverable is left untouched. The adopter lost the better part of a session bisecting three
  deck variants because the run that caused the damage reported success — 2026-08-29.
- **Scope item 3 is deferred to [T-261](T-261-ds-035-measures-a-text-run-through-its-transform.md)**,
  reasoned in §1's open questions — 2026-08-29.

**Outputs produced**
- `tools/deck/density.py` — `SELF_CLOSING`, the `set_var` insertion, `written_ok`, `write`'s
  refusal, and five `self_test` assertions

**What was measured**

| Measurement | Result |
| :--- | :--- |
| The four shapes through `set_var` — `/>`, ` />`, self-closing with an existing `style=`, and `<p …>` | Two were broken before, all four correct after; the merge branch was sound throughout |
| **Seeded, both directions (L-125)** — the replaced insertion restored and run | `self_test` exits with *--dp was written outside the element*; `write` prints *REFUSED … 2 tag(s) came out malformed* and returns 1, **and the file on disk is unchanged** |
| `write` on all six tracked `.html` files, output to a scratch copy | All six byte-identical. Nothing already correct moved |
| `examples/measure-first/measure-first.html` with its 36 `--dp` values stripped and rewritten, so the add branch runs on four bare self-closing circles rather than the merge branch | **Restored byte-for-byte to the shipped deck**, zero malformed tags. The new insertion produces exactly the markup that shipped |

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy measured, or explicitly deferred with the reason recorded | met | Record [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md) items 1 and 2 are implemented and measured above. Item 3 is deferred to [T-261](T-261-ds-035-measures-a-text-run-through-its-transform.md) with the reason in §1 |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | met | Row 2 of *What was measured*. The guard fires on the seeded insertion and passes every correct edit |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | met | `lint.py` all four steps green with the baselined **eleven** advisories and no more. `check_all.py` **0 failures, 0 unclassified, 0 stale** over 37 commands and all 50 tracked tools, 278 s, run separately and after the last edit |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Every criterion met. The proof that settles it is not the fixture: `measure-first.html`'s 36 `--dp` values stripped and rewritten through the branch the defect lived in came back **byte-for-byte identical to the shipped deck**, and the seeded old insertion is refused with the file left untouched. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-29 | → specified | Batch B1 of [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md). Scope item 3 deferred to [T-261](T-261-ds-035-measures-a-text-run-through-its-transform.md), which already owns the same `DS-035` measurement; `related` gained it and the deliverable is declared. The defect was reproduced at the function before the scope was closed, so *seven invalid tags* is this tree's reading rather than the report's. |
| 2026-08-29 | → in_progress | The insertion fixed, `written_ok` written as `set_var`'s post-condition, `write` taught to refuse, and five assertions added to `self_test`. The proof that mattered most was not the fixture: `measure-first.html`'s 36 `--dp` values stripped and rewritten through the add branch came back **byte-for-byte identical to the shipped deck**. |
| 2026-08-29 | → planned | Seven steps. Steps 3 and 4 are the record's item 2 — the verification is stated as `set_var`'s post-condition rather than as a search for the shape of this one bug, because a guard that only knows the defect it was written for reports green on the next one. |
