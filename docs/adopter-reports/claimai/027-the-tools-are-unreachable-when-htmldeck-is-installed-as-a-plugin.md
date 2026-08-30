# The tools are unreachable when htmldeck is installed as a plugin, and the cache keeps every version

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature |
| **Status** | `open` — **point 2 answered 2026-08-30 by [T-227](../../../tasks/T-227-the-front-pages-adoption-route-names-a-variable-the-skill-removed.md); points 1 and 3 stand.** The version-sorting line this record calls *the one worth the report on its own* was **already correct** in `SKILL.md` section 0 — the documented glob has always sorted as versions — so the gap was never the command, it was that nothing said **why**. A line whose reason is unstated reads as a flourish, and an adopter rewriting the glob drops it; section 0 now states that the sort is load-bearing, that the cache keeps every version, and that the failure reads as *tool not found*. This machine's cache holds the seven versions the record names, `0.1.1` to `0.6.0`, which is where that was re-measured. **Points 1 and 3 — ship a launcher, and make every tool print the version that answered — are packaging decisions T-227 does not own** and are not refused here, only unaddressed. What T-227 did remove is the reason an adopter had to guess: the plugin root is now resolvable from the skill's own location, so the launcher these points ask for no longer has to discover it. |
| **Severity** | Medium — every adopter writes the same launcher, and the obvious version of it silently picks an old tool set |
| **Found while** | Building the executive board deck from 2026-08-24 onward; the launcher was written for `E70` on 2026-08-26 |
| **Version seen** | 0.6.0 |

## What happens

Installed as a plugin, htmldeck's tools live under the plugin cache and are **not on `PATH`**. There is
no documented invocation, so every project invents one. This one wrote a launcher; it is 70 lines, and
each of them is there because something went wrong without it.

## What the launcher has to know

| It handles | Because |
| :--- | :--- |
| Resolving the plugin cache path | Not on `PATH`, and the path carries a version number that changes on update, so a hard-coded path rots silently |
| **Sorting versions as versions** | The cache keeps **every** version installed. A first-match glob picks `0.1.1`, which lacks scripts that exist in `0.6.0`, and the failure reads as *tool not found* |
| Finding a working Python | On this machine `python3` is a Store stub: it passes `Get-Command`, then prints an install notice and exits non-zero. A candidate has to prove it runs |
| Rooting relative paths | So the deck path works from any working directory |
| Refusing `density.py write` | It corrupts self-closing SVG tags — [`015`](015-density-py-write-corrupts-a-self-closing-svg-tag.md) |

The version-sorting line is the one worth the report on its own. The cache directory listing here holds
seven versions, `0.1.1` through `0.6.0`, and only the last has the tools the docs describe.

## What to change

1. **Ship a launcher, or a documented invocation.** One entry point that resolves the installed
   version and passes everything through. Every adopter is writing this, and most will write the
   first-match glob.
2. **Say in the docs that the cache keeps every version**, and that a glob must sort as versions. This
   is the failure mode an adopter cannot diagnose, because the error names a missing tool.
3. **Make the tools say which version answered.** Every command printing its own version turns a
   confusing failure into an obvious one.

## Related

- This project's `taskmd` note on the same problem — the launcher there exists for the same reasons,
  which is what makes it a plugin-packaging gap rather than a quirk of one tool.
