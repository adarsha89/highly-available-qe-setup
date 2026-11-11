# AWS Root Module - High Availability QE Platform Orchestration

# 1. Networking (Multi-AZ VPC, Subnets, NAT Gateways)
module "networking" {
  source             = "../modules/networking"
  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  cluster_name       = var.cluster_name
  single_nat_gateway = var.use_localstack ? true : false
}

# 2. IAM Roles & ServiceAccount Federation
module "iam" {
  source            = "../modules/iam"
  environment       = var.environment
  oidc_provider_arn = var.use_localstack ? "" : module.kubernetes.oidc_provider_arn
  oidc_provider_url = var.use_localstack ? "" : module.kubernetes.cluster_endpoint
}

# 3. Persistent Storage, Artifacts & Backups
module "storage" {
  source      = "../modules/storage"
  environment = var.environment
  vpc_id      = module.networking.vpc_id
  subnet_ids  = module.networking.private_subnet_ids
}

# 4. Kubernetes (EKS HA Cluster)
module "kubernetes" {
  source             = "../modules/kubernetes"
  environment        = var.environment
  cluster_name       = var.cluster_name
  vpc_id             = module.networking.vpc_id
  subnet_ids         = module.networking.private_subnet_ids
  cluster_role_arn   = module.iam.cluster_role_arn
  node_role_arn      = module.iam.node_role_arn
  desired_node_count = var.desired_node_count
  min_node_count     = var.min_node_count
  max_node_count     = var.max_node_count
}

# 5. Monitoring & CloudWatch/SNS Alerting
module "monitoring" {
  source        = "../modules/monitoring"
  environment   = var.environment
  cluster_name  = var.cluster_name
  alert_emails  = var.alert_emails
}
