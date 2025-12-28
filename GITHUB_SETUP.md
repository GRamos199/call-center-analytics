# =============================================================================
# GitHub Actions & AWS Configuration Guide
# =============================================================================

## 🔐 Required GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

### AWS Credentials (Required for Terraform & Deploy)
```
AWS_ACCESS_KEY_ID       → Your AWS IAM access key ID
AWS_SECRET_ACCESS_KEY   → Your AWS IAM secret access key
```

### Creating AWS IAM User for GitHub Actions

1. Go to AWS Console → IAM → Users → Create User
2. Name: `github-actions-deployer`
3. Attach these policies:
   - `AmazonECS_FullAccess`
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonVPCFullAccess`
   - `ElasticLoadBalancingFullAccess`
   - `CloudWatchLogsFullAccess`
   - `IAMFullAccess` (for creating ECS roles)
   - Or create a custom policy with the JSON below

4. Create Access Key → Select "Application running outside AWS"
5. Copy the Access Key ID and Secret Access Key
6. Add them as GitHub Secrets

### Custom IAM Policy (More Restrictive)
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:*",
                "ecs:*",
                "ec2:*",
                "elasticloadbalancing:*",
                "application-autoscaling:*",
                "logs:*",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:AttachRolePolicy",
                "iam:DetachRolePolicy",
                "iam:PutRolePolicy",
                "iam:DeleteRolePolicy",
                "iam:GetRole",
                "iam:PassRole",
                "iam:CreateServiceLinkedRole"
            ],
            "Resource": "*"
        }
    ]
}
```

---

## 🌐 GitHub Environments Setup

For production deployments with approval:

1. Go to Settings → Environments → New environment
2. Name: `production`
3. Add protection rules:
   - ✅ Required reviewers (add your username)
   - ✅ Wait timer (optional, e.g., 5 minutes)
4. Add environment secrets if different from repository secrets

---

## 📄 GitHub Pages Setup

1. Go to Settings → Pages
2. Source: "GitHub Actions"
3. The workflow will automatically deploy on push to main

---

## 🔄 Workflow Overview

### 1. `test.yml` - Testing
- **Triggers**: Push/PR to main, develop
- **Jobs**: Lint, Unit Tests, Integration Tests, Security Scan
- **No secrets required** (runs without AWS)

### 2. `terraform.yml` - Infrastructure
- **Triggers**: Changes to terraform/, manual dispatch
- **Jobs**: Format, Validate, Plan, Apply, Destroy
- **Secrets required**: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
- **Manual actions**: Use workflow_dispatch to select plan/apply/destroy

### 3. `deploy.yml` - Application Deployment
- **Triggers**: Push to main (excluding terraform changes)
- **Jobs**: Build Docker image, Push to ECR, Deploy to ECS
- **Secrets required**: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

### 4. `pages.yml` - Documentation
- **Triggers**: Push to main, changes to docs/
- **Jobs**: Build static docs, Deploy to GitHub Pages
- **No secrets required**

---

## 🚀 First Time Setup Steps

1. **Create GitHub Repository** (if not done)
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/call-center-analytics.git
   git branch -M main
   git push -u origin main
   ```

2. **Add AWS Secrets** (see above)

3. **Run Terraform Plan** (manual)
   - Go to Actions → Terraform → Run workflow
   - Select action: "plan"
   - Review the plan output

4. **Apply Infrastructure** (manual)
   - Go to Actions → Terraform → Run workflow
   - Select action: "apply"
   - Wait for approval if environment protection is set

5. **Deploy Application**
   - Push code changes to main
   - Deploy workflow runs automatically

---

## 📊 Terraform State Management (Production)

For production, enable remote state in `terraform/main.tf`:

1. Create S3 bucket for state:
   ```bash
   aws s3 mb s3://your-terraform-state-bucket --region us-east-1
   ```

2. Create DynamoDB table for locking:
   ```bash
   aws dynamodb create-table \
     --table-name terraform-state-lock \
     --attribute-definitions AttributeName=LockID,AttributeType=S \
     --key-schema AttributeName=LockID,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST
   ```

3. Uncomment backend configuration in `terraform/main.tf`

---

## 🔧 Customization

### Change AWS Region
Update in:
- `.github/workflows/terraform.yml` → `env.AWS_REGION`
- `.github/workflows/deploy.yml` → `env.AWS_REGION`
- `terraform/terraform.tfvars` → `aws_region`

### Change Container Resources
Edit `terraform/terraform.tfvars`:
- `container_cpu` (256, 512, 1024, 2048, 4096)
- `container_memory` (512, 1024, 2048, etc.)

### Add HTTPS
1. Get/create ACM certificate
2. Uncomment HTTPS listener in `terraform/alb.tf`
3. Add certificate ARN variable

---

## ⚠️ Important Notes

1. **Streamlit on GitHub Pages**: Not supported - Streamlit needs a server.
   The pages workflow creates documentation only.

2. **Costs**: AWS resources incur charges. Use `terraform destroy` to remove all resources.

3. **First Deploy**: Terraform must run before deploy workflow (creates ECR repository).

4. **NAT Gateway**: Costs ~$32/month. For dev, consider using public subnets only.
