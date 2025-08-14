import requests
import subprocess
import time

request_headers = {
            "Content-Type": "application/json"
        }

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


def send_post_request(api_url):
    payload = {"message": f"Hello from run.py {int(time.time())}!"}
    try:
        response = requests.post(f"{api_url}/write", json=payload, headers=request_headers)
        response.raise_for_status()  # Raise an error for bad responses
        print("POST request sent successfully to API Gateway.\n Response:", response.text)
        print (f"Response JSON: {response.json().get('file_name', 'No file name returned')}")
        return response.text.split(":")[-1].strip() # Extract the file name from the response
    except requests.RequestException as e:
        print(f"Failed to create issue: {e}")
        
    

def send_get_request(api_url, file_name):
    try:
        response = requests.get(f"{api_url}/read", params={"file_name": file_name}, headers=request_headers)
        response.raise_for_status()  # Raise an error for bad responses
        print("GET request sent successfully to API Gateway.\n Response:", response.text)
    except requests.RequestException as e:
        print(f"Failed to retrieve issues: {e}")

if __name__ == "__main__":
    print("Starting test via API Gateway...\n")
    api_url = get_api_url()
    file_name = send_post_request(api_url)
    time.sleep(2)  # Wait 2 seconds before sending the GET request
    send_get_request(api_url, file_name)