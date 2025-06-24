# 📦 Terraform Module: S3 Bucket for Lambda Integration

This Terraform module provisions an **Amazon S3 bucket** that is **securely restricted** to access only by a specific **AWS Lambda function's IAM role**.

---

## 🔧 Features

- Creates a private S3 bucket.
- Attaches a restrictive bucket policy that:
  - ✅ Allows only the specified Lambda role to access the bucket.
  - ❌ Denies access to all other identities (even if they have IAM permissions).
- Optional tags and versioning support.

---

## 📥 Inputs

| Name              | Type     | Description                                               | Required |
|-------------------|----------|-----------------------------------------------------------|----------|
| `bucket_name`     | `string` | Name of the S3 bucket                                     | ✅ Yes    |
| `lambda_role_arn` | `string` | ARN of the IAM role for Lambda that should access bucket | ✅ Yes    |
| `tags`            | `map`    | Tags to apply to the bucket                              | ❌ No     |

---

## 📤 Outputs

| Name           | Description                      |
|----------------|----------------------------------|
| `bucket_name`  | The name of the created bucket   |
| `bucket_arn`   | The ARN of the created bucket    |

---

## 🚀 Usage Example

```hcl
module "s3_bucket" {
  source           = "./modules/s3"
  bucket_name      = "wiz-task-bucket"
  lambda_role_arn  = aws_iam_role.lambda_exec.arn

  tags = {
    environment = "dev"
    terraform   = "true"
  }
}
