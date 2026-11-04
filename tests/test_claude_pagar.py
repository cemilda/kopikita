"""Memastikan pagar Claude Code di repo tidak melemah tanpa sengaja (Lab L2.1)."""
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SETTINGS = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))


def test_deny_rule_rahasia_dan_jaringan():
    deny = SETTINGS["permissions"]["deny"]
    for rule in ["Read(./.env*)", "Read(~/.ssh/**)", "Read(~/.aws/**)", "Bash(curl *)"]:
        assert rule in deny


def test_git_push_harus_ditanya():
    assert "Bash(git push *)" in SETTINGS["permissions"]["ask"]


def test_sandbox_aktif_dengan_domain_minimal():
    sandbox = SETTINGS["sandbox"]
    assert sandbox["enabled"] is True
    assert "github.com" in sandbox["network"]["allowedDomains"]
    assert "*" not in sandbox["network"]["allowedDomains"]


def test_hook_mencatat_perintah(tmp_path):
    event = {
        "session_id": "uji",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "pytest -q"},
        "cwd": str(tmp_path),
    }
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(tmp_path))
    result = subprocess.run(
        [sys.executable, str(ROOT / ".claude" / "hooks" / "log-bash.py")],
        input=json.dumps(event), text=True, env=env, capture_output=True, check=False,
    )
    assert result.returncode == 0
    line = (tmp_path / "logs" / "claude-audit.jsonl").read_text(encoding="utf-8").strip()
    assert json.loads(line)["command"] == "pytest -q"
