---
paths:
  - "README.md"
  - "docs/PUBLISHING.md"
---

# htmldeck — release rules

The harness appends this file after a session reads `README.md` or `docs/PUBLISHING.md`. It holds the
publishing constraints that bind a release, cut from [`CLAUDE.md`](../../CLAUDE.md) by
[T-295](../../tasks/T-295-complete-t-288s-observation-and-decide-the-move.md). The ones that bind every commit stay there.

## Step 1

**Step 1 of [`docs/PUBLISHING.md`](../../docs/PUBLISHING.md) §8 is one command** — `python tools/check_all.py` — which discovers every checker a clone receives and
every deck this repository ships, and ends with a partition: each **ran**, **was skipped with a
stated reason**, or **failed**. A tool in none of those three fails the run. What it replaced, and
what its first run found that a hand-kept list could not, are that section as well.

## The humanizing rule

- **Humanized where a human reads it.** **No release ships until the human-facing text has been
  through the humanizer** — every release, not the first. The test is *what a stranger reads before
  installing anything*: today `README.md` and the repository description. **Plugin files are not
  human-facing and must stay AI-optimized** — the skill, `CLAUDE.md`, these rule files, tool docstrings, commit messages
  and the task record — and a humanizer pass over them is a defect, not a courtesy. Deck copy is
  DS-106's, gated by `check.py`. The covered-set test, the exclusions and the owner's verbatim
  exception: [`docs/PUBLISHING.md`](../../docs/PUBLISHING.md), which is the rule and outlives any task.
  The first release's pass is recorded in
  [T-056](../../tasks/T-056-humanize-the-human-facing-documents-before-publishing.md); **every release
  after it runs the rule again.**
