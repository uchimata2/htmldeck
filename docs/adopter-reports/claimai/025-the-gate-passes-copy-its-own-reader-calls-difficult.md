# The gate passes copy its own reader calls difficult, and the project had to build an instrument for it

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature |
| **Status** | `closed` — closed 2026-08-30 by [T-258](../../../tasks/T-258-the-gate-passes-copy-its-own-reader-calls-difficult.md). **All three changes taken; the subject was refused and re-decided by measurement.** [`../../../tools/deck/readability.py`](../../../tools/deck/readability.py) reports Flesch, Flesch–Kincaid, Fog, a three-syllable share and a nominalisation rate — the last two because this record's own evidence says that is where the difficulty lived — and **names the hardest lines ranked, which is the output**; the aggregate is context. This record's note is why: its author scored **Flesch 64.6, plain English, on copy their reader called difficult**, so an aggregate that agrees with nobody cannot be the answer. **It never gates and its exit code is always 0.** **The subject is contracted prose, not *the deck's own text nodes* as proposed**: scored both ways on the four tracked decks the two readings differ by **8 Flesch points on `measure-first`**, a reading grade, and the sign is not constant, so it is not an offset — an axis tick has no verb and no sentence end, and scoring it measures label style. Words left out are counted and named in the report rather than dropped. Change 3 is in [`../../../tools/deck/check.py`](../../../tools/deck/check.py)'s closing account, beside the sentence that already says a clean `DS-106` is never *reads as human-written*. **The second half — the six AI tells — is not this task's** and was closed by [T-229](../../../tasks/T-229-ds-106s-check-omits-a-word-the-rule-names.md), which derived `DS-106`'s list from the rule's own row. |
| **Severity** | High — the deck's whole purpose is a reader understanding it, and every rule that touches copy was green while the author found it hard |
| **Found while** | The author reporting that the deck's language was hard for the audience it was written for, on 2026-08-28 — `E82` |
| **Version seen** | 0.6.0 |

## What happens

The gate has two rules over copy and both were green on a deck the author called difficult:

```
DS-092   sentences over 20 words: 0, paragraphs over 4 sentences: 0     pass
DS-106   banned terminology                                             pass
```

`DS-092` measures **length**. `DS-106` measures a **banned list**. Neither measures difficulty, and
difficulty was the problem — vocabulary, noun stacks, abstraction, and claims that need a second
reading to attach to their subject.

Measured afterwards on the same deck, with an instrument this project had to write:

```
Flesch Reading Ease      64.6      Gunning Fog        10.3
Flesch-Kincaid Grade      6.9      3-syllable words   18.0% of all copy
Nominalisations           129      Words over 12 letters  13
```

**18% three-syllable words and 129 nominalisations is where the difficulty lived**, and no rule looks
at either.

## The second half: six AI tells the build check does not gate

`DS-106` was checked directly during the build and found to cover banned terminology only. Six tells
had to be read for **by hand**, once, and the read recorded:

rule-of-three cadence · negative parallelism · superficial `-ing` analyses · vague attribution ·
em-dash overuse · reflex bullet lists

A hand read does not repeat, does not survive an edit, and is not evidence.

## What to change

1. **Add a readability verdict over drawn slide copy** — Flesch, Fog and a three-syllable share.
   Pure standard library; the instrument this project wrote is about 200 lines and reads the deck's
   own text nodes.
2. **Report it rather than gate it.** A number that names the hardest lines is what an author acts
   on; a threshold on prose invites writing to the threshold.
3. **Say what a green copy run means.** The gate already says a clean run is never *reads as
   human-written*. It should say the same about *reads easily* — the two rules that exist measure
   length and a word list, and an author reads green as "the copy is fine".

## Note on the instrument

A score is not the answer either. This project's own record is that **the numbers above read as plain
English on copy whose reader called it difficult** — they located the hard lines, they did not judge
them. Report the measurement and name the worst lines; leave the verdict to a person.
