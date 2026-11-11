output "critical_alerts_topic_arn" {
  value       = aws_sns_topic.critical_alerts.arn
  description = "ARN of the SNS topic for critical platform alerts"
}

output "log_group_name" {
  value       = aws_cloudwatch_log_group.qe_platform_logs.name
  description = "Name of the CloudWatch log group"
}
