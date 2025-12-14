# Terraform Smart Pack (TSP)

**The Developer-First Infrastructure Wrapper**

> "Don't just write Terraform. Ship secure, cost-optimized infrastructure with confidence."

## The Problem
Terraform is powerful, but dangerous. 
- **State Loopholes**: Local state files get lost; concurrent applies corrupt state.
- **Security Loopholes**: Default configurations often leave S3 buckets open or databases unencrypted.
- **Cost Blindness**: You don't know the price until the bill arrives.

## The Solution: Terraform Smart Pack (TSP)
TSP is a CLI tool that wraps Terraform to enforce best practices automatically.

### Features
1.  **Smart Init (`tsp init`)**:
    - Automatically generates a secure directory structure.
    - **Fixes State Loopholes**: Configures S3 remote backend with DynamoDB locking and encryption enabled by default.
    - Includes pre-built "Secure-by-Design" modules.

2.  **Pre-Flight Check (`tsp check`)**:
    - **Fixes Security Loopholes**: Scans code for hardcoded secrets and unencrypted resources.
    - **Fixes Cost Blindness**: Provides an instant cost estimate for the resources defined.
    - **Fixes Configuration Drift**: Validates that state locking is active.

## Installation

```bash
pip install .
```

## Usage

**1. Initialize a new project:**
```bash
tsp init
```

**2. Audit your infrastructure:**
```bash
tsp check
```

## "Debate" Origin
This product was born from a simulated debate between AI models:
- **GPT5.2** proposed a fully autonomous agent.
- **Gemini 3 Pro** proposed a strict security compliance tool.
- **Composer 1** (The Builder) synthesized these into **TSP**: a pragmatic tool that developers will actually use.

## Reference
Project ID: `bc-1b412232-ad86-43da-8faf-bb16b0354c4f`

## License
MIT
