---
id: T-067
title: The published upgrade instructions do not upgrade anything
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-056, T-061]
work_package: v0.1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-10
updated: 2026-08-10
deliverables: []
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
- <recorded as the work is done>

**Outputs produced**
- <path>

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
