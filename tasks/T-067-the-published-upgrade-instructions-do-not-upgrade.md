---
id: T-067
title: The published upgrade instructions do not upgrade anything
type: fix
status: review
phase: implement
parent: null
blocked_by: []
related: [T-056, T-061]
work_package: v0.1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-10
updated: 2026-08-10
deliverables:
  - README.md
  - .claude-plugin/plugin.json
---

# T-067 — The published upgrade instructions do not upgrade anything

## 1. Specify

**Outcome**
Someone on an older version can reach the current one by following what this repository tells them.
Today they cannot, and two releases have shipped saying otherwise.

**The report**
From the project running htmldeck, 2026-08-10, upgrading 0.1.1 to 0.1.2:

> `marketplace update` on its own upgraded nothing. It refreshed the cache to 0.1.2, but
> `installed_plugins.json` still said 0.1.1 afterwards. `claude plugin install htmldeck@htmldeck`
> then reported "already installed" and did nothing. The command that actually moves the version is
> `claude plugin update htmldeck@htmldeck` — and the bare name fails with "Plugin htmldeck not
> found", so the `@marketplace` suffix is required.

They ended up with 0.1.1 and 0.1.2 side by side in the cache while Claude Code loaded the older one,
because it loads by the install record rather than by highest version. The first gate result of their
session came from an explicit cache path while the *installed* plugin was still the old one.

**Where this repository says the wrong thing**
- `README.md` *Install it* gives `marketplace add` then `install`, with no upgrade path at all.
- The **v0.1.1 release notes** say: *"If you added the marketplace before this release, refresh it
  first: `/plugin marketplace update htmldeck`"*.
- The **v0.1.2 release notes** repeat it.

So the two releases that exist *because* the previous one was broken both tell an affected user to
run a command that leaves them on the broken version. That is the worst place for this defect to be.

**This is covered text, not a nicety.** `docs/PUBLISHING.md` §2's test is *what a stranger reads
before they have installed anything*, and release notes and the install section are squarely inside
it. It is also the first defect found in text that had already been through the humanizer, which is
worth noticing: that pass checks how prose reads, not whether a command works.

**Scope**
- In: `README.md`'s install section gains an upgrade path with the command that works.
- In: the v0.1.1 and v0.1.2 **release notes on GitHub**, edited in place, since those are what an
  affected user is reading.
- In: whether the two forms differ inside Claude Code (`/plugin ...`) and at the shell
  (`claude plugin ...`), because the report used the shell form and the README uses the other.
- Out: anything about how Claude Code resolves versions. Not this repository's to fix, and the
  report already describes the behaviour well enough to write around.

**Acceptance criteria**
- [ ] The README gives a working upgrade path, distinct from first install
- [ ] Both published release notes are corrected in place
- [ ] The `@marketplace` suffix is shown, since the bare name fails
- [ ] Verified by actually upgrading on this machine, not by reading the CLI's help text
- [ ] The corrected text has been through the humanizer, per `docs/PUBLISHING.md` §2

**Open questions**
- **Does `/plugin update` exist inside Claude Code, or only `claude plugin update` at the shell?**
  The report used the shell. The README uses the in-session form throughout, so the two need
  checking rather than assuming they mirror each other.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Establish the working command in both forms, by running them | The transcript, in §3 |
| 2 | Correct the README install section | The edit |
| 3 | Correct both release notes in place with `gh release edit` | Two edited releases |
| 4 | Verify by upgrading from an older version on this machine | The run |

## 3. Implement

**Decisions & assumptions**

- **The open question is answered, and the answer is that there is no in-session equivalent —
  2026-08-10.** `claude plugin --help` lists `update [options] <plugin>`, *"Update a plugin to the
  latest version (restart required to apply)"*. The published documentation for installing and
  managing plugins lists `/plugin install`, `/plugin list`, `/plugin enable`, `/plugin disable`,
  `/plugin uninstall`, and `/plugin marketplace add|list|update|remove` — **and no per-plugin
  `/plugin update`**. So the README's in-session voice cannot be kept for this instruction, and the
  upgrade section says "in a terminal rather than inside Claude Code" rather than implying a
  symmetry that does not exist.

- **The reason `marketplace update` does nothing is worth stating, because without it the correction
  reads as an arbitrary second command.** Claude Code does update installed plugins after a
  marketplace refresh — but only where **auto-update is enabled for that marketplace, and
  third-party marketplaces have it off by default.** That single fact explains the whole report:
  the catalog moved to 0.1.2, the install record stayed at 0.1.1, and `/plugin install` then
  correctly reported the plugin was already installed. It also yields a second working route, which
  the README now gives: enable auto-update for the marketplace in the `/plugin` panel.

- **The bare name was tested rather than quoted from the report:**

```
$ claude plugin update htmldeck
Checking for updates for plugin "htmldeck" at user scope…
✘ Failed to update plugin "htmldeck": Plugin "htmldeck" not found
```

- **Both release notes were edited by pattern match, requiring exactly one hit each**, so a silent
  partial edit was not possible. Each reported `1 replacement(s)` before anything was published.

- **Two README figures were stale and are re-derived, per `PUBLISHING.md` §6.** `refcheck.py` reads
  1034 pointers and 1188 unbound section references, against 1031 and 1184 on the page. **This is
  L-52 firing for the second time in two days**, and neither drift came from the edit that caused
  it — the documents grew.

- **A third README claim had gone false and is not a figure.** *"one project … found three defects
  in two days … All three are fixed"* is now four, and the third took two attempts. Written that way
  rather than incremented, because "the first fix looked for other instances with a throwaway script
  that read only part of what it claimed to have read" is the fact a reader deciding whether to
  trust this plugin should have.

**Outputs produced**
- `README.md` (the *Upgrade it* section, two re-derived figures, the defect count)
- `.claude-plugin/plugin.json` (0.1.3)
- the v0.1.1 and v0.1.2 release notes on GitHub, edited in place
- `CLAUDE.md`, `docs/BRIEF.md` (the release state)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → proposed | Reported by the project running htmldeck while upgrading to v0.1.2. **The instruction is published in two release notes and both were written to help someone off a broken version**, which is what makes an `xs` documentation fix `high` value rather than trivial. Also the first defect found in text that had already passed the humanizer: that pass judges how prose reads and cannot tell whether a command works, which is worth remembering before treating it as a quality gate for instructions. |
