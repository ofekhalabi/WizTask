import requests
import json
import subprocess

def get_api_url():
    result = subprocess.run(
        ["terraform", "output", "-raw", "gateway_endpoint"],
        capture_output=True,
        text=True
    )
    # Check if the command was successful
    if result.returncode != 0:
        raise Exception(f"❌ Failed to get API Gateway URL: {result.stderr}")
    return result.stdout.strip()


api_url = get_api_url()
def send_post_request(api_url):
    payload = {"message": "Hello from run.py!"} 
    try:
        response = requests.post(f"{api_url}/write", json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        print("POST request sent successfully.")
    except requests.RequestException as e:
        print(f"Failed to create issue: {e}")

def send_get_request(api_url, file_name):
    try:
        response = requests.get(f"{api_url}/read", params={"file_name": file_name})
        response.raise_for_status()  # Raise an error for bad responses
        issues = response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve issues: {e}")