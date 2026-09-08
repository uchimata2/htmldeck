---
tool: htmldeck
version: 0.7.0
date: 2026-09-08
severity: friction
---

# `shell.py sync` reports a deck fully up to date while its chrome tail is a release behind

## Expected

After a htmldeck upgrade, one command should say whether a deck carries anything the new release
changed. `sync` is the command an adopter reaches for, and its report is written to be read as the
answer: it names the regions that would change and the regions it will not touch.

## Actual

`sync` owns the **shared** regions only. The chrome tail is a **per-deck** region it must never
write, and a second command — `shell.py tail` — owns that. Nothing in `sync`'s output says so. Its
closing line reads as reassurance about the very regions it cannot see:

> `3 region(s) would change; 13 per-deck region(s) untouched.`

A deck can be current by `sync` and a release behind by `tail`, and the adopter has no signal.

## The command that proves it

One file, a 2026-09-04 snapshot of this project's deck, both commands on 0.7.0, 2026-09-08:

```bash
python <htmldeck>/tools/deck/shell.py sync stale-tail.html
python <htmldeck>/tools/deck/shell.py tail stale-tail.html
```

```
sync:  SKELETON 135 lines -> 137 lines
       COMPONENTS 1281 lines -> 1353 lines
       SCRIPT 998 lines -> 1078 lines
       3 region(s) would change; 13 per-deck region(s) untouched. Nothing written.

tail:  stale-tail.html - `Motion` would move inside the menu (DS-218).
       Nothing written. Run again with --write.
```

`tail` is right, and `sync` never mentions it.

## What it cost here

The upgrade landed on 2026-09-03. `sync` was run, it reported nothing outstanding, and this project
recorded the upgrade debt as cleared. **The deck's owner found the defect three days later by
looking at the deck** — the Motion control sitting outside the More menu, which is exactly what
`tail` reports and precisely what `DS-218` fixes. One wrong claim to the owner, one release of
chrome shipped stale, and an hour to work out that two commands own two halves of one shell.

## Workaround used in this project

Both commands are now run together after any upgrade, in that order. The rule is written into the
project's build notes, where it will be read by whoever reads them.

## Suggested fix

Cheapest first: have `sync`'s summary **name the other half** rather than imply there isn't one —

```
3 region(s) would change; 13 per-deck region(s) untouched.
The chrome tail is per-deck and is not checked here: run `shell.py tail <deck>`.
```

Better: have `sync` **run the tail comparison read-only** and print its one line in the same report.
It already knows the shipped shell, so the comparison costs nothing, and no adopter can then be
up to date by one command and behind by another.
