---
name: spawn-claude
description: Spawn headless Claude Code sessions (`claude -p`) with an exact allowlist of tools, MCP tools, skills, system prompt and model — one-off or in parallel batches of cheap models, optionally appending results to a shared log. Use when delegating work to an isolated or cheaper Claude process, fanning out many small tasks, or when the user asks to spawn, batch or sandbox a Claude session.
---

# spawn-claude

Compose the command yourself from the task's needs. The helper
`bin/spawn-claude` (next to this file) does the two parts the CLI can't do
directly; everything else is plain `claude` flags.

## Principles

- **Default closed.** Name what the child gets; everything else stays off.
- **Cheapest model that can do it.** `claude-haiku-5-5` + `--effort low` for
  mechanical work; step up only when output quality demands it.
- **Children never write shared state.** They print; the parent appends.
- **Cap cost** with `--max-turns` / `--max-budget-usd` on every batch.
- **Check before a big batch**: `--dry-run` prints the tools, skills and MCP
  servers the child will actually have.

## What each control needs (verified on claude 2.1.319)

| Control | How | Note |
|---|---|---|
| Isolation | `--setting-sources "" --strict-mcp-config`, and no `CLAUDE_CODE_PLUGIN_DIRS` in the env | drops user settings, CLAUDE.md, plugins, user MCP; a terminal such as Calm adds its plugin through that variable, which the helper drops (checked on 2.1.322) |
| Built-in tools | `--tools "Read,Bash"` (`""` = none) | does not touch MCP tools |
| MCP servers | `--mcp-config file.json` | |
| MCP tools | helper `--mcp-tools 'mcp__srv__a,mcp__srv__b_*'` | CLI only filters by deny list; helper probes and denies the rest |
| Skills | helper `--skills name-or-path,...` | CLI can't allowlist skills; helper disables all and injects an index the child Reads; a name is looked up in `$CLAUDE_CONFIG_DIR/skills`, then `~/.claude/skills` |
| System prompt | `--system` / `--system-file` replace, `--append-system[-file]` add | |
| Model | `--model`, `--effort`, `--fallback-model` | |
| Approval | allowlisted tools are pre-approved; else `--permission-mode` | |
| Append-only log | helper `--log FILE --tag LABEL` | locked append, safe in parallel |

Avoid `--bare`: it ignores OAuth login and needs `ANTHROPIC_API_KEY`.

## Helper

```
spawn-claude [prompt] [--prompt-file F]
  [--system T | --system-file F] [--append-system T | --append-system-file F]
  [--tools LIST] [--mcp-config F]... [--mcp-tools GLOBS] [--skills LIST]
  [--model M] [--effort E] [--fallback-model M]
  [--max-turns N] [--max-budget-usd X] [--permission-mode P]
  [--cwd DIR] [--add-dir DIR]... [--log FILE] [--tag T]
  [--dry-run] [--quiet] [-- extra claude args]
```

Prompt comes from the argument, `--prompt-file`, or stdin. Args after `--`
pass to `claude` (e.g. `--output-format json`, `--json-schema ...`,
`--no-session-persistence`). A summary goes to stderr unless `--quiet`.

## Recipes

Isolated one-off with one skill and a replaced system prompt:

```bash
spawn-claude --model claude-haiku-5-5 --effort low \
  --skills himalaya --tools Bash --system-file role.md "List unread mail subjects"
```

Browser task limited to two MCP tools:

```bash
spawn-claude --mcp-config pw.json \
  --mcp-tools 'mcp__pw__browser_navigate,mcp__pw__browser_snapshot' \
  "Open https://example.com and summarize it"
```

Parallel cheap batch, one line of input per job, results appended to one log:

```bash
cat items.txt | xargs -P8 -I{} spawn-claude --quiet \
  --model claude-haiku-5-5 --effort low --max-turns 3 --max-budget-usd 0.05 \
  --tools Read --log report.md --tag "{}" "Classify {}: bug/feature/question" \
  -- --no-session-persistence > /dev/null
```

Structured results for machine merging:

```bash
spawn-claude --model claude-haiku-5-5 --log results.jsonl "..." \
  -- --output-format json --json-schema "$(cat schema.json)"
```

## Known limits

- Skills load via `Read`, not the `Skill` tool; `$ARGUMENTS` substitution and
  skill-scoped tool permissions don't apply.
- `--mcp-tools` starts each MCP server twice (probe + run).
- A child with no tools can still *claim* it did something; trust the log and
  the filesystem, not its words.
