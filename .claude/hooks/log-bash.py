#!/usr/bin/env python3
"""Hook PreToolUse: mencatat setiap perintah Bash dari Claude Code ke log audit (Lab L2.1).

Claude Code mengirim JSON event lewat stdin. Hook ini hanya mencatat (exit 0, tanpa keputusan),
sehingga alur izin normal tetap berlaku. Log: logs/claude-audit.jsonl (di-gitignore).
"""
import datetime
import json
import os
import sys


def main():
    event = json.load(sys.stdin)
    project = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or "."
    log_dir = os.path.join(project, "logs")
    os.makedirs(log_dir, exist_ok=True)
    record = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "session_id": event.get("session_id"),
        "event": event.get("hook_event_name"),
        "tool": event.get("tool_name"),
        "command": (event.get("tool_input") or {}).get("command"),
        "cwd": event.get("cwd"),
    }
    with open(os.path.join(log_dir, "claude-audit.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
