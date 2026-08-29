# DS-202 refuses a two-sentence bottom line, including one the author chose in review

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature |
| **Status** | `closed` — closed 2026-08-29 by [T-270](../../../tasks/T-270-two-rules-whose-escape-hatch-teaches-the-wrong-habit.md). **Proposal 2 taken, proposal 1 refused.** The count stays: replacing it with a word or clause cap trades a crisp rule for a fuzzy one, and the task that raised this report found eight bottom lines restating their own headline, which is the work the count does. What changes is the verdict, which now reads *one sentence is the rule so the line cannot become an argument; shorten it rather than joining the two with `and`* — **the second clause names the workaround this report actually took**, so the message answers the thing an author is about to do rather than only the thing they did. The `DS-202` row says the same. Proved on htmldeck's `examples/measure-first/measure-first.html`: control `bottom lines that are not one sentence: 0` pass, a bottom line seeded to two sentences `1 - Larkfield Dental Group - one sentence is the rule so the line cannot become an argument…` FAIL. |
| **Severity** | Low — the joined sentence is acceptable, but the author's wording was changed to satisfy a count |
| **Found while** | Making round 2's copy fixes, on 2026-08-25 — `E55`, from the survey answers registered in `E52` |
| **Version seen** | 0.6.0 |

## What happens

`DS-202` allows a bottom line of exactly one sentence. Shown two forms in review, the author chose
the two-sentence one. Built that way, the gate said:

```
bottom lines that are not one sentence: 1 - Treatment works, and stops short
```

The two sentences were joined with *and*. Not one of the author's words was changed, but the form he
picked was.

## Why it is worth a look

`DS-202` exists for a good reason — the same task found **eight** bottom lines restating their own
headline, and the rule is part of what keeps that text load-bearing. This is not an argument to drop
it.

The narrow point is that *one sentence* is a proxy for *short and factual*, and it is not always the
right proxy. Two short clauses can be shorter and plainer than one clause joined with *and*, which is
what happened here.

## What to change

1. **Measure what the rule is protecting** — length and factuality — rather than sentence count.
   A word cap, or a cap on clauses, would have passed the author's form and still caught the eight.
2. **Or keep the count and say the reason in the failure.** *A bottom line is one sentence so it
   cannot become an argument* is a sentence an author accepts. `not one sentence: 1` is one they work
   around.
