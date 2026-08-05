
provider "aws" {
  region = "us-east-1"
}

module "secure_bucket" {
  source = "./modules/secure_storage"
  bucket_name = "my-secure-tsp-bucket"
}
