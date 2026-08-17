---
id: T-160
title: Correct the three errors the recipients found in the delivered registers
type: admin
status: done
phase: review
parent: null
blocked_by: []
related: [T-157, T-141, T-130]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-15
updated: 2026-08-15
shipped_in: 0.3.0
deliverables: []
---

# T-160 — Correct the three errors the recipients found in the delivered registers

## 1. Specify

**Outcome**
The two registers [T-157](T-157-hand-the-upstream-registers-to-their-owners.md) delivered are correct
where they are wrong, at the source and on the threads. Both recipients invited corrections on the
terms this register offered — *a row that turns out to be wrong gets corrected here rather than
quietly dropped* — and **three errors are now known**, one found by each recipient and one found here
while reading their replies.

**Why this exists**
A register that promises corrections and does not make them is worse than one that promised nothing.
Two of the three errors are **live misinformation in someone else's backlog**: taskmd is carrying an
item on our word that the version sort is broken here, and it is not. That is the failure mode the
whole *no priority* discipline exists to avoid — an observation that costs the receiving project work
it did not need to do.

**The three errors**

| | What is wrong | Found by | Where the fix goes |
| :--- | :--- | :--- | :--- |
| **1** | **`O-T2` reports the version text-sort as live. It is fixed.** `tools/tasks/lint.py`'s `version_key` sorts on the parsed version and a self-test in the same file asserts `0.10.0` beats `0.5.0`. The row described a real defect and never said it had been repaired, so the recipient read it as outstanding and told us to fix it | here, reading their reply | the register and the thread |
| **2** | **`O-T6` cites the wrong id of theirs.** It points at *their* `T-063` for *an open task at `specified` or later declaring no deliverable*; their `T-063` is the character-count task. The preamble warned that their id could be read as ours and did not guard the harder direction — **a wrong id of theirs resolves to a real task, so it reads as evidence the work is already covered** | taskmd | the register and the thread |
| **3** | **The delivered issue body lost the *before* quote in the O-H4 patch section.** The transformation that replaced the sender-facing banner replaced **every** blockquote in the document, so the quote of the old §4 bullet became a second copy of the report's own banner. The committed document is intact; only what was delivered is wrong | the handoff skill | the thread, and the transformation |

**Scope**
- In: correcting the two register documents under [`../docs/upstream/`](../docs/upstream)
- In: a correction on each thread, since the delivered copy is what the recipient is working from
- In: **auditing the register's remaining cross-references to foreign ids**, which taskmd explicitly
  recommended after finding error 2. `O-T1`, `O-T3`, `O-T5` and `O-T6` all cite ids of theirs
- Out: **acting on their advice to delete the two wrappers.** It does not apply and that is error-adjacent
  rather than an error: the shipped fallback locates the launcher in *the skill directory the harness
  named when it served the skill*, which is available to an agent in a session and not to
  `python tools/tasks/lint.py` run by the gate from any working directory. Worth telling them, because
  an adopter running a tool outside a served skill is a case their fallback does not cover
- Out: re-triaging their verdicts. Five of six and six of seven rows landed; that is their call and it
  is made
- Out: adding new observations. `../docs/CONTEXT-AUDIT.md` §7's standing rule is unchanged, and a row
  added after a handover date is unsent by construction

**Inputs**
- The two threads: `uchimata2/handoff-skill#75` and `uchimata2/taskmd#1`
- [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md) and
  [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) — the sources to correct
- [`../tools/tasks/lint.py`](../tools/tasks/lint.py) — `version_key` and its self-test, the evidence for error 1

**Acceptance criteria**
- [ ] `O-T2` states that the text sort was found and fixed here, with what fixes it, so the recipient
      can close whatever they raised on it
- [ ] `O-T6` cites the right id, or no id, and says which
- [ ] Every remaining foreign id in both registers has been checked against the project it names, and
      the count checked is written down — **a spot check is not an audit**
- [ ] Each thread carries the corrections, so the delivered copy and the source agree
- [ ] The O-H4 section reads correctly wherever the recipient looks at it
- [ ] The transformation that caused error 3 cannot silently do it again

**Open questions**
- **Does the delivered issue body get edited, or corrected in a comment?** Editing makes the artifact
  right for a later reader and quietly rewrites what the recipient replied to; a comment leaves the
  damage visible and the thread honest. **Recommend the comment**, with the missing quote in it — the
  thread is already the record of the exchange, and the recipient reconstructed the rule from
  behaviour rather than being blocked. *The owner answers this, because it edits public content.*

## 2. Plan

**The cross-reference audit runs first, because it decides how many corrections there are.** It was
the one acceptance criterion whose answer was unknown when this task was written — the other four
correct errors already named.

**The owner ruled the open question on 2026-08-15: post a comment, do not edit the issue body.** The
thread is the record of the exchange, and rewriting what someone replied to is the worse of two
imperfect options.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Extract every foreign id from both registers with the claim it sits in, and check each against the project it names — the taskmd ids against that repository's task files, the handoff ids against the live issues | A verdict per citation, and a count, so the criterion is met by an audit rather than a spot check |
| 2 | Correct `O-T2` at the source: the text sort was real, was found, and is fixed by `version_key` and a self-test. The row never said so, which is why it was read as outstanding | A row that cannot cost the recipient work again |
| 3 | Correct `O-T6` at the source: drop the wrong id, and say what the audit found in its place | A row citing nothing rather than citing something false |
| 4 | Post one correction comment per thread — the corrections above, the missing O-H4 quote in full, and why the wrapper advice does not reach the gate | The delivered copy and the source agree |
| 5 | Give the standing send rule a home in `../docs/CONTEXT-AUDIT.md` §7, so the next send diffs the whole artifact rather than the part it feared for | Error 3's class cannot recur silently |
| 6 | Gates, commit, push | `lint`, `check_all`, one commit |

## 3. Implement

**The audit, which is the part that was not already known**

Seven foreign-id citations across the two registers. Each was checked against the project it names —
the taskmd ids against that repository's task files, the handoff ids against the live issues.

| Id | Claim in the register | Verdict |
| :--- | :--- | :---: |
| their `T-028` | established the tiering rule and the budget-as-a-relation | correct |
| their `T-063` | *an open task at `specified` or later declaring no deliverable* | **wrong** — it is *Measure the tier-1 member the rule declares*, and closed |
| their `T-085` | *install the published plugin on a machine that has never seen it* | correct, both uses |
| their `T-087` | let `list` filter on a field the index shows | correct |
| `#53` | nearest open item to `O-H1`, and does not cover it | correct |
| `#57` | nearest open item to `O-H1`, and does not cover it | correct **when sent**, see below |
| `#8` | adjacent to `O-H2` — about pickup, not accumulation | correct, and the recipient confirmed it |

**One wrong out of seven, and it is the one the recipient found.** The audit's value was in the six it
cleared: *a spot check is not an audit* was an acceptance criterion because the alternative is
asserting the rest are fine, which is what produced the error in the first place.

**Decisions & assumptions**
- **`#57` is not a fourth error and no correction was made to the row** — 2026-08-15. It closed at
  `2026-08-14T22:07Z`, during the recipient's triage and after this register was sent, so `O-H1`'s
  *nearest open items* was true when written and when delivered. **A register that names someone
  else's open issues goes stale the moment they act on it, and that is not a defect in the register.**
  Flagged on the thread anyway, because a later reader has no way to tell a stale claim from a wrong
  one, and it is `O-H7`'s *message with latency* seen from the sending end.
- **The two wrong-in-the-register corrections were struck rather than rewritten** — 2026-08-15,
  following §1's own rule and `O-T2`'s precedent. A row corrected invisibly teaches the next reader
  nothing; `O-T6`'s strike-through is now the clearest statement in either document of why a wrong
  foreign id is worse than a dangling one.
- **The wrapper advice was answered rather than adopted, and recorded as a new observation** —
  2026-08-15. Their fallback resolves the launcher from *the directory the harness names when it
  serves the skill*; the release gate is a plain `python tools/tasks/lint.py` from any working
  directory, in a process never served the skill and with no channel to ask. Unranked, per the
  standing rule, and explicitly allowing that a gate script may simply be outside what they support.
- **The exit-code exposure was checked and reported as a negative result** — 2026-08-15. They asked.
  `tools/tasks/query.py` consumes `-h`/`--help` only as the first argument and never passes it
  through, so the unknown-command path still exits 2. A negative result they asked for is worth the
  three lines it takes.
- **The comment was the route, not an edit to the issue body** — the owner's ruling, 2026-08-15.

**Outputs produced**
- Two correction comments: [`handoff-skill#75`](https://github.com/uchimata2/handoff-skill/issues/75)
  and [`taskmd#1`](https://github.com/uchimata2/taskmd/issues/1)
- [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md) — `O-T2` and `O-T6` corrected at the source
- [`../docs/upstream/handoff-skill.md`](../docs/upstream/handoff-skill.md) — the handover record carries
  the correction and the `#57` finding
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §7 — the standing send rule
- The two handover prompts below

**The handover prompts, second pair.** Same reason as
[T-157](T-157-hand-the-upstream-registers-to-their-owners.md)'s: a comment notifies a watcher and
nobody else, and the handoff skill's thread is **closed**, which makes a correction on it easier to
miss than the report was. Each prompt starts a session in the receiving repository with no access to
this context. **What they carry that the first pair did not is an instruction to change the
recipient's own record** — taskmd's disposition lists work that is not theirs — because a correction
that only reaches a thread leaves the wrong fact where the project actually keeps it.

For the handoff skill:

```text
A correction landed on https://github.com/uchimata2/handoff-skill/issues/75 — the adopter report
from htmldeck that we triaged and closed. The issue is closed; the comment is on the thread.

It supplies the thing we asked for: the missing before-text in the report's "O-H4 patch, as
applied here" section. The quote of the old handoff.core.md §4 bullet is in the comment, in full,
with the cause — their delivery transform replaced every blockquote in the document instead of the
first, so our quote became a second copy of their banner. Their committed source was never damaged.

Two things to do, both small. If we keep a copy or a summary of that report anywhere, attach the
before-text to it, because the version we were working from is the one missing it. And read their
note about #57 before filing it as an error: O-H1 called #53 and #57 "the nearest open items", and
#57 closed during our triage, hours after they sent. The row was accurate when written and when
delivered, and our own action made it stale. It is O-H7 seen from the sending end.

Nothing to re-triage. All seven verdicts stand, nothing new arrived, and no reply is needed.
```

For taskmd:

```text
A correction landed on https://github.com/uchimata2/taskmd/issues/1 — the adopter report from
htmldeck that we triaged. Three corrections, all theirs, and one answer to something we asked them
to check.

The one that costs us: our disposition comment lists "the version sort goes with them" as theirs
to act on. It is wrong, and they say so. The text-sort defect was found and fixed on their side
before that row was ever written — the locator parses the version and a self-test asserts 0.10.0
beats 0.5.0 — and the row simply never said so. O-T2's surviving clause is unchanged and we
accepted it correctly; it is evidence that re-deriving a locator is error-prone, not an open
defect. Correct our record so a later reader does not chase it.

Our O-T6 finding is confirmed. They audited the rest at our suggestion: seven foreign-id citations
across both their registers, one wrong, the one we found.

One new observation, unranked as everything in that register is. Our SKILL.md fallback resolves the
launcher from the directory the harness names when it serves the skill. Their release gate is a
plain `python tools/tasks/lint.py` run from any working directory, in a process that was never
served the skill and has no channel to ask for that directory — so the documented route does not
reach it, and the cache glob is not them ignoring it. They explicitly allow that a gate script may
be outside what this plugin means to support. That is our call to make, and it is worth making
deliberately rather than by omission, because it is the same shape as O-T2's surviving clause one
level up: the mechanism is stated as available, and the caller that most needs it cannot reach it.

Also, on T-145: they checked their wrapper for the `--help` exit-code exposure we flagged and are
not affected — it consumes -h/--help only as the first argument and never passes it through. That
is a negative result we asked for, so it is worth recording on T-145 rather than losing.

Nothing needs a reply, and no row needs re-triage.
```

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `O-T2` states the text sort was found and fixed here, with what fixes it | met | Corrected at the source and on the thread, naming `version_key` and the self-test. The correction says plainly that this is **the reporting project's error, not a change of mind** — the row was wrong when written, and a recipient cannot tell those apart from outside. |
| `O-T6` cites the right id, or no id, and says which | met | No id: the class was uncovered in their backlog until they raised their `T-146` in response. The struck text stays visible, and the row now states the general rule the error taught — a wrong foreign id resolves to a real task, so it reads as coverage and a reader who trusts it stops looking. |
| Every remaining foreign id checked, and the count written down | met | **Seven citations, one wrong**, table in §3, each checked against the project it names rather than against memory. |
| Each thread carries the corrections | met | Two comments, and each carries what only the sender could supply: the missing quote in full, and why the fallback does not reach a gate script. |
| The O-H4 section reads correctly wherever the recipient looks | met | The committed source was never damaged; the delivered body was, and the comment carries the missing quote verbatim. **The issue body was deliberately not edited** — the owner's ruling, and the thread is the record of the exchange rather than a document to keep tidy. |
| The transformation cannot silently do it again | met | The rule is in `../docs/CONTEXT-AUDIT.md` §7, next to the standing rules a future send reads — *diff the whole delivered artifact and account for every difference*. It is a rule and not a checker on purpose: the transformation is written fresh each time a register is sent, so there is no durable code for a gate to guard. |

**What the audit was actually worth**
One of seven citations was wrong, and the recipient had already found that one. On a narrow reading the
audit returned nothing. **That is the wrong reading**: the deliverable was the six cleared, because the
alternative to checking them is asserting they are fine — which is exactly the move that produced the
error. The criterion said *a spot check is not an audit* before the answer was known, and it would have
read as pedantry if the audit had found a second error.

**Child fix tasks raised**
- none. The wrapper-locator observation was recorded on the recipient's thread rather than raised here:
  it is a fact about their fallback's reach, and this project's own locator works.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | (delivered) | **Both prompts entered in the receiving repositories by the owner.** That closes the last thing either upstream exchange was waiting on from this side — registers sent, rows triaged, corrections posted, notices delivered. **A prompt is delivered when it is pasted, not when it is written**, which is why this row exists: §3 held two finished prompts and no fact about whether anyone had run them, and that gap is exactly the one the whole handover task was raised to close for the registers themselves. |
| 2026-08-15 | (addendum) | **The second pair of handover prompts added to §3**, at the owner's request and for the reason T-157 established: a thread notifies a watcher and nobody else. Sharper here — the handoff skill's issue is **closed**, so a correction on it is easier to miss than the report was. **These prompts differ from the first pair in asking the recipient to change their own record**, because taskmd's disposition lists work that is not theirs, and a correction that only reaches a thread leaves the wrong fact where the project keeps it. |
| 2026-08-15 | → done | Three corrections posted, both sources corrected, and the audit run: **seven foreign-id citations, one wrong** — the one the recipient found. The open question was ruled by the owner: **comment, do not edit the issue body**, because the thread is the record of an exchange rather than a document to keep tidy. Two things came out that §1 did not anticipate. `#57` closed *during* their triage, so a row can be true when sent and stale on arrival with nobody at fault — flagged rather than corrected. And their advice to delete both wrappers turned out not to reach a release gate, which is an observation about their fallback and went back as one, unranked. |
| 2026-08-15 | → proposed | Raised from what came back on the two threads T-157 opened. **Three errors, one found by each recipient and one found here**, and two of them are live in someone else's backlog. The one this project found is the worst of the three: `O-T2` reported a defect that had already been repaired, so taskmd's reply tells us to fix something that is fixed. A register that reports a repaired defect as open spends the recipient's attention on nothing, which is the same currency the *no priority* rule was protecting. `s` rather than `xs` because the cross-reference audit is a real pass over two documents, not a lookup. **`PH3` and `admin`**, following T-157: this is not a defect in the published plugin. |
