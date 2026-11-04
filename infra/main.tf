# Infrastruktur KopiKita di AWS (Jakarta).
# PERINGATAN: SENGAJA berisi salah konfigurasi untuk Lab L3.4 dan L4.1. Jangan di-apply.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type    = string
  default = "ap-southeast-3"
}

variable "admin_cidr" {
  type    = string
  default = "10.0.0.0/8"
}

resource "aws_s3_bucket" "menu_assets" {
  bucket = "kopikita-menu-assets-lab"
}

resource "aws_s3_bucket_public_access_block" "menu_assets" {
  bucket                  = aws_s3_bucket.menu_assets.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_security_group" "api" {
  name        = "kopikita-api"
  description = "Akses ke server API KopiKita"

  # SSH hanya dari CIDR kantor/VPN (ganti dengan rentang Anda).
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Keluar"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Volume data dienkripsi at rest (CKV_AWS_3).
resource "aws_ebs_volume" "data" {
  availability_zone = "ap-southeast-3a"
  size              = 20
  encrypted         = true
}
