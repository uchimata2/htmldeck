---
id: T-128
title: Publish the adopting project's D6 deck as a third worked example, sanitized on the way in
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-123, T-124, T-125, T-085]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - examples/
  - CLAUDE.md
  - examples/README.md
  - tools/check_all.py
---

# T-128 — Publish the adopting project's D6 deck as a third worked example, sanitized on the way in

## 1. Specify

**Outcome**
`examples/` carries a third deck: the one the first adopting project actually built, specified and
presented, with its foundation and slide specifications beside it. It is the only deck here that was
**not written to be an example** — which is exactly what makes it worth shipping, because the two
existing ones were both authored inside this repository against its own rules.

**The owner's ruling, 2026-08-13**
`CLAUDE.md` forbids copying deck content in and requires an example to be written fresh on a neutral
topic. The owner lifted that **for this deliverable only**: it is an exam exercise, not a real
engagement, and nothing personal or sensitive is involved. Two conditions came with it — **sanitize
the copy**, and **leave the source folder untouched**. `CLAUDE.md` carries the exception; this task
carries the work.

**What is there, surveyed read-only 2026-08-13**

| | |
| :--- | :--- |
| the deck | 13 slides, 5 stages, **zero external references**, 364 KB |
| its specifications | a foundation spec and a slide spec, ~37 KB together |
| what it cites | five analysis documents and two BPMN diagrams, all in the same project |
| shell state | **two releases behind** — `COMPONENTS` and `SCRIPT` both differ from `shell/` |
| printed | 14 pages, and its contents sheet carries the T-116 collision ([T-123](T-123-nothing-can-see-a-print-only-layout-fault.md) §1) |

**What sanitizing actually costs, measured rather than assumed**
A scan for personal names, e-mail addresses, local paths, `file://` links and third-party URLs
returns **nothing** — the only URLs are the three font-licence links the plugin embeds itself. What
it does return is two classes, and **both are visible slide copy rather than comments**, so this is
editorial work and not a find-and-replace:

- **the case company, 53 occurrences in rendered text** — the invented firm the exercise is set at;
- **`exam` / `exercise`, 54 occurrences in rendered text** — the deck names its own assessment
  context, which a published example must not do.

**The one thing this task must not decide by itself**
The deck analyses a business case **supplied by a training provider** as module material. Renaming
the company does not change where the scenario, its structure and possibly its figures came from,
and this repository is public. That is a provenance question for the owner, not a sanitization step
— it is the first open question below, and nothing gets published until it is answered.

**Why it is worth the effort anyway**
1. **It is the only deck here nobody wrote to pass these gates.** Every rule this project states was
   either written before the two existing examples or fixed by them; a deck built elsewhere, by
   someone reading the published skill, is the only honest test of the ruleset.
2. **It is 13 slides.** Both current examples are 12, which is the floor the brief says is not the
   target, and 13 is where the contents page first collided.
3. **It exercises the upgrade path end to end.** The copy is two releases behind, so the migration
   is a real `shell.py sync --write` on a real adopter deck — the first, and the thing
   [T-124](T-124-an-adopter-cannot-refresh-a-decks-shell-after-an-upgrade.md) shipped for.
4. **It gives [T-123](T-123-nothing-can-see-a-print-only-layout-fault.md) a fixture with a known
   answer** — a deck that printed the collision before the fix and must print clean after it.

**Scope**
- In: the deck, its two specifications, and whatever source documents the provenance ruling allows.
- In: sanitization, the shell sync, the gates, and a print that is looked at.
- In: `examples/README.md`, and `check_all.py` if a third deck needs registering.
- Out: the adopting project's folder. **It is read-only in this matter** — copy out, never write
  back, and never regenerate anything in place there.
- Out: the exam material in that project's `docs/source/`. Third-party PDFs are not ours to move.
- Out: rebuilding the deck from its specification. This ships what was built, brought up to date.

**Inputs**
- The adopting project's `deliverables/` — the deck, the two specs, the five analysis documents.
- [`CLAUDE.md`](../CLAUDE.md) *Publishing constraints* — the exception and its two conditions.
- [`examples/README.md`](../examples/README.md) — how the existing two examples are documented, and
  the measurement claims a third one will owe.
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) §2, §5 — the humanizer's covered set, which a new
  human-facing page joins.

**Acceptance criteria**
- [ ] The provenance question is answered by the owner before anything is copied
- [ ] No occurrence of the two sanitization classes survives in any published file, checked by
      re-running the scan rather than by reading
- [ ] The deck passes every per-deck gate `check_all.py` runs, and `check_all.py` accounts for it
- [ ] It renders offline and is **printed and looked at** — the contents sheet clean at 13 entries
- [ ] The source project's folder is byte-for-byte unchanged, verified rather than asserted
- [ ] `examples/README.md` states what the deck is, where it came from, and what it demonstrates

**Open questions**
- **May the scenario itself be published, or only the artefact?** The case comes from a provider's
  module material. **Recommended: publish the artefact with the scenario re-based** — keep the
  structure, the diagrams, the pipeline record and the analysis, and replace the case's identity and
  any figure the provider supplied rather than the author derived. The alternative is to publish it
  as-is once the owner confirms the case is theirs to republish, which is cheaper and is the owner's
  to assert, not mine. — the owner
- **Does it ship with its sources, like `sort-window/`, or alone?** Recommended: with them, since a
  provenance mark that opens nothing is a mark for a feature the deck is demonstrating. Depends
  entirely on the answer above.
- **Does it keep its `D6` name?** Recommended: no — a name from another project's numbering means
  nothing here. Name it for its subject, as `sort-window` is.

## 2. Plan

**The order matters and the first step is a gate, not a task.** Nothing is copied until the
provenance question is answered, because an unpublishable copy in the working tree is one commit
away from being published.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Get the provenance ruling, and the naming decision with it | the answers |
| 2 | Copy the deck and its two specifications out to `examples/<name>/`, read-only at the source | the raw copy |
| 3 | Sanitize the copy: the case identity and every `exam` / `exercise` mention, in the deck **and** both specs, keeping the analysis intact | the copy |
| 4 | Re-run the scan over the copy — zero hits in both classes, and re-run it over the two font-licence URLs to confirm they are all that is left | the evidence |
| 5 | `shell.py sync <deck> --write`, then `shell.py check` — the first real adopter upgrade this repository performs | a current deck |
| 6 | Every per-deck gate: `check.py`, `component.py`, `theme.py`, `spec.py` against the specs | green or a list |
| 7 | Register it: `check_all.py`'s deck list, `examples/README.md`, and the measurement figures `figures.py` watches | the account |
| 8 | Print it and **look at it** — 14 pages, contents sheet clean at 13 entries (**L-01**, **L-76**) | the printed evidence |
| 9 | Verify the source folder is unchanged, then close | the record |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised on the owner's instruction, with the source surveyed read-only and the sanitization surface measured rather than guessed: no personal data of any kind, and two classes of visible copy totalling 107 occurrences. Specified and planned in one pass because the owner was closing the session and asked for the migration *prepared*; nothing has been copied, which is deliberate — step 1 is a question only they can answer. `l` because the sanitizing is editorial work across a 13-slide deck and two specifications, not a substitution. |
