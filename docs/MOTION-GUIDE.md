# Motion — style guide

**This is guidance and it gates nothing.** Nothing here fails a deck. The rules that do are
[`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §5.2, and where this document and a rule disagree the rule
wins — say so and fix this file, because a guide contradicting a gate is worse than no guide.

**Why it exists.** DS-140 used to be an allow-list of four motions. On 2026-08-19 the owner ruled
that any animation aligned with the rules is admissible and the four names are a suggestion, and
[T-187](../tasks/T-187-open-the-motion-vocabulary-into-a-style-guide.md) opened the rule on
2026-08-21. A list answers *may I?* in one word; a guide has to argue. This is the argument.

**Who reads it.** Whoever is designing a motion, and the critique pass, which is the part that needs
it most: with a closed vocabulary the pass could only observe that a motion had a name, and it can
now say why a conformant motion is still the wrong one.

---

## 1. The principles

Stated by the owner, 2026-08-19, verbatim in
[T-187](../tasks/T-187-open-the-motion-vocabulary-into-a-style-guide.md) §1. Numbered as they were
given. **Two of the six are already rules**, which is worth knowing before you read them as advice.

**1. Keep animation gentle.** The reader is reading. A motion loud enough to be noticed as a motion
has taken attention from the thing it was meant to help, and the attention does not come back
cleanly. Gentle is small distance, modest scale, no bounce that reads as a cartoon. The shipping
theme's Rise travels a short distance and fades — that is the calibration, not a minimum.

**2. Add significant motion when it is specifically requested.** The default is restraint, and
restraint is not the same as absence: a deck with no motion at all reads as a document. What is
reserved for a request is *significant* — a long sequence, a build with several stages, a motion the
audience is expected to watch rather than absorb.

**3. Ease in and out, as the default for almost everything.** **This is already a rule** — DS-141,
as [T-016](../tasks/T-016-the-interaction-and-motion-layer.md) amended it: eased rather than linear,
with `linear` surviving only where the mechanism requires it, such as a looping dash. The guide does
not restate the rule; it agrees with it, and DS-240 adds the case the principle does not cover — a
control tracking a pointer has no arrival to shape, so `linear` is right there.

**4. 300–500 ms as the default length; longer for illustration or on request.** **This is also
already a rule** — DS-141's cap, and its licence. Where the guide adds something is at the bottom of
the band rather than the top: under about 150 ms a motion stops reading as a movement and starts
reading as a flicker, so a "fast" entrance is usually a broken one. The exception is a control
answering the hand, which DS-240 puts at or under 250 ms deliberately, and its press under 150 —
those are *not* entrances and the floor does not apply to them.

**5. One motion per page's content, and skip it where there is no room.** One entrance gesture per
slide is what makes a deck read as one deck. Two content motions competing on one slide is the
commonest way a slide starts to feel busy, and the second is nearly always the one that could go.
*Skip it where there is no room* is the important half: a dense slide is not improved by animating
it, and no rule anywhere requires a slide to move.

**6. The page is not designed around its own animation.** **This one became a rule** — **DS-243**,
because it is what DS-140's closure was standing in for and the ruleset would otherwise have had no
answer to [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §4. It is stated here because it is the
principle most worth having in mind while designing, and because the failure is easy to miss from
the inside: the slide looks considered, every motion encodes something real, and the argument was
still bent to give them somewhere to live.

**7. And so on.** The owner's own seventh: *these are not hard rules, more like a style guide, and
can be adjusted, refined, extended.* Extending this file needs no ruleset change and no ceremony.
Extending §5.2 does.

---

## 2. The starter set

DS-140's four, which the shipping theme supplies and a deck gets without designing anything:

| Motion | What it is for | Band |
| :--- | :--- | :--- |
| **Rise** | an entrance, staggered — the arriving half of the slide transition | inside DS-141's cap |
| **Current** | a flow: dashed, looping, saying *this is a sequence* | 3–6 s, and DS-218's stop control follows |
| **Open / Turn / Scale** | a reveal — something the reader asked to see | inside DS-141's cap |
| **Pulse-once** | one mark on one figure, never looping | 0.8–1.6 s |

**Reach for these first, and not out of obedience.** They are four gestures a deck can make
repeatedly without the repetition becoming noise, which is a property a new motion has to earn. The
honest reason to add a fifth is that none of the four says the thing you mean — not that four felt
few.

---

## 3. Designing a new motion

**The admission test is DS-140's and it is short.** A motion is admissible when it encodes something
(DS-150), does not shape the page (DS-243), declares its kind (DS-237), declares its subject
(DS-142), sits inside DS-141's band or declares `--motion-long`, and survives reduced motion, print
and the stop control. Nothing else is required, and no name is.

What the test does not tell you, and this guide does:

- **Say what the reader learns from it.** Not what it looks like. *The arrowhead scales out of the
  line* is a description; *the reader is told which end is the destination* is an encoding. If the
  second sentence is hard to write, the motion is decoration and DS-150 will say so eventually.
- **Prefer reusing a gesture over inventing one.** A deck making four gestures well reads better
  than one making seven. `.arrow-pop` is Scale applied to an arrowhead rather than a new motion, and
  that was the right call before the vocabulary opened and stays the right call after.
- **Choose the kind before the timing.** DS-237's `affordance` / `content` split decides which band
  you are in — affordance answers the hand and lives in DS-240's short bands; content answers the
  argument and lives in DS-141's. Getting this backwards is what made the pager's press take 420 ms
  ([T-198](../tasks/T-198-give-affordance-motion-its-own-band-faster-than-content-motion.md)).
- **If it loops, say what it is about.** `--motion-subject` takes `live` or `static`, and DS-142
  bans continuous motion on static content. This is the one declaration that can fail a deck on its
  own: a loop declaring `static`, or declaring nothing, is ambient decoration by definition. Write
  `live` only where something really is in flight — a flow carrying a sequence, a process still
  running — and never as the token that makes the gate quiet.
- **If it runs long, write down why.** `--motion-long` takes `loop`, `illustration`, `emphasis` or
  `request`. The value is a claim on the artifact, so the critique pass can disagree with it — which
  is the point, and is more than a name ever offered.
- **And write the number where a theme can reach it.** The duration goes in the licensed long band —
  `--long-dur`, `--long-ease`, `--long-delay` — declared in the deck's own theme region
  ([`THEME-CONTRACT.md`](THEME-CONTRACT.md) §3.6). They are `optional`, so a deck that runs no long
  motion declares none of them. **Do not borrow a neighbouring dial**: `--pulse-dur` is paced for an
  emphasis mark, and a motion wearing another motion's band is the defect
  [T-198](../tasks/T-198-give-affordance-motion-its-own-band-faster-than-content-motion.md) recorded.
- **Check it with motion off.** DS-143, DS-218, DS-221 and DS-224 all reduce to one question: does
  the deck still say what it says when nothing moves? If the answer is no, the motion is carrying
  content and the content needs somewhere else to live.

---

## 4. What this guide will not do

It will not enumerate admissible motions. That was the previous design and its failure was structural
rather than a matter of the list being too short: a list can only rule on motions someone has already
met, and it forbids by silence — which is indistinguishable, from the inside, from having considered
and rejected the thing.
