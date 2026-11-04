#!/usr/bin/env bash
# Verifikasi tanda tangan dan provenance image sebelum deploy (Lab L3.3b).
# Pakai identitas workflow yang PERSIS, bukan regex .* (yang menerima siapa pun).
set -euo pipefail

IMAGE="${1:?pakai: verify-image.sh ghcr.io/OWNER/REPO@sha256:...}"
REPO="${GITHUB_REPOSITORY:?set GITHUB_REPOSITORY=OWNER/REPO}"
REF="${IMAGE_REF:-refs/heads/main}"

IDENTITY="https://github.com/${REPO}/.github/workflows/release.yml@${REF}"
ISSUER="https://token.actions.githubusercontent.com"

echo "Verifikasi tanda tangan cosign..."
cosign verify \
  --certificate-identity "${IDENTITY}" \
  --certificate-oidc-issuer "${ISSUER}" \
  "${IMAGE}"

echo "Verifikasi provenance attestation..."
gh attestation verify "oci://${IMAGE}" --repo "${REPO}"

echo "OK: isi, asal, dan keutuhan image terbukti. Aman untuk deploy."
