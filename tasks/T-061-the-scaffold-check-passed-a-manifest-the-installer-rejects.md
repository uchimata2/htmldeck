---
id: T-061
title: The scaffold check passed a manifest the installer rejects
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-008, T-015]
work_package: PH1
shipped_in: 0.1.1
owner: the project owner
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - .claude-plugin/plugin.json
  - tools/plugin/check_scaffold.py
---

# T-061 — The scaffold check passed a manifest the installer rejects

## 1. Specify

**Outcome**
`v0.1.0` does not install. `.claude-plugin/plugin.json` declares `"author"` as a string where the
schema requires an object, and Claude Code refuses the plugin. Both halves get fixed: the manifest,
and **the check that called it valid**.

**What happened**
Reported from another project, 2026-08-09, and reproduced here:

```
claude plugin marketplace add uchimata2/htmldeck
✔ Successfully added marketplace: htmldeck

claude plugin install htmldeck@htmldeck
✘ Failed to install plugin "htmldeck@htmldeck": ... invalid manifest file at
  ...\.claude-plugin\plugin.json.
  Validation errors: author: Invalid input: expected object, received string
```

The marketplace entry is fine; `marketplace add` succeeded. Only the plugin manifest is rejected.

**The instance is one line. The defect is the gate.**
`tools/plugin/check_scaffold.py` printed **`OK - manifest valid`** for this manifest, in the same run
that the README quotes as evidence the package is sound. It checks that `author` is **present** and
never what it **is**:

```python
for field in ("version", "description", "author", "license"):
    if field not in data:
        notes.append("no `%s` in the manifest - optional, wanted for distribution" % field)
```

Presence is the whole test, so every one of those four fields could hold a wrong-typed value and the
gate would still print `OK`. That is a check whose subject is absent by construction, which this
repository has a rule and a lesson about already (**L-44**, **L-51**), and it shipped a release.

**The published claim was false, not merely optimistic.** `README.md` *Install it* ends in
`check_scaffold.py` as the command that proves the package, and the release notes say the install
route is checked. It was checked by an instrument that could not see the defect.

**Why the working example did not save us.** `humanizer@humanizer` declares `author` as an object and
installs. Nothing compared the two, because the gate was believed. A second plugin on this machine
installs by **omitting `author` entirely**, which is also valid and which makes "it works for them"
useless as evidence either way.

**Scope**
- In: `author` as an object, per the schema at `json.schemastore.org/claude-code-plugin-manifest.json`
  (`required: ["name"]`, with optional `email` and `url`).
- In: **type validation for every field the schema types**, not just `author`, since the same blind
  spot covers `version`, `description`, `license`, `keywords` and the rest.
- In: fixtures that **fail before the fix**, per **L-04**. A check added without one is the same
  mistake one level up.
- In: a patch release, because the artefact users can reach does not install.
- Out: full JSON-Schema validation with a third-party validator. `CLAUDE.md` says pure standard
  library, and the schema is small enough to encode the field types directly.
- Out: `marketplace.json`, which `marketplace add` accepted. Its schema URL 301s and is not a
  dependency.

**Inputs**
- The other project's transcript, quoted above.
- `https://json.schemastore.org/claude-code-plugin-manifest.json`, fetched 2026-08-09: only `name` is
  required; `author` is an object requiring `name`.
- A manifest that installs, for comparison: the `humanizer` plugin's.
- [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-04** on fixtures, **L-05** on what a check that
  cannot fail is worth, **L-44** on a check whose subject is absent.

**Acceptance criteria**
- [ ] `plugin.json` validates against the schema, `author` included
- [ ] `check_scaffold.py` **rejects** a string `author`, demonstrated by a fixture that fails without
      the fix
- [ ] Every field the schema gives a type is type-checked, not just the one that broke
- [ ] The install is verified **from the published repository**, not from the working tree
- [ ] The README's pasted fixture count is re-derived, since adding fixtures moves it (**L-52**)
- [ ] A patch release ships, and the `v0.1.0` release notes say it does not install

**Open questions**
- none. The schema is unambiguous and the failure is reproducible.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add fixtures for a string `author`, and for a wrong-typed `keywords`, and watch them fail | The failing run, in §3 |
| 2 | Encode the schema's field types in `check_scaffold.py` and re-run until the fixtures pass | The edited tool |
| 3 | Fix `plugin.json` | The edited manifest |
| 4 | Re-derive the README's fixture count | The edited `README.md` |
| 5 | Commit, push, tag `v0.1.1`, release | The tag and release |
| 6 | Amend the `v0.1.0` release notes to say it does not install | The edited release |
| 7 | Verify the install end to end from the published repository | The transcript, in §4 |

## 3. Implement

**Decisions & assumptions**

- **The schema was fetched, not inferred from the working example — 2026-08-09.**
  `json.schemastore.org/claude-code-plugin-manifest.json` gives `author` as an object with a required
  `name`, and types twelve other fields. Copying `humanizer`'s shape would have fixed the one line and
  left the other twelve untyped, which is the defect rather than the symptom.

- **The field types are encoded in the tool, not validated by a library — 2026-08-09.** `CLAUDE.md`
  says pure standard library, and the schema is one dict wide. *Rejected: `jsonschema`*, which buys
  full draft support at the cost of the one rule this repository will not trade.

- **Fixtures first, and they failed — 2026-08-09.** Three of the four new fixtures reported
  `expected BAD TYPE, got: nothing` before the fix existed. That run is the evidence the check was
  blind rather than merely quiet, and **L-04** is why it was done in that order.

- **The fourth fixture asserts a well-formed `author` is *not* flagged.** A type check that rejects
  everything passes its negative fixtures and breaks every real manifest, which is the failure the
  positive cases exist to catch.

- **Version bumped to `0.1.1` — 2026-08-09.** The published `0.1.0` does not install, so this is a
  patch rather than a correction to an unreleased state.

- **The tool's docstring was already wrong, and was fixed with it.** It claimed *"six checks"* and
  *"six fixtures, three that must pass and three that must fail"* against ten actual fixtures. A
  self-test whose own count is stale is the same class of defect one altitude up (**L-52**).

**Outputs produced**
- `.claude-plugin/plugin.json`
- `tools/plugin/check_scaffold.py`
- `README.md` (the pasted fixture count)
- `docs/LESSONS.md` (**L-53**)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `plugin.json` validates against the schema, `author` included | **met** | Checked against the fetched schema's own types, not against the tool that had already been wrong once: `type mismatches vs the real schema: none`, `author.name present: True` |
| `check_scaffold.py` rejects a string `author`, shown by a fixture failing without the fix | **met** | `FAIL an author that is a string, which is what v0.1.0 shipped   expected BAD TYPE, got: nothing`, then `14 of 14` after |
| Every schema-typed field is type-checked | **met** | Thirteen fields in `MANIFEST_TYPES`, plus `author.name`. The run against the shipped manifest printed `BAD TYPE  \`author\` is a string, the schema says object` before it was fixed |
| The install is verified from the published repository | **see below** | Left to the owner: it needs a Claude Code client, which this session cannot drive. Everything checkable without one is checked |
| The README's pasted fixture count re-derived | **met** | 10 to 14, from the run rather than by counting the table |
| A patch release ships and `v0.1.0` says it does not install | **met** | `v0.1.1`, and the `v0.1.0` release notes carry a notice at the top |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Fixed in both halves, and the gate is the half that mattered.** `author` is now an object per the schema, and `check_scaffold.py` types thirteen fields plus `author.name` instead of asking whether four keys exist. The order was fixtures first: three reported `expected BAD TYPE, got: nothing` before the fix, which is what the blind spot looked like from inside the tool. Shipped as `v0.1.1`; the `v0.1.0` release notes now say it does not install. **L-53** records the general form, that optional is not untyped and a presence test reads like a validator. One criterion is left to the owner because it needs a Claude Code client this session cannot drive: the end-to-end install. |
| 2026-08-09 | → proposed | Raised from an install failure reported by another project on the day `v0.1.0` published. **`PH1` rather than `PH2`:** the shipped artefact does not install, so this is not a improvement held for later, it is the release not working. The one-line manifest fix is the smaller half. The larger half is that `check_scaffold.py` printed `OK - manifest valid` for it, because it tested that four fields were *present* and never what they contained, and the README cites that command as the proof the package is sound. |
