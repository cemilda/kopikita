#!/usr/bin/env bash
# Terapkan ruleset branch default dari berkas JSON (Lab L3.4, diperluas di L4.3).
# Pemakaian: scripts/terapkan-ruleset.sh OWNER/REPO
# Perlu gh yang login dengan hak admin repo (dijalankan pemilik repo, BUKAN agen).
set -euo pipefail
REPO="${1:?pakai: scripts/terapkan-ruleset.sh OWNER/REPO}"
FILE=".github/rulesets/main-dilindungi.json"
ID=$(gh api "repos/${REPO}/rulesets" --jq '.[] | select(.name=="main-dilindungi") | .id' || true)
if [ -n "${ID}" ]; then
  gh api -X PUT "repos/${REPO}/rulesets/${ID}" --input "${FILE}" --jq '.name + " diperbarui"'
else
  gh api -X POST "repos/${REPO}/rulesets" --input "${FILE}" --jq '.name + " dibuat"'
fi
