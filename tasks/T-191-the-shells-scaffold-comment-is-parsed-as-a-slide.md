---
id: T-191
title: The shell's own scaffold comment is parsed as a slide and injects a figure into slide 1
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-167]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-191 - The shell's own scaffold comment is parsed as a slide and injects a figure into slide 1

## 1. Specify

**Outcome**
A deck that still carries the comment `shell.py new` wrote passes the content half. Today it cannot.

**The defect**
`shell.py new` writes, at the slide insertion point:

    <!-- slides go here, one <section class="slide"> each (COMPONENT-CONTRACT.md 3.2) -->

Four tools split a deck into slides with the same regex -
[`../tools/deck/audit.py`](../tools/deck/audit.py) line 674,
[`../tools/deck/content.py`](../tools/deck/content.py) line 191,
[`../tools/deck/spec.py`](../tools/deck/spec.py) line 59, and `density.py`:

    <section[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>(.*?)</section>

That pattern matches the `<section class="slide">` **inside the comment**. The comment therefore
opens a phantom slide which runs to the first real `</section>`. `runs()` does strip comments, but it
runs on the fragment *after* the split, by which point the opening `<!--` has been consumed and there
is no comment left to strip - so the trailing text survives and `3.2` is harvested as a figure.

**Reproduced 2026-08-20**, comment outside every section:

    [{'value': '3.2', 'slide': 'opener', 'label': ['each', 'component-contract'],
      'context': 'each (COMPONENT-CONTRACT.md 3.2) -->'}]

`FIG-1` then reports a figure on slide 1 that appears in no source - **on a string the shell itself
wrote**. The adopter build of 2026-08-19 hit exactly this and spent a diagnosis round on it.

**The second half, which the adopter's report did not reach.** The phantom does not only add a
figure; it moves slide 1's boundary. Whatever reads the opening tag's attributes reads the comment's,
and the four tools above share the fault, not just `content.py`.

**Scope**
- In: the comment `shell.py new` writes - the cheap fix is to stop it containing literal `<section`.
- In: stripping comments from the whole document before splitting, in the one place the split is
  defined. Two copies of the fix is the failure the shell exists to prevent.
- In: a fixture that keeps the scaffold comment and asserts no figure comes off it.

**Acceptance criteria**
- [ ] A fresh skeleton with one slide, comment untouched, yields zero figures from the comment.
- [ ] The four splitters resolve to one definition, or each is shown immune with its own fixture.
- [ ] The fixture is watched failing against today's code before it is watched passing.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision - rationale - date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
