package main

import rego.v1

# Kebijakan IaC lintas cloud untuk KopiKita (Lab L4.1), dijalankan dengan Conftest.
#   conftest test -p policy/ infra/main.tf
# Conftest membaca berkas .tf dengan parser HCL2 (hcl2json): setiap blok resource
# menjadi daftar objek, jadi kita iterasi dengan `some r in input.resource.<tipe>[nama]`.

# --- Aturan 1: bucket S3 tidak boleh publik ---
deny contains msg if {
	some name
	some acl in input.resource.aws_s3_bucket_acl[name]
	acl.acl in {"public-read", "public-read-write"}
	msg := sprintf("aws_s3_bucket_acl '%s' memakai ACL %s; bucket tidak boleh publik", [name, acl.acl])
}

# --- Aturan 2: port 22 tidak boleh terbuka ke internet ---
deny contains msg if {
	some name
	some sg in input.resource.aws_security_group[name]
	some rule in sg.ingress
	rule.from_port <= 22
	rule.to_port >= 22
	"0.0.0.0/0" in rule.cidr_blocks
	msg := sprintf("aws_security_group '%s' membuka port 22 ke 0.0.0.0/0", [name])
}

# --- Aturan 3 (bonus): volume EBS wajib terenkripsi ---
deny contains msg if {
	some name
	some vol in input.resource.aws_ebs_volume[name]
	not vol.encrypted == true
	msg := sprintf("aws_ebs_volume '%s' harus encrypted = true", [name])
}
