# Storage Module - Persistent Storage, Artifacts & Backups
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
  }
}

# 1. S3 Bucket for Automation Artifacts & Test Reports
resource "aws_s3_bucket" "artifacts" {
  bucket        = "${var.environment}-qe-artifacts-${var.account_id}"
  force_destroy = var.force_destroy_buckets

  tags = {
    Name        = "${var.environment}-qe-artifacts"
    Environment = var.environment
    Purpose     = "Test Reports and Allure Results"
  }
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 2. S3 Bucket for Velero Cluster Backups & Disaster Recovery
resource "aws_s3_bucket" "backups" {
  bucket        = "${var.environment}-qe-velero-backups-${var.account_id}"
  force_destroy = var.force_destroy_buckets

  tags = {
    Name        = "${var.environment}-qe-velero-backups"
    Environment = var.environment
    Purpose     = "Kubernetes State and Volume Snapshots"
  }
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Lifecycle policy to transition old backups to Glacier / Infrequent Access
resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    id     = "expire-old-backups"
    status = "Enabled"

    filter {}

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = var.backup_retention_days
    }
  }
}

# 3. EFS File System for ReadWriteMany (RWX) Shared Volumes (Jenkins HA Controller State)
resource "aws_efs_file_system" "jenkins_storage" {
  creation_token = "${var.environment}-jenkins-efs"
  encrypted      = true

  performance_mode = "generalPurpose"
  throughput_mode  = "bursting"

  tags = {
    Name        = "${var.environment}-jenkins-efs"
    Environment = var.environment
  }
}

resource "aws_efs_mount_target" "jenkins" {
  count           = length(var.subnet_ids)
  file_system_id  = aws_efs_file_system.jenkins_storage.id
  subnet_id       = var.subnet_ids[count.index]
  security_groups = [aws_security_group.efs.id]
}

resource "aws_security_group" "efs" {
  name        = "${var.environment}-efs-sg"
  description = "Allow NFS traffic from Kubernetes worker nodes to EFS"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 2049
    to_port     = 2049
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.environment}-efs-sg"
  }
}
