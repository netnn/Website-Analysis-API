import pytest
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption(
        "--target-url",
        action="store",
        default="https://www.cbssports.com/betting",
        help="Target URL for website tests."
    )

@pytest.fixture(scope="session")
def browser_context():
    """
    Fixture to open a browser for the entire session.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture
def page(browser_context):
    """
    Fixture to open a new page for each test.
    """
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture
def target_url(request):
    """
    Fixture to retrieve the target URL from the pytest command-line options.
    """
    return request.config.getoption("--target-url")
