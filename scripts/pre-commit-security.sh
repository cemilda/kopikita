#!/usr/bin/env bash
# Memasang pre-commit hook keamanan untuk repo KopiKita (Demo Sesi 1.3, Lab L1.3).
# Diadaptasi dari resources/module-01-shift-left/scripts/pre-commit-security.sh
# di repo paulasilvatech/Secure-Code-AI-Dev (lisensi MIT).
#
# Hook yang dipasang:
#   - detect-private-key (pre-commit-hooks): menolak kunci privat
#   - detect-secrets (Yelp): menolak rahasia baru di luar baseline
#   - gitleaks: pemindai rahasia berbasis aturan
#   - pip-audit: cek dependensi Python (stage manual, karena repo lab SENGAJA
#     memakai dependensi rentan; dijalankan dengan: pre-commit run pip-audit --hook-stage manual)
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
say() { echo -e "${1}${2}${NC}"; }

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  say "$RED" "Jalankan dari dalam repo git."
  exit 1
fi
cd "$(git rev-parse --show-toplevel)"

if ! command -v pre-commit >/dev/null 2>&1 || ! command -v detect-secrets >/dev/null 2>&1; then
  say "$YELLOW" "Memasang pre-commit dan detect-secrets..."
  pip install -q "pre-commit==4.7.0" "detect-secrets==1.5.0"
fi

cat > .pre-commit-config.yaml <<'EOF'
# Dibuat oleh scripts/pre-commit-security.sh
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: detect-private-key
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks
  - repo: https://github.com/pypa/pip-audit
    rev: v2.10.1
    hooks:
      - id: pip-audit
        args: ["-r", "api/requirements.txt"]
        stages: [manual]
EOF

if [ ! -f .secrets.baseline ]; then
  say "$YELLOW" "Membuat .secrets.baseline (rahasia yang sudah ada dicatat, rahasia baru ditolak)..."
  detect-secrets scan > .secrets.baseline
fi

pre-commit install
pre-commit install-hooks
say "$GREEN" "Hook terpasang. Uji: buat berkas berisi kunci privat palsu lalu git commit."
say "$YELLOW" "Ingat: hook bisa dilewati dengan --no-verify. Push protection di GitHub tetap wajib."
