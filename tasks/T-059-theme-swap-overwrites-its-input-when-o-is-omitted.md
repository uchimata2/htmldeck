---
id: T-059
title: Theme swap overwrites its input when -o is omitted
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-007]
work_package: PH2
shipped_in: 0.1.4
owner: the project owner
business_value: high
effort: s
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - tools/deck/theme.py
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
- Out: the four copy sites that print the bare command — the `<style id="theme">` comment in
  [`examples/reference-deck.html`](../examples/reference-deck.html),
  [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html),
  [`examples/sort-window/sort-window.html`](../examples/sort-window/sort-window.html) and
  [`themes/quarto.css`](../themes/quarto.css). Under the decision below they become correct without
  being touched, which is most of why that decision went the way it did.

**Inputs**
- [`tools/deck/theme.py`](../tools/deck/theme.py) — `main`'s `swap` branch, and the usage line in
  the module docstring.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §1 — *built, not committed*, which is the
  convention the default breaks.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-04**: a tool refuses to report if its self-test
  fails, and this is the same discipline applied to what the tool writes rather than what it reads.

**Acceptance criteria**
- [ ] `swap` with no `-o` writes to `.assets-cache/deck/themed/<deck-stem>-<theme-stem>.html` and
      never to the input deck
- [ ] That default works on a fresh clone: the directory is created if it is not there, rather than
      the command failing on a path nobody was asked to make
- [ ] `swap` refuses to write to its input path even when `-o` names it, compared by resolved
      absolute path rather than by the string given — so a second relative spelling of the same file
      is refused too
- [ ] The module docstring's usage line says what the default destination is, and
      [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §1's command block is still true of the tool
- [ ] A self-test assertion covers both guarantees — the default destination and the refusal — so
      they are checked on every run rather than reviewed once

**Open questions**
- **Settled 2026-08-10, on the convention the repository already has: default to
  `.assets-cache/deck/themed/<deck-stem>-<theme-stem>.html` rather than requiring `-o`.** Three
  things decide it, and the third is what the question was missing.
  [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §1 already names that destination — *"a themed
  copy of it is an output of `theme.py swap` and belongs in `.assets-cache/`"* — so requiring `-o`
  would make every caller retype a path the contract has already chosen. Every other writing tool
  in `tools/` resolves its own output the same way and holds it in a module constant
  ([`render.py`](../tools/deck/render.py), [`print_variants.py`](../tools/deck/print_variants.py),
  [`content_variants.py`](../tools/deck/content_variants.py),
  [`contract_variants.py`](../tools/deck/contract_variants.py),
  [`deliverable_variants.py`](../tools/deck/deliverable_variants.py)); `swap` is the only writer
  without one, which is the anomaly rather than the design. And **four shipped copy sites print the
  bare two-argument command** (Scope, above): requiring `-o` turns all four into documentation of a
  command that errors, while defaulting makes all four correct with nothing edited. `-o` stays
  supported, so nothing that passes it today changes.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Lift the destination decision out of `main`'s `swap` branch into a function of its own — module constant for the default root, `-o` honoured when given, input refused by resolved path — so the guarantee can be asserted rather than only exercised. | `OUT` and `destination()` in `tools/deck/theme.py` |
| 2 | Point the `swap` branch at it, create the output directory, and leave the existing success line alone so the printed form does not change. | The rewritten `swap` branch in `main` |
| 3 | Assert it in `self_test()`: the default lands under `.assets-cache/deck/themed/` and is not the deck; the refusal fires both for `-o <the deck itself>` and for a second spelling of that same file; and an ordinary `-o` elsewhere is **not** refused. | Four assertions in `self_test()` |
| 4 | Rewrite the usage line in the module docstring so it names the default destination, and re-read `THEME-CONTRACT.md` §1's command block to confirm it is still true rather than assuming it. | The usage block in `tools/deck/theme.py`, and a checked statement about the contract |
| 5 | Run it against the reference deck for real, both ways — no `-o`, and `-o` naming the deck — and confirm the deck is byte-identical afterwards. | Two command outputs and a before/after byte count, recorded in Implement |

**Shape of the deliverable, decided**

`destination()` **raises `ValueError`; it does not call `sys.exit`.** `main` catches it and exits with
the message. That split exists for one reason: the self-test has to be able to *observe* the refusal,
and a function that ends the process cannot be asserted against — it can only be trusted.

*Rejected: an `if` guard inside the `swap` branch.* It is two lines shorter and behaves identically
at the command line. It is also exactly the shape step 3 cannot reach, which makes it the version
where the refusal silently stops working and every signal available still says the tool is fine.
**L-04**'s discipline is the same argument applied to what a tool reads; this is it applied to what a
tool writes.

**Output paths**
- `tools/deck/theme.py`

## 3. Implement

**Decisions & assumptions**
- **`destination()` raises; `main` exits.** As planned, and for the reason planned: the four
  assertions in `self_test()` exist only because the refusal is observable. Had the guard stayed an
  `if` inside the `swap` branch, every one of them would have had to shell out or be left unwritten.
- **The directory is created for `-o` too, not only for the default.** The criterion asked only that
  the default work on a fresh clone, but `os.makedirs` sits after the refusal and before the write,
  so it covers both — and `-o` into a path two levels deep that does not exist now works rather than
  failing on the parent. Cheaper than a branch, and there is no case where the caller wanted the
  write to fail because a folder was missing.
- **`THEME-CONTRACT.md` §1 was re-read rather than assumed, and is left unedited.** Its command
  block shows the `-o` form, which is still true of the tool and still the better habit to
  document. The contract's other claim — that a themed copy belongs in `.assets-cache/` — is now
  what the tool does by default rather than what a caller has to remember.
- **One assertion was dead code, and only seeding the defect found it.** The first version of the
  default-destination check compared `destination()`'s *return value* against the deck. It can never
  run: with the old `out = deck` default restored, `destination()` **raises** rather than returning,
  so the comparison is unreachable and the seeded defect surfaced as a bare traceback instead of a
  diagnosis. It is now a `try/except` that catches the `ValueError` and prints the message. Exit
  status was 1 either way — which is exactly why reading the assertion would not have found this and
  running it did (**L-36**).
- **Assumption, recorded as one:** the default writes under the *plugin's* `ROOT`, so a deck on
  another drive still themes into the plugin's `.assets-cache/`. That is what every other writing
  tool here does, and `display_path` already handles printing it (T-064). If a project ever wants
  the output beside its own deck, that is a change of destination policy for all of `tools/`, not
  for this command.

**Outputs produced**
- [`tools/deck/theme.py`](../tools/deck/theme.py) — `OUT` constant, `destination()`, the rewritten
  `swap` branch, four self-test assertions, and the two usage lines.

**Checked by being used.** All four destination cases run against the real reference deck:

```
A. no -o        reference-deck.html + lattice.css -> .assets-cache/deck/themed/reference-deck-lattice.html (224554 bytes)
B. -o <deck>    refusing to swap: that would overwrite the deck it was given (examples/reference-deck.html)   exit=1
C. -o <deck> by another spelling                                                                             exit=1
D. -o elsewhere reference-deck.html + lattice.css -> .assets-cache/deck/themed/explicit.html (224554 bytes)
```

The deck was **225922 bytes before and 225922 after all four**, and `git status` reports it
unmodified — which is the whole point, and the measurement the original defect was caught by.

With `.assets-cache/deck/themed/` deleted, the default swap recreated it; `-o` into
`.assets-cache/deck/themed/a/b/probe.html` created both missing levels. The two routes agree byte
for byte (`cmp` on the default output against the `-o` output: identical), so the guarantee did not
cost a difference in what gets written.

The swapped deck is still a deck: `check.py` on it returns 113 owned / 0 SILENT / exit 0, and
`theme.py check` on it passes DS-168 and DS-010 with 38 literals scanned, 38 exempt, 0 offending.

**Both defects were put back, on a throwaway copy of the module, to prove the self-test fails.** A
guard only ever seen passing is one nobody can tell from a guard that returns nothing (**L-36**):

```
seed: the old `out = deck` default    exit=1  SELF-TEST FAILED: the default destination is the input deck...
seed: the refusal removed             exit=1  SELF-TEST FAILED: -o naming the input deck was accepted as ...
unseeded                              exit=0
```

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| No `-o` writes to `.assets-cache/deck/themed/<deck>-<theme>.html`, never the input deck | **met** | Case A produced `reference-deck-lattice.html`; the deck measured 225922 bytes before and after all four cases, and `git status` reports it unmodified |
| The default works on a fresh clone — the directory is created rather than the command failing | **met** | `.assets-cache/deck/themed/` deleted, default swap recreated it. `-o` into `a/b/probe.html` created both missing levels, so the guarantee is wider than the criterion asked |
| Refuses to write to its input even when `-o` names it, by resolved path, so a second spelling is refused too | **met** | Cases B and C both exit 1 with the same message; C reached the file through `examples/../examples/` |
| The docstring says what the default is, and `THEME-CONTRACT.md` §1's command block is still true | **met** | Docstring and the `usage:` line both name the destination. The contract was **re-read, not assumed** — its `-o` form is still valid and still the better habit, so it is left unedited |
| A self-test assertion covers both guarantees, checked on every run rather than reviewed once | **met**, after a fix | Four assertions. Judged by putting **both** defects back: each exits 1 with its own diagnosis. The first attempt did not — one assertion was unreachable and failed as a traceback; found here, fixed in `implement`, re-verified |

**On that last row.** Review does not repair — the taskmd method's *review* procedure is explicit
that a phase which repairs what it finds destroys the record of what was wrong. So the dead
assertion was not patched in this phase. It is recorded as what
it is: evidence that `implement` had not exited properly, because its criterion was *checked on every
run* and an unreachable line checks nothing. The fix went back into `implement` with its own entry,
and both seeds were re-run afterwards. No child task, because nothing is left carried.

The generic half is not this task's to keep: it is recorded as **L-55** in
[`docs/LESSONS.md`](../docs/LESSONS.md) — *seeding a defect proves the exit status; only the message
proves the assertion*.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → proposed | Created after `swap` overwrote the reference deck during [T-016](T-016-the-interaction-and-motion-layer.md). **PH2**: nothing shipped depends on it, and the workaround is one flag that every correct invocation already passes — but it is a destructive default on a hand-built artefact, and the reason it was caught at all was a byte count that happened to change. |
| 2026-08-10 | → done | Plan, implement and review in one pass. `swap` now defaults to `.assets-cache/deck/themed/` and refuses its own input by resolved path; four self-test assertions hold it there. All five criteria met — the last one only after seeding both defects exposed an **unreachable assertion**, which was fixed back in `implement` rather than in review. No child task. |
| 2026-08-10 | → specified | Specify closed. The output question is settled in favour of a default under `.assets-cache/deck/themed/`; the deciding evidence is new — **four shipped copy sites print the bare two-argument command**, so requiring `-o` would have made all four document a command that errors. Criteria sharpened to that answer and split so the fresh-clone case and the refusal are judged separately. Estimated `high`/`s`. |
