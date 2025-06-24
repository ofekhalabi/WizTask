import boto3
import time
import os


# AWS clients
s3_client = boto3.client("s3")
BUCKET_NAME = os.environ["BUCKET_NAME"]


def lambda_handler(event, context):
    print("Lambda handler started")
    try:
        http_method = event['requestContext']['http']['method']
    except KeyError as e:
        print (f"error: {e}")
        return {
            'statusCode': 400,
            'body': 'Invalid request format'
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': 'Internal server error'
        }
    
    if http_method == 'POST':
        body_message = event['body']
        object_name = f"wiz_body_{int(time.time())}.txt"
        try:
            s3_client.put_object(Bucket=BUCKET_NAME, Key=object_name, Body=body_message)
            print(f"File uploaded successfully: {object_name}")
        except Exception as e:
            print(f"Error uploading file: {e}")
            return {
                'statusCode': 500,
                'body': 'Error uploading file'
            }
        
        return {
            'statusCode': 200,
            'body': f"File uploaded successfully:{object_name}"
        }
    
    elif http_method == 'GET':
        try:
            object_name = event['queryStringParameters']['file_name']
            print (f"Retrieving file: {object_name}")
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=object_name)
            print(f"File retrieved successfully: {object_name}")
        except Exception as e:
            print(f"Error retrieving file: {e}")
            return {
                'statusCode': 500,
                'body': 'Error retrieving file'
            }

        content_message = response['Body'].read().decode('utf-8')
        return {
            'statusCode': 200,
            'body': content_message
        }