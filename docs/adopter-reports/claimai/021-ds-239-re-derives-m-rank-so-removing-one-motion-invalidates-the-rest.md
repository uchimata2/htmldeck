# DS-239 re-derives --m-rank from the deck, so removing one motion silently invalidates every other rank

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `open` |
| **Severity** | Medium — an unrelated edit makes a passing deck fail, and the failure names ranks the author never touched |
| **Found while** | Deciding what the verdict pulse should do, on 2026-08-26 — `E79`; met first on 2026-08-26 — `E66` |
| **Version seen** | 0.6.0 |

## What happens

`DS-239` requires each content motion's `--m-rank` to be the value the rule derives, and it derives
that value **from the deck** — from how many content motions there are and in what order.

So the ranks are not properties of a motion. They are properties of the set. Remove two of five
content motions and the remaining three are wrong: this deck was left with `21`, `41` and `81`
against a rule that now wanted different numbers. Nothing in the edit touched them.

The same coupling in the other direction — *adding* two content motions re-ranked all five — is what
made `density.py write` the right tool to apply the change, and that tool corrupted seven tags. That
is [`015`](015-density-py-write-corrupts-a-self-closing-svg-tag.md), and this rule is why it was
being run at all.

**This is not an argument that the rule is wrong.** `DS-239` caught five ranks that had silently gone
stale, which is exactly its job. The cost is that the correct value of any one rank is unknowable
without recomputing the whole deck.

## What to change

1. **Have the gate print the value it wants, per motion.** The failure says a rank is wrong; it does
   not say what the rule derives. It already knows, and printing it turns a bisection into an edit.
2. **Make the safe writer safe.** `density.py write` exists precisely for this arithmetic and is
   currently the thing an author must not run — see [`015`](015-density-py-write-corrupts-a-self-closing-svg-tag.md).
   With that fixed, the coupling costs one command instead of a manual renumbering.
