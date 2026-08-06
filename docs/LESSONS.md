# Lessons

Things this project has already paid for once. Each is **generic** — it survives the task that
produced it and applies to the next one — and each is stated so it can be *acted on*, not
admired.

Cite them by ID. `L-07` and `L-11` are cited from `tools/tasks/task.py`, so **IDs are stable**:
add at the end of a section, never renumber.

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
a hard rule with a computed floor** (body ≥ 24 design units, nothing under 18), tightened a corpus
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

---

## Tooling

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

---

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
