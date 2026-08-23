# Audit method — htmldeck

**The method is not here.** It is the taskmd skill's — `METHOD.md` §5 for the type and the one rule
that matters, `audit.md` for the procedure, and `pre-release-audit.md` for an audit whose subject is
everything about to be released. This file is the local binding: the handful of things that are
htmldeck's own and cannot be written in a document every adopter receives.

*The generic half was written here on 2026-08-22 and handed upstream the same day
([T-218](../tasks/T-218-record-the-pre-release-audit-method-and-its-machinery.md)), because most of it
either already existed in taskmd's `audit.md` or contradicted a rule in it. **It has arrived:
`pre-release-audit.md` ships in taskmd `0.6.0`, tagged 2026-08-23, at 11,371 bytes** — their T-223,
merged as [PR #2](https://github.com/uchimata2/taskmd/pull/2). This file stopped describing what the
upstream document would carry; read it instead. A session whose installed taskmd is older than `0.6.0`
will not find it.*

---

## 1. Which audits this project runs

| Audit | Subject | Trigger | Register |
| :--- | :--- | :--- | :--- |
| **Pre-release** | the whole repository — project and product | **the owner's request, never automatic** | [`PRE-RELEASE-AUDIT.md`](PRE-RELEASE-AUDIT.md), ids `PR-nn` |
| **Context economy** | what a session loads without asking for it | request, or a change to tier 1 | [`CONTEXT-AUDIT.md`](CONTEXT-AUDIT.md), ids `CE-nn` |
| **Ruleset** | rules that cost more to satisfy than they return | request | [`RULESET-AUDIT.md`](RULESET-AUDIT.md) |

Ran as [T-042](../tasks/T-042-audit-the-whole-repository-against-itself.md),
[T-119](../tasks/T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md),
[T-130](../tasks/T-130-audit-the-context-economy-of-an-agent-driven-repository.md) and its grading pass
[T-153](../tasks/T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md).

**No audit is a release step**, and [`PUBLISHING.md`](PUBLISHING.md) §8 says so where the sequence
lives.

---

## 2. What is local, and belongs in an audit's own plan

taskmd's `audit.md` puts a given audit's procedure in its `plan`, not in a shared document — a
standing checklist examines each new subject for the last subject's problems. So the four items below
are the plan's to decide, and this list is what has been decided *here*, not a rule for anywhere else.

- **Aspects.** Project method, project documentation, product documentation, and the product.
- **The instrument-only grade applies to the decks.** `CLAUDE.md` rule 6 forbids reading a deck whole;
  five tracked `.html` files are 1,773,568 bytes, measured 2026-08-22. They are rendered, looked at
  offline, and measured with the tools in `tools/deck/`. Their specifications are read.
- **Two surfaces outside git are in scope**: the working directories `.gitignore` names, and this
  project's memory and handoff record.
- **The coverage partition is `tools/check_all.py`'s, one altitude up** — read, skipped with a stated
  reason, or produced a finding, and an item in none of the three is a gap in the audit. **The
  membership behind it is `python tools/docs/cycles.py`**, which assigns every tracked path to
  exactly one cycle of the pre-release run and fails when a path belongs to none, or when a rule
  names a path that is gone. It is deliberately **not** wired into `tools/check_all.py`: a file with
  no audit cycle is a defect in the audit's coverage, not in the release, and §1 says no audit is a
  release step. It runs at each cycle's step 2 instead —
  [T-223](../tasks/T-223-derive-the-audit-cycles-membership-instead-of-counting-it.md), and **L-136**
  is why a count was not enough.

---

## 3. The one tool gap

**`tools/docs/findings.py` reads a single register.** `docs/CONTEXT-AUDIT.md` and the `CE-nn` pattern
are hardcoded, and `tools/tasks/lint.py` runs it — so a task carrying `finding: PR-nn` fails the lint
today. Generalising it was to be the first step of any second audit; **cycle 0 decided against it**,
below — so a child task is tied to its finding by `parent:` alone, and a register's task column
is hand-kept and known to drift.

*Raised upstream as well: validating a `finding:` field against a register is schema work, not method.
**It is not in taskmd `0.6.0`** — no `finding` field in its schema — and their
[T-247](https://github.com/uchimata2/taskmd/blob/master/tasks/T-247-decide-whether-taskmd-validates-a-finding-field-against-a-register.md)
was still `proposed` on 2026-08-23, so the remedy stays local. **Cycle 0 settled it that day:
`parent:` is the fallback and no task may carry `finding: PR-nn`**, because the tool binds to
`CONTEXT-AUDIT.md`'s table *shape* rather than to its path, and a second reader would be written
against a table that has never held a row.
[T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md) section 3 carries the argument,
the command that proves the lint fails on one, and the trigger to revisit at cycle 40.*
