output "vpc_id" {
  value       = module.networking.vpc_id
  description = "VPC ID"
}

output "cluster_name" {
  value       = module.kubernetes.cluster_name
  description = "EKS Cluster Name"
}

output "cluster_endpoint" {
  value       = module.kubernetes.cluster_endpoint
  description = "EKS Cluster API Endpoint"
}

output "artifacts_bucket_name" {
  value       = module.storage.artifacts_bucket_name
  description = "S3 bucket for artifacts and reports"
}

output "backups_bucket_name" {
  value       = module.storage.backups_bucket_name
  description = "S3 bucket for Velero disaster recovery backups"
}

output "critical_alerts_topic_arn" {
  value       = module.monitoring.critical_alerts_topic_arn
  description = "SNS topic ARN for critical HA alert notifications"
}
