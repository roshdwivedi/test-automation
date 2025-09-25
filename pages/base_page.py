"""
Base page class containing common functionality for all page objects.
"""

from playwright.async_api import Page, Locator
from typing import Optional, Union


class BasePage:
    """Base page class with common methods and properties."""
    
    def __init__(self, page: Page):
        """
        Initialize base page.
        
        Args:
            page: Playwright page instance
        """
        self.page = page
        self.base_url = "https://the-internet.herokuapp.com"
    
    async def navigate_to(self, path: str = "") -> None:
        """
        Navigate to a specific path.
        
        Args:
            path: Path to navigate to (relative to base URL)
        """
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        await self.page.goto(url)
    
    async def get_title(self) -> str:
        """Get the page title."""
        return await self.page.title()
    
    async def get_url(self) -> str:
        """Get the current URL."""
        return self.page.url
    
    async def wait_for_element(self, selector: str, timeout: int = 30000) -> Locator:
        """
        Wait for an element to be present.
        
        Args:
            selector: CSS selector or XPath
            timeout: Timeout in milliseconds
            
        Returns:
            Locator: Element locator
        """
        return await self.page.wait_for_selector(selector, timeout=timeout)
    
    async def click_element(self, selector: str) -> None:
        """
        Click an element.
        
        Args:
            selector: CSS selector or XPath
        """
        await self.page.click(selector)
    
    async def fill_input(self, selector: str, value: str) -> None:
        """
        Fill an input field.
        
        Args:
            selector: CSS selector or XPath
            value: Value to fill
        """
        await self.page.fill(selector, value)
    
    async def get_text(self, selector: str) -> str:
        """
        Get text content of an element.
        
        Args:
            selector: CSS selector or XPath
            
        Returns:
            str: Text content
        """
        element = await self.wait_for_element(selector)
        return await element.text_content() or ""
    
    async def is_element_visible(self, selector: str) -> bool:
        """
        Check if an element is visible.
        
        Args:
            selector: CSS selector or XPath
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            locator = self.page.locator(selector)
            return await locator.is_visible()
        except Exception:
            return False
    
    async def is_element_enabled(self, selector: str) -> bool:
        """
        Check if an element is enabled.
        
        Args:
            selector: CSS selector or XPath
            
        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            locator = self.page.locator(selector)
            return await locator.is_enabled()
        except Exception:
            return False
    
    async def wait_for_url_change(self, expected_url_part: str, timeout: int = 30000) -> None:
        """
        Wait for URL to change and contain expected part.
        
        Args:
            expected_url_part: Part of URL to wait for
            timeout: Timeout in milliseconds
        """
        await self.page.wait_for_url(f"**/*{expected_url_part}*", timeout=timeout)
    
    async def take_screenshot(self, path: str) -> None:
        """
        Take a screenshot.
        
        Args:
            path: Path to save screenshot
        """
        await self.page.screenshot(path=path)
    
    async def get_all_elements(self, selector: str) -> list:
        """
        Get all elements matching selector.
        
        Args:
            selector: CSS selector or XPath
            
        Returns:
            list: List of element locators
        """
        return await self.page.locator(selector).all()