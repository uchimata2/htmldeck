---
id: T-073
title: Decide whether to keep refcheck now that upstream has ruled on bare paths
type: analysis
status: done
phase: review
parent: null
blocked_by: []
related: [T-062, T-063]
work_package: PH2
shipped_in: 0.1.5
owner: the project owner
business_value: high
effort: s
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - tools/docs/refcheck.py
  - tasks/TASK-WORKFLOW.md
---

# T-073 — Decide whether to keep refcheck now that upstream has ruled on bare paths

## 1. Specify

**Outcome**
This project knows whether `tools/docs/refcheck.py` still earns its place, and the decision is made
against what the tool actually reports on this tree rather than against what it was built to do.

**Why this one**
[T-063](T-063-improvements-to-propose-upstream-to-taskmd.md) closed on the exit criterion that its
proposals had been copied upstream and were being processed there. **Upstream answered on 2026-08-10,
and item 1 was decided *out*:** taskmd's `check` will not resolve a path written as prose or inside a
fenced block. Only Markdown link syntax counts as a pointer. That is now documented adopter-facing in
taskmd's README, deliberately, so the next project retiring its own checker is told what it gives up
rather than finding out.

It was decided by measurement, not by argument — including a measurement of **this project's corpus**,
which this project has never seen:

| | taskmd's own tree | **This project** |
| :--- | ---: | ---: |
| Markdown links (dead) | 947 (0) | 1561 (**0**) |
| Distinct bare pointers | 683 | 481 |
| — in the task folder | — | 388 |
| Reported dead | 237 | 31 |
| — in the task folder | 235 | 27 |
| Real defects among them | **0** | **0** |

**19 of those 27 name one file: `tools/tasks/task.py`** — the pre-split tool
[T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) retired. The rest are
`.assets-cache/` and `.kb/` artefacts named as evidence, a bare `examples/README` without its
extension, and an id prefix written with an ellipsis. Of the 4 outside `tasks/`, one is
`.handoff/config.md` naming where the live handoff file *will* be — upstream produces the identical
false positive — one is a research id that is not a path, and two are hook scripts named in config
prose.

**That is the finding this task exists for, and it is not the one T-063 expected.** The argument for
keeping refcheck was coverage upstream would not provide. The coverage is real and the alarms are
not: a task record naming a tool that has since been removed is a **correct dated statement**, and a
path checker cannot tell it from a broken promise. A tracker accumulates those structurally, which is
why the same rule that validates a documentation tree cries wolf over a backlog. Upstream's reasoning
before it measured pointed the other way — this project's own report was the strongest evidence *for*
the feature.

**Do not delete `tools/docs/refcheck.py` on the strength of this alone.** Upstream's T-093 — whether
`check` resolves a **section** reference — is still open, and this file is the offered MIT reference
implementation for it, with the adjacency decision already made. Deleting it would cost upstream that
and cost nothing here to keep.

**Scope**
- In: whether refcheck keeps running, keeps existing without running, or goes.
- In: if it keeps running, what to do about the 31 — because a checker with 31 standing alarms that
  are all correct-but-dead is a checker people learn to skip, which is worse than not having one.
- In: whether the dead pointers are worth fixing *as records*. They are not defects, but 19 of them
  naming one retired file may be worth one sweep, and that is a different question from the checker.
- Out: taskmd's decision, which is made and shipped. This project does not reopen it; if the evidence
  above is wrong for this tree, that is a report upstream, not a change here.
- Out: the section-reference rule, which is upstream's T-093 and is not blocked on anything here.

**Expect the numbers to move when this project updates.** v0.2.0 also shipped upstream's T-094: `check`
now reads only the documents a clone would receive, so gitignored material — `.kb/`, `.assets-cache/`,
the live handoff — drops out of the walk and the document and link counts fall on an unchanged tree.
A new `Scope` line reports how many were skipped. Nothing has broken when that happens; a run of this
project's tracker at v0.2.0 is clean, with 31 documents excluded.

```bash
claude plugin update taskmd@taskmd
```

**Inputs**
- `tools/docs/refcheck.py`, and whatever currently invokes it.
- [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md), for the five proposals as sent and the
  evidence behind each.
- taskmd v0.2.0's README, section *Which documents `check` reads, and which pointers in them* — the
  adopter-facing statement of what is and is not covered.

**Acceptance criteria**
- [ ] The decision is recorded with its rejected alternative
- [ ] If refcheck keeps running: the 31 standing alarms are resolved, suppressed or explained, so a
      clean run means something
- [ ] If it stops running: the file survives at least until upstream's T-093 closes, and the reason is
      written where someone tidying the tools folder will read it
- [ ] Whatever is decided, `docs/` says what validates a pointer in this project and what does not

**Open questions**
- ~~**Keep, park, or delete.**~~ **Settled 2026-08-10: keep it running.** Decided from measurement
  rather than handed back, because the measurement turned out to answer it — see §3. The framing above
  is left standing because it is the input that had to be checked, not because it held.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Run refcheck on this tree and reconcile what it reports against the 31 in §1 | this file §3 |
| 2 | Decide keep, park or delete, with the rejected alternative | this file §3 |
| 3 | Settle whether the dead pointers are worth one sweep as records | this file §3 |
| 4 | Write down what validates a pointer here and what nothing validates | [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 |
| 5 | Record why the file survives even if it ever stops running | [`refcheck.py`](../tools/docs/refcheck.py) docstring |
| 6 | Re-run `python tools/tasks/lint.py` | this file §4 |

## 3. Implement

**Decisions & assumptions**

- **The 31 are not refcheck's alarms, and §1 attributes them to the wrong tool** — found 2026-08-10,
  step 1. `python tools/docs/refcheck.py` on this tree reports **1139 pointers, 0 broken; 509 section
  references, 0 dead**. It has no standing alarms at all. The 31 come from the wider rule upstream
  prototyped and then **rejected**, which resolved a repo-relative path of any extension; refcheck's
  `POINTER` matches `.md` only, on purpose. The single largest group upstream reported — the 19 naming
  the retired `tools/tasks/task.py` — is invisible to refcheck for exactly that reason.
- **So the corpus is not wrong for the rule.** §1 concluded that a tracker structurally accumulates
  correct-but-dead pointers and that this is why the rule cries wolf here. The first half is true and
  is why upstream was right to decline. The second half does not follow for **this** tool: the narrow
  scope that makes refcheck quiet is the scope it was written with, and it is green on the corpus that
  was offered as evidence against it.
- **Keep it running** — 2026-08-10. It is green, it costs one command in a chain that already runs,
  and it covers two things upstream has now settled it will never cover: bare `.md` paths in prose or
  printed into a fence, and `<document> §n` references. **The rejected alternative is park** — keep the
  file, stop invoking it — which is what §1's measurement appeared to argue for and which fails on the
  finding above: parking a checker on the strength of another checker's false positives would remove
  live coverage to answer alarms this project never had. Delete was never live; upstream's **T-093**,
  *Decide whether check resolves a section reference*, is still `proposed`, and this file is the
  offered reference implementation for it.
- **No sweep. The dead pointers stay** — 2026-08-10, scope item 3. All **46** mentions of
  `tools/tasks/task.py` are inside `tasks/`, across 22 task files; `docs/`, `CLAUDE.md`, `README.md`
  and `tools/` carry none. Every one is a dated statement in a record of work done while the tool
  existed, which is §1's own argument, and rewriting them would falsify the record to satisfy a checker
  that is not complaining. A mention in live instructional prose would have been a real defect; there
  is not one.

**One thing found that is out of scope and is not fixed here.** This project runs **taskmd 0.1.1** —
the plugin cache holds `0.1.0` and `0.1.1`, and `lint.py` takes the newest — while upstream's own
repository is at **0.3.0**. So the v0.2.0 behaviour §1 anticipates has not reached this tree, and the
`Scope` line it describes is not in the output above. Updating the plugin changes the environment
rather than the repository and is nobody's task yet; **T-081** raises it.

**Outputs produced**
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6 — amended. It already said refcheck reads `.md` paths; what
  it did not say is the consequence, that a bare path with any other extension is checked by **nothing**
  and that upstream has now decided it never will be. That is the fact which makes 46 pointers to a
  deleted file coexist with three green gates, and without it the next reader re-derives it.
- [`refcheck.py`](../tools/docs/refcheck.py) — docstring amended with the reason the file outlives its
  own usefulness here, where someone tidying `tools/` will read it.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The decision is recorded with its rejected alternative | met | Keep it running; park is the rival, and §3 says what defeats it. |
| If refcheck keeps running: the 31 standing alarms are resolved, suppressed or explained | met | **Explained, and the premise corrected.** There are 0, not 31 — the criterion inherited §1's misattribution. A clean run already means something; what it means is now written down. |
| If it stops running: the file survives until upstream's T-093 closes, and the reason is written where someone tidying the tools folder will read it | met | Not applicable as written — it kept running — but the reason was worth having anyway, so it is in the docstring regardless. T-093 confirmed `proposed` upstream on 2026-08-10. |
| Whatever is decided, `docs/` says what validates a pointer in this project and what does not | met, elsewhere | Written in `tasks/TASK-WORKFLOW.md` §6, not under `docs/`. That is where the two checkers are already described, and a second description under `docs/` disagrees with it the first time either changes (**L-13**). The criterion named a folder; what it wanted was a single true home. |

All three gates green after the change — 80 tasks, 1142 document pointers and 517 section references,
nothing broken. The counts are above the pre-task run because this task added a task file and a lesson,
not because anything was reclassified.

Generalised as **L-60** in [`LESSONS.md`](../docs/LESSONS.md): a measurement of your corpus by someone
else's instrument is not a measurement of your tool. That is the transferable half; the refcheck
decision is not.

**Child fix tasks raised**
- [T-081](T-081-the-installed-taskmd-is-two-minor-versions-behind.md) — the installed plugin is two
  minor versions behind upstream.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | Kept, and the acceptance criteria are met with two corrections rather than silently. **Running the tool before deciding about it was the whole task**: §1 carried an upstream measurement of this corpus and read it as a verdict on refcheck, when refcheck reports nothing on that corpus — the 31 belong to a wider rule that upstream tried and threw away. Criterion 2 inherited the same error and is answered by correcting it, which is `not met` territory handled as METHOD allows rather than by rewording the criterion to fit. Criterion 4 is met at the existing single home instead of the folder it named (**L-13**). |
| 2026-08-10 | → in_progress | Step 1 first, deliberately: the decision hung on a number that had never been produced here. It came back **0 broken over 1139 pointers**, which inverted the reading of §1's table — and the same run explained the gap, since `POINTER` matches `.md` and the largest reported group is a `.py` file. Two things fell out that §1 did not anticipate: nothing in this repository checks a bare path that is not `.md`, and 46 pointers to a tool deleted in T-062 sit in the tracker with every gate green. Both are correct; neither was written down. |
| 2026-08-10 | → proposed | Raised on the upstream answer to T-063 item 1, which came back *out* with a measurement of this tree attached. `high` because the standing assumption here is that refcheck covers something upstream does not, and the measurement says what it covers on this corpus is 31 alarms and no defects — while the one thing it uniquely still buys, the section-reference implementation, is a reason to keep the file rather than to keep running it. `s` because nothing needs building; the evidence is in hand and the work is one decision and its consequences. |
