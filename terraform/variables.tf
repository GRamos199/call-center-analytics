# =============================================================================
# Variables Definition
# =============================================================================

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "call-center-analytics"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# =============================================================================
# VPC Variables
# =============================================================================

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

# =============================================================================
# ECS Variables
# =============================================================================

variable "container_port" {
  description = "Port exposed by the container"
  type        = number
  default     = 8501
}

variable "container_cpu" {
  description = "CPU units for the container (1024 = 1 vCPU)"
  type        = number
  default     = 256
}

variable "container_memory" {
  description = "Memory for the container in MB"
  type        = number
  default     = 512
}

variable "desired_count" {
  description = "Desired number of containers"
  type        = number
  default     = 1
}

variable "max_capacity" {
  description = "Maximum number of containers for auto-scaling"
  type        = number
  default     = 3
}

variable "min_capacity" {
  description = "Minimum number of containers for auto-scaling"
  type        = number
  default     = 1
}

# =============================================================================
# Application Variables
# =============================================================================

variable "health_check_path" {
  description = "Health check path for the application"
  type        = string
  default     = "/_stcore/health"
}

variable "docker_image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}
