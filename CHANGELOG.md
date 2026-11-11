# Changelog

## Unreleased

### Spawn

You can start a headless Claude Code session that loads none of your settings, `CLAUDE.md` files, plugins or MCP servers. This holds in a terminal that adds a plugin of its own, such as Calm. You pick its system prompt, model and effort. A dry run shows what the session would get before it costs anything.

### Allowlists

You can give the session exactly the built-in tools, single MCP tools and skills you name. Skills load by reading their file, so `$ARGUMENTS` does not work in them.

### Output

You can append each session's output to a shared log under a lock. Parallel runs never mix their entries.

### Skill

Your Claude Code sessions can load the `spawn-claude` skill and write the spawn command on their own.
