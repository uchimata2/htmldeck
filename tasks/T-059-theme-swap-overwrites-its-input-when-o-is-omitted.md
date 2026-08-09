---
id: T-059
title: Theme swap overwrites its input when -o is omitted
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-007]
work_package: v0.2
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-059 — Theme swap overwrites its input when `-o` is omitted

## 1. Specify

**Outcome**
`python tools/deck/theme.py swap <deck> <theme.css>` cannot destroy the deck it was given. The
output path is either required, or defaults somewhere disposable — and the tool refuses to write to
its own input either way.

**Why this one**
[`tools/deck/theme.py`](../tools/deck/theme.py) line 603 reads:

```python
out = argv[argv.index("-o") + 1] if "-o" in argv else deck
```

So the *default* destination is the source file. **This is a destructive default on the one artefact
in the repository that is built by hand**, and it fired on 2026-08-09 during
[T-016](T-016-the-interaction-and-motion-layer.md): the reference deck was replaced by the lattice
build mid-task, and recovering it cost a `git checkout` plus re-applying an edit that had not been
committed yet. It was noticed because the file's byte count changed. **Nothing would have caught it
had the themed build been the same size** — the gate reads whatever deck it is pointed at, and a
themed reference deck passes every check, which is exactly the property that makes this quiet.

**The default also contradicts the project's own convention.**
[`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §1 says *the demonstration deck is built, not
committed* — a themed copy belongs in `.assets-cache/`, beside the seeded variants. So in-place is
not merely risky, it is the one destination the contract rules out, and every correct invocation
already carries `-o`. A default nobody should use is a trap rather than a convenience.

**Scope**
- In: `swap`'s output resolution, and a refusal to write to the input path however it was reached —
  including `-o` naming the same file, and the same file reached by a different relative path.
- In: the usage line in the module docstring, so it matches whatever is decided.
- Out: every other command in the file. `check` and `validate` do not write.
- Out: a general audit of destructive defaults across `tools/`. If one is wanted it is its own task;
  this one is about the command that has already cost something.

**Inputs**
- [`tools/deck/theme.py`](../tools/deck/theme.py) — `main`'s `swap` branch, and the usage line in
  the module docstring.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §1 — *built, not committed*, which is the
  convention the default breaks.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-04**: a tool refuses to report if its self-test
  fails, and this is the same discipline applied to what the tool writes rather than what it reads.

**Acceptance criteria**
- [ ] `swap` with no `-o` does not write to the input deck — either it exits with usage, or it
      writes to a derived path under `.assets-cache/`
- [ ] `swap` refuses to write to its input path even when `-o` names it, compared by resolved
      absolute path rather than by the string given
- [ ] The module docstring's usage line matches the behaviour, and says what the default is
- [ ] A self-test assertion covers it, so the guarantee is checked on every run rather than reviewed
      once

**Open questions**
- **Require `-o`, or default to `.assets-cache/deck/<deck>-<theme>.html`?** Requiring it is the
  smaller change and makes every invocation say where it is going; defaulting is friendlier and
  matches where the contract says the output belongs. Whoever works this one — the criteria above
  admit either, and the deciding question is whether a themed build is a thing you ask for by name
  or a thing you generate constantly.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- none yet

**Outputs produced**
- none yet

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → proposed | Created after `swap` overwrote the reference deck during [T-016](T-016-the-interaction-and-motion-layer.md). **v0.2**: nothing shipped depends on it, and the workaround is one flag that every correct invocation already passes — but it is a destructive default on a hand-built artefact, and the reason it was caught at all was a byte count that happened to change. |
