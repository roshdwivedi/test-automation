"""
Page object model for the login/authentication page.
"""

from playwright.async_api import Page
from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page."""
    
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    FLASH_MESSAGE = ".flash"
    SUCCESS_MESSAGE = ".flash.success"
    ERROR_MESSAGE = ".flash.error"
    LOGOUT_BUTTON = "a[href='/logout']"
    
    def __init__(self, page: Page):
        """
        Initialize login page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url_path = "login"
    
    async def navigate(self) -> None:
        """Navigate to the login page."""
        await self.navigate_to(self.url_path)
    
    async def login(self, username: str, password: str) -> None:
        """
        Perform login with given credentials.
        
        Args:
            username: Username to login with
            password: Password to login with
        """
        await self.fill_input(self.USERNAME_INPUT, username)
        await self.fill_input(self.PASSWORD_INPUT, password)
        await self.click_element(self.LOGIN_BUTTON)
    
    async def login_with_valid_credentials(self) -> None:
        """Login with valid credentials (tomsmith/SuperSecretPassword!)."""
        await self.login("tomsmith", "SuperSecretPassword!")
    
    async def login_with_invalid_credentials(self) -> None:
        """Login with invalid credentials."""
        await self.login("invaliduser", "invalidpassword")
    
    async def get_flash_message(self) -> str:
        """
        Get the flash message text.
        
        Returns:
            str: Flash message text
        """
        return await self.get_text(self.FLASH_MESSAGE)
    
    async def is_success_message_displayed(self) -> bool:
        """
        Check if success message is displayed.
        
        Returns:
            bool: True if success message is visible
        """
        return await self.is_element_visible(self.SUCCESS_MESSAGE)
    
    async def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            bool: True if error message is visible
        """
        return await self.is_element_visible(self.ERROR_MESSAGE)
    
    async def is_logout_button_displayed(self) -> bool:
        """
        Check if logout button is displayed (indicates successful login).
        
        Returns:
            bool: True if logout button is visible
        """
        return await self.is_element_visible(self.LOGOUT_BUTTON)
    
    async def logout(self) -> None:
        """Logout by clicking the logout button."""
        await self.click_element(self.LOGOUT_BUTTON)
    
    async def is_login_form_displayed(self) -> bool:
        """
        Check if login form is displayed.
        
        Returns:
            bool: True if login form elements are visible
        """
        return (await self.is_element_visible(self.USERNAME_INPUT) and
                await self.is_element_visible(self.PASSWORD_INPUT) and
                await self.is_element_visible(self.LOGIN_BUTTON))
    
    async def clear_username(self) -> None:
        """Clear the username field."""
        await self.page.fill(self.USERNAME_INPUT, "")
    
    async def clear_password(self) -> None:
        """Clear the password field."""
        await self.page.fill(self.PASSWORD_INPUT, "")