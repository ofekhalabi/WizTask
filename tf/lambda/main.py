import boto3
import time
import os


# AWS clients
s3_client = boto3.client("s3")
BUCKET_NAME = os.environ["BUCKET_NAME"]



def lambda_handler(event, context):
    print("Lambda handler started")
    object_name = f"wiz_body_{int(time.time())}.txt"
    try:
        http_method = event['requestContext']['http']['method']
    except KeyError as e:
        print (f"error: {e}")
        return {
            'statusCode': 400,
            'body': 'Bad Request: Missing httpMethod'
        }
    
    if http_method == 'POST':
        body_message = event['body']
        try:
            s3_client.put_object(Bucket=BUCKET_NAME, Key=object_name, Body=body_message)
            print(f"File uploaded successfully: {object_name}")
        except Exception as e:
            print(f"Error uploading file: {e}")
        
        return {
            'statusCode': 200,
            'body': f"File uploaded successfully: {object_name}"
        }
    
    elif http_method == 'GET':
        try:
            body_message = event['queryStringParameters']['file_name']
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=object_name)
            print(f"File retrieved successfully: {object_name}")
        except Exception as e:
            print(f"Error retrieving file: {e}")

        content_message = response['Body'].read().decode('utf-8')
        return {
            'statusCode': 200,
            'body': content_message
        }