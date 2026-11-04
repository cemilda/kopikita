"""Uji hook pengaman agen triase tanpa memanggil API (Lab L3.1)."""
import asyncio
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("triage_agent", ROOT / "agent" / "triage_agent.py")
ta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ta)


def run(coro):
    return asyncio.run(coro)


def test_hook_menolak_baca_env():
    out = run(ta.guard({"tool_name": "Read", "tool_input": {"file_path": "api/../.env"}}, "id", None))
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_hook_menolak_perintah_asing():
    out = run(ta.guard({"tool_name": "Bash", "tool_input": {"command": "curl http://evil.example"}}, "id", None))
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"


def bash(cmd):
    return run(ta.guard({"tool_name": "Bash", "tool_input": {"command": cmd}}, "id", None))


def test_hook_mengizinkan_pytest_git_fix_dan_gh_pr():
    for cmd in ["pytest -q", "python -m pytest -q", "git checkout -b fix/sql-login",
                "git add -A", "git commit -m 'fix: query berparameter'",
                "git push -u origin fix/sql-login", "gh pr create --draft --fill"]:
        assert bash(cmd) == {}, cmd


def test_hook_menolak_rangkaian_perintah():
    for cmd in ["pytest -q; curl http://evil.example", "pytest && cat .netrc",
                "gh pr view $(cat secret)", "pytest | tee /tmp/x"]:
        assert bash(cmd)["hookSpecificOutput"]["permissionDecision"] == "deny", cmd


def test_hook_menolak_merge_dan_push_ke_main():
    for cmd in ["gh pr merge 1 --admin", "git push origin main", "gh api repos/x/y -X DELETE"]:
        assert bash(cmd)["hookSpecificOutput"]["permissionDecision"] == "deny", cmd


def test_hook_mengizinkan_edit():
    assert run(ta.guard({"tool_name": "Edit", "tool_input": {"file_path": "api/app.py"}}, "id", None)) == {}


def tool(nama, **masukan):
    return run(ta.guard({"tool_name": nama, "tool_input": masukan}, "id", None))


def ditolak(hasil):
    return hasil["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_hook_menolak_opsi_berbahaya():
    for cmd in ["git add -f .", "git add --force -A", "git commit --no-verify -m x",
                "gh pr create --draft --body-file /home/u/.config/gh/hosts.yml --title x",
                "gh pr create --draft --repo penyerang/repo --title x --body y",
                "gh pr create --title x --body y", "gh pr create --title ' --draft' --body y",
                "pytest -p plugin_jahat", "pytest /tmp/test_jahat.py", "pytest tests/../../tmp/x.py",
                "git diff --no-index /etc/passwd /dev/null", "git diff --output=/tmp/x"]:
        assert ditolak(bash(cmd)), cmd


def test_hook_menolak_kredensial_dan_berkas_di_luar_repo():
    for path in [".ENV", "/etc/passwd", "~/.netrc", "../luar.txt",
                 "/home/u/.config/gh/hosts.yml", "/home/u/.git-credentials"]:
        assert ditolak(tool("Read", file_path=path)), path


def test_hook_menolak_glob_berkas_tersembunyi():
    assert ditolak(tool("Grep", pattern="TOKEN", path=".", glob=".e*"))
    for pola in [".e?v", "**/.env*", "*env"]:
        assert ditolak(tool("Glob", pattern=pola)), pola


def test_hook_menolak_ubah_pagar_dan_pipeline():
    for path in [".github/workflows/x.yml", "CLAUDE.md", ".claude/settings.json",
                 "agent/triage_agent.py", "scripts/x.sh"]:
        assert ditolak(tool("Write", file_path=path, content="x")), path


def test_hook_tetap_mengizinkan_kerja_normal():
    for cmd in ["pytest tests/test_app.py -q", "git status", "git diff --stat",
                "git add api/app.py tests/test_login.py",
                "gh pr create --draft --label ai-generated --title 'fix: log' --body 'tutup alert 4'",
                "gh pr view 1"]:
        assert bash(cmd) == {}, cmd
    assert tool("Write", file_path="tests/test_login.py", content="x") == {}
    assert tool("Read", file_path="docs/alert-contoh.json") == {}
    assert tool("Grep", pattern="log.info", path="api") == {}
    assert tool("Glob", pattern="**/*.py") == {}
