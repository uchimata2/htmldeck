---
id: T-192
title: shell.py icons --help crashes, and no command lists what the sprite holds
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-192 - shell.py icons --help crashes, and no command lists what the sprite holds

## 1. Specify

**Outcome**
`shell.py icons --help` prints usage. Today it prints a traceback.

**The defect**

    $ python tools/deck/shell.py icons --help
    ...twenty lines of self-test...
    FileNotFoundError: [Errno 2] No such file or directory: '--help'

`--help` is taken as the deck path and `read()` dies on it. Reproduced 2026-08-20.

**The second half.** There is no way to ask what concepts the sprite carries. `icons --sheet
<out.svg>` writes a sheet, which answers the question only if you then open the file. The adopter
build of 2026-08-19 ran `icons --help` twice, got the traceback twice, then grepped `icons.svg`
directly - and its first regex was wrong, so four tool calls went on *what icons exist*.

**Scope**
- In: `--help` on every `shell.py` subcommand, printing that subcommand's usage.
- In: `icons --list`, printing the sprite's concept ids to stdout.
- In: whether the self-test should run before `--help` at all. My reading is no - a help request is
  not evidence and does not need any.

**Acceptance criteria**
- [ ] `shell.py <any subcommand> --help` exits 0 and prints usage for that subcommand.
- [ ] `shell.py icons --list` prints the ids, and the list is generated from `icons.svg` rather
      than written down beside it.

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
