# Observations for the handoff skill

**From the htmldeck project, which uses it.** Six observations, none of them ranked and none of them
a request. They come from one adopting repository over about a week of daily use, and they are
written down because an adopter sees usage the author's own repositories cannot show.

## How to read this

- **Nothing here carries a priority.** Assigning one would be a guess about your project. What an
  observation is worth is your call, not the reporter's — which is also why the marginal-looking
  ones are here rather than filtered out.
- **Each row is stamped with how it was found.** *audit* rows came from a deliberate context-economy
  audit that **read your open issues and `PROJECT_BOARD.md` first**. *implementation* rows came later,
  from sessions building things, and **no backlog was re-read for them** — so read an *implementation*
  row as *this was observed*, never as *this is not already known or already decided*.
- **Ids.** `#nn` is one of yours. A `T-nnn` written as *the reporting project's* is htmldeck's and
  will collide with your own numbering if quoted bare.
- The environment throughout is Windows 11 with Git Bash and PowerShell 7, one machine.

## The observations

| | Observation |
| :--- | :--- |
| **O-H1** *audit* | **A measured figure propagated through five successive handoffs and was wrong by 3×.** A release-gate run time appeared in five consecutive handoff files here; measuring it returned 154 seconds against the 7–11 minutes being carried. The core's own golden rule — *the handoff points, it does not store* — already forbids this, and the failure is that a **number** does not look like the kind of fact the rule is about. **Where it might land:** the create flow's pre-write checklist already scans for secrets; measured figures are a second category with the same shape — value in the handoff, no durable home, copied forward untested. `#53` and `#57` are the nearest open items and neither covers it |
| **O-H2** *audit* | **There is no retention rule for archived handoffs.** This repository had **47** archived files at the time of the audit, mean 4,932 bytes, and **49** two days later; they are gitignored here so they cost a clone nothing, but in another adopting repository the archives are tracked and sit in the tree agents glob. `#8` is adjacent — it is about *pickup* when several exist, not about how many accumulate |
| **O-H3** *audit* | **A confirmation, not a finding.** The spine-plus-one-branch design measurably works. The audit's own session loaded the core and `flows/resume.md` and never touched `flows/create.md` or the tracker binding — **about 13 KB present, ~13 KB not paid.** Confirmed a second time by a later session that resumed work: core plus one flow, `flows/create.md` never opened. It is also the design the same author's task tracker explicitly copied when it settled its own tier model |
| **O-H4** *implementation* | **A mode word followed by a qualifier routes to the opposite mode.** The spine's §4 says trailing text that is *just* a mode word selects that mode, and that **otherwise the whole argument is the subject of a handoff to create**. A user typed `resume, full lifecycle` — a mode word plus a qualifier about how to work — which by the letter of the rule selects **Create** and records *"resume, full lifecycle"* as the next session's task. Resume was obviously meant, and Resume was run. The rule reads as though the alternative to a bare mode word is a sentence describing future work, but `<mode> <qualifier>` is ordinary phrasing and lands on the wrong side of it. **A patch is proposed below** |
| **O-H5** *implementation* | **A handoff that states a board count is storing a derived fact, and the one consumed here was already stale.** It read *22 open, 115 closed*; the tracker said 23 active before that session changed anything. Harmless once, and the same class as `O-H1` — the golden rule *the handoff points, it does not store* is broken by counts and figures without looking as though it is, because a count feels like state rather than like a fact with a home. A pointer to the command that answers it costs one line and cannot go stale |
| **O-H6** *implementation* | **`reconcile_targets` is a hand-kept list, and the §3a sweep went outside it.** This project declares `tasks/, docs/BRIEF.md`. Closing four tasks made statements stale in two further documents, and both were reconciled because the session had touched them — which is the *fallback* rule, not the declared one. A declared list is subject to exactly the staleness it exists to prevent. **Where it might land:** §0's key description, or §3a's closing test — possibly as *the declared targets are a floor, never a ceiling*, which is what actually happened here |

## The O-H4 patch, as applied here

The installed copy at the adopter's machine was edited so the behaviour is right today. **That copy
is not under version control and is not your source**, so the change is written out here to reach the
repository it belongs in. In `handoff.core.md` §4, *Explicit invocation and its argument*, the second
bullet currently reads:

> **otherwise the whole argument is the *subject of the handoff to create*** — a description of what
> the **next** session should do.

The asymmetry is in the parenthesis that follows it: text after `create` is already treated as *mode
plus subject*, while text after `resume`, `status` or `close` is treated as a subject that happens to
contain a mode word. What was applied instead:

1. **A leading mode word always selects the mode**, whatever follows it.
2. After `create`, the remainder is the **subject** — what the next session should do — exactly as
   today.
3. After `resume`, `status` or `close`, the remainder is a **qualifier on this run** — how to do the
   thing — because those modes act on a handoff that already exists and have no subject to take.
4. **If that trailing text plainly describes work for a later session rather than guidance for this
   one, ask** which was meant. That case is genuinely ambiguous — `resume the migration next week`
   can be either — and §4 already prefers asking over guessing when a bare *wrap up* is ambiguous.

Rule 4 is the part worth arguing with. It adds a question to a flow that currently never asks in this
position, and the alternative — always treating the remainder as a qualifier — is simpler and wrong
about one real phrasing.

## Provenance

Assembled by the htmldeck project as part of a context-economy audit of its own development
workflow, and extracted here so it arrives as its own document. The audit that produced the *audit*
rows is [`../CONTEXT-AUDIT.md`](../CONTEXT-AUDIT.md) §7.1; the rules the register follows are in
[`../research/R8-context-economy-for-coding-agents.md`](../research/R8-context-economy-for-coding-agents.md)
§6. Replies, corrections and *already knew that* are all useful; a row that turns out to be wrong
gets corrected here rather than quietly dropped.
