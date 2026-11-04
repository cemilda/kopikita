"""Metrik laporan risiko dihitung oleh kode, bukan AI (Lab L4.2)."""
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("risk_report", ROOT / "scripts" / "risk_report.py")
rr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rr)
ALERTS = json.loads((ROOT / "tests" / "fixtures" / "alerts.json").read_text(encoding="utf-8"))


def test_backlog_per_severity():
    assert rr.build(ALERTS)["backlog_per_severity"] == {"critical": 1, "high": 2}


def test_mttr_rata_rata():
    # (4 hari + 2 hari) / 2 = 3.0
    assert rr.build(ALERTS)["mttr_hari"] == 3.0


def test_dismissed_tanpa_alasan_terdeteksi():
    assert rr.build(ALERTS)["dismissed_tanpa_alasan"] == 1


def test_tiga_risiko_teratas_urut_severity_lalu_umur():
    top = rr.build(ALERTS)["top_risiko"]
    assert [r["number"] for r in top] == [1, 2, 5]
    assert top[0]["rule"] == "py/sql-injection"
