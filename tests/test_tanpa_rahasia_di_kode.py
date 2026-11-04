"""Mencegah API key KopiKita kembali tertanam di kode (Lab L1.3)."""
import pathlib
import re

POLA_KEY_KOPIKITA = re.compile(r"kopikita_(live|test)_[0-9a-f]{32}")
ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_tidak_ada_key_kopikita_di_api():
    temuan = [
        str(p.relative_to(ROOT))
        for p in (ROOT / "api").rglob("*.py")
        if POLA_KEY_KOPIKITA.search(p.read_text(encoding="utf-8"))
    ]
    assert temuan == [], f"API key tertanam di: {temuan}"


def test_payment_key_dibaca_dari_environment(monkeypatch):
    import importlib

    import config

    monkeypatch.setenv("PAYMENT_API_KEY", "nilai-dari-env")
    importlib.reload(config)
    assert config.PAYMENT_API_KEY == "nilai-dari-env"
