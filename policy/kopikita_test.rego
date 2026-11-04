package main

import rego.v1

# Test kebijakan: conftest verify -p policy/
# parse_config("hcl2", ...) adalah builtin Conftest yang mem-parse HCL persis seperti
# saat `conftest test` membaca berkas .tf, sehingga bentuk input di test = bentuk input asli.

test_bucket_publik_ditolak if {
	cfg := parse_config("hcl2", `
		resource "aws_s3_bucket_acl" "menu" {
			acl = "public-read"
		}
	`)
	deny["aws_s3_bucket_acl 'menu' memakai ACL public-read; bucket tidak boleh publik"] with input as cfg
}

test_bucket_privat_lolos if {
	cfg := parse_config("hcl2", `
		resource "aws_s3_bucket_acl" "menu" {
			acl = "private"
		}
	`)
	count(deny) == 0 with input as cfg
}

test_ssh_terbuka_ditolak if {
	cfg := parse_config("hcl2", `
		resource "aws_security_group" "api" {
			ingress {
				from_port   = 22
				to_port     = 22
				cidr_blocks = ["0.0.0.0/0"]
			}
		}
	`)
	deny["aws_security_group 'api' membuka port 22 ke 0.0.0.0/0"] with input as cfg
}

test_ssh_terbatas_lolos if {
	cfg := parse_config("hcl2", `
		resource "aws_security_group" "api" {
			ingress {
				from_port   = 22
				to_port     = 22
				cidr_blocks = [var.admin_cidr]
			}
			ingress {
				from_port   = 443
				to_port     = 443
				cidr_blocks = ["0.0.0.0/0"]
			}
		}
	`)
	count(deny) == 0 with input as cfg
}

test_volume_tanpa_enkripsi_ditolak if {
	cfg := parse_config("hcl2", `
		resource "aws_ebs_volume" "data" {
			size      = 20
			encrypted = false
		}
	`)
	deny["aws_ebs_volume 'data' harus encrypted = true"] with input as cfg
}
