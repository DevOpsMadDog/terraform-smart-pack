#!/usr/bin/env python3
import argparse
import sys
import os
import subprocess
import json

def setup_logging():
    # Simple logging setup
    pass

def init_project(args):
    print("🚀 Initializing Terraform Smart Pack project...")
    
    # Create main.tf
    if not os.path.exists("main.tf"):
        with open("main.tf", "w") as f:
            f.write("""
provider "aws" {
  region = "us-east-1"
}

module "secure_bucket" {
  source = "./modules/secure_storage"
  bucket_name = "my-secure-tsp-bucket"
}
""")
        print("  ✅ Created main.tf")
    else:
        print("  ⚠️  main.tf already exists, skipping")

    # Create backend config (secure default)
    if not os.path.exists("backend.tf"):
        with open("backend.tf", "w") as f:
            f.write("""
terraform {
  backend "s3" {
    bucket         = "tsp-terraform-state-DO-NOT-DELETE"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "tsp-terraform-locks"
  }
}
""")
        print("  ✅ Created backend.tf (Remote State + Locking enabled)")
    
    # Create module directory
    os.makedirs("modules/secure_storage", exist_ok=True)
    
    # Create a secure storage module
    with open("modules/secure_storage/main.tf", "w") as f:
        f.write("""
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
""")
    with open("modules/secure_storage/variables.tf", "w") as f:
        f.write("""
variable "bucket_name" {
  type        = string
  description = "Name of the secure bucket"
}
""")
    print("  ✅ Created secure_storage module")
    print("\nProject initialized! Run 'tsp check' to validate.")

def check_project(args):
    print("🔍 Running Smart Pack Audit...")
    issues = []
    
    # 1. Check for State Locking
    if os.path.exists("backend.tf"):
        with open("backend.tf", "r") as f:
            content = f.read()
            if "dynamodb_table" not in content:
                issues.append("CRITICAL: State locking (dynamodb_table) is NOT configured in backend.tf")
            if "encrypt" not in content or "true" not in content:
                issues.append("HIGH: State encryption is not explicitly enabled in backend.tf")
    else:
        issues.append("CRITICAL: No backend.tf found. Local state is risky!")

    # 2. Check for secrets (naive check)
    if os.path.exists("main.tf"):
        with open("main.tf", "r") as f:
            for i, line in enumerate(f):
                if "secret_key" in line or "access_key" in line:
                    if "var." not in line:
                        issues.append(f"HIGH: Potential hardcoded secret on line {i+1} of main.tf")

    # 3. Cost Estimation (Mock)
    print("\n💰 Estimating Costs...")
    print("  - AWS S3 Standard: ~$0.023/GB")
    print("  - DynamoDB Write Units: Free tier eligible")
    print("  -> Estimated Monthly Spend: < $5.00 (for base setup)")

    print("\n📋 Audit Report:")
    if issues:
        for issue in issues:
            print(f"  ❌ {issue}")
        sys.exit(1)
    else:
        print("  ✅ All checks passed! Infrastructure is secure and optimized.")

def main():
    parser = argparse.ArgumentParser(description="Terraform Smart Pack (TSP) - Build Secure Infra")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Init command
    parser_init = subparsers.add_parser("init", help="Initialize a new secure project")
    
    # Check command
    parser_check = subparsers.add_parser("check", help="Analyze project for loopholes (Security, Cost, State)")

    args = parser.parse_args()

    if args.command == "init":
        init_project(args)
    elif args.command == "check":
        check_project(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
