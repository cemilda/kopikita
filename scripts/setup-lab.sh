#!/usr/bin/env bash
# Menyiapkan lingkungan lab KopiKita di laptop peserta.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r api/requirements.txt -r requirements-dev.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Berkas .env dibuat dari .env.example (nilai palsu untuk latihan)."
fi

python api/db.py
pytest -q
echo
echo "Siap. Jalankan API dengan: source .venv/bin/activate && python api/app.py"
