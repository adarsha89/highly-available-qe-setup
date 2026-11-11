output "cluster_name" {
  value       = aws_eks_cluster.qe_cluster.name
  description = "EKS Cluster Name"
}

output "cluster_endpoint" {
  value       = aws_eks_cluster.qe_cluster.endpoint
  description = "EKS API Server Endpoint"
}

output "cluster_certificate_authority_data" {
  value       = aws_eks_cluster.qe_cluster.certificate_authority[0].data
  description = "Base64 encoded certificate data required to communicate with the cluster"
}

output "oidc_provider_arn" {
  value       = aws_iam_openid_connect_provider.cluster.arn
  description = "ARN of the OIDC Provider for ServiceAccount IAM roles"
}
