# htmldeck — design rationale

**Why the rules are what they are.** Companion to [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md), which
holds the operative ruleset and nothing else.

**No runtime loads this file.** It is for whoever maintains the ruleset, argues with it, or needs to
know whether a rule was measured, inherited, or decided. Entries are keyed by `DS-nnn`.

**Sources.** `R1`–`R6` in [`research/`](research/); corpus rule IDs (`C1`, `F11`) and their verdicts
in [`research/R1-rules-candidate.md`](research/R1-rules-candidate.md); external principles (`P-01`)
with E1–E4 evidence grades in [`research/R2-external-principles.md`](research/R2-external-principles.md);
archetypes and anti-patterns in [`research/R3-exemplar-decks.md`](research/R3-exemplar-decks.md);
provenance in [`research/R4-prior-art.md`](research/R4-prior-art.md).

---

## 1. How a rule got its verdict

154 corpus rules were resolved into this ruleset: **110 keep · 17 amend · 1 drop · 26 defer.**

**The precedence used, and it ran the same way for all 154:**

1. **A standing owner decision** (`BRIEF.md` § *Decisions taken*, or a CLAUDE.md rule) overrides an
   observed habit. **This class is not in the owner's stated tie-break, and it fired four times** —
   DS-011, DS-030, DS-001, DS-002.
2. **An E1/E2 external principle contradicting the habit** — the stated tie-break. **Fired once**, on
   the stage (§3 below).
3. **A named contradiction X-1…X-11** — resolved individually, §2.
4. **Otherwise, keep.** An E3/E4 principle does not outrank a corpus habit, so it was never a
   conflict. This is most of why the keep count is high.

**Keeping 71% of an observed corpus is the expected result.** The tie-break only fires where an
external principle is E1/E2 *and* contradicts a habit, and that combination is rare. No external
principle addresses whether the mono layer carries the domain vocabulary.

**Provenance was context, never a verdict.** No rule was dropped for being inherited. All seven of
the source skill's navigation rules are kept (DS-130–DS-135). What R4's grading bought is knowing
which rules may be cited as the owner's signature — not which to discard.

**The 26 defers are boundary, not indecision:** 11 process rules to T-020, 5 check mechanics to
T-005, 7 critique-format rules to T-004, 4 pipeline rules from group A. Nothing was deferred for want
of an answer.

---

## 2. The sixteen conflicts

| # | The tension | Resolution |
| :--- | :--- | :--- |
| **X-1** | CDN libraries **vs** self-contained | Self-containment, and it generalises. The icon-sprite pattern is the general principle: embed only what is used. R5 measured a whole deck at 192 KB — no cost argument remains. → DS-001, DS-113 |
| **X-2** | Never hand-draw icons **vs** no external references | Not a conflict. Embedding an icon set's *official* symbols is using the set. → DS-112, DS-113 |
| **X-3** | "No overdose", "no ambient motion" **vs** the brief's rich animation | Resolved by §4 — motion must encode something. The four-motion vocabulary already implements it. *The sharpest conflict in the set, and it dissolved rather than being arbitrated.* → DS-140, DS-150 |
| **X-4** | Canvas effects read as artificial **vs** 3D now wanted | The restraint survives; the suspicion of canvas does not. A particle field that encodes nothing fails in SVG, canvas or WebGL alike. → DS-115, DS-150 |
| **X-5** | "Aim 8, max 10" **vs** "do not exceed 18" **vs** "completeness overwrites the size limitations" | Three rulings, three decks, all the owner's. **Deck length is a per-deck decision, not a house rule** — averaging would invent a rule no deck follows. What holds across all three is kept: single clean message per slide, and nothing is dropped, it is folded. → DS-082, DS-083, DS-084 |
| **X-6** | Stated rules run ahead of the artefacts | **Frequency is evidence of effort, not of intent.** A `stated` rule the corpus under-delivered is still a rule — the specs are the considered position, the decks are what time allowed. Applied: `prefers-reduced-motion` (5/12 in the corpus) is promoted to hard, not weakened. → DS-143 |
| **X-7** | Provenance mark: plain text, no dead links **vs** the owner praising the working link | Both, conditioned on reachability. The underlying rule is *never ship a dead link*; the two decks differ in circumstance, not principle. → DS-105 |
| **X-8** | "No 3D spins" **vs** "Turn: `rotateY` with `preserve-3d`" | Not a conflict. A 3D *transition between slides* is forbidden; a 3D *reveal of a card* is prescribed. Stated precisely so the ban is not read too widely. → DS-144 |
| **X-9** | Icons via CDN **vs** self-containment | As X-1. → DS-113 |
| **X-10** | A word-list check **vs** "text can pass all five and still sound like AI" | Both true. The check is necessary and not sufficient and **must say so** — a clean terminology pass may never be reported as "this reads as human-written". → DS-106, DS-107 |
| **X-11** | `100dvh` flex slides **vs** the fixed scaled stage | **The stage, and the alternative is ruled out rather than dispreferred** — see §3. |
| **R2 §12.1** | Richness **vs** Mayer's coherence principle | Motion must encode something. §4. |
| **R2 §12.2** | Line length: reading speed **vs** preference | Optimise for preference, make it a token. A deck is read voluntarily by a reader who can stop, so comfort dominates throughput. → DS-039 |
| **R2 §12.3** | WCAG 2 **vs** APCA | Conform to AA, design with APCA, never report APCA as conformance. |
| **R2 §12.4** | Redundancy **vs** the standalone file | Dissolved structurally by the disclosure layer, not by compromise. The two audiences are separated in time. → §5 |
| **R2 §12.5** | Sans-serif at distance **vs** R5's serif display face | Not a conflict once roles are separated. P-12 governs *projected* text; a display face at headline size is well above the angular size where serifs fail. Recorded so it is not re-derived. |

---

## 3. The stage — DS-060 to DS-065, and the numbers behind them

**The owner's reason is not the one the corpus recorded, and the difference reshaped the ruleset.**

The corpus rationale was *"what was rehearsed is what appears"* — a rehearsal guarantee, which reads
as presenter convenience. Weighed as convenience it **lost** to two WCAG criteria, and T-014
escalated it. **The actual reason is two observed failures:**

1. A deck built for small screens **breaks when opened on a 4K display** — breakpoints land in a
   bucket nobody designed, `max-width` containers leave dead gutters, absolute positioning drifts.
2. A deck presented from a high-resolution monitor **arrives illegible**, because a video call
   re-encodes the shared screen at 1080p or 720p and the text goes down with the frame.

### Why no responsive layout can solve the second

Text in the received stream measures:

```
stream_px  =  S  ×  (viewport_h / 1080)  ×  (F / viewport_h)
           =  S  ×  (F / 1080)
```

`S` = design-unit size, `F` = the call's frame height. **The presenter's viewport cancels.**

**Under a uniformly scaled stage, what the audience can read depends only on the design size and the
call's resolution — never on the machine it is presented from.** A responsive layout renders
different text fractions on different presenter monitors, so its legibility over a call is a
function of whichever machine is used. That is failure 2, exactly.

**This is why "drop the stage for flex slides" is ruled out rather than merely dispreferred**, and
why DS-061 forbids media queries inside the stage.

### The type floor, computed — DS-034, DS-035, DS-036

| Role | Design units | Share of frame | at 1080p | at 720p | at 540p |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Display | 67 | 6.2% | 67 px | 45 px | 33 px |
| Subhead | 34 | 3.1% | 34 px | 23 px | 17 px |
| **Body — the floor** | **24** | **2.2%** | **24 px** | **16 px** | 12 px |
| Below the floor | 18 | 1.7% | 18 px | 12 px | 9 px ✗ |
| Mono label (corpus value) | 16 | 1.5% | 16 px | **11 px ✗** | 8 px ✗ |

**720p is the binding case.** It sets body at 24 design units, **tightens the corpus's D5 range of
18–24 to 24–28** — its lower half does not survive a screen share — and **demotes the corpus's 11–13
unit mono labels to decoration** (DS-036), because they were never legible to a remote audience.

Neither number was derivable before the reason was stated. Generalised as **L-22**.

### Viewer scale — why 960 CSS px is the reflow threshold

`scale = min(vw/1920, vh/1080)`:

| Viewer | CSS viewport | Scale | Body renders at |
| :--- | :--- | ---: | ---: |
| 4K monitor, 100% OS scaling | 3840 × 2000 | 1.85 | 44 px |
| FullHD laptop, 100% | 1920 × 950 | 0.88 | 21 px |
| FullHD laptop, 125% | 1536 × 760 | 0.70 | 17 px |
| FullHD laptop, 150% | 1280 × 634 | 0.59 | 14 px |
| Below 960 CSS px | — | < 0.5 | reflow engages |

**Every laptop case stays on the stage and stays readable**, which is the requirement.

**Why 1920×1080 design units rather than the corpus's 1600×900:** purely a change of units — both
16:9, both scale, nothing renders differently. It buys **one design unit = one pixel in a 1080p
stream**, making every size directly checkable against what an audience receives.

### The accessibility trade, and how it was resolved

**1.4.4 Resize Text** and **1.4.10 Reflow** are both AA, and a scale-to-fit stage defeats both —
zooming rescales the stage instead of enlarging the text. **This is the one place the owner's
tie-break fired.** Settled by adding the reflow view (DS-070–DS-076) as a conforming alternate
version — the same shape as the printing decision.

**Ruled out and recorded so neither is revisited casually:** dropping the stage (re-introduces the
defect above), and claiming bare AA while shipping a scaled stage (a silent omission).

---

## 4. Motion — DS-140, DS-150

**Adopted: motion must encode something.** The brief's *Richness* decision says "no JavaScript
budget" and reads as permission. Mayer's coherence principle is the best-supported result R2 found —
23 of 23 tests, median effect size 0.86 — and it cuts against decorative motion.

**The conflict is narrower than it looks.** The owner's own practice is already on the evidence's
side: the corpus's most developed spec defines exactly four motions and nothing else, for the stated
reason that a named vocabulary is what stops animation becoming decoration, and two specs
independently forbid 3D spins. **The conflict is between the brief's wording and a practice that
never took that permission.** No re-scope requested; a wording change proposed in `BRIEF.md`.

---

## 5. Progressive disclosure — DS-160 to DS-170

**Load-bearing, not a signature flourish.** R2 §12.4 finds it is the *only* structure that lets the
dual-audience decision survive the redundancy principle. R3 §8 reaches the same place from the
catalogue's shape: every archetype has a tier-one/tier-two form, and A-13 is what that means in
practice — so it belongs *across* the catalogue, not *beside* it.

**Two independent routes to one conclusion is the strongest signal in the research.** It is why the
catalogue is thirteen archetypes plus one modifier rather than fourteen archetypes, and why the
build must decide a tier split for **every** slide.

**The density trap is the failure mode this project is most exposed to.** The lone-reader half of
the *Use case* decision tempts every slide to carry everything. Meeker's Internet Trends is that
carried to its conclusion — genuinely authoritative, and a punishing read, because every slide pays
the full density cost whether or not the reader needs that slide. **X-06 is therefore a check, not
an observation: if the deck reads acceptably only because the reader is assumed to be diligent, the
split is wrong.**

---

## 6. Drops and amendments worth knowing

**DS-011 — one palette per deck was dropped.** The corpus rule (C7) is `dominant`; it describes what
the decks actually do. It lost to CLAUDE.md rule 4, **not to evidence** — a standing decision
overriding an observed habit. R4 also grades C7 inherited (the source skill's four presets adapted
per deck), so dropping it costs the owner's signature nothing. Everything else in §2.1 is
*within-palette* discipline and is unaffected. The variety it provided returns from the template
generator, not from per-deck improvisation.

**DS-030 — the per-deck font rotation went with it.** R4 traced *"a deliberate pairing per deck"* to
the source skill's instruction to rotate pairings and never repeat one; it was never the owner's
signature. **The role structure was the valuable half and it is kept.** R5 recommends Instrument
Serif · Space Grotesk · JetBrains Mono at 97.3 KB.

**DS-031 — do not read corpus frequency as intent.** Inter is the most frequent face in the older
decks and the refined specs reject it by name. R5 adds the cost argument: Inter is the most
expensive of the four at 62.8 KB inlined and the least distinctive.

**DS-001/DS-002 — there is no quality/self-containment trade-off.** The corpus rule said *maximise
quality at all cost, even in multiple files*. R5 measured a full 12-slide deck with three embedded
faces, icons, a motion library and four SVG diagrams at **191.8 KB with zero external references**.
The escape hatch has nothing left to buy.

**DS-005 — nothing `file://` refuses costs the deck anything.** R6 measured 95 rows on Chrome 151 and
Edge 151: `file://` is a secure context, so `crypto.subtle`, view transitions, container queries,
popover, WebGL1/2 and a WebGPU adapter are all available, as are fullscreen, clipboard, audio resume,
download and every storage API. **Do not design around fears this research retired.**

**DS-123 — "boxes everywhere" is one of seventeen unflagged departures.** The source skill
*prescribes* the card grid and step-card pipeline as house style. This is where R2's best-supported
findings and the owner's sharpest instinct agree, which is rare enough to name.

**DS-090 — the heading check went semantic.** The brief's *every `<section>` has a heading* becomes
*every `<section>` has a heading that is a claim*. **That constrains the writing, not just the
markup** — tractable only because the brief already decided the plugin writes the words. It grows
build mode as well as the check.

**A-09, A-13, A-14 are the owner's signature.** They are the three archetypes added to an inherited
set, and the three that external practice independently arrives at. The other six corpus archetypes
match external exemplars only because both descend from the same design canon — **one source counted
twice, not convergence.** Where this project cites the owner's taste, it cites these three.

**A-01 and A-02 are admitted on external evidence alone.** The corpus never named them, probably
because a layout-oriented spec would not. Both are structural, and R2 says they carry the argument.
