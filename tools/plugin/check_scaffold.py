#!/usr/bin/env python3
"""Check the plugin package against the packaging contract in `docs/research/R5-assets-and-licences.md` §6.

Eight checks, all mechanical:

  0. Every field the manifest schema types holds that type, and `author` carries the `name` the
     schema requires of it. **Optional is not untyped** - v0.1.0 shipped a string `author`, the
     installer refused the plugin, and this tool called the manifest valid (T-061).
  1. `.claude-plugin/plugin.json` exists, parses, and its `name` is kebab-case.
  2. Component directories sit at the plugin **root**, never inside `.claude-plugin/`.
  3. Every skill has a `SKILL.md` with a `name` and a `description` in its front matter.
  4. Every intra-plugin path in a skill file goes through `${CLAUDE_PLUGIN_ROOT}` - no absolute
     paths, no `~`, nothing working-directory-relative. This is L-09 as a packaging rule.
  5. Every `${CLAUDE_PLUGIN_ROOT}/...` path resolves in a fresh clone.
  6. The always-loaded skill body stays under the budget below (**L-12**).
  7. Every command a skill documents names a tool that exists, and a subcommand and flags that
     tool's source knows. **A documented invocation is a claim like any other** - `build.md` told
     every build to run a `--out` flag `render.py` did not have, and the crash landed at the step
     that closes the visual gate. An adopting project reported it; nothing here could (T-074).

    python tools/plugin/check_scaffold.py            # check this repository
    python tools/plugin/check_scaffold.py --self-test

**The self-test is not optional decoration.** A scan that looks like a tool gets believed; this one
runs first against nineteen fixtures whose answers are known, one per failure mode it claims to
catch and one per case it must not flag (**L-04**). It got believed anyway: the count was ten and
none of them typed a field, so the manifest that shipped v0.1.0 passed (T-061).

Pure standard library (**L-07**).
"""

import ast
import io
import json
import os
import re
import sys
import tokenize

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NAME_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

# The manifest schema's field types, encoded rather than fetched, from
# json.schemastore.org/claude-code-plugin-manifest.json read 2026-08-09. Standard library only
# (CLAUDE.md), and the schema is small enough that a dict is the whole of it.
#
# Only `name` is required. Every field here is optional, and OPTIONAL IS NOT UNTYPED - that
# conflation is T-061: v0.1.0 shipped `"author": "the htmldeck maintainers"`, the installer
# refused the plugin, and this tool printed `OK - manifest valid` because it asked whether the
# field was present and never what it held.
MANIFEST_TYPES = {
    "$schema": str, "name": str, "version": str, "description": str,
    "homepage": str, "repository": str, "license": str,
    "author": dict, "settings": dict, "userConfig": dict,
    "keywords": list, "dependencies": list, "channels": list,
}
TYPE_NAMES = {str: "string", dict: "object", list: "array"}
ROOT_VAR = "${CLAUDE_PLUGIN_ROOT}"

# The body is read on every invocation, so its cost is paid whether or not a deck is built.
# 8 KB is roughly two screens of prose - enough to route, far too little to restate a ruleset.
BODY_BUDGET = 8192

# Paths that look intra-plugin but are not ours to resolve. `~` is caught separately.
ABSOLUTE_RE = re.compile(r"(?<![\w`])(?:[A-Za-z]:[\\/]|/(?:home|Users|mnt|opt|usr|var)/)")
TILDE_RE = re.compile(r"(?<![\w`])~/")

# Every backticked repo-relative path in a skill file, outside fenced blocks. **All of them must
# be written from ${CLAUDE_PLUGIN_ROOT}**, not only the ones inside a sentence containing the word
# "load". An earlier version of this check keyed on that word and let "Build to <a doc>" past,
# which is L-30 exactly: a rule keyed on one value exempts everything that value does not match.
# The user's own project may hold a `docs/` of its own, so a bare path is a live mis-resolution.
BARE_RE = re.compile(r"`((?:docs|skills|examples|tools|reference)/[^`\s]+)`")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def front_matter(text):
    """Return the front-matter block of a markdown file, or None."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else None


def check(root):
    """Return (problems, notes) for the plugin rooted at `root`."""
    problems, notes = [], []

    # ---------------------------------------------------------------- 1. the manifest
    manifest_dir = os.path.join(root, ".claude-plugin")
    manifest = os.path.join(manifest_dir, "plugin.json")
    if not os.path.isfile(manifest):
        problems.append("NO MANIFEST   .claude-plugin/plugin.json is missing")
        return problems, notes

    try:
        data = json.loads(read(manifest))
    except ValueError as exc:
        problems.append("BAD JSON      plugin.json does not parse: %s" % exc)
        return problems, notes

    for field, want in MANIFEST_TYPES.items():
        if field in data and not isinstance(data[field], want):
            got = TYPE_NAMES.get(type(data[field]), type(data[field]).__name__)
            problems.append("BAD TYPE      `%s` is a %s, the schema says %s"
                            % (field, got, TYPE_NAMES[want]))

    author = data.get("author")
    if isinstance(author, dict) and not author.get("name"):
        problems.append("BAD AUTHOR    `author` is an object without `name`, which the schema "
                        "requires of it")

    name = data.get("name")
    if not name:
        problems.append("NO NAME       plugin.json has no `name`, which is the one required field")
    elif not isinstance(name, str):
        pass          # already reported as BAD TYPE; kebab-case is not a question you can ask of it
    elif not NAME_RE.match(name):
        problems.append("BAD NAME      `%s` is not kebab-case" % name)
    else:
        notes.append("plugin `%s` v%s" % (name, data.get("version", "-")))

    for field in ("version", "description", "author", "license"):
        if field not in data:
            notes.append("no `%s` in the manifest - optional, wanted for distribution" % field)

    # ---------------------------------------------------------------- 2. component placement
    for component in ("skills", "commands", "agents", "hooks"):
        stray = os.path.join(manifest_dir, component)
        if os.path.isdir(stray):
            problems.append("MISPLACED     %s/ belongs at the plugin root, not inside "
                            ".claude-plugin/" % component)

    skills_dir = os.path.join(root, "skills")
    if not os.path.isdir(skills_dir):
        problems.append("NO SKILLS     skills/ is missing, so nothing is auto-discovered")
        return problems, notes

    # ---------------------------------------------------------------- 3-6. per skill
    skills = sorted(d for d in os.listdir(skills_dir)
                    if os.path.isdir(os.path.join(skills_dir, d)))
    if not skills:
        problems.append("NO SKILLS     skills/ holds no skill directory")

    for skill in skills:
        body_path = os.path.join(skills_dir, skill, "SKILL.md")
        if not os.path.isfile(body_path):
            problems.append("NO BODY       skills/%s/ has no SKILL.md" % skill)
            continue

        body = read(body_path)
        fm = front_matter(body)
        if fm is None:
            problems.append("NO FRONT      skills/%s/SKILL.md has no front matter" % skill)
        else:
            for field in ("name", "description"):
                if not re.search(r"^%s\s*:\s*\S" % field, fm, re.M):
                    problems.append("NO %-9s skills/%s/SKILL.md front matter has no `%s`"
                                    % (field.upper() + ":", skill, field))

        size = len(body.encode("utf-8"))
        if size > BODY_BUDGET:
            problems.append("BODY TOO BIG  skills/%s/SKILL.md is %d bytes, budget %d (L-12)"
                            % (skill, size, BODY_BUDGET))
        else:
            notes.append("skills/%s/SKILL.md is %d bytes of %d" % (skill, size, BODY_BUDGET))

        # Every markdown file the skill owns, body and references alike.
        for dirpath, _, files in os.walk(os.path.join(skills_dir, skill)):
            for fname in sorted(f for f in files if f.endswith(".md")):
                path = os.path.join(dirpath, fname)
                rel = os.path.relpath(path, root).replace("\\", "/")
                text = read(path)
                problems.extend(check_paths(root, rel, text))
                problems.extend(check_commands(root, rel, text))

    return problems, notes


def check_paths(root, rel, text):
    """Checks 4 and 5 over one markdown file."""
    problems = []
    body = strip_fences(text)

    for match in ABSOLUTE_RE.finditer(body):
        problems.append("ABSOLUTE PATH %s: `%s...` - use %s (L-09)"
                        % (rel, body[match.start():match.start() + 24].strip(), ROOT_VAR))
    for match in TILDE_RE.finditer(body):
        problems.append("HOME PATH     %s: `%s...` - use %s"
                        % (rel, body[match.start():match.start() + 20].strip(), ROOT_VAR))

    # Check 5: what the skill says it loads must exist.
    for target in re.findall(re.escape(ROOT_VAR) + r"/([A-Za-z0-9_./-]+)", body):
        target = target.rstrip(".,;:`")
        if not os.path.exists(os.path.join(root, target)):
            problems.append("DEAD POINTER  %s: %s/%s does not exist" % (rel, ROOT_VAR, target))

    # Every bare repo-relative path is working-directory-relative at runtime, which is what the
    # criterion forbids - whether the sentence around it says "load" or not.
    for target in BARE_RE.findall(body.replace(ROOT_VAR + "/", "\x00")):
        problems.append("UNBASED PATH  %s: `%s` - write it from %s" % (rel, target, ROOT_VAR))

    return problems


def strip_fences(text):
    """Drop fenced code blocks - templates inside them are illustrations, not load instructions."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


# A command line the skill tells a build to run. Only inside fences, which is exactly where checks
# 4 and 5 do not look - so until T-074 the one part of a skill file that is meant to be executed
# verbatim was the one part nothing read.
COMMAND_RE = re.compile(r"^\s*python\s+" + re.escape(ROOT_VAR) + r"/(tools/[A-Za-z0-9_./-]+\.py)"
                        r"(.*)$", re.M)


def check_commands(root, rel, text):
    """Check 7: every documented invocation names a tool that exists, and a subcommand and flags
    that tool's source knows.

    **A documented command is a claim, and it was the only kind this package made that nothing
    checked.** `build.md` told every build to run `render.py shots <slug>.html --out <dir>`; there
    was no `--out`, the third argument was parsed as a slide list, and the command crashed in
    `int()` at the step that closes the visual gate. It was reported by an adopting project on
    2026-08-10 (T-074), not by anything here, and the other twelve invocations in the skill were
    correct by luck.

    **What it decides, and what it does not.** It decides that the tool exists, and that every
    subcommand and every flag written down appears in that tool's source. It does **not** decide
    that the tool would accept the whole line: positional arity, flag order, and whether a flag is
    valid for that particular subcommand are all beyond a static read, and executing the line for
    real would launch Chrome. The defect it exists for is a flag or a subcommand the tool has never
    heard of, which is the shape all four found so far have had.
    """
    problems = []
    for block in re.findall(r"```(.*?)```", text, flags=re.S):
        # A trailing backslash continues the command onto the next line, as in `shell.py new`.
        for match in COMMAND_RE.finditer(re.sub(r"\\\n\s*", " ", block)):
            tool, rest = match.group(1), match.group(2)
            path = os.path.join(root, tool)
            if not os.path.isfile(path):
                problems.append("NO SUCH TOOL  %s: %s/%s is invoked and does not exist"
                                % (rel, ROOT_VAR, tool))
                continue
            known = literals(read(path))
            # `<...>` is a placeholder the caller fills in, `[...]` marks an optional group, and
            # `>` is a shell redirect. None is a token the tool ever sees.
            words = [w.strip("[],") for w in re.sub(r"<[^>]*>", " ", rest).split()
                     if not w.startswith(">")]
            for i, word in enumerate(words):
                if word.startswith("-"):
                    what, wanted = "FLAG", word.split("=")[0]
                elif i == 0 and not re.search(r"[./]", word):
                    what, wanted = "SUBCOMMAND", word
                else:
                    continue                      # a positional the caller supplies
                if wanted not in known:
                    problems.append(
                        "UNKNOWN %-6s%s: `%s` is documented for %s, which has no such literal"
                        % (what, rel, wanted, tool))
    return problems


def literals(src):
    """Every string literal in a tool's source — **comments and docstrings excluded, and matched
    whole**.

    Both exclusions were bought with a false pass. The first version searched the raw file for the
    flag between quotes, and the fixture went green against a `render.py` with `--out` deliberately
    removed: the flag was still in the file, in a *comment* quoting the traceback it used to
    produce. A check that reads a mention as an implementation is worse than none (**L-36**), and
    matching whole literals is what makes the answer *the parser compares against this string*
    rather than *this string occurs somewhere*.
    """
    found = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok[0] != tokenize.STRING:
                continue                          # COMMENT is its own type, so comments are out
            text = tok[1]
            if re.match(r"[a-zA-Z]*('''|\"\"\")", text):
                continue                          # a docstring, or an embedded blob of JS or CSS
            try:
                found.add(ast.literal_eval(text))
            except (ValueError, SyntaxError):
                continue
    except (tokenize.TokenError, IndentationError):
        # A tool that will not tokenise is a defect, but it is not this check's to report: the
        # tools all self-test, and reporting every flag as unknown would bury that.
        return found
    return found


# ------------------------------------------------------------------------ self-test (L-04)

# Fixture paths are **assembled, not written**. A path literal here would be read as a pointer
# into this repository by the project's own reference check, and reported dead - nothing
# distinguishes a fictional path in a test table from a real reference in prose. Building them
# from components makes them what they are: structured data, not prose. That is the same
# distinction the reference check already draws for front-matter.
MANIFEST = "/".join((".claude-plugin", "plugin.json"))
SKILL = "/".join(("skills", "example", "SKILL" + ".md"))
STRAY_SKILL = "/".join((".claude-plugin", SKILL))
DOC = "/".join(("docs", "THING" + ".md"))
GONE = "/".join(("docs", "MISSING" + ".md"))
HEAD = "---\nname: example\ndescription: d\n---\n"

# Check 7's fixtures need a tool to invoke and a fenced invocation of it. The tool is a real,
# tokenisable module, because the check reads its string literals rather than its text.
TOOL = "/".join(("tools", "fixture" + ".py"))
TOOL_SRC = ('"""A fixture tool."""\n'
            'import sys\n'
            'if sys.argv[1] == "shots":\n'
            '    sources = "--sources" in sys.argv\n')
FENCE = "\n```\npython " + ROOT_VAR + "/%s %s\n```\n"

FIXTURES = [
    # (label, files, must_fail_with)
    ("a well-formed plugin", {
        MANIFEST: '{"name": "example", "version": "0.1.0"}',
        SKILL: HEAD + "\nBody.\n",
        DOC: "thing",
    }, None),
    ("a load pointer that resolves", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + "Load `%s/%s`.\n" % (ROOT_VAR, DOC),
        DOC: "thing",
    }, None),
    ("a template inside a fence, not a load instruction", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + "```\nC:/somewhere/absolute.md\n```\n",
    }, None),
    ("a manifest whose name is not kebab-case", {
        MANIFEST: '{"name": "Example_Plugin"}',
        SKILL: HEAD + "Body.\n",
    }, "BAD NAME"),
    # The four below are T-061. `author` as a string is what shipped in v0.1.0 and what the
    # installer rejected while this tool printed `OK - manifest valid`; the rest are the same
    # blind spot in the fields either side of it, which presence-testing could never have seen.
    ("an author that is a string, which is what v0.1.0 shipped", {
        MANIFEST: '{"name": "example", "author": "a person"}',
        SKILL: HEAD + "Body.\n",
    }, "BAD TYPE"),
    ("an author object with no name, which the schema requires", {
        MANIFEST: '{"name": "example", "author": {"url": "https://example.com"}}',
        SKILL: HEAD + "Body.\n",
    }, "BAD AUTHOR"),
    ("a well-formed author object", {
        MANIFEST: '{"name": "example", "author": {"name": "a person"}}',
        SKILL: HEAD + "Body.\n",
    }, None),
    ("keywords as a string where the schema says array", {
        MANIFEST: '{"name": "example", "keywords": "deck"}',
        SKILL: HEAD + "Body.\n",
    }, "BAD TYPE"),
    ("a skill pointing at an absolute path", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + "Load /home/user/%s.\n" % DOC,
    }, "ABSOLUTE PATH"),
    ("a load pointer that does not resolve", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + "Load `%s/%s`.\n" % (ROOT_VAR, GONE),
    }, "DEAD POINTER"),
    ("a bare path inside a load instruction", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + "Load `%s` before starting.\n" % DOC,
        DOC: "thing",
    }, "UNBASED PATH"),
    ("a bare path in prose, which the word-keyed version let past", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + "Build to `%s` directly.\n" % DOC,
        DOC: "thing",
    }, "UNBASED PATH"),
    ("a based path is not flagged as bare", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + "Build to `%s/%s` directly.\n" % (ROOT_VAR, DOC),
        DOC: "thing",
    }, None),
    ("a skill directory inside .claude-plugin/", {
        MANIFEST: '{"name": "example"}',
        STRAY_SKILL: HEAD + "Body.\n",
        SKILL: HEAD + "Body.\n",
    }, "MISPLACED"),
    # ---- check 7, and the defect it was built from: `--out` documented, never implemented.
    ("a documented flag the tool does not have", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + FENCE % (TOOL, "shots <slug>.html --out <dir>"),
        TOOL: TOOL_SRC,
    }, "UNKNOWN FLAG"),
    ("a documented subcommand the tool does not have", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + FENCE % (TOOL, "measure <slug>.html"),
        TOOL: TOOL_SRC,
    }, "UNKNOWN SUBCOMMAND"),
    ("a documented command the tool implements", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + FENCE % (TOOL, "shots <slug>.html [--sources <dir>]"),
        TOOL: TOOL_SRC,
    }, None),
    # **The false pass that tightened the check.** `--out` here is only ever mentioned - in a
    # comment, quoting the traceback the missing flag produces - and the first version of check 7
    # read that as an implementation. This fixture is the reason `literals` tokenises.
    ("a flag mentioned in a comment is not a flag the tool has", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + FENCE % (TOOL, "shots <slug>.html --out <dir>"),
        TOOL: TOOL_SRC + "\n# crashes on '--out', which it does not take\n",
    }, "UNKNOWN FLAG"),
    ("an invoked tool that is not there", {
        MANIFEST: '{"name": "example"}',
        SKILL: HEAD + FENCE % (TOOL, "shots <slug>.html"),
    }, "NO SUCH TOOL"),
]

def self_test():
    import shutil
    import tempfile

    failures = 0
    for label, files, expect in FIXTURES:
        tmp = tempfile.mkdtemp(prefix="htmldeck-scaffold-")
        try:
            for rel, content in files.items():
                path = os.path.join(tmp, rel.replace("/", os.sep))
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(content)
            problems, _ = check(tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

        if expect is None:
            good = not problems
            detail = "; ".join(problems)[:70]
        else:
            good = any(p.startswith(expect) for p in problems)
            detail = "expected %s, got: %s" % (expect, "; ".join(problems)[:60] or "nothing")

        failures += 0 if good else 1
        print("  %-4s %-46s %s" % ("ok" if good else "FAIL", label, "" if good else detail))

    print("\n%d of %d fixtures behaved as specified.\n" % (len(FIXTURES) - failures, len(FIXTURES)))
    return failures


def main(argv):
    if "--self-test" in argv:
        return 1 if self_test() else 0

    print("Self-test first - a scan that has not been shown to fail is not evidence (L-04).\n")
    if self_test():
        print("SELF-TEST FAILED - the check itself is wrong; the result below means nothing.")
        return 2

    problems, notes = check(ROOT)
    for note in notes:
        print("  %s" % note)
    print("")
    for problem in problems:
        print("  %s" % problem)

    if problems:
        print("\n%d problem(s)." % len(problems))
        return 1

    print("OK - manifest valid, components at the root, every ${CLAUDE_PLUGIN_ROOT} pointer "
          "resolves,\n     skill body within budget.")
    print("""
This checks the **package**, not the plugin's behaviour. It cannot tell you the skill asks two
questions, stops where it should, or writes the files it promises - those are traced by hand in
T-015 §3 (L-05).""")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
