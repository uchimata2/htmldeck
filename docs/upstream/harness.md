# Observations for the agent harness

> **Handover record — not sent, 2026-08-14. This is the document's disposition, not an omission.**
> **Route:** none identified. The other two registers went as issues on repositories their owners
> control; this one's owner is a vendor, and no channel was found that accepts an observation carrying
> no priority.
> **What would change it:** a vendor channel, an issue tracker, or a support path. Any one of them is
> enough, and a later session can send this without re-deciding whether it should be sent — that
> question is settled and the answer is yes.
> **Response:** none, and none is pending.
>
> Written down rather than left implicit because *no route found* and *withheld* look identical from
> outside, and only one of them is waiting for something. This is the first. Recorded by
> [T-157](../../tasks/T-157-hand-the-upstream-registers-to-their-owners.md), which sent the other two.

**From the htmldeck project, one machine, two shells.** Two observations, neither ranked and neither
a request. This document exists because the first of them was originally filed against the wrong
project, and the register it sat in had no home for an owner that is not a plugin.

**Scope warning, up front.** Everything below was measured on **one machine — Windows 11, Git Bash
and PowerShell 7** — in one session. That is enough to correct an attribution. It is not enough to
describe a surface, and nothing here should be read as a claim about how the harness behaves
generally.

## The observations

| | Observation |
| :--- | :--- |
| **O-C1** | **The shell snapshot's `PATH` line is truncated mid-value, and it silently removes every plugin's `bin/` directory.** The snapshot's `export PATH='…'` line is **5,551 characters, 67 entries, and ends mid-path with no closing quote**; the shell that sources it has **37 entries and zero plugin `bin/` directories**, so 30 entries were lost including all three from the plugin cache. **20 of the 67 are session-scoped `local-agent-mode-sessions/<id>/<id>/rpm/plugin_<id>/bin` paths of about 200 characters each**, which is where the length comes from. Nothing reports the failure: a plugin's command simply does not exist, which reads as a broken install |
| **O-C2** | **PowerShell gets no plugin `bin/` at all, by a different route.** `Get-Command <plugin-command>` does not resolve and `$env:PATH` contains no `plugins` entry, on the same machine and in the same session where the Bash snapshot at least *contained* the directory before losing it. So the two shells this environment offers disagree about what commands exist, and neither offers the plugin's. Recorded separately from `O-C1` because the mechanism is not the same and a fix for one need not fix the other |

## What it cost, which is the argument for `O-C1` mattering

A plugin whose command does not resolve looks exactly like a plugin that is installed wrong. In this
repository that produced, in order: two wrappers that locate the installed skill themselves, a
latent version-ordering defect inside one of them, and **an observation filed against the plugin
author for a defect that was never theirs**. The plugin ships a working launcher; running it directly
returns the right answer with exit 0. Nothing in the failure points at `PATH`, and nothing points at
truncation.

**Two directions worth considering, neither of them ours to choose:**

- **Shorten what goes in.** Twenty session-scoped entries dominate the line, and they are the ones an
  adopter never types.
- **Fail loudly rather than truncate.** A `PATH` that cannot be written whole is worth an error. The
  current behaviour is the worst case for diagnosis — the value is present in the file, absent in the
  shell, and nothing in between says so.

## Provenance

Assembled by the htmldeck project as part of a context-economy audit of its own development
workflow. Both rows are *implementation* vintage: they were found while building something, not
while auditing, and **no backlog was consulted** — there was none available to read. See
[`../CONTEXT-AUDIT.md`](../CONTEXT-AUDIT.md) §7.3 for where they sat before this document existed,
and [`../research/R8-context-economy-for-coding-agents.md`](../research/R8-context-economy-for-coding-agents.md)
§6 for the rules the register follows — chiefly that an observation is recorded and never ranked.
