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

resource "aws_s3_bucket" "menu_assets" {
  bucket = "kopikita-menu-assets-lab"
}

# RENTAN: bucket bisa dibaca publik
resource "aws_s3_bucket_acl" "menu_assets" {
  bucket = aws_s3_bucket.menu_assets.id
  acl    = "public-read"
}

resource "aws_security_group" "api" {
  name        = "kopikita-api"
  description = "Akses ke server API KopiKita"

  # RENTAN: SSH terbuka ke seluruh internet
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
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

# RENTAN: volume data tidak dienkripsi
resource "aws_ebs_volume" "data" {
  availability_zone = "ap-southeast-3a"
  size              = 20
  encrypted         = false
}
