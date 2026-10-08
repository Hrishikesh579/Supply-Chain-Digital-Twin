output "ec2_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "s3_bucket_name" {
  description = "Name of the created S3 bucket"
  value       = aws_s3_bucket.data_bucket.id
}

output "s3_bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.data_bucket.arn
}

output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID of the created public subnet"
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "ID of the created security group"
  value       = aws_security_group.allow_web.id
}

output "iam_role_arn" {
  description = "ARN of the IAM role for EC2"
  value       = aws_iam_role.ec2_role.arn
}

output "iam_instance_profile" {
  description = "Name of the IAM instance profile"
  value       = aws_iam_instance_profile.ec2_profile.name
}

output "ebs_volume_id" {
  description = "ID of the additional EBS data volume"
  value       = aws_ebs_volume.data_vol.id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.igw.id
}

output "route_table_id" {
  description = "ID of the public route table"
  value       = aws_route_table.public_rt.id
}

output "cloudwatch_app_log_group" {
  description = "CloudWatch application log group name"
  value       = aws_cloudwatch_log_group.app_logs.name
}

output "cloudwatch_sys_log_group" {
  description = "CloudWatch system log group name"
  value       = aws_cloudwatch_log_group.sys_logs.name
}

output "ssh_command" {
  description = "Command to SSH into the EC2 instance"
  value       = "ssh -i ../keys/${var.project_name}-key.pem ubuntu@${aws_instance.app_server.public_ip}"
}

output "ssh_private_key_file" {
  description = "Path to the SSH private key file"
  value       = local_file.private_key.filename
}

output "flask_url" {
  description = "URL of the Flask application"
  value       = "http://${aws_instance.app_server.public_ip}:5000"
}

output "grafana_url" {
  description = "URL of Grafana dashboard"
  value       = "http://${aws_instance.app_server.public_ip}:3000"
}

output "prometheus_url" {
  description = "URL of Prometheus"
  value       = "http://${aws_instance.app_server.public_ip}:9090"
}
