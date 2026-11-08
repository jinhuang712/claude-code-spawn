# AGENTS.md

This repo is a Claude Code skill (`SKILL.md`) and its helper (`bin/spawn-claude`). Both are the product. The docs below describe them.

## Read order

1. [README.md](README.md)
2. [FEATURES.md](FEATURES.md)
3. [CLI.md](CLI.md)
4. [INSTALL.md](INSTALL.md)
5. [CHANGELOG.md](CHANGELOG.md)

## Layout

| Where | What |
|---|---|
| `SKILL.md` | the skill a session loads, self-contained |
| `bin/` | the helper command |
| the root | the docs and `LICENSE` |

`SKILL.md` repeats facts from the docs on purpose. A session loads it alone, so it must stand alone. When a fact changes, change it in `SKILL.md` too.

## Docs this repo leaves out

The what-we-build skill asks for more docs. The user chose against these on 2026-11-08 because the project is one small script:

- `PROPOSAL.md` · `PHILOSOPHY.md` · `DESIGNS.md`: the principles live in `SKILL.md`.
- `specs/decisions/`: each reason sits beside its rule in `SKILL.md`.
- `GOALS.md` · `ROADMAP.md` · `TODO.md`: no checkpoints yet.
- `CONTRIBUTING.md` · `SECURITY.md`: not yet.

Do not add them back unless the user asks.

## While you work

- Follow these rules strictly unless the user rejects one.
- Read every doc you work on in full.
- Never give a doc to a subagent to read or write.
- When the window is new or was compacted: read the what-we-build skill and its guides in full if it is installed, then every doc in the read order.
- When you are about to change something: read the doc that owns it first.
- When the work needs the code: a subagent may read it.
- When you change a fact or a rule: search the docs and `SKILL.md` for what it now contradicts.
- When the user says something a doc contradicts: say so before you act.
- When you find a contradiction: tell the user and pick no side.
- When other developers build on the project: say it may need a wiki and let the user pick its form.
- When you change something: check what you touched against these rules.
- When a change lands: fix what it left behind in the docs before you report.
- When the user stops you: stop at once with all your agents.

Update only the docs an event affects:

```
What just happened?
├── A requirement was agreed ··· FEATURES
├── A change was done
│   ├── CHANGELOG ·············· what shipped
│   ├── FEATURES ··············· its status
│   ├── CLI ···················· how it is called now
│   ├── README, INSTALL ········ how it is used now
│   └── SKILL.md ··············· what a session must know now
└── A fork was closed ·········· SKILL.md, beside the rule it shapes
```
