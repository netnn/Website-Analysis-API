"""
This script fetches API data from jsonplaceholder and validates each post by checking:
    - 'userId' is an integer.
    - 'title' is not empty.
    - 'body' is not empty.

We use pytest's parametrize feature to treat each post as an individual test case.
If any post fails validation, a detailed error message is printed to the console and the test fails.
"""

import requests
import pytest

def fetch_posts():
    """
    Fetch posts from the API and return them as a list of dictionaries.
    """
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    response.raise_for_status()
    return response.json()

@pytest.mark.parametrize("post", fetch_posts())
def test_post_api(post):
    # Validate each post's fields
    user_id_valid = type(post['userId']) == int
    title_valid = post['title'] != ''
    body_valid = post['body'] != ''

    # If any validation fails, build a list of failure reasons
    failed_reasons = []
    if not (user_id_valid and title_valid and body_valid):
        if not user_id_valid:
            failed_reasons.append("userId is not an integer")
        if not title_valid:
            failed_reasons.append("title is empty")
        if not body_valid:
            failed_reasons.append("body is empty")

    # Log failure reasons to the console (optional: also write to a file)
    if failed_reasons:
        print(f"Post ID {post['id']} failed: {', '.join(failed_reasons)}")

    # If there are failure reasons, fail the test with a detailed error message
    assert not failed_reasons, f"Post ID {post['id']} failed: {', '.join(failed_reasons)}"
