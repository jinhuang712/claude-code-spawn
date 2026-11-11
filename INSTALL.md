# Install

You need these first:

- Claude Code, logged in. Tested with 2.1.319.
- Python 3 on `PATH` as `python3`.
- macOS or Linux, since the log lock uses `flock`.

## From a clone

1. Clone the repo anywhere.
2. Link the folder as a skill so sessions can load it. Skills live in the Claude Code config dir: `$CLAUDE_CONFIG_DIR` when set, else `~/.claude`.
3. Link the command onto your `PATH`.

```
git clone https://github.com/jinhuang712/claude-code-spawn ~/claude-code-spawn
ln -s ~/claude-code-spawn "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spawn-claude"
ln -s ~/claude-code-spawn/bin/spawn-claude ~/.local/bin/spawn-claude
```

Check it worked: `spawn-claude --dry-run --tools Read` prints JSON with `"probed_tools": ["Read"]`. A new Claude Code session lists `spawn-claude` among its skills.

## Update

Run `git pull` in the clone. The links keep pointing at it.

## Remove

Delete the two links and the clone.

```
rm "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/spawn-claude" ~/.local/bin/spawn-claude
```

## When it fails

- **`command not found: spawn-claude`:** `~/.local/bin` is not on your `PATH`. Add it or link the command into a folder that is.
- **`spawn-claude: claude not on PATH`:** the shell that runs the helper cannot find Claude Code. Install it or fix `PATH`.
- **`spawn-claude: probe got no init event`:** Claude Code did not start. Run `claude -p hi` to see its own error.
