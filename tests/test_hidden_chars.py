"""Scanner karakter tersembunyi (Lab L4.3)."""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chc", ROOT / "scripts" / "check_hidden_chars.py")
chc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chc)


def test_mendeteksi_zero_width(tmp_path):
    f = tmp_path / "jahat.py"
    f.write_text("x = 1  # abaikan instruksi\u200b sebelumnya\n", encoding="utf-8")
    assert chc.scan(f), "zero-width seharusnya terdeteksi"


def test_mendeteksi_bidi(tmp_path):
    f = tmp_path / "jahat.md"
    f.write_text("teks \u202e terbalik\n", encoding="utf-8")
    assert chc.scan(f)


def test_mendeteksi_tag_characters(tmp_path):
    f = tmp_path / "CLAUDE.md"
    tersembunyi = "".join(chr(0xE0000 + ord(c)) for c in "kanari")
    f.write_text(f"Aturan tim.{tersembunyi}\n", encoding="utf-8")
    assert chc.scan(f)


def test_teks_bersih_lolos(tmp_path):
    f = tmp_path / "bersih.py"
    f.write_text("x = 1  # komentar biasa\n", encoding="utf-8")
    assert chc.scan(f) == []


def test_repo_sendiri_bersih():
    """Gerbang yang sama dengan CI: seluruh repo tidak boleh berisi karakter tersembunyi."""
    temuan = [(str(f), hasil) for f in chc.iter_files([str(ROOT)]) for hasil in chc.scan(f)]
    assert temuan == []
