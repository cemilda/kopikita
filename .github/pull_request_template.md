<!-- Template PR KopiKita (Lab L4.3) -->

## Ringkasan

## Jenis perubahan
- [ ] Ditulis manusia
- [ ] Dibantu/ditulis agen AI (beri label `ai-generated`)

## Checklist zero-trust
- [ ] PR buatan agen diberi label `ai-generated` dan punya minimal satu reviewer manusia
- [ ] Tidak mengubah `CLAUDE.md`, `.claude/`, `.github/`, atau `infra/` tanpa review code owner
- [ ] Perubahan pada `tests/` dijelaskan (tidak ada test yang dihapus/dilemahkan tanpa alasan)
- [ ] `pytest -q` hijau; gerbang CI (hidden-chars, policy, IaC) lolos
