# Terraform Engineer - Examples

This document provides detailed, production-ready examples for the terraform-engineer skill.

---

## Example 1: Multi-Tier AWS Web Application

**Scenario:** Deploy a scalable 3-tier web application on AWS with high availability, auto-scaling, and RDS database.

### Project Structure
```
terraform-aws-webapp/
├── main.tf
├── variables.tf
├── outputs.tf
├── backend.tf
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── compute/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── database/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── dev.tfvars
    ├── staging.tfvars
    └── production.tfvars
```

### Backend Configuration
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "aws-webapp/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456789012:key/abc123"
    dynamodb_table = "terraform-state-lock"
  }
  
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### Networking Module
```hcl
# modules/networking/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-vpc"
    }
  )
}

# Public subnets for load balancer
resource "aws_subnet" "public" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.availability_zones[count.index]
  
  map_public_ip_on_launch = true
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-public-${count.index + 1}"
      Tier = "Public"
    }
  )
}

# Private subnets for application tier
resource "aws_subnet" "private_app" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-private-app-${count.index + 1}"
      Tier = "Application"
    }
  )
}

# Private subnets for database tier
resource "aws_subnet" "private_db" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 20)
  availability_zone = var.availability_zones[count.index]
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-private-db-${count.index + 1}"
      Tier = "Database"
    }
  )
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-igw"
    }
  )
}

# NAT Gateways for private subnets
resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? length(var.availability_zones) : 0
  domain = "vpc"
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-nat-eip-${count.index + 1}"
    }
  )
  
  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat_gateway ? length(var.availability_zones) : 0
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-nat-${count.index + 1}"
    }
  )
}

# Route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-public-rt"
    }
  )
}

resource "aws_route_table" "private" {
  count  = length(var.availability_zones)
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = var.enable_nat_gateway ? aws_nat_gateway.main[count.index].id : null
  }
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-private-rt-${count.index + 1}"
    }
  )
}

# Route table associations
resource "aws_route_table_association" "public" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_app" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.private_app[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

resource "aws_route_table_association" "private_db" {
  count          = length(var.availability_zones)
  subnet_id      = aws_subnet.private_db[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# Outputs
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_app_subnet_ids" {
  description = "List of private application subnet IDs"
  value       = aws_subnet.private_app[*].id
}

output "private_db_subnet_ids" {
  description = "List of private database subnet IDs"
  value       = aws_subnet.private_db[*].id
}
```

### Compute Module
```hcl
# modules/compute/main.tf

# Application Load Balancer
resource "aws_lb" "app" {
  name               = "${var.project_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids
  
  enable_deletion_protection = var.environment == "production"
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-alb"
    }
  )
}

# Target Group
resource "aws_lb_target_group" "app" {
  name     = "${var.project_name}-${var.environment}-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  deregistration_delay = 30
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-tg"
    }
  )
}

# Listener
resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = var.certificate_arn
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Launch Template
resource "aws_launch_template" "app" {
  name_prefix   = "${var.project_name}-${var.environment}-"
  image_id      = var.ami_id
  instance_type = var.instance_type
  
  vpc_security_group_ids = [aws_security_group.app.id]
  
  iam_instance_profile {
    name = aws_iam_instance_profile.app.name
  }
  
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
    db_endpoint = var.db_endpoint
    region      = var.region
  }))
  
  monitoring {
    enabled = true
  }
  
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  
  tag_specifications {
    resource_type = "instance"
    
    tags = merge(
      var.common_tags,
      {
        Name = "${var.project_name}-${var.environment}-app"
      }
    )
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name                = "${var.project_name}-${var.environment}-asg"
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300
  
  min_size         = var.min_size
  max_size         = var.max_size
  desired_capacity = var.desired_capacity
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupTotalInstances"
  ]
  
  tag {
    key                 = "Name"
    value               = "${var.project_name}-${var.environment}-app"
    propagate_at_launch = true
  }
  
  dynamic "tag" {
    for_each = var.common_tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
  
  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Policies
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "${var.project_name}-${var.environment}-scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_policy" "scale_down" {
  name                   = "${var.project_name}-${var.environment}-scale-down"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.app.name
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.project_name}-${var.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "70"
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
  
  alarm_description = "Scale up if CPU > 70%"
  alarm_actions     = [aws_autoscaling_policy.scale_up.arn]
}

resource "aws_cloudwatch_metric_alarm" "low_cpu" {
  alarm_name          = "${var.project_name}-${var.environment}-low-cpu"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "30"
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
  
  alarm_description = "Scale down if CPU < 30%"
  alarm_actions     = [aws_autoscaling_policy.scale_down.arn]
}

# Security Groups
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-${var.environment}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = var.vpc_id
  
  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-alb-sg"
    }
  )
}

resource "aws_security_group" "app" {
  name        = "${var.project_name}-${var.environment}-app-sg"
  description = "Security group for application servers"
  vpc_id      = var.vpc_id
  
  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-app-sg"
    }
  )
}

# Outputs
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.app.dns_name
}

output "alb_arn" {
  description = "ARN of the load balancer"
  value       = aws_lb.app.arn
}

output "asg_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.app.name
}
```

### Database Module
```hcl
# modules/database/main.tf

# DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-db-subnet-group"
  subnet_ids = var.subnet_ids
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-db-subnet-group"
    }
  )
}

# Security Group
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-${var.environment}-rds-sg"
  description = "Security group for RDS instance"
  vpc_id      = var.vpc_id
  
  ingress {
    description     = "MySQL from application tier"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = var.app_security_group_ids
  }
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-rds-sg"
    }
  )
}

# Get database password from Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = var.db_password_secret_id
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-${var.environment}-db"
  engine         = "mysql"
  engine_version = "8.0.35"
  instance_class = var.instance_class
  
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = var.kms_key_id
  
  db_name  = var.database_name
  username = var.master_username
  password = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)["password"]
  
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  
  multi_az               = var.multi_az
  publicly_accessible    = false
  backup_retention_period = var.backup_retention_period
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  enabled_cloudwatch_logs_exports = ["error", "general", "slowquery"]
  
  auto_minor_version_upgrade = true
  deletion_protection        = var.environment == "production"
  skip_final_snapshot       = var.environment != "production"
  final_snapshot_identifier = var.environment == "production" ? "${var.project_name}-${var.environment}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null
  
  performance_insights_enabled    = true
  performance_insights_kms_key_id = var.kms_key_id
  performance_insights_retention_period = 7
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-db"
    }
  )
  
  lifecycle {
    prevent_destroy = true
    ignore_changes  = [final_snapshot_identifier]
  }
}

# Read Replica (production only)
resource "aws_db_instance" "replica" {
  count = var.environment == "production" && var.create_read_replica ? 1 : 0
  
  identifier          = "${var.project_name}-${var.environment}-db-replica"
  replicate_source_db = aws_db_instance.main.identifier
  instance_class      = var.replica_instance_class
  
  publicly_accessible = false
  skip_final_snapshot = true
  
  performance_insights_enabled = true
  performance_insights_kms_key_id = var.kms_key_id
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-db-replica"
      Type = "ReadReplica"
    }
  )
}

# Outputs
output "db_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
}

output "db_name" {
  description = "Database name"
  value       = aws_db_instance.main.db_name
}

output "replica_endpoint" {
  description = "Read replica endpoint"
  value       = var.environment == "production" && var.create_read_replica ? aws_db_instance.replica[0].endpoint : null
}
```

### Main Configuration
```hcl
# main.tf
provider "aws" {
  region = var.region
  
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      CostCenter  = var.cost_center
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

# Networking
module "networking" {
  source = "./modules/networking"
  
  project_name        = var.project_name
  environment         = var.environment
  vpc_cidr            = var.vpc_cidr
  availability_zones  = slice(data.aws_availability_zones.available.names, 0, 3)
  enable_nat_gateway  = var.enable_nat_gateway
  common_tags         = local.common_tags
}

# Compute
module "compute" {
  source = "./modules/compute"
  
  project_name      = var.project_name
  environment       = var.environment
  vpc_id            = module.networking.vpc_id
  public_subnet_ids = module.networking.public_subnet_ids
  private_subnet_ids = module.networking.private_app_subnet_ids
  
  ami_id           = var.ami_id
  instance_type    = var.instance_type
  min_size         = var.min_size
  max_size         = var.max_size
  desired_capacity = var.desired_capacity
  certificate_arn  = var.certificate_arn
  
  db_endpoint  = module.database.db_endpoint
  region       = var.region
  common_tags  = local.common_tags
}

# Database
module "database" {
  source = "./modules/database"
  
  project_name            = var.project_name
  environment             = var.environment
  vpc_id                  = module.networking.vpc_id
  subnet_ids              = module.networking.private_db_subnet_ids
  app_security_group_ids  = [module.compute.app_security_group_id]
  
  instance_class          = var.db_instance_class
  allocated_storage       = var.db_allocated_storage
  max_allocated_storage   = var.db_max_allocated_storage
  database_name           = var.database_name
  master_username         = var.db_master_username
  db_password_secret_id   = var.db_password_secret_id
  kms_key_id              = var.kms_key_id
  
  multi_az                = var.environment == "production"
  backup_retention_period = var.environment == "production" ? 30 : 7
  create_read_replica     = var.environment == "production"
  replica_instance_class  = var.db_replica_instance_class
  
  common_tags = local.common_tags
}

# Outputs
output "application_url" {
  description = "Application load balancer URL"
  value       = "https://${module.compute.alb_dns_name}"
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = module.database.db_endpoint
  sensitive   = true
}
```

### Environment Variables
```hcl
# environments/production.tfvars
project_name = "webapp"
environment  = "production"
region       = "us-east-1"
cost_center  = "engineering"

# Networking
vpc_cidr           = "10.0.0.0/16"
enable_nat_gateway = true

# Compute
instance_type    = "t3.medium"
min_size         = 3
max_size         = 10
desired_capacity = 3

# Database
db_instance_class       = "db.r6g.xlarge"
db_allocated_storage    = 100
db_max_allocated_storage = 1000
db_replica_instance_class = "db.r6g.large"
```

### Testing
```go
// tests/aws_webapp_test.go
package test

import (
    "testing"
    "time"
    
    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/gruntwork-io/terratest/modules/terraform"
    http_helper "github.com/gruntwork-io/terratest/modules/http-helper"
    "github.com/stretchr/testify/assert"
)

func TestAWSWebApp(t *testing.T) {
    t.Parallel()
    
    terraformOptions := &terraform.Options{
        TerraformDir: "../",
        VarFiles:     []string{"environments/dev.tfvars"},
        Vars: map[string]interface{}{
            "ami_id": aws.GetMostRecentAmiId(t, "us-east-1", aws.CanonicalAccountId, map[string]string{
                "name": "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*",
            }),
        },
    }
    
    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)
    
    // Validate VPC
    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)
    
    // Validate ALB
    albUrl := terraform.Output(t, terraformOptions, "application_url")
    http_helper.HttpGetWithRetry(
        t,
        albUrl,
        nil,
        200,
        "expected content",
        30,
        10*time.Second,
    )
    
    // Validate RDS
    dbEndpoint := terraform.Output(t, terraformOptions, "database_endpoint")
    assert.Contains(t, dbEndpoint, "rds.amazonaws.com")
}
```

---

## Example 2: Azure Landing Zone

**Scenario:** Create an Azure landing zone with hub-spoke network topology, shared services, and governance.

### Project Structure
```
azure-landing-zone/
├── main.tf
├── variables.tf
├── outputs.tf
├── backend.tf
├── modules/
│   ├── hub/
│   ├── spoke/
│   ├── shared-services/
│   └── governance/
└── spokes/
    ├── production/
    ├── staging/
    └── development/
```

### Hub Module
```hcl
# modules/hub/main.tf
resource "azurerm_resource_group" "hub" {
  name     = "${var.organization}-${var.environment}-hub-rg"
  location = var.location
  
  tags = var.common_tags
}

# Hub Virtual Network
resource "azurerm_virtual_network" "hub" {
  name                = "${var.organization}-${var.environment}-hub-vnet"
  resource_group_name = azurerm_resource_group.hub.name
  location            = azurerm_resource_group.hub.location
  address_space       = [var.hub_vnet_cidr]
  
  tags = var.common_tags
}

# Subnets
resource "azurerm_subnet" "gateway" {
  name                 = "GatewaySubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = [var.gateway_subnet_cidr]
}

resource "azurerm_subnet" "firewall" {
  name                 = "AzureFirewallSubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = [var.firewall_subnet_cidr]
}

resource "azurerm_subnet" "bastion" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.hub.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = [var.bastion_subnet_cidr]
}

# Azure Firewall
resource "azurerm_public_ip" "firewall" {
  name                = "${var.organization}-${var.environment}-fw-pip"
  resource_group_name = azurerm_resource_group.hub.name
  location            = azurerm_resource_group.hub.location
  allocation_method   = "Static"
  sku                 = "Standard"
  
  tags = var.common_tags
}

resource "azurerm_firewall" "hub" {
  name                = "${var.organization}-${var.environment}-fw"
  resource_group_name = azurerm_resource_group.hub.name
  location            = azurerm_resource_group.hub.location
  sku_name            = "AZFW_VNet"
  sku_tier            = "Standard"
  
  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.firewall.id
    public_ip_address_id = azurerm_public_ip.firewall.id
  }
  
  tags = var.common_tags
}

# Azure Bastion
resource "azurerm_public_ip" "bastion" {
  name                = "${var.organization}-${var.environment}-bastion-pip"
  resource_group_name = azurerm_resource_group.hub.name
  location            = azurerm_resource_group.hub.location
  allocation_method   = "Static"
  sku                 = "Standard"
  
  tags = var.common_tags
}

resource "azurerm_bastion_host" "hub" {
  name                = "${var.organization}-${var.environment}-bastion"
  resource_group_name = azurerm_resource_group.hub.name
  location            = azurerm_resource_group.hub.location
  
  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.bastion.id
    public_ip_address_id = azurerm_public_ip.bastion.id
  }
  
  tags = var.common_tags
}

# VPN Gateway (optional)
resource "azurerm_public_ip" "vpn" {
  count = var.enable_vpn ? 1 : 0
  
  name                = "${var.organization}-${var.environment}-vpn-pip"
  resource_group_name = azurerm_resource_group.hub.name
  location            = azurerm_resource_group.hub.location
  allocation_method   = "Static"
  sku                 = "Standard"
  
  tags = var.common_tags
}

resource "azurerm_virtual_network_gateway" "vpn" {
  count = var.enable_vpn ? 1 : 0
  
  name                = "${var.organization}-${var.environment}-vpn-gw"
  resource_group_name = azurerm_resource_group.hub.name
  location            = azurerm_resource_group.hub.location
  
  type     = "Vpn"
  vpn_type = "RouteBased"
  
  active_active = false
  enable_bgp    = false
  sku           = "VpnGw1"
  
  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.vpn[0].id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
  
  tags = var.common_tags
}

# Outputs
output "hub_vnet_id" {
  value = azurerm_virtual_network.hub.id
}

output "hub_vnet_name" {
  value = azurerm_virtual_network.hub.name
}

output "firewall_private_ip" {
  value = azurerm_firewall.hub.ip_configuration[0].private_ip_address
}
```

### Spoke Module
```hcl
# modules/spoke/main.tf
resource "azurerm_resource_group" "spoke" {
  name     = "${var.organization}-${var.spoke_name}-rg"
  location = var.location
  
  tags = merge(
    var.common_tags,
    {
      Spoke = var.spoke_name
    }
  )
}

# Spoke Virtual Network
resource "azurerm_virtual_network" "spoke" {
  name                = "${var.organization}-${var.spoke_name}-vnet"
  resource_group_name = azurerm_resource_group.spoke.name
  location            = azurerm_resource_group.spoke.location
  address_space       = [var.spoke_vnet_cidr]
  
  tags = merge(
    var.common_tags,
    {
      Spoke = var.spoke_name
    }
  )
}

# Subnets
resource "azurerm_subnet" "workload" {
  count = length(var.workload_subnets)
  
  name                 = var.workload_subnets[count.index].name
  resource_group_name  = azurerm_resource_group.spoke.name
  virtual_network_name = azurerm_virtual_network.spoke.name
  address_prefixes     = [var.workload_subnets[count.index].cidr]
  
  # Service endpoints
  service_endpoints = var.workload_subnets[count.index].service_endpoints
  
  # Delegation (if needed for ACI, AKS, etc.)
  dynamic "delegation" {
    for_each = var.workload_subnets[count.index].delegation != null ? [1] : []
    content {
      name = "delegation"
      service_delegation {
        name    = var.workload_subnets[count.index].delegation
        actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
      }
    }
  }
}

# VNet Peering to Hub
resource "azurerm_virtual_network_peering" "spoke_to_hub" {
  name                      = "${var.spoke_name}-to-hub"
  resource_group_name       = azurerm_resource_group.spoke.name
  virtual_network_name      = azurerm_virtual_network.spoke.name
  remote_virtual_network_id = var.hub_vnet_id
  
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false
  use_remote_gateways          = var.use_hub_gateway
}

resource "azurerm_virtual_network_peering" "hub_to_spoke" {
  name                      = "hub-to-${var.spoke_name}"
  resource_group_name       = var.hub_resource_group_name
  virtual_network_name      = var.hub_vnet_name
  remote_virtual_network_id = azurerm_virtual_network.spoke.id
  
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = var.use_hub_gateway
  use_remote_gateways          = false
}

# Route Table (force traffic through hub firewall)
resource "azurerm_route_table" "spoke" {
  name                = "${var.organization}-${var.spoke_name}-rt"
  resource_group_name = azurerm_resource_group.spoke.name
  location            = azurerm_resource_group.spoke.location
  
  route {
    name                   = "default-via-firewall"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = var.firewall_private_ip
  }
  
  tags = merge(
    var.common_tags,
    {
      Spoke = var.spoke_name
    }
  )
}

resource "azurerm_subnet_route_table_association" "workload" {
  count = length(var.workload_subnets)
  
  subnet_id      = azurerm_subnet.workload[count.index].id
  route_table_id = azurerm_route_table.spoke.id
}

# Network Security Group
resource "azurerm_network_security_group" "spoke" {
  name                = "${var.organization}-${var.spoke_name}-nsg"
  resource_group_name = azurerm_resource_group.spoke.name
  location            = azurerm_resource_group.spoke.location
  
  tags = merge(
    var.common_tags,
    {
      Spoke = var.spoke_name
    }
  )
}

# Default deny all inbound
resource "azurerm_network_security_rule" "deny_all_inbound" {
  name                        = "DenyAllInbound"
  priority                    = 4096
  direction                   = "Inbound"
  access                      = "Deny"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.spoke.name
  network_security_group_name = azurerm_network_security_group.spoke.name
}

# Allow from hub
resource "azurerm_network_security_rule" "allow_hub" {
  name                        = "AllowHub"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = var.hub_vnet_cidr
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.spoke.name
  network_security_group_name = azurerm_network_security_group.spoke.name
}

resource "azurerm_subnet_network_security_group_association" "workload" {
  count = length(var.workload_subnets)
  
  subnet_id                 = azurerm_subnet.workload[count.index].id
  network_security_group_id = azurerm_network_security_group.spoke.id
}

# Outputs
output "spoke_vnet_id" {
  value = azurerm_virtual_network.spoke.id
}

output "spoke_resource_group_name" {
  value = azurerm_resource_group.spoke.name
}

output "workload_subnet_ids" {
  value = azurerm_subnet.workload[*].id
}
```

### Governance Module
```hcl
# modules/governance/main.tf

# Management Group Structure
resource "azurerm_management_group" "root" {
  display_name = var.organization
}

resource "azurerm_management_group" "platform" {
  display_name               = "Platform"
  parent_management_group_id = azurerm_management_group.root.id
}

resource "azurerm_management_group" "workloads" {
  display_name               = "Workloads"
  parent_management_group_id = azurerm_management_group.root.id
}

# Azure Policy Definitions
resource "azurerm_policy_definition" "require_tags" {
  name         = "require-resource-tags"
  policy_type  = "Custom"
  mode         = "Indexed"
  display_name = "Require specified tags on resources"
  
  metadata = jsonencode({
    category = "Tags"
  })
  
  policy_rule = jsonencode({
    if = {
      anyOf = [
        {
          field  = "[concat('tags[', parameters('tagName1'), ']')]"
          exists = "false"
        },
        {
          field  = "[concat('tags[', parameters('tagName2'), ']')]"
          exists = "false"
        }
      ]
    }
    then = {
      effect = "deny"
    }
  })
  
  parameters = jsonencode({
    tagName1 = {
      type = "String"
      metadata = {
        displayName = "Tag Name 1"
        description = "Name of the first required tag"
      }
    }
    tagName2 = {
      type = "String"
      metadata = {
        displayName = "Tag Name 2"
        description = "Name of the second required tag"
      }
    }
  })
}

# Policy Assignment
resource "azurerm_management_group_policy_assignment" "require_tags" {
  name                 = "require-tags"
  management_group_id  = azurerm_management_group.root.id
  policy_definition_id = azurerm_policy_definition.require_tags.id
  
  parameters = jsonencode({
    tagName1 = { value = "Environment" }
    tagName2 = { value = "CostCenter" }
  })
}

# Diagnostic Settings for Activity Logs
resource "azurerm_monitor_diagnostic_setting" "subscription" {
  name                       = "subscription-diagnostics"
  target_resource_id         = data.azurerm_subscription.current.id
  log_analytics_workspace_id = var.log_analytics_workspace_id
  
  enabled_log {
    category = "Administrative"
  }
  
  enabled_log {
    category = "Security"
  }
  
  enabled_log {
    category = "ServiceHealth"
  }
  
  enabled_log {
    category = "Alert"
  }
  
  enabled_log {
    category = "Policy"
  }
}

# Azure Security Center
resource "azurerm_security_center_subscription_pricing" "vm" {
  tier          = "Standard"
  resource_type = "VirtualMachines"
}

resource "azurerm_security_center_subscription_pricing" "sql" {
  tier          = "Standard"
  resource_type = "SqlServers"
}

resource "azurerm_security_center_subscription_pricing" "storage" {
  tier          = "Standard"
  resource_type = "StorageAccounts"
}

# Cost Management Budget
resource "azurerm_consumption_budget_subscription" "monthly" {
  name            = "monthly-budget"
  subscription_id = data.azurerm_subscription.current.id
  
  amount     = var.monthly_budget_amount
  time_grain = "Monthly"
  
  time_period {
    start_date = formatdate("YYYY-MM-01'T'00:00:00Z", timestamp())
  }
  
  notification {
    enabled   = true
    threshold = 80.0
    operator  = "GreaterThan"
    
    contact_emails = var.budget_contact_emails
  }
  
  notification {
    enabled   = true
    threshold = 100.0
    operator  = "GreaterThan"
    
    contact_emails = var.budget_contact_emails
  }
}
```

---

## Example 3: Reusable Multi-Cloud Kubernetes Module

**Scenario:** Create a reusable module that can deploy Kubernetes clusters on AWS (EKS), Azure (AKS), or GCP (GKE).

### Module Structure
```
terraform-k8s-module/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── aws/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── azure/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── gcp/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

### Main Module
```hcl
# main.tf
module "eks" {
  count  = var.cloud_provider == "aws" ? 1 : 0
  source = "./aws"
  
  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version
  region          = var.region
  
  node_groups = var.node_groups
  
  vpc_id              = var.vpc_id
  subnet_ids          = var.subnet_ids
  
  enable_cluster_autoscaler     = var.enable_autoscaling
  enable_metrics_server         = var.enable_metrics_server
  enable_container_insights     = var.enable_monitoring
  
  tags = var.tags
}

module "aks" {
  count  = var.cloud_provider == "azure" ? 1 : 0
  source = "./azure"
  
  cluster_name        = var.cluster_name
  kubernetes_version  = var.kubernetes_version
  location            = var.region
  resource_group_name = var.resource_group_name
  
  node_pools = var.node_groups
  
  vnet_subnet_id = var.subnet_ids[0]
  
  enable_auto_scaling       = var.enable_autoscaling
  enable_azure_policy       = true
  enable_oms_agent          = var.enable_monitoring
  log_analytics_workspace_id = var.log_analytics_workspace_id
  
  tags = var.tags
}

module "gke" {
  count  = var.cloud_provider == "gcp" ? 1 : 0
  source = "./gcp"
  
  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version
  region          = var.region
  project_id      = var.project_id
  
  node_pools = var.node_groups
  
  network    = var.network
  subnetwork = var.subnet_ids[0]
  
  enable_autoscaling      = var.enable_autoscaling
  enable_monitoring       = var.enable_monitoring
  enable_logging          = var.enable_monitoring
  
  labels = var.tags
}

# Unified outputs
output "cluster_endpoint" {
  value = var.cloud_provider == "aws" ? module.eks[0].cluster_endpoint : (
    var.cloud_provider == "azure" ? module.aks[0].kube_config.0.host :
    module.gke[0].cluster_endpoint
  )
}

output "cluster_ca_certificate" {
  value = var.cloud_provider == "aws" ? module.eks[0].cluster_ca_certificate : (
    var.cloud_provider == "azure" ? module.aks[0].kube_config.0.cluster_ca_certificate :
    module.gke[0].cluster_ca_certificate
  )
  sensitive = true
}

output "kubeconfig" {
  value = var.cloud_provider == "aws" ? module.eks[0].kubeconfig : (
    var.cloud_provider == "azure" ? module.aks[0].kube_config_raw :
    module.gke[0].kubeconfig
  )
  sensitive = true
}
```

### AWS EKS Implementation
```hcl
# aws/main.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"
  
  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  
  vpc_id                   = var.vpc_id
  subnet_ids               = var.subnet_ids
  control_plane_subnet_ids = var.control_plane_subnet_ids
  
  cluster_endpoint_public_access = true
  
  # Encryption
  cluster_encryption_config = {
    provider_key_arn = var.kms_key_arn
    resources        = ["secrets"]
  }
  
  # Logging
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  
  # Node groups
  eks_managed_node_groups = {
    for ng in var.node_groups : ng.name => {
      name           = ng.name
      instance_types = [ng.instance_type]
      
      min_size     = ng.min_size
      max_size     = ng.max_size
      desired_size = ng.desired_size
      
      labels = ng.labels
      taints = ng.taints
      
      update_config = {
        max_unavailable_percentage = 33
      }
      
      iam_role_additional_policies = {
        AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
      }
    }
  }
  
  # Cluster security group rules
  cluster_security_group_additional_rules = {
    ingress_nodes_ephemeral_ports_tcp = {
      description                = "Nodes on ephemeral ports"
      protocol                   = "tcp"
      from_port                  = 1025
      to_port                    = 65535
      type                       = "ingress"
      source_node_security_group = true
    }
  }
  
  # IRSA for cluster autoscaler
  enable_irsa = true
  
  tags = var.tags
}

# Cluster Autoscaler
resource "helm_release" "cluster_autoscaler" {
  count = var.enable_cluster_autoscaler ? 1 : 0
  
  name       = "cluster-autoscaler"
  repository = "https://kubernetes.github.io/autoscaler"
  chart      = "cluster-autoscaler"
  namespace  = "kube-system"
  version    = "9.29.0"
  
  set {
    name  = "autoDiscovery.clusterName"
    value = var.cluster_name
  }
  
  set {
    name  = "awsRegion"
    value = var.region
  }
  
  set {
    name  = "rbac.serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = aws_iam_role.cluster_autoscaler[0].arn
  }
}
```

---

## Example 4: Multi-Cloud Disaster Recovery Setup

**Scenario:** Primary infrastructure in AWS, automated DR replication to Azure, with Terraform managing both.

### Main Configuration
```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  backend "s3" {
    bucket         = "disaster-recovery-tfstate"
    key            = "multi-cloud-dr/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# AWS Provider (Primary)
provider "aws" {
  region = var.primary_region
  alias  = "primary"
  
  default_tags {
    tags = {
      Project     = "Multi-Cloud-DR"
      Environment = var.environment
      Site        = "Primary"
      ManagedBy   = "Terraform"
    }
  }
}

# Azure Provider (DR)
provider "azurerm" {
  features {}
  alias = "dr"
}

# Primary Infrastructure (AWS)
module "primary_aws" {
  source = "./modules/aws-primary"
  
  providers = {
    aws = aws.primary
  }
  
  environment  = var.environment
  project_name = var.project_name
  vpc_cidr     = var.primary_vpc_cidr
  
  # Application configuration
  instance_count  = var.primary_instance_count
  instance_type   = var.primary_instance_type
  database_config = var.primary_database_config
  
  # DR replication configuration
  enable_cross_region_replication = true
  dr_region                       = var.dr_region
  
  tags = local.common_tags
}

# DR Infrastructure (Azure)
module "dr_azure" {
  source = "./modules/azure-dr"
  
  providers = {
    azurerm = azurerm.dr
  }
  
  environment     = var.environment
  project_name    = var.project_name
  location        = var.dr_location
  vnet_cidr       = var.dr_vnet_cidr
  
  # Standby configuration (reduced capacity)
  vm_count        = var.dr_vm_count
  vm_size         = var.dr_vm_size
  database_config = var.dr_database_config
  
  # Replication from AWS
  aws_s3_backup_bucket = module.primary_aws.backup_bucket_name
  aws_region           = var.primary_region
  
  tags = merge(local.common_tags, { Site = "DR" })
}

# Cross-cloud replication job
module "replication" {
  source = "./modules/replication"
  
  providers = {
    aws     = aws.primary
    azurerm = azurerm.dr
  }
  
  # Source (AWS)
  source_bucket_name = module.primary_aws.backup_bucket_name
  source_region      = var.primary_region
  
  # Destination (Azure)
  destination_storage_account = module.dr_azure.storage_account_name
  destination_container       = module.dr_azure.backup_container_name
  
  # Replication schedule
  replication_schedule = "0 */6 * * *"  # Every 6 hours
  
  tags = local.common_tags
}

# Traffic Manager / Route 53 for failover
module "dns_failover" {
  source = "./modules/dns-failover"
  
  providers = {
    aws     = aws.primary
    azurerm = azurerm.dr
  }
  
  domain_name = var.domain_name
  
  # Primary endpoint (AWS)
  primary_endpoint = module.primary_aws.application_endpoint
  primary_region   = var.primary_region
  
  # DR endpoint (Azure)
  dr_endpoint = module.dr_azure.application_endpoint
  dr_region   = var.dr_location
  
  # Health check configuration
  health_check_path     = "/health"
  health_check_interval = 30
  
  tags = local.common_tags
}

# Outputs
output "primary_endpoint" {
  value = module.primary_aws.application_endpoint
}

output "dr_endpoint" {
  value = module.dr_azure.application_endpoint
}

output "failover_domain" {
  value = module.dns_failover.failover_domain
}

output "replication_status" {
  value = module.replication.status
}
```

### Variables
```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "primary_region" {
  description = "AWS primary region"
  type        = string
  default     = "us-east-1"
}

variable "dr_location" {
  description = "Azure DR location"
  type        = string
  default     = "West Europe"
}

variable "primary_instance_count" {
  description = "Number of instances in primary site"
  type        = number
  default     = 6
}

variable "dr_vm_count" {
  description = "Number of VMs in DR site (standby)"
  type        = number
  default     = 2
}

variable "domain_name" {
  description = "Domain name for the application"
  type        = string
}

locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    DREnabled   = "true"
  }
}
```

---

## Summary

These examples demonstrate:

1. **Multi-Tier AWS Application**: Complete 3-tier architecture with networking, compute (Auto Scaling), and RDS database
2. **Azure Landing Zone**: Hub-spoke topology with governance, security, and management groups
3. **Reusable Multi-Cloud Module**: Abstracted Kubernetes deployment across AWS, Azure, and GCP
4. **Multi-Cloud DR**: Primary AWS infrastructure with automated replication to Azure DR site

Each example includes:
- Proper module structure and organization
- Security best practices (encryption, network segmentation, least privilege)
- State management and backend configuration
- Testing strategies
- Production-ready configurations
- Detailed documentation

All examples follow Terraform best practices and can be adapted for specific use cases.
