# Install

## Claude Code

Install the managed plugin:

```text
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

For local development, run `claude --plugin-dir /absolute/path/to/engineering-skills`.
The SessionStart hook loads the shared principles. Skill resources use source-relative paths.

## Codex

Clone the repository and use the self-contained installer (Python 3.10 or later):

```bash
git clone https://github.com/int2t05/engineering-skills.git
cd engineering-skills
python scripts/install-skills.py
```

Default destination: `~/.agents/skills`, the user-level Codex discovery location. No symlink permission or Bash is needed for installation, including on Windows.
Select individual skills:

```bash
python scripts/install-skills.py --skill implement --skill debugging
```

Specify an explicit destination for another host or isolated setup:

```bash
python scripts/install-skills.py --dest /absolute/path/to/agent-skills
```

The installer flattens phase folders, copies required shared resources, rewrites local links and includes license and Codex adapters. Installed skills do not need the original checkout.
It does not modify global agent instructions or install a Claude hook. Read the bundled engineering principles when using a skill.

Update after pulling the repository:

```bash
git pull --ff-only
python scripts/install-skills.py --replace
```

Repeated unchanged installation does nothing. Updates affect only installer-owned, unmodified folders; name conflicts, symlinks and local edits cause a diagnostic before installation. Preserve or reconcile local changes before updating.
For removal, remove only the individual installed folders after inspecting local changes. The installer does not manage unrelated skills.

Invoke with `$implement`, `$debugging` or another skill name. Codex discovers changes automatically; restart if the skill picker has not refreshed.

## Other agents

Use the same installer with the host's documented discovery directory. Plain SKILL.md content is portable, but automatic invocation and available tools depend on the host.
Directly copying one source skill omits shared resources. Use the installer for standalone folders or retain the complete repository layout.
Avoid installing the same skill through multiple routes in one host; duplicate names can appear independently.

## Verify

```bash
python scripts/gen-agents-yaml.py
bash scripts/validate-skills.sh
python -m unittest discover -s test -v
```

Tests install into temporary directories. They do not modify your real skill installation.
Official discovery and invocation behavior: [Codex skills](https://learn.chatgpt.com/docs/build-skills).
