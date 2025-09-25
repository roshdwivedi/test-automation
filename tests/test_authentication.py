"""
Authentication tests for Web Automation Test Suite.

This module contains tests for login/logout functionality.
"""

import pytest
from playwright.async_api import Page
from ..pages.login_page import LoginPage


@pytest.mark.asyncio
@pytest.mark.auth
@pytest.mark.smoke
class TestAuthentication:
    """Test class for authentication scenarios."""
    
    async def test_valid_login(self, page: Page):
        """Test successful login with valid credentials."""
        login_page = LoginPage(page)
        
        # Navigate to login page
        await login_page.navigate()
        
        # Verify login form is displayed
        assert await login_page.is_login_form_displayed(), "Login form should be displayed"
        
        # Perform login with valid credentials
        await login_page.login_with_valid_credentials()
        
        # Verify successful login
        assert await login_page.is_success_message_displayed(), "Success message should be displayed"
        
        flash_message = await login_page.get_flash_message()
        assert "You logged into a secure area!" in flash_message, f"Expected success message, got: {flash_message}"
        
        # Verify logout button is present (indicates successful login)
        assert await login_page.is_logout_button_displayed(), "Logout button should be displayed after login"
        
        # Verify URL changed to secure area
        current_url = await login_page.get_url()
        assert "/secure" in current_url, f"URL should contain '/secure', but got: {current_url}"
    
    async def test_invalid_login(self, page: Page):
        """Test login failure with invalid credentials."""
        login_page = LoginPage(page)
        
        # Navigate to login page
        await login_page.navigate()
        
        # Perform login with invalid credentials
        await login_page.login_with_invalid_credentials()
        
        # Verify error message is displayed
        assert await login_page.is_error_message_displayed(), "Error message should be displayed"
        
        flash_message = await login_page.get_flash_message()
        assert "Your username is invalid!" in flash_message, f"Expected error message, got: {flash_message}"
        
        # Verify still on login page (login failed)
        current_url = await login_page.get_url()
        assert "/login" in current_url, f"Should still be on login page, but got: {current_url}"
        
        # Verify logout button is not present
        assert not await login_page.is_logout_button_displayed(), "Logout button should not be displayed after failed login"
    
    async def test_empty_credentials(self, page: Page):
        """Test login with empty credentials."""
        login_page = LoginPage(page)
        
        # Navigate to login page
        await login_page.navigate()
        
        # Try to login with empty credentials
        await login_page.login("", "")
        
        # Verify error message is displayed
        assert await login_page.is_error_message_displayed(), "Error message should be displayed for empty credentials"
    
    async def test_empty_username(self, page: Page):
        """Test login with empty username."""
        login_page = LoginPage(page)
        
        # Navigate to login page
        await login_page.navigate()
        
        # Try to login with empty username
        await login_page.login("", "password")
        
        # Verify error message is displayed
        assert await login_page.is_error_message_displayed(), "Error message should be displayed for empty username"
    
    async def test_empty_password(self, page: Page):
        """Test login with empty password."""
        login_page = LoginPage(page)
        
        # Navigate to login page
        await login_page.navigate()
        
        # Try to login with empty password
        await login_page.login("tomsmith", "")
        
        # Verify error message is displayed
        assert await login_page.is_error_message_displayed(), "Error message should be displayed for empty password"
    
    async def test_logout_functionality(self, authenticated_page: Page):
        """Test logout functionality with pre-authenticated page."""
        login_page = LoginPage(authenticated_page)
        
        # Verify we're in the secure area
        current_url = await login_page.get_url()
        assert "/secure" in current_url, "Should be in secure area"
        
        # Verify logout button is displayed
        assert await login_page.is_logout_button_displayed(), "Logout button should be displayed in secure area"
        
        # Perform logout
        await login_page.logout()
        
        # Verify we're back on login page
        await authenticated_page.wait_for_timeout(1000)  # Wait for redirect
        current_url = await login_page.get_url()
        assert "/login" in current_url, f"Should be back on login page, but got: {current_url}"
        
        # Verify success message for logout
        flash_message = await login_page.get_flash_message()
        assert "You logged out of the secure area!" in flash_message, f"Expected logout message, got: {flash_message}"
        
        # Verify login form is displayed again
        assert await login_page.is_login_form_displayed(), "Login form should be displayed after logout"
    
    async def test_case_sensitive_username(self, page: Page):
        """Test that username is case sensitive."""
        login_page = LoginPage(page)
        
        # Navigate to login page
        await login_page.navigate()
        
        # Try to login with uppercase username
        await login_page.login("TOMSMITH", "SuperSecretPassword!")
        
        # Verify login fails
        assert await login_page.is_error_message_displayed(), "Login should fail with case-sensitive username"
    
    async def test_case_sensitive_password(self, page: Page):
        """Test that password is case sensitive."""
        login_page = LoginPage(page)
        
        # Navigate to login page
        await login_page.navigate()
        
        # Try to login with incorrect case password
        await login_page.login("tomsmith", "supersecretpassword!")
        
        # Verify login fails
        assert await login_page.is_error_message_displayed(), "Login should fail with case-sensitive password"