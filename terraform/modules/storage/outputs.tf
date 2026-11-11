output "artifacts_bucket_name" {
  value       = aws_s3_bucket.artifacts.id
  description = "S3 bucket for automation artifacts and reports"
}

output "artifacts_bucket_arn" {
  value       = aws_s3_bucket.artifacts.arn
  description = "ARN of the artifacts bucket"
}

output "backups_bucket_name" {
  value       = aws_s3_bucket.backups.id
  description = "S3 bucket for cluster Velero backups"
}

output "backups_bucket_arn" {
  value       = aws_s3_bucket.backups.arn
  description = "ARN of the backups bucket"
}

output "efs_id" {
  value       = aws_efs_file_system.jenkins_storage.id
  description = "ID of the shared EFS file system for Jenkins HA"
}
