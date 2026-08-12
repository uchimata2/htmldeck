# Lessons

Things this project has already paid for once. Each is **generic** — it survives the task that
produced it and applies to the next one — and each is stated so it can be *acted on*, not
admired.

Cite them by ID. `L-07` and `L-11` are cited from `tools/assets/build_probe_deck.py`, so **IDs are
stable**: add at the end of a section, never renumber.

Seeded from the "Carried lessons" table in [`BRIEF.md`](BRIEF.md), which keeps the corpus
evidence behind several of them, and from `docs/research/R4-prior-art.md` §1. Project-specific
findings stay in the task file or the research note that produced them; only what generalises
comes here.

---

## Evidence and verification

### L-01 — Look at the output

Every automated check can pass on something visibly broken. A deck that validates is not a deck
that reads well; a report that renders is not a report that makes sense.

**How to apply.** Open the artefact the way its audience will — for a deck, from `file://` with
the network off — and look at it before writing "done". This is rule 6 in
[`../CLAUDE.md`](../CLAUDE.md) and part of the definition of done in
[`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) §2.

### L-02 — Verify on the real case, not a toy

Layout, pacing and performance problems appear at real size and nowhere else. A three-slide
example proves the generator runs; it proves nothing about what it produces.

**How to apply.** Pick the smallest case that is genuinely representative — for this project, a
12-slide deck with diagrams — and make that the acceptance case, not the demo.

### L-03 — Count, don't read

Defects that span documents are invisible to reading and obvious to counting. A figure that is
right where it is stated and wrong where it is quoted survives every careful read of each
document on its own.

**How to apply.** Tally the table's own verdict column. Count the nodes in the model the sentence
describes. Build the one boring table that lists every figure, its origin, and every place it is
reused — then compare. Cheap, and it finds what review does not.

### L-04 — Verify the checker on a known case

A measurement is believed in proportion to how little it looks like a tool. One scan in the
corpus split sentences line by line against hard-wrapped Markdown and under-reported by 15×; it
was trusted because it printed numbers.

**How to apply.** Every check ships with a self-test on a case whose answer was worked out by
hand. Run it before believing the check, and again whenever the check changes.

**The checker's *inputs* need the same suspicion.** Three rows of T-017's `file://` probe reported
the environment as refusing something when the fixture was simply invalid — a 2 ms audio clip no
element will ever report metadata for, a 36-byte fragment of an mp4 header that is not a decodable
video, and a font check that would have passed while the page rendered in Arial. A false FAIL is
quieter than a false PASS and just as wrong: it deletes a capability from the record that was never
actually tested.

### L-05 — Say which half you checked

A check that *looks* complete is worse than no check, because a partial pass gets read as a
verdict on the whole.

**How to apply.** State in the output what was **not** examined. `task.py check` reporting "0
broken links" was true and misleading in the same breath: it validated links between task files
while two documents the tooling itself pointed at did not exist. Name the scope in the success
line, not only in the failure.

### L-06 — Ask the authoritative source, not the convenient one

The convenient source answers confidently and wrongly. Two versions of this cost time in one
sitting:

- **A sandboxed shell reports "denied" as "does not exist".** `Get-ChildItem` on a directory
  outside the sandbox returns *cannot find path*, and a recursive search returns nothing at all,
  with no error. Bash and the file-reading tools read the same path without trouble. A session
  that trusts the shell here concludes the files are not on disk, which is false.
- **A skill's own body is half of it.** `SKILL.md` is a routing table; the substance sits in
  `references/` and `templates/`, several times longer, and that is where nearly everything
  worth finding was found.
- **A preview pane is not a browser.** It renders `file://` pages as static snapshots, and the
  snapshot renderer draws SVG `text-anchor` wrongly. It produced a convincing picture of a broken
  diagram that was not broken — the DOM geometry was correct to the pixel when measured. A visual
  defect very nearly went into a research note on the strength of a screenshot.

**How to apply.** When a source says "nothing here", confirm with a second tool before recording
it as a finding. Absence claimed by a restricted reader is not evidence of absence. Two
acceptance criteria on T-009 were reported unmet on this exact mistake and were both wrong — the
material existed in documents that had not been read.

The visual case has its own move: **measure, do not only look.** For anything rendered, get the
computed geometry out of the DOM before recording what the picture seems to show. This does not
weaken **L-01** — you still have to look — it says a screenshot alone is one source, and the
lesson above applies to it like any other.

### L-14 — Say which layer of a conclusion is load-bearing

A decision is rarely one claim. It is usually a measurement, a structural ruling that follows from
it, and a specific choice that follows from neither — and those have completely different
strengths. Recorded as a single verdict, the weakest layer inherits the confidence of the
strongest, and a later reader cannot tell which part they are allowed to revisit.

The concrete case: closing the font decision recorded *"embedded subsets, and the faces are these
three"* as one decision. The first half rested on measurement and nothing left in the research
could move it. The second was a preference that two unfinished research tasks could reasonably
overturn — and it was written with the same certainty.

**How to apply.** When a task closes ahead of research that touches it, split the verdict into
settled / provisional and name **what specifically could move each row**. "Provisional" without a
named mover is just hedging; it has to say *which* task, so the synthesis step knows what to
re-test rather than inherit. This also protects the strong rows, which otherwise get re-litigated
alongside the weak ones.

### L-15 — A tool that fails optimistically is worse than one that fails

An unreliable tool that errors is a nuisance. One that answers *confidently and permissively* —
reporting a capability as available when the real environment denies it — puts the defect in the
shipped artefact instead of the console. The cost is paid by the recipient, not the author.

The case: a preview pane loaded with a `file://` page allowed `fetch()` of a local file. A real
restricted origin denies it. Every check run there passes, and the deck breaks on the recipient's
machine. It is **L-06** with the stakes inverted — the convenient source did not say "nothing
here", it said "everything works".

> **One of the two original proofs was withdrawn, 2026-08-06, by T-017's measurement.** This
> lesson also cited the pane reporting `location.origin` as `"file://"` rather than an opaque
> `"null"`. **Real Chrome 151 reports `"file://"` too**, on a genuinely double-clicked file — it is
> what Chrome does, and it is evidence of nothing. The origin *is* opaque there (Chrome's own
> worker error names it `'null'`), but `location.origin` does not say so. The `fetch()` half is
> the real discriminator and the lesson stands on it.
>
> Which makes this lesson an instance of itself, and that is why the correction is kept rather
> than tidied away: **the diagnostic used to convict the untrustworthy tool had not been checked
> against the trustworthy one either.** When you catch a tool lying, verify the test you caught it
> with — on the real environment, before it becomes the thing everyone cites.

> **A third instance, 2026-08-11, from [T-019](../tasks/T-019-build-the-capability-preflight-the-deck-ships-wit.md),
> and this one is a flag rather than a pane.** Chrome offers two ways to run a page with scripting
> off, and they fail in opposite directions. `--blink-settings=scriptEnabled=false` genuinely
> disables it and then produces neither a screenshot nor a `--dump-dom` payload — honest and
> unusable. **`--disable-javascript` writes the screenshot and disables nothing**: the deck presented
> normally under it, and the picture would have shipped as *what a recipient with no scripting sees*.
> The suppression went into the file instead, where it can be read back. **A switch that is supposed
> to take a capability away needs a positive test that it took it away** — here, that the degraded
> banner is in the output — or it is another confident permissive answer.

**How to apply.** For any constraint that only bites in the delivery environment, test *in* that
environment — for a deck, a real double-click on a clean profile. When a tool cannot be trusted
for a given question, record the prohibition in the task that will ask it, not only in the note
where it was discovered; the next session reads the task.

### L-16 — A probe cannot report through the channel it is testing

The natural way to get results out of an experiment is the most capable channel available. When
the experiment is *about what the environment permits*, that channel is one of the things under
test — and its failure erases the result instead of recording it.

The case: the `file://` probe reported by downloading a JSON file. Downloading is itself a row in
that matrix. Worse, a *second* download from one page makes Chrome raise a permission dialog, and
the dialog takes focus away from the page — so the download channel disabled the very rows that
were about to be measured. The fallback, a result payload rotated through the window title in
chunks, needed no permission from anyone and carried every row.

**How to apply.** Give any probe a reporting path that spends nothing the probe is measuring, and
prefer the dumbest channel available: something already visible from outside the subject — a title,
an exit code, a file the harness wrote itself — over anything the subject must be *permitted* to
do. Build the fallback first; it is the one that reports the interesting failures.

### L-17 — A permission you spend once cannot be shared across measurements

Some capabilities are gated on a resource that is *consumed on use* rather than merely checked: a
browser's transient user activation, a one-time token, a rate-limited call, a single confirmation.
Test several such capabilities from one grant and only the first is measured honestly. The rest
report the exhaustion of the grant — and they report it in the vocabulary of refusal, so the
result reads exactly like the environment saying no.

The case: four gesture-gated rows (fullscreen, clipboard, audio resume, download) were chained
off a single click. Three came back `NotAllowedError` and were about to be written into the
portability contract as `file://` restrictions. Given one click each, **all four pass** — nothing
had been refused. A second instance of the same fault sat underneath it: the first click on a
newly opened window is spent focusing that window, so even the one-click-each version failed its
*first* row until an unmeasured arming click was put in front.

**How to apply.** One grant, one measurement. Give each gated call its own fresh grant, and if
acquiring the grant has its own side effect (focus, a dialog, a redirect), spend one on arming and
measure nothing with it. Then ask what a failure would look like if the harness were at fault: for
consumable permissions the answer is *identical to a genuine refusal*, which is why this cannot be
caught by reading the result.

### L-18 — A shared readback channel carries the previous run's answer

When results come back over a channel that is not private to the run — a window title, a
well-known file, a fixed port, a shared clipboard, a log — a leftover producer from an earlier run
is indistinguishable from the current one, and it answers first.

The case: the probe reports through the window title, which is global to the desktop. A run
launched by double-click harvested a complete, well-formed, *correct-looking* payload from a probe
window still open from the previous run — gesture rows the freshly opened page had not yet run and
could not have produced. Nothing was malformed; the reassembly succeeded; the answer was simply
from the wrong run.

**How to apply.** Before starting a run, record which producers already exist, and ignore them —
by handle, pid or inode, not by name or title, since those are exactly what a stale producer
shares with a fresh one. Where possible make the channel per-run instead. Treat a plausible
result arriving *sooner than the work could have finished* as the signature of this fault.

### L-19 — Repetition is not evidence; grade the source, then let the grade decide

A claim repeated in fifty places is one claim with fifty citations, and it loses to a single
controlled result. Read literature arrives pre-laundered: practitioner advice quotes practitioner
advice until an unsourced number looks like a finding.

The case: R2 found the most-repeated rule in slide typography — a minimum point size for body text
— had no measurement behind it anywhere, and its sources disagreed with each other by more than 2×.
Meanwhile the best-supported result in the field (23 of 23 tests, median effect size 0.86) pointed
against a thing this project had already decided it wanted. Without grades, the loud rule would have
won on familiarity and the quiet one would have been softened into a suggestion.

**How to apply.** Put an explicit grade on every claim as you record it — controlled result ·
specification · consensus-with-a-mechanism · bare assertion — and write the rule that grades
decide conflicts, *before* meeting one. Then two things follow that are otherwise hard to do:
a well-loved rule can be rejected on the record with a reason, and a rule you keep anyway can be
labelled unsupported so a later session knows it is cheap to overturn. **Record silence too** —
"the literature does not address this case" is a finding, and it is the honest alternative to
inferring a rule and presenting it as sourced.

### L-20 — Reconcile the plan against the research, not only research against research

When research *is* the work, the document that commissioned it goes stale silently. Nothing inside a
research pass forces you back to the plan, and every new note makes the plan feel better supported
rather than more suspect — the evidence base grows while the thing it was meant to correct sits
untouched.

The case: six research notes were written against a *What to build* section that three of them had
already contradicted. R1 recorded a seven-stage authoring pipeline with two reviews before any HTML
exists; R1 §14 proved a second critique format; R4 §9 graded the whole structure owner-authored with
zero prior art. The plan still listed three modes. Each note was carefully reconciled against the
*other notes* — provenance checked, overlaps filtered, contradictions surfaced — and none was
reconciled against the plan. **The gap was found when the owner described their own process out
loud**, not by any review, and not by the tooling, which validates structure and cannot read intent.

**How to apply.** Make it a required output of every research task: re-read the section of the plan
the research was commissioned to inform, and state either what changed in it or that nothing did.
"The plan still says X; the research now says Y" is a finding, and it must be written down at the
time — a later session cannot recover it, because by then the plan reads as settled. Treat a
research note whose only citations are other research notes as unchecked: it has not yet been held
against anything with the standing to contradict it.

### L-21 — A tie-break between two sources cannot resolve a conflict with a third

A rule for choosing between evidence and habit is a rule about *two* inputs. Standing decisions are
a third, they outrank both, and a tie-break written without them silently has no verdict for the
cases they govern — which are usually the ones that matter, because a decision gets made precisely
where something was contested.

The case: T-014's tie-break was set carefully — principle wins on anything measurable, habit wins
where evidence is weak. Applied to 154 rules it fired **once**. Four other rules changed, and every
one of them changed because a standing owner decision overrode an observed habit with no external
principle involved at all: the per-deck palette and the per-deck font rotation both lost to *one
theme*, and two portability rules lost to a measurement that had retired their premise. Had the
lookup only known its two named classes, all four would have been resolved on the merits, one at a
time — the exact failure the tie-break was written to prevent.

**How to apply.** When a conflict rule is written, enumerate every class of input that can win, not
only the two in tension. State their precedence explicitly and resolve in that order — standing
decisions first, then the graded evidence, then the named contradictions, then the default. Then
**count how often each class fires**: a class that never fires is either wrong or unnecessary, and a
class that fires four times while the headline rule fires once was the real rule all along.

### L-22 — Ask what a constraint is for; the mechanism is not the requirement

A constraint arrives stated as a mechanism — *a fixed scaled stage*, *no external references*, *one
accent*. The mechanism is one solution to a requirement nobody wrote down. Implement the mechanism
and you satisfy the letter; ask for the requirement and you usually get a **number**, because
requirements come from things that went wrong and things that went wrong were observed.

The case: the fixed 1600×900 stage sat in the corpus with the rationale *"what was rehearsed is what
appears"* — which reads as presenter convenience, and is weak enough that T-014 escalated it as
losing to two WCAG criteria. The owner's actual reason was two observed failures: decks built for
small screens **break on a 4K display**, and decks presented from a high-resolution monitor **arrive
illegible** because a video call re-encodes the shared screen at 1080p or 720p. The second has an
arithmetic answer — under a uniform scale the presenter's viewport cancels out, so stream legibility
depends only on the design size and the call's resolution. **That turned a contested preference into
a hard rule with a computed floor** (body ≥ 24 design units, nothing under 16 anywhere — the floor
the owner later set), tightened a corpus
range that had been carried unexamined, and demoted a corpus element — mono labels — that the
arithmetic showed had never been legible to a remote audience. **It also flipped an option from
"cheaper but worse" to "ruled out", because it re-introduces the defect.**

None of that was derivable from the mechanism. It was one question away the whole time.

**How to apply.** When a rule is inherited as a mechanism and the rationale is thin, do not weigh it
as taste — **ask what it prevents, and ask for the incident.** Then check whether the mechanism is
the only thing that prevents it: if it is, the rule is hard and the alternatives are ruled out, not
merely dispreferred. Watch especially for constraints whose stated reason is a *convenience* — a
convenience rationale on a rule someone insists on is usually a symptom of the real reason not
having been written down.

### L-23 — A standard needs IDs and a score, or it cannot drive anything

A ruleset written as prose is readable and inert. To *operate* — to be checked, reported on, fixed
against, and converged toward — it needs two things that feel like bureaucracy while you are writing
it and turn out to be the whole mechanism:

- **A stable ID per rule.** Without one, a finding cannot cite what it violates, a fix cannot be
  verified as landing, and two reviews of the same deck cannot be compared. Prose rules produce prose
  findings, and prose findings cannot be counted.
- **A score, distinct from a gate.** Pass/fail cannot show progress, so it cannot terminate a loop
  except at "no failures left". Prose cannot show convergence at all. **Something has to answer *is
  this better than the last iteration?* numerically, or the loop stops when the agent feels
  finished.**

The case: this project produced 131 carefully-reasoned design rules with sources, evidence grades
and resolved conflicts — and no way to answer *"is this deck good enough yet?"* The rules had no IDs,
so nothing could point at one. There was a pass/fail check and a prose critique, and neither could
drive an iteration. **The owner's phrase for it was exact: a design system without an effective
pipeline is decoration.**

**How to apply.** When writing any standard meant to be applied repeatedly, add three columns before
the prose: **ID** (permanent, never reused), **severity class** (gate versus scored — a gate failure
must never be averaged away), and **how it is checked** (automatic · needs rendering · judgement).
That last column is the routing table for the whole pipeline and it costs nothing to write while the
rule is fresh. Then ask the question that exposes whether the standard is operable at all: **what
number goes up when this gets better?** If there is no answer, nothing built on it can converge.

### L-24 — A standard is unvalidated until something is built strictly against it

Reading a ruleset tells you whether it is coherent. **Building to it tells you whether it is
possible**, and those are different questions with different answers.

The case: 131 rules, reviewed repeatedly, cited by ID, with conflicts already resolved and recorded.
The first real deck built strictly against them produced **thirteen findings** — four of them
conflicts between two rules both labelled `hard`, so a compliant deck could not exist; three rules
unimplementable as written; one rule whose check was impossible as specified. One finding surfaced
before a line of code, from reading the rules *in order to build*. **Every one of the other twelve
came from the build or from measuring what the build produced.** Review of the ruleset as a document
had found none of them, because a reader resolves an ambiguity silently and a builder cannot.

**How to apply.** Treat "build one real artifact strictly to it" as part of writing a standard, not
as the first use of a finished one — and budget for it, because the findings arrive at roughly one
per ten rules. Two disciplines make it work: **build to the rule even where the rule is painful**
(softening it destroys the evidence), and **record the finding rather than fixing the rule
mid-build** — a test that edits the thing it is testing is not a test. Hand the findings to a
separate task.

### L-25 — Two conformance floors on one element can be jointly unsatisfiable

Accessibility minima are usually met one at a time, so it is easy to assume they compose. They do
not always. A neutral data mark must be **dark enough** to clear 3:1 against the page (non-text
contrast) and **light enough** to carry 4.5:1 text (text contrast). In a neutral hue there is no
value that does both — the requirement is not "pick a better colour", it is *"text does not belong
inside that mark"*.

The same shape appeared twice more in one build: a target-size minimum in CSS pixels silently sets a
minimum in *design units* once a scaled stage is involved (and the binding number comes from an
unrelated rule — the width at which the layout stops being shown at all); and a panel required to
open downward cannot do so if its control sits near the foot of a fixed-height stage.

**How to apply.** When a rule constrains an element, check it against the *other* rules touching the
same element before choosing a value — especially where one is expressed in absolute units and the
other in the design's own units. Where two floors genuinely cannot both hold, **the resolution is
usually structural rather than numeric**: move the text out, move the control up. Record which rule
yielded and why, because the next builder will hit the same pair.

### L-28 — Most conflicts between two hard rules are a missing scope, not a real impossibility

A build reports *"these two rules cannot both be satisfied"* and the instinct is to arbitrate — weigh
the two, pick a winner, soften the loser. **Usually there is nothing to arbitrate.** The rules were
written at different altitudes about different cases, and the conflict is that neither says which
case it governs.

The case: four conflicts between two rules both labelled `hard`, from one build. Only **one** was a
genuine impossibility (two contrast floors on one element — **L-25**). Of the other three, one was a
number set too high in a rule whose principle was never in doubt, and **two were a general rule and
its own specific case, both marked `hard` with no precedence between them**: a 500 ms animation cap
against a named vocabulary containing a 1.2 s pulse and a 4.5 s loop, and a rule requiring charts to
"draw in" against a rule closing the motion vocabulary at four. In both, **the intended design was
consistent and the text was not.** The reference deck implemented both correctly by guessing the
scope — which is the tell: a builder who has to infer the precedence will sometimes infer it wrong,
and nothing will catch that, because both readings cite a `hard` rule.

Two failure shapes produce this, and both are worth recognising by sight:

- **The general rule with an unnamed exception.** Write the scope into the general rule and name the
  specific one as the override. Both stay `hard`; neither is softened.
- **The rule that bans a mechanism instead of a failure.** "No `px` inside the stage" is
  unsatisfiable as written — every CSS length resolves to an absolute unit, so a design unit must be
  declared as one somewhere. The rule was right about what goes wrong and wrong about what causes it,
  which is what happens when a rule is written from a symptom. **A rule nobody can satisfy is not
  strict; it is ignored.**

**How to apply.** Before arbitrating a conflict, ask *is one of these the other's specific case?* and
*can this rule be satisfied at all, by anyone?* If either is yes, the fix is text — a scope clause, a
named override — and no rule loses. Reserve yielding for conflicts that survive both questions. And
**put the ruling in the rule itself, not only in the rationale**: nothing loads the rationale at
build time, so a precedence recorded only there will be re-derived by guess on the next build.

### L-29 — Evidence arriving after a recommendation must re-derive it, not ratify it

Deferring a decision until there is evidence is right. But the recommendation written *while*
deferring it does not wait — it sits in the document as the default answer, and when the evidence
finally arrives the question asked of it is **"does this support the recommendation?"** rather than
**"what does this say the answer is?"** Those come apart in a specific and easy-to-miss way: the
evidence can confirm the recommendation's *rationale* exactly while showing its *scope* was set too
small. Confirmation of the reasoning then reads as confirmation of the answer.

The case: an open question — *who scores a deck?* — carried the recommendation "author scores each
slide, fresh context scores the whole deck", written before any deck existed. The validating build
then produced the measurement the question had been waiting for: of ten scoring dimensions, **five
are invisible to every mechanical check**, so whoever scores those five is the entire quality
mechanism. The same build supplied a textbook confirmation of the recommendation's reasoning — one
dimension scored 4 only after counting, having been read past repeatedly, exactly the self-review
failure the recommendation named. Every instinct said ratify. **But the recommendation put only two
of those five dimensions in fresh context.** The other three were per-slide, so the recommendation
left them with the author — a three-dimension hole in the quality mechanism that the confirming
evidence made *easier* to miss, not harder. It cost one pass per round to close.

**How to apply.** When evidence lands on a deferred question, re-derive the answer from the evidence
before re-reading the recommendation — and where that is not practical, at minimum **check the
recommendation's coverage against the evidence's own categories**, one by one, rather than checking
its argument. Ask *what does the evidence say the problem is made of, and does the standing answer
address all of it?* Two habits make this routine: state each option's cost in the same unit so the
alternatives stay comparable rather than rhetorical, and **put the options to the decider with the
coverage stated, not the recommendation with its support attached.** A recommendation is a hypothesis
recorded at a time of lower information; treat it as an input to the decision, never as its default.

### L-30 — An exemption keyed on a value silently exempts everything that value matches

**L-05** says a check must state what it did not examine. This is the mechanism that makes that
hard to obey: an exemption written as *"skip anything matching X"* has no fixed size. It looks like
a small carve-out at the point it is written, and its real cost is however much of the corpus
happens to match X — a quantity nobody measures, because the check's output reports what it looked
at, not what it declined to.

The case: `task.py check` skipped any path a task had declared as a deliverable, on the reasoning
that an unproduced output is a promise about the future rather than a broken pointer. Sound as far
as it goes. But it keyed on the **path**, so one declaration exempted that path *in every document
in the repository, permanently* — and most declared outputs are the long-lived documents everything
else cites. **It was hiding 110 of 357 pointers, roughly a third, while printing `0 broken`.**

**The measurement trap is the second half, and it is the part that generalises.** The defect was
found by declaring one existing file and watching the count fall by **six** — so it was reported,
and initially scoped, as a six-pointer problem. Six was the *marginal* cost of one new declaration.
The *standing* cost was 110, and nothing in the discovery hinted at the difference. **What you
measure when you trip a rule is what tripping it cost, not what the rule costs.**

**A second case, and it is the same shape read from the other end.** A check on the plugin package
flagged a working-directory-relative path only when the sentence around it contained the word
*load* — an inclusion keyed on a value rather than an exemption, but with the identical property:
its size is whatever happens to match. `Build to <a doc>` is a load instruction and does not say
*load*, so it passed. Replacing the keyed rule with a blanket one — **every** bare repo-relative
path in a skill file — found **13 live mis-resolutions**, four of them inside the load table that is
the skill's entire routing job. **Inclusions key on values as readily as exemptions do**, and the
tell is the same: the rule names a token instead of a position.

**How to apply.** Prefer an exemption keyed on the **site** — this field, this file, this call —
over one keyed on a **value**, because a site-keyed rule has a size you can see and cannot widen
when unrelated content starts matching. Where a value-keyed exemption is genuinely needed, **count
what it currently excludes and print that count**, so the number is visible when it grows. And when
a coverage defect surfaces, measure the rule with the exemption removed entirely before scoping the
fix — the discovery gives you a delta, and the delta is not the total.

### L-31 — A dependency edge is a claim with a date on it, and nothing re-checks it

An edge records what was true when someone wrote it. The work it describes then moves, and the edge
does not. **The index cannot tell a correct edge from an unrevisited one** — both render as the same
row — so a stale gate is invisible in exactly the view built to make dependencies visible.

The case: `T-005` (the build check) was `blocked_by` build mode, written when neither existed. A
later task then built the reference deck by hand, and with it a measurement layer running 30 checks
against two decks now committed to the repository — one of them the seeded-defect fixture T-005's
own criteria demand. **T-005 was a third built while the board reported it gated**, and nothing in
the backlog said so, because nothing re-reads an edge once it is written.

Note what did *not* fix it: the blocking task never landed. The gate went false because unrelated
work supplied what the gate was protecting against. **An edge can be invalidated by something that
touches neither of its endpoints**, which is why "re-check the edges when the blocker closes" is not
enough.

**How to apply.** Treat a `blocked_by` as a dated assertion, not a fact. When any task closes,
re-read the edges of everything it plausibly touched, not only its own. Periodically audit the whole
graph — the cost is one pass and the finding is usually that most edges are right, which is itself
worth knowing, because *unblocked* and *unrevisited* are otherwise the same picture. And when a
ruling is made in prose — a release gate, a precedence — **write the edge the same day**; a
dependency stated only in a document is one the tooling cannot enforce and the board will contradict.

### L-32 — Building one instance by hand does the first pass of every task downstream of it

To make a hand-built reference artifact comply with a ruleset, you must build a first version of
whatever the ruleset requires — the tokens, the components, the checks. Those are usually other
tasks' deliverables. **The work lands, and the specifications that asked for it never notice**, so
they go on describing authorship when what is actually left is extraction and proof.

The case: one reference deck produced a first instance of **four** downstream tasks — 57 custom
properties (the token layer), a disclosure component and a motion vocabulary (the interaction
layer), a reflow view carrying all tier-two content, and a 30-check measurement layer. Two of the
four recorded it in their logs. The other two still read as greenfield, which misprices them badly:
extracting a contract from something that works is a different and much cheaper job than authoring
one.

**How to apply.** When a task builds something end to end, list what it had to build *incidentally*
and write a log row on each downstream task that now owns a first instance. Say what exists and,
more importantly, **what is still missing** — an instance is not a contract, and a thing that works
once is not a thing that is specified. The bar for the downstream task does not drop; only its
starting point moves.

### L-33 — A decision recorded in prose is unchecked until something has to wire it

A ruling written into a document reads as settled. Nothing verifies that it agrees with the ruleset
it depends on, with the diagram three paragraphs above it, or **with the argument the same document
makes two sections later**. Pointer checks do not catch it: every link resolves, and the documents
still contradict each other. **The first real check on a decision is the first task that has to
build against it.**

The case: a decision task adopted a seven-stage pipeline and placed one approval gate *after* the
specification review. The design system put the artifact that gate covers **before** the
specification — the specification is expanded *from* it. The decision task's own later section then
argued that this gate exists to cut work before it is expanded, which its earlier section had made
impossible. **Three documents, one order, three positions**, and the task closed `done` with every
acceptance criterion met and a clean `check`. It surfaced when the downstream task tried to wire the
gates and found it could not wire both.

This is L-24 at the level of decisions rather than standards: *a standard is unvalidated until
something is built strictly against it.* The correction is not more review of the deciding task —
its own review pass had read all of it and missed this — but recognising **where** the check
actually happens.

**How to apply.** When a decision fixes an *order*, a *precedence* or a *placement*, name the other
documents that state the same order and reconcile them in the same edit — that is the sweep, and it
is cheap while the decision is being written. When a downstream task opens against a decision,
read the decision for self-consistency **before** absorbing it into a scope: that reading is the
validation pass, so spend it there rather than assuming a `done` task is coherent. And when the
contradiction is found, fix **every** document that carried it, including the one a reader reaches
first — correcting the decision alone leaves the wrong version in the specification.

### L-34 — A test fixture is indistinguishable from the real thing, which is the point and the problem

A fixture earns its keep by looking exactly like live input. Any *other* scanner over the same
repository therefore reads it as live input, because there is nothing in the text to read
differently. Two checks that are individually right then contradict each other, and the one that
loses is usually the one that runs second.

The case: a scaffold check needed fixtures naming plausible files — a manifest, a skill body, a
document one of them points at — to demonstrate it catches a dead pointer. Written as string
literals, those names were then picked up by the project's *reference* check as pointers into the
repository, and four of them reported dead. Both checks were correct. The fixture names were not
references; nothing said so.

**The fix is not an exemption, which would be L-30 again.** Assembling the paths from components
makes them what they already were — structured data rather than prose — and the reference check
already draws exactly that distinction for front-matter, having reached it independently and from
the other side. **When two checks in one repository disagree about a string, one of them is reading
structure as prose**, and naming which is cheaper than carving either one back.

**How to apply.** Before writing realistic fixture data, ask what else scans this repository. Give
fixtures a form the other checks already exclude — assembled values, a directory the ignore rules
cover, a file type nobody parses — rather than a carve-out keyed on their content. And when a check
fails on its own test data, do not reach for the exemption first: the collision is usually telling
you that one of the two is treating a structured record as prose.

### L-35 — An instrument scoped out for being a different code path will eventually prove it

A substitute instrument is adopted because it agrees with the real one on the cases tried so far.
Every run where it agrees feels like evidence that it is equivalent. It is not: it is evidence
about the cases tried, and the disagreement arrives on the case that matters, because that is the
case where the code paths differ.

The case: headless `--print-to-pdf` was scoped out of [R7](research/R7-printable-mode.md) as a
*measurement* instrument and used only to diagnose. It then disagreed with the real browser on the
central question — the deck flips itself into its reading view when printing narrows the layout
viewport, and headless did not flip. The headless check passed while the real print was producing
blank pages, and a marker experiment run headlessly **ruled out the true explanation** and sent the
diagnosis down a false path for several rounds.

The same shape twice more in one task, both in how quality was *measured* rather than produced: a
dead-space metric counted the browser's header and footer as page content, and reported 2.4% on
pages that were visibly half empty; and it was run on Letter portrait while the deck is printed on
A4 landscape, when page height is the exact variable that decides whether an unbreakable block is
ruinous. Both flattered the result, which is the dangerous direction (**L-15**).

**How to apply.** Write down what the substitute cannot see *before* using it, and treat every
result from it as a hypothesis the real instrument has to confirm. When the substitute and the real
thing disagree, the real one wins and the substitute's earlier agreements are retroactively worth
nothing. And when a measurement disagrees with what someone is plainly looking at, suspect the
measurement first — check what it counts and what conditions it runs under, before concluding the
artifact is fine.

### L-36 — A stated tolerance is a claim about the instrument, not only about the artifact

A threshold looks verified once a number sits next to it. But a threshold is only as real as the
values that were compared to produce it, and **a category the probe never sampled produces no
values and no complaint** — the rule reads as measured, the citation resolves, and nothing anywhere
says the number covers nothing.

The case: DS-063 states two tolerances, non-text geometry ≤ 0.25 design units and text runs ≤ 2.
Both were recorded as *measured rather than guessed*, sourced to 384 values across two resolutions,
and carried through a full split of the design system into rules and rationale. When
[T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md) turned the rule into a gate,
**the probe behind those 384 values turned out to contain nine keys and all nine are text runs.**
The stricter tolerance had never had a single value in it, and the *"positions agreed to 0.09 du"*
line under it was the worst placement disagreement among text elements, filed under non-text.

Adding four non-text boxes to the probe measured it for the first time: **116 values, worst
disagreement 0.000 du.** The rule was right and the evidence for it was not there. A second finding
came with it — the split belongs to element kind, not to axis, because glyph rounding moves a text
run's position and height as well as its width — and holding text placement to the non-text figure
would have failed a provably-identical layout on 27 values.

**It happened again, in a different part of the system, and that is what makes it a property rather
than an accident.** [T-027](../tasks/T-027-specify-the-slide-deliverable-and-the-outline-contract.md)
wrote five rules and labelled them `auto` and `render` — *a machine decides this* — and no machine
did. [T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) found the
reference deck carrying a bottom line on **none** of its twelve slides and **three** simultaneous
encodings of position, while a 43-check gate reported zero failures. The label was a plan, and
nothing distinguished a rule that was gated from a rule that merely intended to be. Two further
turns of the same screw arrived in the same task:

- **The gate was driving the deck through a piece of chrome a rule required deleting.** Both
  `audit.py` and `render.py` clicked `#dots.children[i]`. Removing the dots made stage 3 print *NO
  RESULT* and made `render.py measure` emit a DS-063 verdict computed from **16 values, all from
  slide 1** — a tolerance line that read as a pass. Navigation now uses next/previous, which are
  controls rather than position encodings.
- **Two of the new checks were wrong when written**, and the variant suite is the only reason that
  is known: the chrome item count scored every ribbon stage twice and reported 24 items for an
  11-item chrome.

**How to apply.** When a rule cites a measurement, check what the instrument sampled before
trusting the number, and prefer a check that reports *how many values it compared* over one that
reports a verdict — a count of zero is then visible instead of silent. **A gate must fail on
"nothing measured", never pass on it** — including when the reason nothing was measured is that
the gate could not drive the artifact. This is **L-05** — *say which half you checked* — and
DS-191 arriving from underneath: a measurement confirms the geometry you suspect, and says
nothing at all about geometry you never put in the probe.

Two rules follow from the second instance. **A check label is a claim that something checks it**,
so a rule marked `auto` or `render` with no implementation is a defect in the ruleset, not a
to-do. And **a gate must not depend on anything a design rule is allowed to delete** — drive an
artifact through the parts that exist because it has to work, not through the parts that exist
because they currently look that way.

### L-37 — An answer that contradicts a rule is a rule amendment, not a permission

An owner answers an open question. The answer is authoritative, it settles the task, and it is
written down where the task expects it — struck question, date, rationale. **What nothing checks is
whether the answer just licensed something a `hard` rule forbids.** The task then reads as decided,
the rule keeps saying the opposite, and the next thing built from the ruleset is either
non-conformant or quietly ignores the rule.

The case: seventeen open questions answered in one pass, 2026-08-07. Two of them landed on rules,
and **only one of the two was visible as a rule question when it was asked.**

- **DS-131, and it was already a task.** *Per-stage jump targets, not one per slide* contradicted
  DS-131 as it then read — *"clickable dots"*.
  [T-033](../tasks/T-033-reconcile-ds-131-with-the-chrome-budget.md) existed precisely because
  [T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) had obeyed
  DS-216 and DS-217 and made the reference deck depart from DS-131. The conflict was on the board.
  **Closed 2026-08-08**: DS-131 moved, as the side that named a widget where the others named a
  requirement, and now reads *a bounded set of named targets*.
- **DS-140, and it was on nobody's board.** *3D is wanted for functional visualisation — a diagram
  wobbling slightly so peaks read as peaks* is **continuous motion**, against a rule that closes the
  motion vocabulary at exactly four named motions, `hard` and `auto`-checked. Neither the question
  nor the answer mentioned DS-140. It surfaced only because the answer was being written next to
  the same task's scope line requiring a motion rest state.

This is **not L-28.** There, two rules written at different altitudes conflict, and the fix is a
scope clause that costs neither of them anything. Here **one side is not a rule** — it is a decision
that outranks the ruleset, so the ruleset is what moves. The risk runs the opposite way too: L-28
warns against arbitrating a conflict that isn't real; this warns against **not** arbitrating at all
— taking the answer as a one-off licence and leaving the rule for whoever builds against it to
discover, which is **L-33**'s mechanism one step earlier. The third instance is already in the
repository: T-025 made the motion control **DS-218** rather than a note, because *"a floor that
reaches the builder as a criterion rather than an instruction produces non-conformant decks by
default"*.

**How to apply.** Before writing *answered*, read the answer against the rules it touches — the
ruleset is addressable by `DS-nnn` and the `Check` column says which rules a machine enforces, so an
answer contradicting an `auto` rule will **fail a gate**, not merely disagree with a document. Name
the rule in the answer and say **which side moves**: if the answer wins, that is a rule amendment
with an owner and a task, raised before the task closes; if the rule wins, the answer needs putting
again with the rule in front of it. What must not happen is the third option, which is the default
one — recording the answer, not naming the rule, and leaving the precedence to be inferred.

### L-38 — A sweep is blind in the direction its brief did not name

A measurement inherits the shape of the question that commissioned it. When the question names a
direction — *past twelve slides*, *above the threshold*, *under load* — the instrument gets built
to run that way, every value it returns is on that side, and **the other side produces no values
and no complaint**. The rule reads as measured, because it was: thoroughly, in one direction. This
is [L-36](#l-36--a-stated-tolerance-is-a-claim-about-the-instrument-not-only-about-the-artifact)'s
mechanism on a different axis — there a *category* was never sampled, here it is a *range*.

The case: [T-034](../tasks/T-034-a-contents-page-for-the-printed-deck.md)'s printed contents page.
The spec required the single-page bound to be *measured on a deck longer than twelve slides*, so the
instrument swept 8, 12, 16, 20, 24, 28, 32, 40 and returned a bound of 16 and a hard limit of 24 —
correct, self-tested, in real offline Chrome, and confirmed twice. The owner then asked to see
**seven** slides, a count nothing had ever asked for, and the page was worse there than at any
measured count: grid rows divide the page height regardless of content, so each box was stretched to
377 du around about 150 du of content and printed as a grid of mostly-empty rectangles. The
supported range had been swept from the middle outward in one direction only.

The same task produced a second instance, different mechanism, same result. At 17 slides the tool
reported a description as `0.19 lines`, and the write-up rendered that as *"description gone"*. The
number was right and the phrase was not: *gone* would have been acceptable, whereas 0.19 of a line
on paper is a few units of clipped letterform under the title, which a reader takes for a rendering
fault. **A measurement summarised into a word loses the failure mode the number was carrying** — and
the summary is what everything downstream then reasons from.

**How to apply.** Sweep both ends of a supported range, including the counts nobody asked about;
the cheap end is usually the untested one. When a brief names a direction, write down what that
leaves unmeasured **before** building the instrument, because afterwards its silence is
indistinguishable from a pass. And when a number becomes prose, keep the number beside it: `0.19
lines` and *"gone"* are different claims, and only one of them can be checked against the page.

### L-39 — Cite the content, not the address

A review verdict that names *where* the output is, instead of *what it says*, can record a
deliverable as met that was never produced — and nothing downstream can tell.

[T-014](../tasks/T-014-synthesise-research-into-the-design-system-reference.md) promised the hard
rules pulled into one list of testable conditions and closed recording it **met**, on the evidence
*"§11 — 26 numbered conditions, two of them not machine-checkable"*.
[`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) has ended at **§9 in every one of its 13 commits**, created
that way by that task's own closing commit. The section was never written. **Four tasks then
consumed it for two months** — T-004 assigned itself two of its conditions,
[T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md) elaborated the list from 26 to 33
across two log rows, and [T-030](../tasks/T-030-audit-the-backlog-edges-and-propose-a-build-order.md)
ordered part of the build on it. Only
[T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md) noticed, and it worked around
the gap by hand rather than reporting it.

Two things kept it alive. A **section number is not a pointer `check` can follow** — it validates
markdown links and repo-relative paths, so `§11` in prose is invisible to it, and a reference to a
section that never existed reads exactly like one to a section that does. And the missing thing was
a **second, parallel structure**: the same rules, restated in a different order. Nothing broke when
it was absent, because everything else worked off the rules themselves.

**How to apply.** Write a verdict so it would be false if the output were missing: quote the line,
give the rule ID, state the count you counted — *"§11 exists"* survives the section not existing,
*"26 conditions, of which DS-033 and DS-061 are unreachable"* does not. Prefer carrying a fact
**per item** over restating it in a parallel list; the list is what goes stale silently, and it is
what this failure needed in order to happen. When a document reference cannot be machine-checked,
treat it as a claim to verify rather than a link — and check it against the file, not against what
another document says about the file.

### L-41 — A check with no rule is as wrong as a rule with no check, and much harder to see

**L-36** is the familiar direction: a rule labelled *a machine decides this* that no machine decides.
The inverse runs the other way and hides better. A check exists, it measures something real, it
passes — and the rule ID beside it names something the check does not test. Nothing is missing, so
nothing looks wrong. The gate reports a rule as covered, the coverage account counts it, and the
first thing to actually test that rule is the defect that ships.

The case: [T-037](../tasks/T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) filled in a
`Reach` column, which forced a row-by-row comparison of what the ruleset says a rule is against what
`audit.py` claims about it, and **found two `judge` rules being gated mechanically** — the ruleset's
own `Check` value saying no program should be deciding them.
[T-038](../tasks/T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) then swept all
forty verdicts and found **seven of them wrong** in four shapes — five citing a rule they do not
test, six rule IDs between them, and two more whose assertion could not be false. **Not one had ever
failed**, and the deck was conformant throughout: nothing in a green run distinguishes a check that
holds from a check that cannot fire.

- **A precondition standing in for its rule.** DS-161 — *closed, the slide still makes its point* —
  was gated by counting panels open at load. Whether the panels are shut is the condition under which
  the question is asked; it is not the question, and no count answers a judgement.
- **Evidence of a rule reported as the rule.** DS-137 requires that a **defined precedence rule**
  exist; the gate measured *at most one panel open*, which is one such rule for one interaction pair.
  The particular was being asserted as the general.
- **IDs cited by a verdict that never touched them.** One row read `DS-080/081/082` and tested only
  the slide count, so two rules were reported as covered by a check that could not fail for them. A
  second measured the **default** state and cited DS-143, which is a rule about what survives
  `prefers-reduced-motion`.
- **An assertion that could not be false.** DS-076 — *position preserved in both directions* — passed
  if any slide was current after returning from the reflow view, which every deck satisfies. Its
  neighbour DS-130 measured a slide that has no disclosure control, reported `null`, and passed.

**How to apply.** Read the check against the rule text, in that direction, and ask **can a
conforming artifact fail this, and can a violating one pass it** — one yes means the citation is
wrong even though the measurement may be worth keeping. Where a check measures a proxy, either the
proxy earns its own ID or the verdict stops naming the rule; the test for the ID is whether the
system already leans on the fact, because **inventing a rule so a check has somewhere to live is
backwards, and writing down one the system already depends on is not**. And when a verdict prints a
null or an empty count, make it fail: *nothing measured* must never render as `pass` (**L-36**).

### L-42 — A check reads a model of the artifact, and the model is where it goes blind

Every check simplifies what it reads: CSS becomes a regex, prose becomes tokens, a file becomes a
string. **The simplification is invisible while the check passes**, and it is almost always where
the missing defect lives — because the thing that made the check easy to write is the same thing
that made it unable to see.

Two instances arrived within an hour of each other, both from
[T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md)'s new variant suite, and both
checks had been reporting `pass` on the reference deck before the suite existed:

- **The indirection the design system requires.** DS-141 caps animation durations at 500 ms, and the
  check scanned `animation:` and `transition:` declarations for a number. It found none over the
  cap, and there was none to find: **DS-033 requires every value inside the stage to come from a
  token**, so durations are written `transition: transform var(--slide-dur)` and the number lives
  one hop away. Seeding `--slide-dur:900ms` broke the rule and the check read `var(--slide-dur)` and
  passed. *The system's own rule about where values live is what defeated the check.*
- **The tokeniser that met real content.** DS-092 caps a sentence at 20 words, and the splitter cut
  on `[.!?]`. A deck about money is full of `$5.6M`, so a 28-word sentence split into `Spend the
  whole of the $5`, a middle, and `.5M for bike-share…` — three short sentences, none over the cap.
  The rule found two genuine violations elsewhere and looked like it worked.

**How to apply.** For every check, write down **the model it reads** — *declarations matching this
pattern*, *text split on these characters* — and then ask what the real artifact does that the model
does not represent. Two questions find most of it: **what indirection does the system require here**
(tokens, variables, generated content, a manifest read at run time), and **what does real content
contain that the tokeniser will mistake** (decimals, abbreviations, currency, embedded payloads —
an earlier version of the same check reported six animations over the cap, all of them fragments of
a base64 typeface). The general form of the fix is to make the check resolve what the artifact
resolves: expand the variables, split the way the content is written. And **seed the defect**, since
that is what turned both of these from green rows into found bugs — this is
[L-36](#l-36--a-stated-tolerance-is-a-claim-about-the-instrument-not-only-about-the-artifact)
arriving from a third direction, and it is why a check ships with a variant that breaks it.

### L-43 — A completeness device built for one class makes the classes it does not cover harder to see

**L-36** and **L-41** are about a single rule going unwatched. This is what happens *after* you fix
that properly: build a device that guarantees coverage over one class of rule, and the guarantee
starts covering for everything outside the class.

The case. [T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md) closed the mechanical
half completely and correctly — every rule the ruleset puts in a gate's jurisdiction now ends each
run **checked**, **excused in writing** or **failing**, and a rule in none of them fails the run the
same afternoon. That device is sound. It is also scoped to `auto` and `render`, and
`EVALUATION.md` §1 declares **114 `hard`** rules to be gates. **Twenty-five of them were `judge`**,
so nothing produced a verdict for any of them, eleven were named nowhere in the document at all, and
a `hard` `judge` rule could be added with nothing anywhere noticing it was unowned — for months,
across an audit and four reviews ([T-042](../tasks/T-042-audit-the-whole-repository-against-itself.md),
F-3).

**The mechanism is the reassurance, not the omission.** Before the device, *"is every rule covered?"*
was an open question a reader might ask. After it, the run answers *"112 owned, 0 silent"* — true,
complete about its own jurisdiction, and read as an answer about the ruleset. The green run is what
stops the question being asked again. **A partial guarantee is more dangerous than none**, because
none leaves the doubt intact.

**How to apply.** When a completeness device is built, **state its jurisdiction and the complement in
the same breath**, and give the complement an owner before the device ships — even if the owner is
*"nobody yet, and here is the task"*. Then make the arithmetic cover the whole population rather than
the covered part: `ruleset.py --gates` partitions all 114 `hard` rules across their gates and fails
when the parts do not sum, which is the assertion that would have caught this on day one. The test to
apply to any coverage claim: **what is the denominator, and who chose it?**

### L-44 — A check whose subject is absent reports conformance, and every idiom in the language helps it

**L-36** is a rule with no check. This is a rule *with* a check, that ran, found nothing to look at,
and said `pass`. It is harder to see, because the row is there and it is green.

The case, and the reason it is a lesson rather than a bug. The same fault was found and fixed
**three times, one instance at a time**, and none of the three generalised:

| Found | Rule | The expression | What it meant |
| :--- | :--- | :--- | :--- |
| [T-038](../tasks/T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) | DS-130 | `is not False` on a null | measured on a slide with no disclosure control |
| [T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md) | DS-087 | — | excused *in writing*, for exactly this reason, and the reason stayed local to it |
| [T-051](../tasks/T-051-a-check-with-no-subject-must-not-report-a-pass.md) | DS-140 | `None != "none"` | the deck's only dashed flow was gone |

**The mechanism is that vacuity is the default in every idiom the check would naturally use.**
`not []`, `None != "none"`, `None is not False`, `None == None`, `data.get(k, 0) <= 12`,
`set().issubset(x)` — every one of them returns the passing answer when there is nothing there. So
the author writes the obvious expression, the row is correct on the deck in front of them, and the
defect appears only on a deck missing the thing. **You cannot find this by reading the predicate**;
it reads correctly. It was found, all three times, by a deck built to be missing something.

**Absence is not uniformly a defect, and a gate that treats it that way fails legitimate work.**
The rule's own quantifier decides:

- **prohibition** — *never X*, *at most n X*. The subject is the artefact, which exists. Zero X is a
  genuine pass, and treating it as undecided would make every clean deck red.
- **conditional** — *if X then Y*. No X, no obligation. Vacuous truth is the correct answer here.
- **requirement** — *every X is Y*. **This is the one.** No X and the rule is not decided, which is
  neither a pass nor a failure, and reporting either is a claim the check did not earn.

**A denominator guards only the quantity it counts** — the trap that caught the one place that had
already learned the lesson. `contrast.py` carries a pair count for precisely this reason and cites
L-36 for it, and DS-027 (*both themes readable*) still passed a deck with no dark theme: the token
reader fell back to a copy of the light theme, so there were seventeen pairs to count and one theme
to read them from. The guard counted pairs; the absent subject was a **theme**.

**How to apply.**

1. **Make the third state real.** A verdict is `True`, `False`, or **undecided**, and undecided is
   routed where a rule with no check goes — silent, and the run fails. Do not give it a forgiving
   bucket of its own: coverage then drains into it artefact by artefact while the gate reports
   green, which is L-36 rebuilt one storey up.
2. **Fix it once, with a forcing function, not per row.** Drive every check against an input in
   which *nothing was found*, and require each row that still passes to be declared in writing as a
   prohibition or a conditional. The declaration is cheap, and it is what makes the next instance
   cost a sentence instead of an audit. Where a row is saved by a sibling that fails instead,
   **name the sibling and test the claim** — an untested "something else catches this" is the
   comment three previous fixes left behind.
3. **Ask what the subject is, then ask what would be true if there were none of it.** Not *is the
   predicate right* — it is.

### L-45 — A threshold measured on one artefact encodes that artefact, and only a second one shows it

**A number can be measured, documented, given headroom, and still be a fact about the sample.** It
does not read as a guess — it reads as evidence, which is why it survives review.

Four thresholds in this repository were fixed at the value one deck happened to have. Three were
found by *reading*, once the question was asked; **the fourth needed a second artefact to exist.**

| Rule | The number | How it was wrong |
| :--- | :--- | :--- |
| DS-034 | line height **1.55**, checked to ±0.01 | one theme's value stated as the rule |
| DS-140 | motions at **340 / 380 / 420 / 300 ms, 1.2 s, 4.5 s** | the vocabulary's *names* are the rule; the milliseconds were one theme's |
| DS-141 | a long duration admitted at **exactly 1.2 or 4.5 s** | the same pin, one layer down, in the check |
| **DS-063** | a text run's rect within **2 design units** | **measured over 384 values, worst case 1.17, headroom to 2.0 — and still wrong** |

DS-063 is the instructive one. The measurement was real and the headroom was honest. What nobody
could see was the **shape**: a device-pixel rounding effect expressed in design units silently
carries the scale factor of the deck it was measured on. A second theme with a tighter type scale
fits more glyphs on a line, every one of them rounds, and a deck that breaks nothing reaches 2.23.
Restated as **2 device pixels at the smaller rendering** the bound has a mechanism behind it — a
whole-rect comparison folds two independent roundings, the edge and the extent — and it stops being
about any deck at all.

**A fifth turned up the next day, and it was not a number.** DS-141 read *max 500 ms,
**ease-in-out***, and the keyword is one theme's curve stated as the ruleset's — the same defect as
the line height and the durations, on the easing axis. It hid longer than the others because a
keyword does not look like a measurement: nobody audits a word for being a sample. **The class is
wider than thresholds** — it is any value a rule states that the artefact was free to choose, and a
check enforcing it will read as principled either way.

**The general shape: a check written against one instance cannot distinguish a property of the
artefact from a property of the class.** Both look identical from inside the sample, and the more
carefully the number was measured, the more convincing the wrong one is.

**How to apply.**

1. **Before fixing a number, ask what it is a number *of*.** If the effect is a rounding, a device
   pixel or a viewport, say so in those units. A unit conversion is not cosmetic: it decides whether
   the threshold travels.
2. **Where a rule names a value the artefact chooses, band it and name the instance separately.**
   *Line height 1.40–1.70, this theme's being 1.55* is a rule; *1.55* is a reading.
3. **Build the second artefact earlier than feels necessary.** It is the only instrument that finds
   this class, and it found one here that four passes of reading did not — cheaply, in an afternoon,
   because everything else was already gated.

### L-46 — A contract is kept true by the check that runs from the artefact back to it

**Two directions, and only one of them stops the document decaying.** A contract check normally
asks *does the artefact satisfy the document* — every part the contract names is where it says.
That direction catches a broken deck and cannot catch a stale contract, because a part nobody
wrote a row for is a part the check never looks for. Six months on, the document describes the
artefact as it was the day it was written and every check built on it still passes.

The other direction asks *does the document cover the artefact*, and the trick is to run it from
whatever creates the need for a row:

| Contract | Runs from | The row it forces |
| :--- | :--- | :--- |
| [`THEME-CONTRACT.md`](THEME-CONTRACT.md) | every `--token` the deck declares | *declared and the contract does not name it* |
| [`COMPONENT-CONTRACT.md`](COMPONENT-CONTRACT.md) | every class the shared style block styles | *styled and the contract does not name it* |

Both work because the thing they scan is **what a person edits when they add one**. A component is
added by writing a CSS rule, which is exactly the moment nobody remembers a contract document
exists — so the scan fires on the same keystroke that created the gap.

**The corollary, and it is the sharper half: *declared and unused* has to be checked backwards or
it is not a claim at all.** Five classes in the reference deck are styled and used nowhere. Marking
them *unused* in prose asserts nothing — nothing fails if it stops being true. Marking them
`vocabulary` and **failing the run when one acquires an instance** makes it a claim, and the count
of them a number a reader can watch. This deck already paid for the other way: a
`.ribbon button::before` rule survived the component it styled by a whole task, because **a rule
that matches nothing looks exactly like a rule that passed.**

**How to apply.** For any document that enumerates parts of an artefact — a contract, an inventory,
a registry, a rule index — write the check that walks the artefact and reports what has no entry,
before writing the one that walks the entries. And where an entry claims something is absent, make
its presence the failure.

---

### L-47 — A judgement rule needs the artefact to carry the author's claim, or every review re-derives it

**A rule nothing can check is not a rule nothing can record.** When a rule is `judge`, the temptation
is to write it in the ruleset and stop, because there is no check to build. What that leaves is a
reviewer opening the artefact and reconstructing, from scratch and for every instance, what the
author was trying to do — which is the expensive half of reviewing and the half most likely to be
skipped.

The fix is to make the artefact say it. Two rules here do:

| Rule | The claim, written down | What the gate can still verify |
| :--- | :--- | :--- |
| DS-217 | `data-scale` on the ruler — *this is a regular repeating scale* | the claim itself: uniform mark, uniform pitch, no per-item label at rest |
| DS-230 | `data-disc` on a disclosure — *this panel is a `derivation`* | **closure only** — one of four, never the right one of four |

**The two are not the same strength and the difference has to be stated rather than blurred.** A
declared attribute that nothing verifies is self-reporting, and the answer is not to drop it — it is
to say on the rule's own row how far the gate reaches, so nobody reads a green run as the claim
having been checked. What the declaration buys even when unverifiable is the review question:
*is this claim true* is a far sharper thing to ask than *is this any good*, and it is answerable by
someone who was not there.

**How to apply.** When a rule comes out `judge`, ask what the author decided and whether the
artefact can record the decision — an attribute, a class, a named region. Then say explicitly which
part of it the gate decides. A judgement with a written-down claim is reviewable; a judgement with
nothing written down is re-derived every time, by everyone.

---

### L-48 — Read the claim strictly and its support generously, and which way to err depends on who reads the verdict

**Over-reporting is the safe direction only when a person is the consumer.**
[`content.py`](../tools/deck/content.py) says so in its own docstring, and it is right for the
figure ledger: a source phrased differently from the slide reads as unsourced, someone looks, and
nothing was lost. **A gate row is the opposite case.** It blocks a build, so a false positive is a
conforming deck that cannot ship, and the person who meets it has no reason to think the instrument
is wrong rather than the deck.

DS-231 is where this was learned. The rule — *a bottom line never cites a figure that lives only
behind the click* — has two sides, and the first instrument read both strictly. It failed slide 3
of the reference deck, whose stat figure `11` and unit `minutes, average wait` are two separate
elements, so `11 minutes` is never one figure on that face. The deck was right. The fix is
asymmetry: **the citation is matched strictly, because a citation is the claim; the support is
matched loosely, because support only has to be visible.**

**How to apply.** Before writing a check that compares two halves of an artefact, decide which half
carries the claim and which merely has to exist, and set the strictness per side rather than per
check. Then ask who reads the verdict: a person reviewing can absorb a false positive, and a gate
cannot.

---

### L-49 — Cut the shared part out of a working artefact; do not write a description of it

`shell/` is the reference deck with ten regions replaced by `{{SLOT}}` markers, and **filling them
back reproduces that deck byte for byte.** The round trip is the whole point. A shell written by
hand to describe the deck would be a second opinion about it, and the two would diverge the first
time either changed, silently, because nothing compares an opinion to its subject. A shell that is
*literally the artefact minus its content* can be compared, so `shell.py check` holds any deck to it
and reports the first differing line.

**The cut also finds content the artefact was hiding.** Splitting on a boundary somebody has to
defend forces the question *is this per-deck or not?* on every line. Three of the reference deck's
per-deck facts — its name, the stages of its argument, the icon marking each — had been sitting in
the middle of 560 lines of invariant script for four tasks, and no reading had noticed. The split
noticed immediately, because they would not go on either side.

**How to apply.** When something must exist once and be instantiated many times, derive it from a
working instance by subtraction and keep the subtraction reversible. Assert the round trip in the
self-test: it is one line, and it is the only evidence that the shared copy is the thing rather than
a report about it.

---

### L-50 — A reference can be created by code, so a scan that reads only markup deletes it

DS-113 wants a sprite holding only the icons a deck uses, which is a fact about the file and so a
good thing to derive rather than maintain. The first derivation read `<use href="#i-x">` out of the
markup and rewrote the sprite to match — and **deleted four of the reference deck's nine icons**,
which are named in a script array and put into the DOM at runtime. `COMPONENT-CONTRACT.md` §2.1
already names that source; the tool simply did not honour it. The deck's own gate had been reading
the *rendered* DOM for the same rule all along, which is why nothing had ever disagreed before.

The over-correction is as bad. A loosened pattern matching a bare `i-name` finds `--ui-line` five
times in the same file, so the fix is two exact patterns — the attribute form and the quoted form —
and not one permissive one.

**How to apply.** Before deriving *what is used* from a source scan, ask what else creates a
reference: a script, a template, a print-only rule. Where a contract already labels those sources,
the scan has to cover every label or it is not deciding the rule. And prefer several exact patterns
to one loose one, because the loose one fails in the direction that deletes things.

---

### L-51 — When no threshold separates the two cases, the check is a reading list and not a gate

`FIG-4` was planned as a gate row: two sources answering one question with two numbers. Three
thresholds were tried against two real pairs — *busiest single day* at 31,900 in a table against
30,400 in a summary, which **is** a contradiction, and *mean round utilisation, off-peak* at 71%
against *peak* at 88%, which is **not**. Set equality of the labels misses the first, because a
restatement rephrases. Jaccard at 0.6 misses it, and so does 0.5. **Every threshold loose enough to
catch the true pair catches the false one**, because what separates them is that *peak* and
*off-peak* are contrastive — semantics, not counting.

That is a result about the check, not a tuning problem, and the right response is to change what the
check *is*: it emits candidates a person confirms, and it fails nothing. The two directions of error
are not symmetric (**L-48**) — a gate row's false positive blocks a conforming build, a reading
list's costs a glance.

**How to apply.** When a comparator's two cases are separated by meaning rather than by a measurable
quantity, stop looking for the threshold. Decide who consumes the output, and let that decide
whether it can fail a run. Record the measured false-positive rate beside the constant, because the
next person will otherwise read a clean corpus producing candidates as a malfunction.

### L-53 — Optional is not untyped, and a presence test reads like a validator

`check_scaffold.py` printed **`OK - manifest valid`** for the manifest that shipped `v0.1.0`. The
installer refused it: `author: Invalid input: expected object, received string`. The tool's whole
test of that field was

```python
for field in ("version", "description", "author", "license"):
    if field not in data:
        notes.append("no `%s` in the manifest - optional ..." % field)
```

which asks whether the key is there and never what it holds. Four fields could carry any value of any
shape and the run stayed green. The schema says only `name` is *required*; the tool read that as the
other fields being unconstrained, and those are different claims.

**A working example is not a control.** Another installed plugin was cited as evidence the shape was
fine. It installs because it **omits `author` entirely**, which is also valid, so it could not have
distinguished the two cases in either direction.

The cost was not the wrong line. It was that `README.md` ends its install section with this command as
the proof the package is sound, and the release notes said the install route was checked. **The claim
was false rather than optimistic**, and it took an outside report to find it, which is the failure
mode **L-05** describes arriving from outside instead of from the gate.

**How to apply.** Where an external consumer validates an artefact this repository emits, encode
*that* consumer's contract, not a reading of it: field types, not field presence. Optional fields get
type-checked when present. And when a check is added, add the fixture that fails without it first
(**L-04**) - three fixtures here reported `got: nothing` before the fix, which is what a blind spot
looks like from the inside.

### L-52 — A figure pasted from a run goes stale on the day the thing it measures grows, and nothing says so

`README.md` states its evidence as pasted tool output, which is the right decision (**L-03**) and was
never in doubt. What was in doubt is nothing, because nobody checked: six of its figures were wrong
before anyone touched them. Build mode and critique mode added rules to the ruleset on 2026-08-09,
and **161 rows became 163, 115 hard rules became 117, and 24 judge rules became 25** the same
afternoon. Every gate in the repository stayed green throughout, correctly — no gate owns a number
printed in prose in a document that is not a deck.

The sharpest symptom is that the README had already begun **contradicting itself**: its prose said
the judgement half is 25 rules while a fenced block three sections above printed 24. Two copies of
one derived fact, updated at different times, which is **L-13** with a delay fuse.

A stale figure and a wrong figure are the same thing to a reader, and this is the front door.

**How to apply.** A document that pastes derived figures owes a re-derivation step to whoever edits
it next, written down in the document's own rule rather than remembered. `PUBLISHING.md` §6 is that
step here: every fenced block names the command that produces it, and the obligation is to run them
rather than to read the diff. **The diff cannot see this class of defect at all** — the bytes did
not change, the world did.

### L-54 — A fixture only watches the direction it was asked about, and its model of the subject is part of it

**L-44** ended with *fix it once, with a forcing function, not per row*. The forcing function was
built, it worked, and **the same defect was found twice more afterwards** — the fifth and sixth
instances of one fault. This is what the forcing function did not cover, and neither gap is specific
to gates.

**The fixture asked one direction of a two-directional question.** It required every row that
*passed* on an absent subject to be declared in writing. Nothing asked which rows *failed* on one.
So [T-051](../tasks/T-051-a-check-with-no-subject-must-not-report-a-pass.md) converted three rows and
left four beside them in the same list;
[T-065](../tasks/T-065-four-rules-still-fail-a-deck-for-not-having-their-subject.md) converted those
four and left three; and the deck that had reported the original defect was still being failed by
DS-160 after the fix shipped. **The rows the fixture watched were correct the whole time.** A check
that answers *did anything pass wrongly?* is silent on *did anything fail wrongly?*, and silence
reads exactly like a clean run.

**The fixture's model of what it measures is itself unexamined.** The nothing-was-found measurement
was a hand-kept tuple of eight key names, against a probe emitting more than forty. A row reading
anything outside it got a `.get()` default instead — and **a default that fires is indistinguishable
from a measurement**. DS-217 spent the whole period on the failing list for that reason alone,
against a probe that would have measured zero and passed. The instrument was wrong about the
instrument, and every run agreed with it.

**The two compound.** Because the model was wrong, the first honest attempt to classify the failing
rows would have written DS-217's false failure into a declared table, *with a reason*, and called it
a decision. A bad model does not merely hide defects; it manufactures ones to explain.

**How to apply.**

1. **When you build a forcing function, write down the question it answers — then write the
   negation and check that too.** "Which rows pass on an absent subject" and "which rows fail on
   one" are one question in a person's head and two in code. The cost of the second is one more
   table; the cost of skipping it was three releases.
2. **Derive the fixture's inputs from the thing being modelled, or make the fixture report when it
   cannot.** Here that is recording what each row *reads* and failing on a key the model has never
   heard of. A hand-kept list of what the world contains is a copy of a fact, and it goes stale in
   the direction that produces false confidence (**L-13**, **L-52**).
3. **Enumerate the things under test from the code, never from a list.** An entire verdict producer
   sat outside this fixture from the day it was written, because the fixture named its inputs and
   **a name nobody adds is a name nobody misses**.
4. **A hand-run sweep is not a gate**, and reporting one as a completed criterion is how a false
   claim ships. The sweep that closed T-065's criterion cut each row at the first `),`, read
   truncated expressions, and found one candidate where there were five. Nothing recorded that,
   because a script that ran once leaves nothing behind to disagree with.

### L-55 — Seeding a defect proves the exit status; only the message proves the assertion

**L-04** and **L-36** say put the defect back and confirm the checker fails. Both were followed here,
both passed, and one of the two assertions being confirmed was **unreachable code**.

The case. [T-059](../tasks/T-059-theme-swap-overwrites-its-input-when-o-is-omitted.md) gave
`theme.py swap` a destination function that *raises* when the output would be the input deck, and a
self-test that checked the ordinary default by comparing the function's **return value** against the
deck. Restoring the old destructive default makes that call raise, so the comparison below it can
never execute. Seeding the defect still exited 1 — as a bare traceback, from the uncaught exception,
several frames away from anything that names the rule. **The seeded run and a correct seeded run are
indistinguishable if you only look at the exit status**, and the exit status is what a self-test
harness, a CI job and a person in a hurry all look at.

The general shape: any assertion placed *after* a call that fails by raising is dead, and dead
assertions are invisible precisely when the thing they assert breaks. The seeding discipline finds
the missing check; it does not find the check that cannot run.

**How to apply.**

1. **Read the seeded run's output, not its exit code.** The message must name the rule. A traceback,
   an assertion with no text, or a failure from a different layer means the assertion you thought
   you were testing did not fire — something else did, and it happened to fail too.
2. **When a function signals by raising, assert it with `try`/`except`, not with a comparison.** The
   comparison reads like a check and compiles like one. Ask which line prints when it breaks; if you
   cannot name it, it is not a check.
3. **Seed each guarantee separately.** Two defects put back one at a time gave two distinct
   messages, which is what showed one of them was arriving from the wrong place. Seeding both at
   once, or seeding only the one that seems riskier, would have shown a single failing run and
   proved nothing about which guard produced it.

---

## Tooling

### L-56 — A reading tool's rendering is not the file's bytes, and a one-character defect needs two readers

Found on 2026-08-10 during [T-069](../tasks/T-069-extend-the-provenance-mark-to-multiple-sources.md).
A search tool's context output showed a CSS comment opening `\*` instead of `/*` — which would be a
real and nasty defect, because `\*` is a valid CSS escape, so the parser reads the comment text as a
selector and **swallows the rule beneath it**, leaving a declaration that matches nothing. The
mechanism was worked out, the consequence traced to a live rule, and a fix task raised.

**The file was correct.** The backslash was the tool's own escaping in its context display, not a
byte in the file. Reading the same line with a second tool — and with `git show HEAD:` — printed
`/*` both times, and the task was deleted.

The trap is specific and worth naming: a plausible mechanism makes a rendering artifact **more**
convincing, not less. The reasoning about `\*` was correct CSS; it was just about a character that
was not there. Nothing in the tool's output says *this is escaped*, and the defect it appeared to
show was exactly the kind this project has found before (**L-15** is the same shape one instrument
along — a screenshot is a poor instrument for a two-pixel judgement).

**How to apply.**

1. **Before writing down a defect whose evidence is one character, read it with a second tool.**
   `Select-String`, `git show HEAD:<path>`, `Format-Hex` — anything with different escaping.
2. **Prefer the version-control reader for "was this always wrong?"** `git show` answers the
   provenance question and the byte question in one command.
3. **This does not apply to defects of substance** — a missing row, a wrong number, an absent
   attribute. It applies where the claim rests on punctuation a tool might have escaped.

### L-57 — A derivation is bounded by what it reads, and from inside it that boundary is invisible

Found on 2026-08-10 during [T-075](../tasks/T-075-ds-064-probes-for-the-reference-decks-own-class-names.md),
and it is the seventh instance of the fault **L-44** and **L-54** already generalised — which is the
point. [T-066](../tasks/T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md) replaced a
hand-kept list of the things a fixture had to check with one **derived from the code**, on the correct
reasoning that a name nobody adds is a name nobody misses. The derivation read `globals()`.

`globals()` is one module. **Six of the eight verdict producers in the package were in other files**,
every one of them consumed by the same gate, none of them ever run against a measurement in which
nothing was found. The fixture was complete over its scope and reported so on every run, and a
derivation that is complete over its scope reads *exactly* like one that is complete. An outside
project found the first row this let through; nothing here could have found any of them.

The seventh instance also cost the least to find. Moving the boundary from `globals()` to the
directory took one function, and the first run named four modules nobody had been looking at — with
nine more rows reporting conformance about subjects that were not there.

**How to apply.**

1. **When you replace a list with a derivation, write down what the derivation can see.** The
   question is not *is this complete?* but *complete over what?* — scope is the part that does not
   announce itself.
2. **Prefer the widest cheap source.** Reading the directory finds a producer in a module nothing
   imports; reading `globals()` cannot, and reading the import graph would have missed the same
   four.
3. **A fix that "cannot be forgotten" can still be forgotten one scope out.** Each instance of this
   family was fixed correctly and the next one stayed invisible, because the fix and the blind spot
   were the same size.

### L-58 — A command a document tells someone to run is a claim, and it was the only kind nothing checked

Found on 2026-08-10 during [T-074](../tasks/T-074-the-documented-render-command-does-not-exist.md),
reported by an adopting project. This repository checks a great deal about its documents: that every
path resolves, that every `§n` reference exists, that every pasted figure still matches the command
that produced it. **The one thing it never checked was the commands themselves** — and those are the
only lines in a document meant to be executed verbatim.

`build.md` told every build to run `render.py shots <slug>.html --out <dir>`. There was no `--out`;
the third argument was parsed as a slide list, so the flag reached `int()` and the command died. The
step it died at is the one that closes the *visual* gate, so a build following the documentation hit
a traceback at the moment it was supposed to start looking, and the cheap wrong response — skip the
render, trust the checks that passed — is the one most likely to be taken. Twelve other documented
invocations were correct, by luck rather than by construction.

**The instrument-shaped trap, found while building the check.** The first version searched the
tool's source for the flag between quotes. Its own fixture went green against a `render.py` with
`--out` deliberately removed — because the flag was still in the file, in a *comment* quoting the
traceback. A mention is not an implementation, and matching whole string literals with `tokenize`,
comments and docstrings excluded, is what makes the answer *the parser compares against this string*
rather than *this string occurs somewhere*. That is **L-36** arriving in a new file, as it does
about once a month here.

**How to apply.**

1. **Every command in a document a tool can parse is a claim the gate should decide.** Not the whole
   line — a tool exists, a subcommand exists, a flag exists is most of the value and costs a static
   read.
2. **Say what the check does not decide.** Positional arity, flag order, and whether a flag is valid
   for a particular subcommand are beyond a static read, and executing for real would launch a
   browser. Naming the limit is what keeps the green run honest.
3. **Documentation and tool disagree silently in both directions.** `render.py`'s own docstring had
   the working form the whole time, one file away from the prose that did not.

### L-59 — A tool swap takes behaviour and the paragraph describing it, and neither leaves a mark

Found 2026-08-10 by a status review nobody had scheduled, in
[T-079](../tasks/T-079-the-boards-dependency-columns-list-closed-tasks.md).
[T-062](../tasks/T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) retired
`task.py` for taskmd on 2026-08-09. Two things left with it and nothing said so:

- **A behaviour.** `task.py` filtered closed tasks out of both dependency columns — that was
  [T-031](../tasks/T-031-stop-the-index-blocks-column-listing-closed-tasks.md)'s whole subject.
  taskmd's `index` does not, so three open rows read as blocked while `taskmd list --open` correctly
  ranked them free. The board and the tool disagreed in public for a day.
- **A written rule.** `TASK-WORKFLOW.md` asserted the filtered behaviour **as current fact**, in the
  present tense. It was true when written and false the moment the tool changed, and it still read
  perfectly — which is why nobody caught it. A sentence does not look stale.

**The migration was validated, and the validation could not have seen either.** T-062 compared what
the two tools *did* — seeded defects, both tools run, coverage matched. Neither loss was a command
that stopped existing; one was a difference in the shape of a generated file and the other was a
paragraph. This is **L-57** at project scale: a comparison is bounded by what it reads.

**How to apply.**

1. **Diff the artifacts, not the command list.** When a tool is replaced, regenerate what it
   generates and compare the files. A generated file is the contract; the command surface is how you
   reach it.
2. **Grep the docs for present-tense claims about the tool you just replaced.** Any sentence saying
   the system *does* something is a claim with no owner unless something compares it to output. This
   project checks paths, `§n` references, figures and now commands (**L-58**) — a prose assertion
   about behaviour is the class none of those reach.
3. **Expect the finder to be a review, not a gate.** Both halves were found by reading the project
   end to end with no defect in hand. That is an argument for scheduling the sweep, not for
   remembering harder — the same argument [`BRIEF.md`](BRIEF.md) *Release phases* makes twice about
   its own tables.

### L-26 — Measure the content, not the box; and pin motion before capturing

Two measurement traps, both hit while validating one deck, both of which return a confident clean
result:

- **A box cannot overflow a track that clamps it.** Content taller than a `1fr` grid row does not
  make any element exceed the stage — the track fixes the box and the content spills out of it
  silently. An overflow check written against element bounds reports zero while two slides are
  visibly broken. Compare `scrollHeight` with `clientHeight` instead.
- **An infinite animation stops a headless render from ever settling.** With a looping animation in
  the document, the virtual-time budget never reaches a quiescent state, screenshots fire mid
  transition, and the result is a convincingly blank slide that looks exactly like a real defect.
  Three "defects" chased this way were the harness, not the deck.

**Pinning motion is two obligations, not one, and half of it is worse than none** — added 2026-08-08
after both halves failed in the same session, on the same deck, each presenting as a CSS bug rather
than a capture bug.

- **The selector has to reach pseudo-elements.** `*` does not match `::before` or `::after`. A gate
  pinning `*{transition:none!important}` covers every element and none of the marks a component
  draws with a pseudo-element — so those keep transitioning and the capture reads their *animated*
  size and colour. The ruler's tick marks are `::before`, and the result was dots rendering as
  ovals through three rounds of chasing specificity that was never wrong. Pin
  `*,*::before,*::after`.
- **Killing the animation without restoring what it was going to reveal captures the pre-animation
  state.** Entrance animations hold their start frame until played, so `animation:none` alone
  freezes every risen element at `opacity:0` and photographs a blank slide — which is the very
  defect DS-224 exists to prevent, reproduced by the instrument meant to check for it. Pin motion
  **and** force the revealed state: `.rise,.pulse,.opening{opacity:1!important;transform:none!important}`.

**How to apply.** Any automated render gate pins motion off and disables transitions before
capturing, and measures content extents rather than element bounds. Both are one line each and both
were discovered by disbelieving a result that did not match what the previous render showed —
which is **L-06** again, now with a mechanism. Write the pinning **once, in the harness**, and have
every capture use that one string: both failures above came from ad-hoc capture scripts reinventing
half of a pair that the harness already had complete. And when a rendering looks wrong in a way that
implicates the artifact, check the capture first — **a mid-transition screenshot does not look like
a broken screenshot, it looks like broken CSS** (**L-35**).

### L-27 — An audit of intended values passes defects in rendered values

A checker built from the values an author **nominates** can only ever confirm those values. It is
blind by construction to any pair nobody thought to nominate — and that is where defects live,
because a defect is usually a value the author believed was something else.

The case: a palette audit compared seventeen foreground/background token pairs across two themes and
reported **zero failures**, while text was rendering at **2.17:1** on screen. The colour had been
written as an SVG presentation attribute and silently overridden by a CSS class rule, so the audit
checked a colour that never reached a pixel. It was not one slide: **28 attributes across seven
slides**, meaning a rule the deck appeared to satisfy it had never once satisfied. Three review
passes and a human looking at the deck were needed to find it, and the human found it only where the
backdrop happened to be dark.

**How to apply.** Audit the **computed** value against the **computed** value of whatever it sits on,
enumerated from the rendered tree — never from a list of pairs the author supplies. The general form:
*a check that reads the source reads the intent; only a check that reads the render reads the result.*
Where a platform has two ways to set the same property with different precedence — CSS versus
presentation attributes, inline versus stylesheet, attribute versus property — **ban the losing one
outright** rather than relying on authors to remember which wins. This is **L-05** and **DS-191** with
a mechanism attached, and it is the third time this project has paid for the same shape of error.

### L-07 — Standard library only

Project tooling is run by whoever clones the repository, on a machine nobody configured for it.
A dependency is a thing that can be missing.

**How to apply.** Scripts in `tools/` use the standard library and nothing else. If that makes a
script longer, it is still the right trade — the same reasoning that bans external libraries from
the decks themselves (rule 1 in [`../CLAUDE.md`](../CLAUDE.md)).

### L-08 — Store one edge; derive the rest

Write a fact in exactly one place and compute every view of it. Facts that are computed cannot
drift from facts that are stored; two hand-maintained copies of the same relationship disagree
within a week.

**How to apply.** In the task system, the forward edge lives in the front-matter and the child
list, the "blocks" list and the index are all derived. The same rule governs prose: if another
document owns a fact, point at it (**L-13**).

### L-09 — Every pointer must resolve in a fresh clone

A path in prose, in a template comment, or in a tool's output is a promise that the file is
there. This repository publishes, and CLAUDE.md requires clone-and-run, so a dangling pointer is
a defect and not a cosmetic one.

**How to apply.** Check pointers mechanically, including the ones hard-coded in tools, not only
markdown links between documents. Where a pointer is legitimately unresolvable — a machine-local
path, a deliverable not produced yet — make that explicit rather than letting the checker learn
to ignore it.

### L-10 — Declare the encoding; the console will not

The Windows console defaults to cp1252 and mangles the typographic punctuation this project's
prose is full of. The failure looks like corrupt data rather than a display setting.

**How to apply.** Open files as UTF-8 explicitly, reconfigure `stdout` where the runtime allows
it, and keep console output ASCII when the alternative is a garbled em-dash.

### L-11 — Write LF, everywhere, from every tool

Generated files get compared byte for byte. If line endings depend on who checked the repository
out, every comparison is noise and every regeneration is a diff.

**How to apply.** `.gitattributes` pins `eol=lf`; anything that writes a file passes
`newline="\n"` so the output is identical on every platform.

### L-40 — A gate you do not wait for is not a gate

Running the check and then doing the thing anyway is worse than not running it, because the output
scrolls past and everyone downstream believes it passed.

The retired `task.py`'s `index; check; git add -A; git commit`, chained with semicolons. `check`
reported **three dead pointers** and the commit ran regardless, so a broken state landed with a
message claiming the gate was green. *The tool has since been replaced by `taskmd` and
`tools/docs/refcheck.py` (T-062); the incident is left as it happened, because the lesson is about
the semicolon and not about the tool.* The gate worked perfectly; nothing was
listening. The same shape appears wherever a verdict and an action sit in one sequence — a test run
before a deploy, a validator before a publish.

**How to apply.** Chain a check to what follows it with `&&`, never `;`, so a failure stops the
sequence rather than scrolling past it. When a command's whole purpose is to gate the next one, the
two belong in one expression — and if the output is long, grep the verdict rather than trusting a
glance at the tail.

### L-60 — Someone else's measurement of your corpus is not a measurement of your tool

Found 2026-08-10 in
[T-073](../tasks/T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md). Upstream
evaluated a proposed feature by running a prototype over several repositories, this one included, and
reported **31 dead bare pointers here, 0 of them real defects**. That number arrived as evidence about
this project and was written into a task as a reason to retire `tools/docs/refcheck.py`.

It was evidence about the prototype. Running the actual tool took one command and reported **0 broken
over 1139 pointers** — because the prototype resolved a repo-relative path of any extension and
`refcheck.py` matches `.md` only, so the largest group in the report, 19 pointers to a retired `.py`
file, was never in its remit. The conclusion drawn from the borrowed number was the opposite of the
one the local run supports.

**What makes this hard to catch is that the number was correct.** Nothing was misreported. The corpus
was this project's, the count was accurate, the reasoning above it was sound — and it still measured a
different tool. A figure inherits the instrument that produced it, and the instrument does not travel
with the figure.

**How to apply.**

1. **Run your own tool before deciding about your own tool.** It is usually one command, and it is the
   only measurement whose instrument you can inspect.
2. **When a borrowed figure disagrees with your expectation, diff the rules, not the numbers.** The gap
   here was a single regex clause, and it explained the whole discrepancy in one reading.
3. **Carry the instrument next to the figure.** A measurement quoted without what produced it will be
   read as though produced by whatever the reader has in hand — which is exactly how this one entered
   a task's specification as settled input.

### L-61 — A check tuned against an unverified record learns to agree with its gaps

Found 2026-08-10 in
[T-071](../tasks/T-071-the-intermediate-specifications-carry-their-references.md). A new check made
the figure ledger authoritative: where a slide's declared sources and the ledger disagree, the slide
is corrected. Two of the ledger's `Used on` cells were wrong and three figures had no row at all.

Had the check been written first and the slides filled in until it went green, **the wrong cells
would have become the specification.** Every disagreement it reported would have been resolved in the
ledger's favour, which is what it was told to do, and the record would have ended consistent and
wrong — with a green run standing as evidence for it.

**The trap is that this looks like diligence.** Declaring one record authoritative is the right
design; it is what stops two copies of a fact drifting. The step that is easy to skip is establishing
that the authoritative one is *correct* before anything is tuned to it, because the check cannot
distinguish a record that is right from one that is merely trusted.

**How to apply.**

1. **Read the reference data before you write the check that trusts it** — every row, not a sample.
   Here it was thirty rows and it found five defects.
2. **Fix what you find, in the same change, and say you did.** A correction made silently while
   building the check is indistinguishable afterwards from the check having passed all along.
3. **Separate wrong entries from missing ones.** A wrong cell has to be fixed before the check is
   calibrated; a missing row can be a follow-up, because absence does not corrupt a comparison the
   way a false entry does. That split is why T-071 fixed two and raised a task for three.

---

### L-62 — Sweeping with the instrument that missed the defect measures the blind spot twice

Found 2026-08-10 in
[T-082](../tasks/T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md). Three
figures were known missing from a deck's figure ledger and the task was to sweep for more. The
repository already has a figure recogniser — `content.py`'s `FIGURE` — and its FIG-1 rule reported
*0 unsourced of 69* on the same deck, twice, while eleven values on two slides were in no source
document at all.

**It was not wrong; it could not see them.** The pattern requires a currency mark, a thousands
separator, a decimal, a magnitude letter or a unit word, so `6 rounds`, `04:10`, `27 of 31` and
`31 peak working days` are not figures to it. Sweeping by reading its output would have confirmed
the ledger was fine. The sweep that worked used a deliberately wider pattern written for the
occasion, marked bare-number runs as scale marks, and was thrown away afterwards.

**The hypothesis in the specification was half right, and the sweep is what showed which half.**
T-082 opened by naming the pattern — every known omission sat behind a disclosure, so tier two was
where the ledger leaked. Five of the rows the sweep added are tier one, including the first trunk's
arrival, parcels and finish time, which are labels on the hinge slide's own diagram. A rule stated
from the cases you already have describes those cases.

**How to apply.**

1. **Before sweeping for more of a defect, ask what found the first ones.** If it was a person
   reading, the tool has not been tested; if it was the tool, ask what shape it matches.
2. **Write the throwaway instrument wider than the gate**, and make its extra hits visible rather
   than filtered — the scale marks it over-reports are cheap to dismiss by eye, and the figures a
   narrow pattern drops are not recoverable at all.
3. **Do not promote the throwaway to a gate.** Wide is right for a sweep a human reads and wrong
   for a check that blocks a build; T-082 §3 declined to gate completeness for exactly this reason,
   and gated the direction that needs no recogniser instead.

### L-63 — A label a tool prints is an ordinary word everywhere else

Found 2026-08-10 in
[T-068](../tasks/T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md). A figure pasted
into prose has to be bound to the field that produced it, or a correct number in the wrong sentence
passes. On the page that pastes the command's output, the binding is easy and exact: the command
prints `checked   82`, so a sentence that says `checks` names the field, and `12 slides` stops being
covered by `8-12` inside an unrelated rule note.

**The same rule pointed at documents that paraphrase produced 30 false alarms against 5 true
bindings.** `checked`, `owned`, `rules`, `gate`, `reference` and `deck` are the words a gate labels
its rows with **and** the words five documents use in their ordinary sense — so prose about external
references, inline SVG counts and effect sizes anchored itself to a gate's account and was held to
its numbers. The failure is not the threshold; a looser or tighter word test moves which sentences
are wrong, not whether they are.

**What worked was binding on the claim's construction rather than its vocabulary.** *"82 of the 113
rules a gate owns … the other 31"* states a part, a whole and a remainder. Bind the whole by label,
require the part to be a figure of that same account, and check the subtraction. Five documents,
five bindings, no false alarms — and it caught the drift the sweep was written for, in every one of
them.

**How to apply.**

1. **Ask where the text is relative to the tool.** A page that pastes output can be held to the
   output's own vocabulary. A page that describes the same thing in its own words cannot, and the
   distance is not a tuning parameter.
2. **Bind on structure before vocabulary.** A construction — *part of whole*, *X rose to Y*, *N of M
   passed* — is stated by the sentence itself and is far rarer than any single word in it.
3. **Count the false alarms against the true bindings before keeping the check.** Thirty to five is
   a check that gets switched off in a week; the number is what decides, not whether the rule sounds
   principled.
4. **A figure derived beats a figure excused.** The one exclusion this tool carried was a remainder
   the sentence stated; checking the subtraction closed it, and the closing condition written beside
   the excusal — a new row in the gate — was never needed.

### L-64 — An exact check still needs a normalisation, and the normalisation is a measurement

Found 2026-08-10 in
[T-086](../tasks/T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md). The
rule was specified as the checkable half of a question precisely because it is exact — it searches
for a known string on a known slide rather than deciding what a figure is. Run literally over the
worked example, it could not decide **19 of 89** row-and-slide pairs, and exactly **one** of those
was the defect it was built to find.

**The other eighteen were the deck writing the same value a different way**, and none of the ways was
predictable from the specification: a small number spelled as a word (`6 people` against *Six people*
and *six-person crew*), a month abbreviated (`4 September` against *4 Sep*), one row carrying a whole
series (`4.1 / 11.2 / 15.9 / 18.7%` against a chart that labels its maximum and prints *3.4% or
under* for the rest), and two of the first draft's own boundary guards firing on ordinary
punctuation — a trailing comma, and a `%` left flush against the next word by the run splitter.

**A literal comparison between two documents written by different hands is not a check yet.** It is
the first measurement, and what it cannot decide is the specification for the normalisation. Guessing
that normalisation from the examples quoted in the task would have produced a rule that passed the
four cases in front of it and got switched off on the fifth.

**How to apply.**

1. **Run the first draft over the whole corpus unfiltered and print every undecided case.** The
   residue is the input to the rule; the rule is not the input to the residue.
2. **Read the residue for which kind each one is** — the document is wrong, or the check cannot say
   it. Eighteen to one here, and the ratio is what tells you whether you are still building the
   instrument or already using it.
3. **Test the boundary guards in both directions.** A guard written to stop `27` matching inside
   `27,600` will also stop it matching before a comma, and a false miss looks exactly like a finding
   until someone opens the slide.
4. **Then calibrate against the defects a person already found by hand.** Re-seeding T-082's four
   over-claims and watching all four go red is what separates a rule that works from one that agrees
   with the corpus it was tuned on (**L-61**).

### L-65 — A record that agrees with itself has told you nothing about whether it is true

Found 2026-08-11 in
[T-087](../tasks/T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md). The
reference deck records its provenance twice, from opposite ends: a colophon listing three model
documents and the slides that rest on each, and a mark on each slide naming the sources it uses. The
first check run was those two against each other. **All three slide lists matched the twelve marks
exactly, in both directions, with nothing to fix.**

**That was a consistency check wearing a correctness check's clothes.** Both records are written by
the same hand at the same time from the same belief, so they agree by construction and disagree only
under a clerical slip. Checked against the thing they describe — the figures actually on the slides —
**three slides cited sources they did not declare**, including the slide whose entire subject is the
programme timetable and which declared only the cost model.

**The direction that finds anything is record against artifact.** It is also the harder one, which
is why the easy one gets run and believed: comparing two lists needs no instrument, while comparing a
record to a deck needs something that can attribute a figure to a document.

**How to apply.**

1. **Name which pair a check compares before trusting a green run.** Two records of one belief, or a
   record and the thing it describes. Only the second can find a wrong belief.
2. **When two records agree perfectly on first run, treat that as a reason to check the artifact**,
   not as evidence the artifact is fine. Perfect agreement between hand-written records is the
   expected state, not a result.
3. **Attribute, don't just search.** *Is this figure in any source* is a weaker question than *which
   source carries it, and did the slide say so* — the second is what caught all three, and it is
   `SPEC-4`'s question asked of a deck with no ledger to ask it from.

### L-66 — A workaround written down as a local deviation is a product finding nobody has reported

Found 2026-08-11 in
[T-092](../tasks/T-092-product-feedback-from-the-first-external-deck.md). The first project to build
a deck with this plugin reported six things its owner found wanting after presenting-quality review.
**Two of the six had already been hit, worked around, and written into that project's own build log
as deviations** — one weeks earlier, one hours — and neither was recognised as feedback until the
owner read the finished deck and said the source lines were useless.

**The recognisable form is a log entry reading *built X instead of Y, because rule Z*.** That
sentence already names the rule, the worse outcome and the circumstance: it is most of a report
written by someone who did not think they were writing one. What stops it travelling is that the
deviation feels like a decision the builder made — it is in their log, under their name, and it is
closed. The maintainer never sees the log.

**How to apply.**

1. **On the building side, re-read the deviations before calling a piece of work done**, and ask of
   each whether the rule or the tool would want to know. A deviation that names a rule is a
   candidate; one that names only taste is not.
2. **On the receiving side, ask an adopter for their deviations, not for their bugs.** A bug report
   requires the reporter to believe something is broken, and this class is the tool working exactly
   as documented and failing the reader — nobody files that as a defect.
3. **Keep the two intakes apart.** Filed together, the interesting half gets triaged as bugs and
   closed by making code match documentation. T-092 was kept separate from `T-090` and `T-091` for
   exactly that reason, on the reporting owner's instruction.

### L-67 — A scan for a construct must require the construct, not its name

Found 2026-08-11 in [T-019](../tasks/T-019-build-the-capability-preflight-the-deck-ships-wit.md),
twice in one afternoon, in two tools written hours apart.

**Once in the emitter.** `"<template" in html` decides whether a deck needs the `<template>` row of
its capability preflight. Both `shell/components.css` and `shell/deck.js` explain the quick view in a
comment that names the tag, and both ship inside every deck — so every deck emitted the row,
including the ones with no quick view at all. **Once in the instrument that was supposed to prove the
emitter right.** The suppression harness read `data-preflight` with a pattern that could match
anywhere in the dumped DOM, and `shell/shell.html`'s own comment quotes the tag it explains; with the
attribute correctly removed from the real element, the search ran on and found the comment. It
reported the control — a working deck — as degraded.

Both are the same shape, and the shape is worth more than either instance: **the file contains prose
about the thing being scanned, and prose about a construct looks exactly like the construct.** It
gets worse as the code gets better commented, which is the opposite of the direction a check should
degrade in.

**How to apply.**

1. **Match structure, not vocabulary.** An element row wants an element: require the closing tag, or
   the attribute in the tag the parser would build, not the characters that spell it. `<template ...>
   ... </template>` is a construct; `<template>` in a sentence is a word.
2. **Anchor a document-level read to the document.** The marker regex was fixed by matching the
   *first* `<html ...>` in the dump and searching only inside that tag — the thing the parser would
   call the document element.
3. **Write the fixture that has the comment in it.** Both defects were caught by a self-test fixture
   holding prose that names the construct, and neither would have been caught by a fixture holding
   the construct. This is **L-04** applied to the scanner's own blind spot: a pattern that has only
   ever been shown to match is not evidence about what else it matches.

### L-68 — A check that truncates its input at a marker covers nothing past it

Found 2026-08-11 in [T-019](../tasks/T-019-build-the-capability-preflight-the-deck-ships-wit.md).
The component contract's completeness verdict — *every class the shared block styles has a row* —
read its input as `split("@media print {")[0]`. That is correct exactly as long as the print block is
last in the file, which nothing enforced and nothing checked. A new block appended after it styled
two classes the contract did not name, and the verdict reported **0 uncontracted** in the same run.

**The failure is silent by construction and gets quieter over time.** A truncating read keeps
reporting the coverage it had on the day the marker went last; every later addition past that point
raises the count of what it is not looking at and lowers nothing it prints. It is **L-36** with the
input truncated instead of the rule list — a claim about coverage made over a subset chosen by an
accident of file order.

**How to apply.**

1. **Cut the exclusion out; do not stop at it.** `@media print{...}` is removed by matching its own
   closing brace, so what follows is still read. Nesting is the trap in the naive version: `@page{}`
   and a nested query both put a `}` before the real one.
2. **Test the far side.** The fixture is a rule *after* the excluded block, asserted present, and a
   rule *inside* it, asserted absent. Without the first, the fix is untested in the direction that
   was broken.
3. **Suspect the shape wherever a check reads "the CSS", "the script" or "the body".** Any read that
   narrows its own input by a landmark inherits this, and the symptom is always a clean verdict
   rather than an error.

### L-69 — A phase name is not a version number

Caught 2026-08-11, at the release it would have broken. This backlog was split into phases named
`v0.1`, `v0.2` and `v0.3`, and `v0.1` meant *a defect in the published plugin*. Three such fixes had
been recorded across nine task logs and [`BRIEF.md`](BRIEF.md) as awaiting **`v0.1.6`**. The published
plugin was at **`0.2.0`**. *(The phases are `PH1`, `PH2` and `PH3` since 2026-08-12 — point 4 below
was reversed. The old names are kept in this entry because they are what the failure was made of.)*

**Tagging `v0.1.6` would have shipped the three fixes to nobody.** A plugin manager compares versions;
a tag below the installed one is never offered. Every document in the repository would have said the
release was out, the release page would have existed, and no adopter would have received it. The
symptom is unavailable to any gate here: `figures.py` compares figures to the commands that print
them, and nothing compares a *planned* version to a *published* one.

**A phase says what kind of work this is. A version says what an installed copy compares itself
against.** They were only ever the same string, and they came apart the moment a later phase shipped
first — which is exactly what this project's own splitting rule is designed to allow.

**How to apply.**

1. **Read the published version before tagging, not the phase the tasks carry.** `plugin.json` and
   the newest tag; the phase label is not evidence about either.
2. **A patch takes the next patch number on the published line, whatever phase its tasks belong to.**
   `0.2.0` plus three PH1-phase fixes is `0.2.1`.
3. **The tell in a record is *awaiting vX.Y.Z* where X.Y.Z is not greater than what is installed.**
   Worth a grep at release time; it is cheaper than the alternative, which is finding out from an
   adopter who never got the fix.
4. **Renaming the phases ends the ambiguity, and this entry declined it before taking it a day
   later.** The first answer was that a rename costs a rewrite of the whole backlog, so the cheaper
   fix went where somebody picks a number: [`../CLAUDE.md`](../CLAUDE.md), beside the release status.
   That protected the *release sequence*, which is where the failure had happened, and it did nothing
   for the *reading* cost — which kept accruing until the owner said they had confused the two
   repeatedly in conversation. Renamed to `PH1`–`PH3` on 2026-08-12, 282 mentions across 60 files
   (**T-099**).

   **The transferable half is that those are two different costs and only one of them was measured.**
   A label is read far more often than it is acted on, so pricing a naming fix by the edit it forces
   understates it every time. And the rename could not be automated for the reason it was needed:
   `v0.1` is a prefix of `v0.1.5`, so any pattern that finds the phase finds five real versions too.

### L-70 — A checker that forces a quotation to be edited has stopped checking and started writing

Two checkers here resolved markdown link syntax wherever it appeared, fenced blocks included. This
project states results as what was actually produced, and `taskmd index` prints one markdown link per
row — so quoting a board row put a link inside a fence, and the run went red on a target nobody could
click. The fix each time was to alter the quotation until the checker was satisfied.

**Nothing was wrong, and the record changed anyway.** A quotation adjusted to pass a validator is no
longer a quotation, and the adjustment leaves no mark: the next reader sees evidence that looks
verbatim. That is worse than a false alarm, because a false alarm is visible.

**The test is whether the thing being checked is a promise.** A link a reader can follow is a promise
the file is there. A link rendered as literal characters promises nothing — it cannot be followed, so
it cannot be broken. Same syntax, different position, different question.

**The boundary is not "skip code".** A path a tool *printed* into a fence is still a promise, and
checking those has caught real defects here. So the rule cuts on **syntax**, not on fences: link
syntax in code is literal, a bare path in code is not. Getting that wrong in the other direction
would have deleted a live check while looking like a fix — which is why both directions were
mutation-tested rather than reasoned about (T-080 §3).

**How to apply.**

1. **When a check fires on quoted evidence, ask what promise it thinks was made** before editing the
   evidence. If the answer is "none, this is a picture of a reference", the check is wrong.
2. **Narrow it by construct, not by container.** *Everything inside a fence is exempt* is the ask
   that loses a real check; *this construct is literal wherever it renders literally* is the one that
   holds.
3. **Prove both sides.** A fixture that only shows the false alarm gone cannot tell you whether the
   true positive went with it. Break the fix and require the suite to say so; then over-apply the fix
   and require it to say so again.
4. Where a rule about what may be quoted is written matters more than that it exists: it went to
   [`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) §6.1, next to the same rule for `§`
   marks, because that is the page an author reads before pasting something.

### L-71 — A tool that asserts its own environment fails for everyone except the person who wrote it

Caught 2026-08-12, from an adopting project. `theme.py` ran a self-test before every command and
refused to report if it failed. The test asserted that the destination a swap writes to — derived
from **the deck**, by walking up to the nearest repository — equals a module constant derived from
**the tool**. Those agree in exactly one arrangement: htmldeck sitting in a git clone. Everyone who
installs the plugin the documented way gets the failing branch, so `theme.py check` produced **no
verdict for any deck** for two releases, while the maintainer's every run was green (**T-101**).

**The guard was right to exist and right to be strict.** A default destination that overwrote its
input cost a recovery once (**T-059**), and the assertion is what keeps that fixed. What it must not
do is take the reference environment as the definition of correct.

**It was the fourth of a family, and the family is what makes it a lesson**: `build.md`'s `--out`,
DS-064's probe for the reference deck's own class names, `SPEC-5`'s slide pattern, and this. The
first three fail a conforming deck; this one blocks the tool, which is the same mistake in the one
place where it also silences the instrument that would report it.

**How to apply.**

1. **An expectation derives from the same input as the answer.** If the function takes the deck,
   the assertion about it takes the deck. A constant anchored on `__file__` is a claim about where
   the tool lives, and no function that accepts a path should be asserted against one.
2. **Make the constant unable to express the mistake.** The fix that lasts is not a better
   comparison, it is a **relative** fragment — `.assets-cache/deck/themed` joined onto whichever
   project is being talked about. A relative path cannot name the wrong project.
3. **Test the installed arrangement, not only the developed one.** A case with no repository above
   it costs two lines and is the environment every adopter is in. Prove it by re-seeding the defect
   **in a clone**: a regression test that can only fail where nobody runs it is not a test.
4. **A failing self-test is a silence, not a message.** Any tool that refuses to report on a failed
   pre-check should be assumed to have zero coverage in every environment where that check can fail.

### L-72 — A classification that describes the reference deck becomes a rule against every other deck

Caught 2026-08-12, from an adopting project. The component contract has a `Source` column, and
`vocabulary` means *styled, emittable, and this deck contains none* — checked in the opposite
direction, for **zero** instances, so that a rule matching nothing cannot pass as a rule that
passed. Five rows carried it. One of them, `.fig .pos`, had a note saying in writing that *a figure
encoding a loss is the obvious next deck, which is why the rows stay*. That deck was then built by
an adopter, drew a shortfall in red, used the contract's own class and **failed the gate for it**
(**T-105**).

**The classification was a true statement about one deck and an enforced prohibition on all of
them.** Nobody wrote the prohibition; it fell out of a description being read as a rule, which is
what a `Source` column is.

**The sweep is where the real finding was.** Asked which other rows were in the same position, the
answer was *all of them*: `.t-ink` is the sibling of five `author` text roles, and `.mono` was
documented as a standalone utility. Every row carrying `vocabulary` was a class the contract defines
for a deck to use, so the source emptied.

**How to apply.**

1. **Separate *no deck has needed this yet* from *no deck may have this*.** Only the second is a
   rule. The first is a measurement, and dating it is how it stays one.
2. **When a note anticipates the case that breaks it, that note is the alarm.** *Which is why the
   rows stay* was written before any deck needed them and was still true; what changed is that the
   anticipated deck existed, and nothing was watching for it.
3. **Sweep the whole class, not the reported row.** The report names one instance because one
   adopter hit one. The question to answer is which others would fail the moment somebody did the
   obvious thing.
4. **A check with no members is honest; a check with misfiled members is not.** Emptying the source
   is not losing coverage — the claim it makes is about rows that exist.

---

### L-73 — An advisory you decide to ignore must be pinned to the subject that earns it

Caught 2026-08-12 (**T-098**). taskmd 0.5.0 added a `DUPLICATE INDEX` advisory that fires when a
non-task document names a majority of the board's task ids. It fires here, on `docs/BRIEF.md`, whose
phase tables are the decision record behind the backlog — one row per task, kept deliberately. The
reading is true, the document is right, and the count only climbs: **78 of 105** the day it was
decided, and every release moves it.

**The trap is the shape of the decision, not the decision.** *Ignore `DUPLICATE INDEX`* and *ignore
`DUPLICATE INDEX` on `docs/BRIEF.md`* are one keystroke apart in a document and opposite in effect.
The first spends the rule: a genuine second board arrives as a line in a place everyone reads past.
The second spends one line of it, and leaves the alarm intact for every other file.

**The rival was to make it stop firing**, by proposing a per-document opt-out upstream. It was
refused for what it is rather than for its size: an advisory whose value is that it cannot be
silenced, given a silencer. Every project that trips it believes its own document is legitimate, and
that belief is exactly what upstream found to be wrong in an adopting project.

**How to apply.**

1. **Write the subject, not the rule.** Name the file, the rule id, the artefact — whatever makes
   this instance correct — so a second instance reads as new rather than as the same known noise.
2. **Date the number that made it fire.** A count that climbs with the project is a dated
   measurement, never a current one, and a sentence naming no field is watched by nothing.
3. **Put it where the tool's output is documented, not where the checklist is.** The gate runs far
   more often than the release that enumerates it.
4. **Refuse a silencer on its own terms.** *We are the exception* is what every project says; the
   question is what the mechanism costs the projects that are not.

---

### L-74 — When a fact cannot be derived, make the stored copy fail loudly in both directions

Caught 2026-08-13 (**T-096**). **L-08** says a stored copy of a derivable fact drifts, and the fix is
to derive it. Some facts cannot be derived: *is this file a checker?* has no mechanical answer — 34
scripts under `tools/` all have a `__main__`, and the four that break rules on purpose look exactly
like the one the release runs. So the answer has to be written down, which is the hand-kept list that
had already missed three red checks.

**What makes a written-down answer safe is reconciliation, not care.** The list becomes a manifest
when it is checked against the world **both ways**: a file no entry names fails the run, and an entry
naming a file that is gone fails it too. Neither direction alone is enough — the first catches the
tool nobody wired, the second catches the entry nobody deleted, and a list that goes stale silently
is one that does neither.

**The proof is what the first run found**, on a repository whose gate list had been written down
three days earlier and run twice: three suites nobody had wired, all green and all invisible, and a
printed page count reached by no command at all. None of the three was hidden. Each was one line
missing from a list that nothing compared to anything.

**How to apply.**

1. **Ask whether the fact is derivable before writing it down.** If it is, derive it — that is L-08
   and it is still the first answer.
2. **If it is not, enumerate over a discovered set, never over the entries.** Walk what exists,
   classify each, and let the unclassified be the failure. A loop over the list can only ever confirm
   the list.
3. **Give every entry a stated reason, not a flag.** *Skipped* is a value; *skipped because its
   checks run inside `check.py`* is a fact the next reader can check and disagree with.
4. **Both directions, or it is still a list.** An unwired file and a deleted one are the same defect
   seen from two sides, and a manifest that catches one of them is trusted for catching neither.

---

## Writing

### L-12 — What is read every time must be short

Anything loaded on every run competes with the work for attention and for context. Length there
is a recurring cost, not a one-off one.

**How to apply.** The always-loaded body stays short and routes; the detail lives in a reference
loaded on demand. This is why the design system will be a separate file the skill points at
rather than prose inside the skill.

### L-13 — Point at the source; do not restate it

A paraphrase is a second copy that starts drifting immediately, and the reader cannot tell which
copy is current.

**How to apply.** One document owns each fact. Everything else links to it. If a restatement is
genuinely needed for flow, keep it to a sentence and link the owner in the same breath —
`../CLAUDE.md` owns the rules, [`BRIEF.md`](BRIEF.md) owns what to build,
[`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) owns the task mechanics, and this file
owns the lessons.
