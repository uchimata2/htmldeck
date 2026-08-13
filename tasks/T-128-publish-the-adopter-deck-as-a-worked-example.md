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

**The provenance ruling, 2026-08-13 — the answer is publish, and the figures stay**

The owner ruled step 1: **the case and its figures are theirs and the trainer's, made up rather than
supplied, and neither secret nor proprietary.** So the artefact ships with its analysis coherent —
no re-basing of figures, which was the recommendation below and is now withdrawn as unnecessary
rather than rejected. What must go is wider than the two classes measured above:

| Class | Where it stands |
| :--- | :--- |
| the case company's name | 53 occurrences in rendered text, measured |
| `exam` / `exercise`, **and any reference to the training context** | 54 occurrences measured; *references* are new and widen the scan beyond the two words |
| **place names** | new to the ruling; part of the case identity and not yet counted |
| external dependencies | the deck already measures **zero external references**, so this is a re-check rather than work |
| sensitive, personal or local-system data | the survey returned none of it; re-checked on the copy rather than trusted |
| the figures | **kept** |
| the colour palette | **unchanged.** The owner allowed a new one only if it were free, and it is not free in the way that matters: an example carries the plugin's one theme, which is CLAUDE.md rule 4. A palette of its own would make it the only deck here that does not demonstrate the shipped theme |

**Two questions the ruling settles by implication, decided here rather than sent back**

- **It ships with its sources.** The analysis documents are the author's own by the same ruling that
  freed the figures, and a deck without a `--sources` directory cannot be gated the way both existing
  examples are — `check_all.py` refuses a deck with no declaration. The provider's PDFs stay out;
  that was already Scope.
- **The `D6` name goes.** A name from another project's numbering means nothing here. It is named for
  its subject, as `sort-window` is.

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
- [ ] No occurrence of **any** of the ruling's classes survives in a published file — case identity,
      training context and references to it, place names, external references, sensitive or
      local-system data — checked by re-running the scan rather than by reading
- [ ] The figures and the analysis are intact: the deck still argues what it argued
- [ ] The deck passes every per-deck gate `check_all.py` runs, and `check_all.py` accounts for it
- [ ] It renders offline and is **printed and looked at** — the contents sheet clean at 13 entries
- [ ] The source project's folder is byte-for-byte unchanged, verified rather than asserted
- [ ] `examples/README.md` states what the deck is, where it came from, and what it demonstrates

**Open questions**
- ~~**May the scenario itself be published, or only the artefact?**~~ **Answered by the owner
  2026-08-13: published, with the figures kept** — they were invented by the owner and the trainer,
  and are neither secret nor proprietary. The sanitization list widened; see *The provenance ruling*
  above.
- ~~**Does it ship with its sources, like `sort-window/`, or alone?**~~ **With them**, decided from
  the ruling rather than sent back: the same sentence that frees the figures frees the analysis, and
  a deck with no `--sources` directory cannot be gated the way its two siblings are.
- ~~**Does it keep its `D6` name?**~~ **No** — named for its subject, as `sort-window` is.
- **Where is the adopting project?** No record in this repository names its path, and the survey that
  produced §1 was done in a session that knew it. Needed before step 2. — the owner

## 2. Plan

**The order matters and the first step is a gate, not a task.** Nothing is copied until the
provenance question is answered, because an unpublishable copy in the working tree is one commit
away from being published.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | ~~Get the provenance ruling, and the naming decision with it~~ **done 2026-08-13**; what is still missing is the source path | the answers |
| 2 | Copy the deck, its two specifications and its analysis documents out to `examples/<name>/`, read-only at the source | the raw copy |
| 3 | Sanitize the copy across the ruling's six classes — case identity, training context **and references to it**, place names, external references, sensitive or local-system data — in the deck **and** every document beside it, keeping figures and analysis intact | the copy |
| 4 | Re-run the scan over the copy — zero hits in every class, and confirm the two font-licence URLs are all that is left | the evidence |
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
| 2026-08-13 | (no change) | **The owner ruled step 1: publish, and the figures stay** — the case and its numbers were invented by the owner and the trainer, so nothing here is the provider's to withhold. The re-basing this task recommended is withdrawn as unnecessary rather than rejected. The sanitization list widened in exchange: place names, *references* to the training context as well as the two words, and a re-check for external and local-system data. The palette stays the shipped one — the owner allowed a new one only if free, and an example that does not carry the plugin's single theme is not free (CLAUDE.md rule 4). Two dependent questions decided here rather than sent back: it ships with its sources, and the `D6` name goes. **Still not started, and nothing has been copied**: no record in this repository names the adopting project's path. |
| 2026-08-13 | → proposed | Raised on the owner's instruction, with the source surveyed read-only and the sanitization surface measured rather than guessed: no personal data of any kind, and two classes of visible copy totalling 107 occurrences. Specified and planned in one pass because the owner was closing the session and asked for the migration *prepared*; nothing has been copied, which is deliberate — step 1 is a question only they can answer. `l` because the sanitizing is editorial work across a 13-slide deck and two specifications, not a substitution. |
