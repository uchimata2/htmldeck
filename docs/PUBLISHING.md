# Publishing — the humanizing rule

The detail behind [`../CLAUDE.md`](../CLAUDE.md) *Publishing constraints*, fourth bullet. That bullet
is the rule; this document is what it means in practice — the covered-set test, the exclusions with
their reasons, the owner's exception verbatim, and the boundary against
[`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §3.3.

**This document is agent-facing and is not covered by its own rule** — see §7.

---

## 1. The rule

**No release is published until the human-facing text has been through the humanizer, and no plugin
file has been.** The owner, 2026-08-09:

> No release can be published without humanizing human-facing information. Plugin files are not human
> facing and must be kept AI optimized.

Two halves, and the second is a requirement rather than a scope note. A humanizer pass over
[`../skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md), this file, `CLAUDE.md`, a tool docstring
or a commit message is a **defect**, not a courtesy.

**It binds every release, not the first.** [T-056](../tasks/T-056-humanize-the-human-facing-documents-before-publishing.md)
is `blocked_by` on [T-008](../tasks/T-008-package-document-and-publish.md), and that edge is spent the
moment T-008 closes — which is exactly why the rule does not live on the edge. The edge gates release
one. This document gates release two and everything after it.

---

## 2. What it covers — a test, not a list

> **What does a stranger read before they have installed anything?**

Anything that answers the question is covered. Anything that does not, is not.

Today the test resolves to two things:

- [`../README.md`](../README.md) — the front door.
- **The repository description and any marketplace listing text** — the one or two sentences shown
  beside the name, before a click. Drafted at [T-056](../tasks/T-056-humanize-the-human-facing-documents-before-publishing.md)
  §3 and used by T-008 at publication.

**The test is the rule; those two are only today's answer.** A list of filenames goes stale the first
time a document is added, and it goes stale *silently* — nothing fails, the new document simply is
not covered. This repository has already paid for that once: `reconcile_targets` in
`.handoff/config.md` is an enumeration, and what it had quietly stopped covering is what
[T-042](../tasks/T-042-audit-the-whole-repository-against-itself.md) found.

**Applying the test to a document that does not exist yet.** Ask where the reader is standing, not
what the file is called. A `CONTRIBUTING.md` is read after cloning by someone who has already decided:
not covered. A landing page, a launch post, a screenshot caption, an installation walkthrough: all
read before the decision, all covered.

---

## 3. What it excludes, and why

| Excluded | Why |
| :--- | :--- |
| **Everything agent-facing** — `SKILL.md` and its `references/`, `CLAUDE.md`, this file, tool docstrings | The owner's words: keep them efficient for AI parsing. The compression that reads as machine-written is the *feature*, and `SKILL.md` is under a byte budget on purpose |
| **Commit messages** | Same reason. They are read by tooling and by whoever bisects, not by a stranger deciding whether to install |
| **Task files** | Fifty-odd records of work already done are an audit trail. Rewriting their prose edits the history rather than the product |
| **The ruleset and the research notes** — `DESIGN-SYSTEM.md`, `DESIGN-RATIONALE.md`, `EVALUATION.md`, `LESSONS.md`, `research/` | Not read before installing, cited by ID from code, and their density is what makes them usable |
| **Deck copy** | DS-106's jurisdiction, and gated. See §4 |
| **Anything the humanizer would have to invent a fact to improve** | §6 |

---

## 4. Where this rule ends and DS-106 begins

Two instruments over one text would disagree, and the gated one would win anyway. So they do not
overlap:

| | This rule | DS-106 / DS-107 |
| :--- | :--- | :--- |
| **Jurisdiction** | Repository text a stranger reads before installing | **Deck copy** — the words on a slide |
| **Instrument** | The `humanizer` skill, run by a person, at release time | `tools/deck/check.py`, run per build; the categories are inlined in [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §3.3 and their owning skill is named in [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §8 |
| **On a violation** | The release does not ship | The build fails |
| **Scope of the artifact** | The repository | One deck |

A deck built by this plugin is **never** run through the `humanizer` skill, and the README is
**never** checked against DS-106. If a text seems to fall under both, it is deck copy: the gated
instrument takes it.

---

## 5. How to run it

**The skill.** `humanizer@humanizer`, **2.9.1**, from the `blader/humanizer` marketplace. Verified
present in this project's session 2026-08-09; nothing had to be enabled.

**Mode.** File mode for `README.md` — it rewrites in place and reports a summary. Pasted-text mode for
the repository description, which is short enough that the draft, the audit answers and the final text
should all be recorded.

**The exception, as given by the owner on 2026-08-09 — verbatim:**

> When humanizing docs: preserve tables, code blocks, heading hierarchy, and **Label:** value
> bullets. Skip patterns 15, 16, 18. Apply the rest.

The three skipped patterns are **15 Overuse of Boldface**, **16 Inline-Header Vertical Lists** and
**18 Emojis** — named as well as numbered so the instruction survives the skill being renumbered, and
**re-verified against the installed copy** rather than trusted. Each is load-bearing here: this
project carries its decisions in bolded labels and its rules in inline-header lists, and stripping
them would flatten the structure that makes a document skimmable rather than remove a tell.

**Pattern 14 applies: cut the em dashes.** The owner answered this directly on 2026-08-09.

**The escape that is not being taken.** The skill's *Voice Calibration* section says a user-supplied
writing sample outranks its style rules, §14 included — so this repository's existing prose could be
handed over as a sample and its em dashes kept. It is recorded here because the next person to read
§14 will find that escape too, and the answer above forecloses it.

---

## 6. What must survive byte-identical

Beyond the exception's tables, code blocks, headings and label bullets:

**Every figure in the README is pasted from a run.** Counts, byte sizes, tool output. A rewrite that
rounds one, rephrases it, or re-derives it from memory is a **defect**, not a style improvement — a
correct number quietly becoming a plausible one (**L-03**).

So after any pass over the README, prove it rather than trusting the diff:

```bash
python tools/deck/ruleset.py --counts
python tools/deck/ruleset.py --gates
python tools/tasks/task.py check
python tools/plugin/check_scaffold.py
```

Every fenced block in the README is the output of one of those, or of `tools/deck/check.py`. Diff each
against its command. **A figure stated in prose is checked the same way** — the deck sizes, the slide
counts, the rule totals.

---

## 7. This document

Agent-facing, by §3, and therefore **not** covered by §2's test. It is a working rule read by whoever
prepares a release, not by a stranger choosing whether to install. Its density, its bolded labels and
its tables are deliberate, and a humanizer pass over it is a defect on exactly the same terms as one
over `SKILL.md`.
