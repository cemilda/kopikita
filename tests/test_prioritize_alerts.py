"""Urutan prioritas: KEV dulu, lalu severity, lalu EPSS (Lab L1.4)."""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
spec = importlib.util.spec_from_file_location("prioritize_alerts", ROOT / "scripts" / "prioritize_alerts.py")
pa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pa)


def test_urutan_kev_severity_epss():
    alerts = pa.load_json(FIX / "dependabot-alerts.json")
    rows = pa.prioritize(alerts, pa.kev_set(pa.load_json(FIX / "kev.json")),
                         pa.epss_map(pa.load_json(FIX / "epss.json")))
    # 4 (KEV, medium) > 3 (high, EPSS 0.40) > 2 (high, EPSS 0.01) > 1 (medium, EPSS 0.50)
    assert [r["number"] for r in rows] == [4, 3, 2, 1]


def test_keluaran_markdown(capsys):
    pa.main(["--alerts", str(FIX / "dependabot-alerts.json"),
             "--kev", str(FIX / "kev.json"), "--epss", str(FIX / "epss.json")])
    out = capsys.readouterr().out
    assert out.splitlines()[2].startswith("| 1 | #4 | jinja2 | CVE-2099-0004 | YA |")
