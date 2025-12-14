
terraform {
  backend "s3" {
    bucket         = "tsp-terraform-state-DO-NOT-DELETE"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "tsp-terraform-locks"
  }
}
