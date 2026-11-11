output "cluster_role_arn" {
  value       = aws_iam_role.eks_cluster_role.arn
  description = "EKS Cluster IAM Role ARN"
}

output "node_role_arn" {
  value       = aws_iam_role.eks_node_role.arn
  description = "Worker Node IAM Role ARN"
}

output "jenkins_role_arn" {
  value       = aws_iam_role.jenkins_irsa_role.arn
  description = "Jenkins Controller IRSA Role ARN"
}
