# Monitoring Module - CloudWatch / SNS Alerting Infrastructure
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
  }
}

# 1. CloudWatch Log Group for Platform Audit & CI Logs
resource "aws_cloudwatch_log_group" "qe_platform_logs" {
  name              = "/aws/qe-platform/${var.environment}"
  retention_in_days = var.log_retention_days

  tags = {
    Environment = var.environment
    Component   = "logging"
  }
}

# 2. SNS Alert Topic for High-Availability Incidents (K8s / Jenkins Outages)
resource "aws_sns_topic" "critical_alerts" {
  name = "${var.environment}-qe-critical-alerts"

  tags = {
    Environment = var.environment
    Severity    = "Critical"
  }
}

resource "aws_sns_topic_subscription" "email_sub" {
  count     = length(var.alert_emails)
  topic_arn = aws_sns_topic.critical_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_emails[count.index]
}

# 3. CloudWatch Metric Alarm - EKS Worker Node Not Ready / Node Degradation
resource "aws_cloudwatch_metric_alarm" "node_failure" {
  alarm_name          = "${var.environment}-eks-node-failure"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "node_status_condition"
  namespace           = "ContainerInsights"
  period              = 60
  statistic           = "Minimum"
  threshold           = 1
  alarm_description   = "Triggers when a Kubernetes worker node enters NotReady state in cluster ${var.cluster_name}"
  alarm_actions       = [aws_sns_topic.critical_alerts.arn]

  dimensions = {
    ClusterName = var.cluster_name
    Condition   = "Ready"
    Status      = "True"
  }
}
