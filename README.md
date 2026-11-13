# claude-code-spawn

> Spawn headless Claude sessions that get only what you name.

A Claude Code skill plus one small command. A session that loads the skill can start child sessions with an exact list of tools, MCP tools, skills, system prompt and model. **Nothing else loads:** no settings · no `CLAUDE.md` · no plugins · no other MCP servers.

## What it does

- 🔒 **Start closed:** the child sees none of your setup unless you name it.
- 🎯 **Exact allowlists:** pick single MCP tools and single skills, which `claude` flags alone cannot do.
- 🧠 **Any model:** run cheap batches on `claude-haiku-5-5` and hard tasks on a bigger model.
- 📝 **Append-only log:** children print and the helper appends, so no child can rewrite the log.
- 🚀 **Parallel batches:** run many children at once with `xargs -P`.
- 🧭 **Self-serve:** your sessions read the skill and write the command themselves.

## Install

```
git clone https://github.com/jinhuang712/claude-code-spawn ~/claude-code-spawn && ln -s ~/claude-code-spawn "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spawn-claude" && ln -s ~/claude-code-spawn/bin/spawn-claude ~/.local/bin/spawn-claude
```

Requirements, update and removal are in [INSTALL.md](INSTALL.md).

## How to use

Ask any Claude Code session for a batch:

> Classify each line of issues.txt as bug, feature or question with haiku. Put the results in report.md.

The session loads the skill and runs something like this:

```
cat issues.txt | xargs -P8 -I{} spawn-claude --quiet --model claude-haiku-5-5 \
  --effort low --max-budget-usd 0.05 --log report.md --tag "{}" "Classify: {}"
```

`report.md` then holds one entry per line of the input:

```
## 2026-11-08T23:24:29 login fails on Safari model=claude-haiku-5-5 exit=0 cost=0.000648

bug
```

Try one call yourself:

```
spawn-claude --dry-run --tools Read --skills nyms
```

## Docs

- [FEATURES.md](FEATURES.md)
- [CLI.md](CLI.md)
- [INSTALL.md](INSTALL.md)
- [CHANGELOG.md](CHANGELOG.md)
- [SKILL.md](SKILL.md)

## License

MIT. See [LICENSE](LICENSE).
