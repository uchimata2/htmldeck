# DS-202 refuses a two-sentence bottom line, including one the author chose in review

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature |
| **Status** | `open` |
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
