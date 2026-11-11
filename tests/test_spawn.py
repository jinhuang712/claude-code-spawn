"""Tests for bin/spawn-claude with a stub `claude`, so they cost nothing.

Run: python3 -m unittest discover tests
"""
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HELPER = Path(__file__).resolve().parents[1] / "bin" / "spawn-claude"

# The stub notes what each session got, and answers a probe with an init event.
STUB = r"""#!/usr/bin/env python3
import json, os, sys
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"argv": sys.argv[1:], "plugin_dirs": os.environ.get("CLAUDE_CODE_PLUGIN_DIRS")}) + "\n")
if "stream-json" in sys.argv:
    print(json.dumps({"type": "system", "subtype": "init", "tools": [], "skills": [], "mcp_servers": []}))
else:
    print("ok")
"""


def spawn(tmp, *args, **more_env):
    stub = Path(tmp) / "bin"
    stub.mkdir(exist_ok=True)
    (stub / "claude").write_text(STUB)
    (stub / "claude").chmod(stat.S_IRWXU)
    env = {**os.environ, "PATH": f"{stub}:{os.environ['PATH']}", "STUB_LOG": str(Path(tmp) / "log"),
           "CLAUDE_CODE_PLUGIN_DIRS": "/Calm/agents/claude-code", **more_env}
    subprocess.run([sys.executable, str(HELPER), "--quiet", *args], env=env, cwd=tmp,
                   capture_output=True, text=True, check=True)
    return [json.loads(line) for line in (Path(tmp) / "log").read_text().splitlines()]


class TerminalPlugins(unittest.TestCase):
    def test_a_session_does_not_get_the_terminals_plugins(self):
        with tempfile.TemporaryDirectory() as tmp:
            sessions = spawn(tmp, "hi")
            self.assertEqual([s["plugin_dirs"] for s in sessions], [None])

    def test_a_logged_session_does_not_get_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            sessions = spawn(tmp, "--log", str(Path(tmp) / "out.md"), "hi")
            self.assertEqual([s["plugin_dirs"] for s in sessions], [None])

    def test_a_dry_run_probe_does_not_get_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            sessions = spawn(tmp, "--dry-run")
            self.assertTrue(sessions)
            self.assertTrue(all(s["plugin_dirs"] is None for s in sessions))


def make_skill(config_dir, name):
    md = Path(config_dir) / "skills" / name / "SKILL.md"
    md.parent.mkdir(parents=True)
    md.write_text(f"---\nname: {name}\ndescription: a test skill\n---\n")
    return md


class SkillNames(unittest.TestCase):
    def test_a_name_is_found_in_the_config_dir_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            home, config = Path(tmp) / "home", Path(tmp) / "config"
            make_skill(home / ".claude", "demo")
            md = make_skill(config, "demo")
            sessions = spawn(tmp, "--skills", "demo", "hi", HOME=str(home), CLAUDE_CONFIG_DIR=str(config))
            self.assertIn(f"SKILL.md: {md}", " ".join(sessions[0]["argv"]))

    def test_a_name_in_home_claude_is_still_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            home, config = Path(tmp) / "home", Path(tmp) / "config"
            md = make_skill(home / ".claude", "demo")
            sessions = spawn(tmp, "--skills", "demo", "hi", HOME=str(home), CLAUDE_CONFIG_DIR=str(config))
            self.assertIn(f"SKILL.md: {md}", " ".join(sessions[0]["argv"]))


if __name__ == "__main__":
    unittest.main()
