variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name tag"
  type        = string
  default     = "supply-chain-dt"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public Subnet CIDR block"
  type        = string
  default     = "10.0.1.0/24"
}

variable "ebs_volume_size" {
  description = "EBS volume size in GB"
  type        = number
  default     = 20
}

variable "s3_bucket_name" {
  description = "S3 bucket name. User should override this to something globally unique."
  type        = string
  default     = "supply-chain-dt-data-bucket"
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed to SSH. User should restrict this to their IP."
  type        = string
  default     = "0.0.0.0/0"
}
