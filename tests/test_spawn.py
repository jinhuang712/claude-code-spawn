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

# The stub notes what each session got. It answers a probe with an init event, a JSON
# run with a result event that carries a cost, and any other run with plain text.
STUB = r"""#!/usr/bin/env python3
import json, os, sys
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps({"argv": sys.argv[1:], "plugin_dirs": os.environ.get("CLAUDE_CODE_PLUGIN_DIRS")}) + "\n")
if os.environ.get("STUB_PLAIN"):
    print("boom")
elif "stream-json" in sys.argv:
    print(json.dumps({"type": "system", "subtype": "init", "tools": [], "skills": [], "mcp_servers": []}))
elif "json" in sys.argv:
    print(json.dumps({"type": "result", "subtype": "success", "result": "ok", "total_cost_usd": 0.0012}))
else:
    print("ok")
"""


def run(tmp, *args, **more_env):
    stub = Path(tmp) / "bin"
    stub.mkdir(exist_ok=True)
    (stub / "claude").write_text(STUB)
    (stub / "claude").chmod(stat.S_IRWXU)
    env = {**os.environ, "PATH": f"{stub}:{os.environ['PATH']}", "STUB_LOG": str(Path(tmp) / "log"),
           "CLAUDE_CODE_PLUGIN_DIRS": "/Calm/agents/claude-code", **more_env}
    return subprocess.run([sys.executable, str(HELPER), "--quiet", *args], env=env, cwd=tmp,
                          capture_output=True, text=True, check=True)


def spawn(tmp, *args, **more_env):
    run(tmp, *args, **more_env)
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


class LogCost(unittest.TestCase):
    def test_a_log_entry_carries_the_cost_and_the_answer(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "out.md"
            done = run(tmp, "--log", str(log), "--tag", "t1", "hi")
            head, _, body = log.read_text().partition("\n\n")
            self.assertTrue(head.endswith(" t1 model=default exit=0 cost=0.001200"), head)
            self.assertEqual(body.strip(), "ok")
            self.assertEqual(done.stdout, "ok\n")

    def test_the_callers_own_format_goes_through_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "out.md"
            done = run(tmp, "--log", str(log), "hi", "--", "--output-format", "json")
            argv = json.loads((Path(tmp) / "log").read_text().splitlines()[0])["argv"]
            self.assertEqual(argv.count("--output-format"), 1)
            self.assertEqual(json.loads(done.stdout)["result"], "ok")
            self.assertIn(" cost=0.001200", log.read_text().splitlines()[0])

    def test_a_child_that_prints_no_result_is_logged_as_it_is(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "out.md"
            done = run(tmp, "--log", str(log), "hi", STUB_PLAIN="1")
            self.assertEqual(done.stdout, "boom\n")
            self.assertIn("boom", log.read_text())
            self.assertNotIn("cost=", log.read_text())


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
