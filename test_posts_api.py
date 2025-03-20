import pytest
from posts_api import fetch_posts

@pytest.mark.parametrize("post", fetch_posts())
def test_post_api(post):
    """
    Validates each post's fields:
    - 'userId' must be an integer.
    - 'title' must not be empty.
    - 'body' must not be empty.
    """
    user_id_valid = isinstance(post.get('userId'), int)
    title_valid = bool(post.get('title'))
    body_valid = bool(post.get('body'))

    failed_reasons = []
    if not user_id_valid:
        failed_reasons.append("userId is not an integer")
    if not title_valid:
        failed_reasons.append("title is empty")
    if not body_valid:
        failed_reasons.append("body is empty")

    if failed_reasons:
        print(f"Post ID {post.get('id')} failed: {', '.join(failed_reasons)}")
    assert not failed_reasons, f"Post ID {post.get('id')} failed: {', '.join(failed_reasons)}"
