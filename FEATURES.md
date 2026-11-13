# Features

✅ built · 🚧 built, with a gap named beside it · ❔ claimed and not yet run · ⬜ planned

## Summary

```
Features
├── ✅ F1: Spawn — start one headless Claude session
│   ├── ✅ F1.1: Start closed — nothing loads unless named
│   ├── ✅ F1.2: Prompt and model — system prompt · model · effort
│   └── ✅ F1.3: Dry run — see what the child would get
├── 🚧 F2: Allowlists — exactly which tools and skills the child has
│   ├── ✅ F2.1: Built-in tools — Read · Bash · …
│   ├── ✅ F2.2: MCP tools — single tools out of a server
│   └── 🚧 F2.3: Skills — chosen skills only
├── ✅ F3: Output — where results go
│   ├── ✅ F3.1: Append-only log — one locked entry per run
│   └── ✅ F3.2: Parallel batch — many cheap runs at once
└── ❔ F4: Guidance — the calling session builds its own command
    └── ❔ F4.1: The skill — loaded when a session wants to spawn
```

## F1: Spawn

**Status:** ✅

One call of `spawn-claude` starts one `claude -p` session and returns its output and exit code.

### F1.1: Start closed

**Status:** ✅

The child starts with nothing the caller did not name.

- User, project and local settings stay off.
- `CLAUDE.md` files stay out of its context.
- Installed plugins and their skills stay off.
- A plugin your terminal adds stays off, such as Calm's.
- MCP servers from the user's config stay off.

The child still logs in with the user's Claude Code login.

- **Commands:** [spawn-claude](CLI.md#spawn-claude)

**Stories:**

- A session hands a mail chore to a child that never sees the user's personal instructions.

### F1.2: Prompt and model

**Status:** ✅

The caller replaces the default system prompt or appends to it. The caller picks the model, the effort and a fallback model. Turn and dollar caps stop a run that goes too far.

A replaced prompt also makes a batch cheaper, because the children then share one cached prompt. These numbers come from one-turn runs with Claude Code 2.1.323 on `claude-haiku-5-5` with no tools on 2026-11-13:

- With the default prompt each child cost $0.00065.
- With a replaced prompt the first child cost $0.00013.
- With a replaced prompt each later child cost $0.00001.

- **Commands:** [spawn-claude](CLI.md#spawn-claude)

**Stories:**

- A session runs a classification job on `claude-haiku-5-5` at low effort to keep the cost near zero.
- A session gives the child a role prompt in place of the coding-agent prompt.

### F1.3: Dry run

**Status:** ✅

With `--dry-run` the helper starts the child only far enough to list its tools, skills and MCP servers. It prints that list with the final command and exits before any model call.

- **Commands:** [spawn-claude](CLI.md#spawn-claude)

**Stories:**

- A session checks a batch's allowlist once before it starts a hundred runs.

## F2: Allowlists

**Status:** 🚧 skills load without the Skill tool

Each allowlist names what the child gets, and everything else is off. The tools on a list run without an approval prompt. With `--permission-mode` the caller takes over approval instead.

### F2.1: Built-in tools

**Status:** ✅

The caller lists built-in tools such as `Read` or `Bash`. No list means no built-in tools. A skill on the list adds `Read`, since skills load through it.

- **Commands:** [spawn-claude](CLI.md#spawn-claude)

**Stories:**

- A session gives a child only `Read` so it can study files and change none.

### F2.2: MCP tools

**Status:** ✅

The caller passes MCP server configs and names the tools it wants from them. Names may use globs such as `mcp__pw__browser_*`. No names means every tool of those servers.

- A name that matches nothing prints a warning.
- A server that fails to connect prints a warning.
- Each server starts twice per run: once to list its tools and once for the run.

- **Commands:** [spawn-claude](CLI.md#spawn-claude)

**Stories:**

- A session lets a child open and read web pages but never click or type.

### F2.3: Skills

**Status:** 🚧 `$ARGUMENTS` and a skill's own tool permissions do not apply

The caller names each skill by its folder, its `SKILL.md` path or its name. A name is looked up in `$CLAUDE_CONFIG_DIR/skills`, then in `~/.claude/skills`. The child sees only those skills and reads one when a request matches it. An unknown skill stops the call before the child starts.

- **Commands:** [spawn-claude](CLI.md#spawn-claude)

**Stories:**

- A session gives a child the mail skill and nothing else so it cannot wander into other tools.

## F3: Output

**Status:** ✅

The child prints its result. Only the helper writes files.

### F3.1: Append-only log

**Status:** ✅

With `--log` the helper appends the child's output to a file under a lock. Each entry starts with its time, its tag, the model, the exit code and what the run cost in dollars. The cost is missing when the child ended before it reported one. The child has no write tool for that file, so it cannot change earlier entries.

- **Commands:** [spawn-claude](CLI.md#spawn-claude)

**Stories:**

- A session collects the verdicts of many children into one report it reads at the end.
- A session adds up the cost of a trial batch before it starts the full one.

### F3.2: Parallel batch

**Status:** ✅

Many calls run side by side through `xargs -P` or any other runner. Their log entries never interleave. Each run stays under its own turn and dollar caps.

Children that start at the same moment share no cached prompt, so one run before the batch makes the rest cheaper. This holds with a replaced system prompt only. Measured on 2026-11-13 with three children each time:

- Started together with nothing cached: each paid the first-run price.
- Started together after an earlier batch had finished: each paid the later price.

- **Commands:** [spawn-claude](CLI.md#spawn-claude)

**Stories:**

- A session classifies a list of items with eight cheap children at a time.

## F4: Guidance

**Status:** ❔ no other session has used it yet

### F4.1: The skill

**Status:** ❔ no other session has used it yet

`SKILL.md` teaches a session the flags, the limits and a few recipes. The session then writes the command its task needs. A session loads it when it wants to spawn, batch or sandbox a Claude session.

**Stories:**

- A user says "batch this with haiku" and the session writes the right call without being told how.

## Not planned

- **`--bare` mode:** it ignores the Claude Code login and needs an API key.
- **A batch command in the helper:** `xargs` and other runners already do it.
- **Write tools for the shared log:** a child that can write the log can also rewrite it.
