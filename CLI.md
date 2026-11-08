# CLI

`spawn-claude` is called by a Claude Code session most of the time. A script calls it in a batch, and a person calls it to try a setup.

Status: ✅ built · ⬜ planned

## Commands

### spawn-claude

**Status:** ✅

`spawn-claude [flags] [prompt] [-- claude flags]`

The prompt comes from the argument first, then `--prompt-file`, then stdin.

| Flag | Means | Default |
|---|---|---|
| `--prompt-file F` | read the prompt from a file | — |
| `--system T` · `--system-file F` | replace the system prompt | the Claude Code prompt |
| `--append-system T` · `--append-system-file F` | add to the system prompt | — |
| `--tools LIST` | comma list of built-in tools (repeatable) | none |
| `--mcp-config F` | MCP server config file or JSON string, repeatable | none |
| `--mcp-tools GLOBS` | MCP tools to keep, comma list | every tool of the given servers |
| `--skills LIST` | skill folders · `SKILL.md` paths · names in `~/.claude/skills` | none |
| `--model M` | model of the child | the Claude Code default |
| `--effort E` | `low` · `medium` · `high` · `xhigh` · `max` | the Claude Code default |
| `--fallback-model M` | model to use when the first is overloaded | — |
| `--max-turns N` | turn cap | none |
| `--max-budget-usd X` | dollar cap | none |
| `--permission-mode P` | approval mode, in place of pre-approving the allowlist | allowlist pre-approved |
| `--cwd DIR` | working folder of the child | current folder |
| `--add-dir DIR` | extra folder the child may reach, repeatable | — |
| `--log FILE` | append the output to this file under a lock | — |
| `--tag T` | label of the log entry | — |
| `--dry-run` | list what the child gets and exit | off |
| `--quiet` | no summary on stderr | off |

Everything after `--` goes to `claude` unchanged, such as `--output-format json`.

**Called by:** both

**Prints:**

- stdout: the child's output as `claude -p` prints it.
- stderr: one summary line starting with `spawn-claude:` unless `--quiet`.
- stderr: a warning for an MCP server that failed to connect.
- stderr: a warning for an `--mcp-tools` pattern that matched nothing.

**Fails:**

- `claude` is not on `PATH`: exit 2.
- A skill is not found: exit 2.
- `--mcp-tools` without `--mcp-config`: exit 2.
- No prompt and stdin is a terminal: exit 2.
- The child never reported its tools: exit 2.
- A flag is wrong: exit 2.
- The child fails: its own exit code.

**Example:**

```
$ spawn-claude --quiet --model claude-haiku-5-5 --effort low "What is 3 squared? Digits only."
9
```

## Exit codes

| Code | Means |
|---|---|
| 0 | the child finished · or the dry run printed |
| 2 | the helper refused the call before the child ran |
| other | the child's own exit code |

## Output formats

**Summary line** on stderr:

```
spawn-claude: {"model": …, "effort": …, "tools": […], "mcp_tools": […], "skills": […], "system_prompt": "replaced" | "default"}
```

**Dry run** on stdout: the summary as indented JSON with three more keys, then the final command on one line.

- `probed_tools`: the tools the child would have.
- `probed_skills`: the skills Claude Code itself would list, always empty.
- `probed_mcp_servers`: each server with its `name` and `status`.

**Log entry** in the `--log` file, one per run:

```
## <YYYY-MM-DDTHH:MM:SS> <tag> model=<model> exit=<code>

<the child's stdout>
```

## Environment

| Variable | Means | Default |
|---|---|---|
| `PATH` | where `claude` is found | — |
