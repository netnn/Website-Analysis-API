import requests

# Define the API URL as a variable
API_URL = "https://jsonplaceholder.typicode.com/posts"

def validate_json_response(response):
    """
    Validates that the response contains JSON data by checking the Content-Type header.
    Raises a ValueError if the response is not JSON.
    """
    content_type = response.headers.get('Content-Type', '')
    if 'application/json' not in content_type:
        raise ValueError(f"Expected JSON response but got Content-Type: {content_type}")

def fetch_posts():
    """
    Fetches posts from the API and returns them as a list of dictionaries.
    Checks that the response contains JSON data before returning.
    """
    response = requests.get(API_URL)
    response.raise_for_status()
    validate_json_response(response)
    return response.json()
