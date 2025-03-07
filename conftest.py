import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_context():
    """
    Fixture to open a browser for the entire session.
    """
    # Start Playwright and launch Chromium in headless mode
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create a new browser context
        context = browser.new_context()
        yield context
        # Close the context and the browser after tests complete
        context.close()
        browser.close()

@pytest.fixture
def page(browser_context):
    """
    Fixture to open a new page for each test.
    """
    # Open a new page from the browser context
    page = browser_context.new_page()
    yield page
    # Close the page after the test finishes
    page.close()
