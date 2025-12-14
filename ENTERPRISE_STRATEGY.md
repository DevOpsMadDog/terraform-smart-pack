# Enterprise Migration Strategy: "ClickOps to Polyrepo IaC"

## The Scenario
- **Current State**: 
    - Many distinct modules/projects.
    - Mixed environment: Some legacy "ClickOps" resources, some IaC.
    - **Polyrepo Structure**: One repository per project.
    - **Fragmented State**: Different `backend.tf` files everywhere, potential locking collisions or lost states.

## How TSP Solves This

### 1. The "ClickOps" Problem -> `tsp import`
**Challenge**: Moving manually created resources into Terraform is painful (writing `import` blocks, matching attributes).
**TSP Solution**: 
- **Auto-Import**: `tsp import <resource_id>` scans the real resource via API.
- **Code Generation**: Generates the matching `.tf` HCL code automatically.
- **State Sync**: Runs the `terraform import` command under the hood.

### 2. The "Polyrepo" Problem -> `tsp centralize`
**Challenge**: managing 50 repos means 50 different `backend.tf` configs. If you move a repo, you break the state.
**TSP Solution**:
- **Dynamic Backend**: Instead of a hardcoded `backend.tf`, TSP uses a `tsp.yaml` config in each repo.
- **State Routing**: `tsp init` reads the project name from `tsp.yaml` and dynamically configures the S3 key path (e.g., `s3://corp-state/proj-A/terraform.tfstate`).
- **Standardization**: Enforces the same locking table (`dynamodb_table`) across all 50 repos, preventing collisions.

### 3. The "Mid-Way" Migration
**Strategy**:
1.  **Inventory**: Run `tsp scan-account` (new feature) to list all resources in AWS not managed by Terraform.
2.  **Codify**: Use `tsp import` to bring them into the polyrepos.
3.  **Standardize**: Replace individual `backend.tf` files with `tsp init --standardize` to force all repos to use the corporate secure backend bucket.

## Feature Roadmap (Enterprise Edition)
1.  **`tsp import`**: Generates HCL from existing resources.
2.  **`tsp centralize`**: Standardizes backend configuration across multiple repos.
3.  **`tsp scan-account`**: Finds unmanaged resources (the "ClickOps" residue).
