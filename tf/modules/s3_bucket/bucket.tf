resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name
  tags   = var.tags
}

# Create an S3 bucket policy to allow Lambda function access
resource "aws_s3_bucket_policy" "allow_lambda_access" {
  bucket = aws_s3_bucket.my_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowLambdaAccess"
        Effect    = "Allow"
        Principal = {
          AWS = var.lambda_role_arn
        }
        Action    = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource  = [
          aws_s3_bucket.my_bucket.arn,
          "${aws_s3_bucket.my_bucket.arn}/*"
        ]
      },
      {
        Sid: "DenyOthers",
        Effect: "Deny",
        Principal: "*",
        Action: [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
          ],
        Resource  = [
          aws_s3_bucket.my_bucket.arn,
          "${aws_s3_bucket.my_bucket.arn}/*"
        ]

        Condition: {
          StringNotEquals: {
            "aws:PrincipalArn": var.lambda_role_arn
          }
        }
      }
    ]
  })
}