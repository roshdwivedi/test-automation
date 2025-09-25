"""
Global pytest configuration and fixtures for Web Automation Test Suite.
"""

import pytest
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page


# Remove custom event_loop fixture to use pytest-asyncio default


@pytest.fixture(scope="function")
async def browser():
    """
    Function-scoped fixture to create and manage the browser instance.
    
    Returns:
        Browser: Playwright browser instance
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,   # Headless mode - no browser window
            slow_mo=0,       # No delay needed in headless mode
        )
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def context(browser: Browser):
    """
    Function-scoped fixture to create a new browser context for each test.
    
    Args:
        browser: Browser instance from browser fixture
        
    Returns:
        BrowserContext: Fresh browser context for isolation
    """
    context = await browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    yield context
    await context.close()


@pytest.fixture(scope="function")
async def page(context: BrowserContext):
    """
    Function-scoped fixture to create a new page for each test.
    
    Args:
        context: Browser context from context fixture
        
    Returns:
        Page: Fresh page instance with base URL configured
    """
    page = await context.new_page()
    
    # Set default timeout
    page.set_default_timeout(30000)  # 30 seconds
    
    yield page
    await page.close()


@pytest.fixture(scope="function")
async def authenticated_page(page: Page):
    """
    Fixture that provides a page already authenticated with valid credentials.
    
    Args:
        page: Page instance from page fixture
        
    Returns:
        Page: Authenticated page instance
    """
    # Navigate to login page
    base_url = "https://the-internet.herokuapp.com"
    await page.goto(f"{base_url}/login")
    
    # Perform login
    await page.fill("#username", "tomsmith")
    await page.fill("#password", "SuperSecretPassword!")
    await page.click("button[type='submit']")
    
    # Wait for successful login
    await page.wait_for_selector(".flash.success")
    
    yield page


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their names."""
    for item in items:
        # Add smoke marker to authentication tests
        if "authentication" in item.name:
            item.add_marker(pytest.mark.smoke)
        
        # Add regression marker to all tests
        item.add_marker(pytest.mark.regression)
        
        # Add slow marker to file upload tests
        if "file_upload" in item.name:
            item.add_marker(pytest.mark.slow)