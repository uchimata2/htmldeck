---
id: T-128
title: Publish the adopting project's D6 deck as a third worked example, sanitized on the way in
type: deliverable
status: in_progress
phase: implement
parent: null
blocked_by: [T-167, T-168]
related: [T-123, T-124, T-125, T-085]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-13
updated: 2026-08-16
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

**The surface measured against the ruling, read-only 2026-08-13**

Scanned across the deck, both specifications, D1–D5, D7, the deliverables README and the two BPMN
models. **Nothing was written to the source.**

| Class | Count | Where |
| :--- | ---: | :--- |
| case company — `DentalPro Solutions GmbH` / `DentalPro` | **121** | every file; a rename, plus a legal form that goes with it |
| training context — `course` / `course's` | **17** | deck, both specs, D4, D5, the To-Be model |
| place names | **0** | measured against countries, regions and 24 cities — the case names none |
| external references | 14, **all inert** | 4 OFL licence URLs, 3 SVG namespaces, 3 font repositories, 1 Lucide licence. Text, not loads: the deck still fetches nothing |
| personal data | **3**, all in D7 | the owner's given name in the audit report — **and D7 is not in the copy set**, so the class is empty for what ships |
| local-system paths, `file://` links, e-mail addresses | **0** | the one `file://` hit is a sentence *about* DS-105 forbidding such a link |

**Two of the classes were false alarms until the scan was made to bind on structure rather than on
vocabulary, and the difference is 148 hits.** A first pass matching `exam*`, `exercis*` and
`assessment` returned 165 training-context hits; 97 were the word *example*, 24 were the case's own
*business value assessment matrix*, and `trainer` and `training` are a role and a staff activity in
the redesigned process, not the course. The real class is `course` alone, and every one of its 17
occurrences cites the training material **as a source** — *the same option the course material
suggests*, *the course's four phases*, *the course names that limit*. That makes it editorial work
rather than a substitution: the deck uses the citation as a rhetorical move, and the replacement has
to keep the argument.

**D7 is out of the copy set**, which is what empties the personal-data class. The deck cites D1–D5;
D7 is an audit of the build and names the owner three times.

**A note this task earned the hard way.** The survey above first recorded the owner's given name
verbatim, in this file, in a public repository — the exact class it was measuring, written down while
measuring it. `CLAUDE.md`'s publishing constraint is *free of personal, client and machine data*, and
a scan report is not an exemption from it. **Name the class, never the value**, the same rule
`docs/PUBLISHING.md` applies to secrets. The adopting project's path is deliberately absent from this
record for the same reason: it is an absolute path on somebody's machine and it names a person.

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
- [ ] **No identifier or path from the source project's own namespaces survives** — its lesson,
      requirement, task and deliverable IDs, and every `../` link into its tree — checked by
      **resolving each against this repository**, never by reading. An ID that resolves here to a
      different document passes every other check on this list
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
- ~~**Where is the adopting project?**~~ **Answered by the owner 2026-08-13.** Surveyed read-only
  the same day; the measured surface is in §1 and the naming decisions are in §3.

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
- 2026-08-13 — **the new case identity is `Larkfield Dental Group`**, replacing `DentalPro Solutions
  GmbH`. Invented, and `Group` rather than `GmbH` drops the jurisdiction marker, which is the
  *locations* half of the owner's instruction — there are no other place names to remove. The page
  says it is illustrative, as `examples/README.md` already does for Riverbend.
- 2026-08-13 — **the example is named `measure-first`**, after its argument rather than after
  another project's numbering, as `sort-window` is. The governing idea is that measurement and
  discipline fix demand planning before any AI is bought.
- 2026-08-13 — **the 17 `course` citations become citations of a reference framework**, one at a
  time. They are load-bearing — *the same option the course material suggests, for reasons of our
  own* is a rhetorical move, not a decoration — so each is rewritten to keep the argument rather
  than deleted. This is the editorial work the `l` estimate is about.
- 2026-08-13 — **D7 is not copied.** The deck cites D1–D5; D7 audits the build and carries the only
  three occurrences of personal data in the whole set.

- 2026-08-16 — **a seventh sanitization class, found by reading the two specifications rather than
  by scanning them: identifiers from the source project's own namespaces.** The six ruled classes are
  all about *content*; this one is about *reference*, which is why a vocabulary scan cannot see it.
  Three kinds, and they need opposite treatment:
  - **Collides with an htmldeck ID and resolves to a different document.** The foundation cites
    `(L-25)` for *a count true of the full map is false beside a simplified drawing of it*, and the
    source's deliverables README cites `(L-17)`. Both numbers exist here:
    [`docs/lessons/L-25.md`](../docs/lessons/L-25.md) is *two conformance floors on one element can be
    jointly unsatisfiable* and [`docs/lessons/L-17.md`](../docs/lessons/L-17.md) is *a permission you
    spend once cannot be shared across measurements*. **Neither is broken, and that is the defect** —
    a reader who follows one arrives somewhere real and wrong, and no link checker can object.
  - **Dangles.** `R-612` and `R-619` are the source project's requirement IDs and match nothing in
    this repository; so do `T-001`–`T-007`, `[D-006]`, `[D-007]`, and the specs' link to
    `../tasks/T-068-rebuild-d6-v2-…`, which lands in this repository's `tasks/` where
    [T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) is a different task under
    the same number.
  - **Resolves correctly and stays.** `DS-085`, `DS-105`, `X-04`, the `A-nn` archetypes and the
    `R-6nn`-shaped IDs that *are* this plugin's are htmldeck's own, cited by an adopter that built
    with the published skill — which is the deck's whole value as an example. Verify each against
    [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) before keeping it; do not strip by pattern.
- 2026-08-16 — **`docs/source/` is a training-context reference and goes.** Slide 10's specification
  says the limitations frame *reached this deck from `docs/source/` rather than from D1–D5* — a path
  into the source project's course material. It carries neither of the two scanned words, which is the
  same lesson the 148 false hits taught in the other direction.

**Progress, 2026-08-16 — steps 2 to 6 of the plan, and step 6 is where it stands.**

| Step | State | Evidence |
| :-- | :--- | :--- |
| 2 copy out | **done** | 14 files, 590 KB, into `examples/measure-first/`. A SHA-256 baseline of all 68 source files was taken **before** the copy, so step 9 can verify rather than assert |
| 3 sanitize | **done** | 167 substitutions across all 14 files |
| 4 re-scan | **done** | case identity **0**, training context **0**, place names **0**, foreign paths **0** |
| 5 shell sync | **done** | `COMPONENTS` 815→860 lines, `SCRIPT` 686→847; `shell.py check` green afterwards. **It raised [T-166](T-166-shell-sync-leaves-an-upgraded-deck-failing-the-theme-gate.md)** |
| 9 source untouched | **verified** (re-verify at close) | all **68** source files re-hashed against the pre-copy baseline: **0 changed, 0 added**. The read-only condition held |
| 6 per-deck gates | **diagnosed; 3 defects raised** | `shell.py` pass · `component.py` pass · `theme.py` pass · `check.py` DS-100, DS-168, FIG-1, FIG-3 → [T-167](T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md), [T-168](T-168-sources-open-ships-with-no-minimum-target-size.md), and one false alarm |

**The copy's shape changed once, and `check.py` is what decided it.** The diagrams were first put in
`sources/diagrams/`, and `FIG-0` failed with *source files this reader cannot open: 6* — the sources
directory is the five documents the deck cites, not a folder of everything that came with them. They
now sit at `examples/measure-first/diagrams/` and D1 and D3 reach them as `../diagrams/`.

**`--qv-measure` was declared by hand to get past `theme.py`**, matching the `80rem` both shipped
decks carry. That is the workaround, not the fix;
[T-166](T-166-shell-sync-leaves-an-upgraded-deck-failing-the-theme-gate.md) is the fix.

**All four are now diagnosed, and three are defects in this repository rather than in the deck.**

| Failure | Cause | Where it goes |
| :--- | :--- | :--- |
| `DS-100` | the gate reads the **quoted sources** as slide copy — the questions are D1's and D2's section headings | [T-167](T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md) |
| `FIG-3` | same cause: 122 of the 152 figures it compared were quotations | [T-167](T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md) |
| `DS-168` | `.sources-open` ships with **no minimum target size**; 23.2 px against a 24 px floor | [T-168](T-168-sources-open-ships-with-no-minimum-target-size.md) |
| `FIG-1` | the binder cannot bind a figure split across table cells — D5 carries *Month 4* in one cell and *stop-or-go gate* in the next | below |

**The method mattered more than the answers.** The `DS-100` reading in the previous entry — that
slide 8's four analytics questions were the trigger — **was wrong**, and so was the first `DS-168`
hypothesis, that the ruler compresses at 13 sections. Both were settled by measuring: the quick-view
regions were emptied on a scratch copy and the gate re-run, and the browser was asked which element
was 23.2 px rather than reasoned at. Neither guess would have survived being written into a fix.

**`FIG-1` is a false alarm and is not being raised.** One figure of 30, and the binder is documented
as approximate. Recorded here so a later run does not re-diagnose it: the month-4 gate **is** sourced,
in `D5-management-decision-matrix.md`, split across two cells of one table row.

**Nothing has been written to the source.** Every scan and read opened it read-only, and the copy was
one-way.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | (no change) | **Step 6 diagnosed: three of the four `check.py` failures are this repository's defects, not the deck's.** [T-167](T-167-checkpy-reads-a-quoted-source-as-the-decks-own-slide-copy.md) — the content half charges a deck for what its **quoted sources** say, which failed `DS-100` and `FIG-3` and had 122 of 152 "deck figures" coming out of quotations. [T-168](T-168-sources-open-ships-with-no-minimum-target-size.md) — `.sources-open` ships with no minimum target size and rendered at 23.2 px against DS-168's 24. `FIG-1` is a false alarm, recorded and not raised. **This is the return the task was raised for**: three latent defects in the published plugin, none of which either deck written inside this repository could expose, found by the first deck whose sources somebody else wrote. |
| 2026-08-16 | (no change) | **Steps 2–5 done; step 6 stands at four `check.py` failures.** The upgrade path found its first real defect: `sync` installs a shell that reads `--qv-measure`, the deck built at 0.2.2 never declared it, and both commands an adopter is told to run report success — [T-166](T-166-shell-sync-leaves-an-upgraded-deck-failing-the-theme-gate.md), raised `PH1` because it is reachable from the published plugin. The sanitization scan and the substitution pass are scripted rather than hand-made, so criterion 2's *re-running the scan* is real; whether either tool earns a home in `tools/` is a judgement for step 7, when `check_all.py` is in hand. |
| 2026-08-16 | → in_progress | **The owner supplied the source path, which was the only thing step 1 still lacked, and it stays out of this record.** Both specifications read before copying, on the owner's instruction — and reading them found a class no scan had: the deck's *references*, not its words. `L-25` and `L-17` are cited there in the source project's lesson numbering and **both numbers exist here as different lessons**, so those two citations survive every gate and mislead. `R-612`, `R-619`, `T-001`–`T-007` and a link to a `T-068` that is another task here dangle instead. Recorded as a seventh class in §3 with an acceptance criterion that resolves rather than reads. Two figures also firmed up: the deck is **twelve slides plus a colophon**, thirteen sections, which is what the 13-entry contents sheet counts; and it is **v2 on htmldeck 0.2.2**, so the shell sync in step 5 crosses 0.2.3 and 0.2.4. |
| 2026-08-13 | (no change) | **The owner accepted both naming decisions**, so §3's `Larkfield Dental Group` and `measure-first` are rulings rather than proposals and the copy can be made under them. They also ruled [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) goes first: it closes a binding hole on the page this deck is about to be added to. |
| 2026-08-13 | (no change) | **Source located and surveyed read-only; the sanitization surface is now measured rather than estimated.** 121 case-company occurrences, **17** genuine training-context ones, **no place names, no personal data, no local-system paths**, and 14 external references that are all licence text and SVG namespaces rather than loads. The first scan reported 165 training-context hits and 148 of them were false — *example*, *assessment*, and a `trainer` who is a role in the redesigned process. Bound on structure instead, which is the difference between a rename and an audit. Naming decided: `Larkfield Dental Group`, published as `measure-first`. **Nothing copied; the source is untouched.** |
| 2026-08-13 | (no change) | **The owner ruled step 1: publish, and the figures stay** — the case and its numbers were invented by the owner and the trainer, so nothing here is the provider's to withhold. The re-basing this task recommended is withdrawn as unnecessary rather than rejected. The sanitization list widened in exchange: place names, *references* to the training context as well as the two words, and a re-check for external and local-system data. The palette stays the shipped one — the owner allowed a new one only if free, and an example that does not carry the plugin's single theme is not free (CLAUDE.md rule 4). Two dependent questions decided here rather than sent back: it ships with its sources, and the `D6` name goes. **Still not started, and nothing has been copied**: no record in this repository names the adopting project's path. |
| 2026-08-13 | → proposed | Raised on the owner's instruction, with the source surveyed read-only and the sanitization surface measured rather than guessed: no personal data of any kind, and two classes of visible copy totalling 107 occurrences. Specified and planned in one pass because the owner was closing the session and asked for the migration *prepared*; nothing has been copied, which is deliberate — step 1 is a question only they can answer. `l` because the sanitizing is editorial work across a 13-slide deck and two specifications, not a substitution. |
