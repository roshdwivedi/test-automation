"""
JavaScript alerts tests for Web Automation Test Suite.

This module contains tests for JavaScript alerts, confirm, and prompt dialogs.
"""

import pytest
from playwright.async_api import Page, Dialog
from ..pages.alerts_page import AlertsPage


@pytest.mark.asyncio
@pytest.mark.alerts
class TestJavaScriptAlerts:
    """Test class for JavaScript Alerts functionality."""
    
    async def test_simple_alert(self, page: Page):
        """Test handling a simple JavaScript alert."""
        alerts_page = AlertsPage(page)
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Set up alert handler to accept
        alerts_page.page.on("dialog", lambda dialog: dialog.accept())
        
        # Trigger alert
        await alerts_page.trigger_alert()
        
        # Wait for result to update
        await page.wait_for_timeout(1000)
        
        # Verify result
        result = await alerts_page.get_result_text()
        assert "You successfully clicked an alert" in result, f"Expected success message, got: {result}"
        
        # Clean up
        alerts_page.remove_dialog_handlers()
    
    async def test_confirm_accept(self, page: Page):
        """Test accepting a JavaScript confirm dialog."""
        alerts_page = AlertsPage(page)
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Set up confirm handler to accept
        alerts_page.page.on("dialog", lambda dialog: dialog.accept())
        
        # Trigger confirm
        await alerts_page.trigger_confirm()
        
        # Wait for result to update
        await page.wait_for_timeout(1000)
        
        # Verify result
        result = await alerts_page.get_result_text()
        assert "You clicked: Ok" in result, f"Expected 'Ok' result, got: {result}"
        
        # Clean up
        alerts_page.remove_dialog_handlers()
    
    async def test_confirm_dismiss(self, page: Page):
        """Test dismissing a JavaScript confirm dialog."""
        alerts_page = AlertsPage(page)
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Set up confirm handler to dismiss
        alerts_page.page.on("dialog", lambda dialog: dialog.dismiss())
        
        # Trigger confirm
        await alerts_page.trigger_confirm()
        
        # Wait for result to update
        await page.wait_for_timeout(1000)
        
        # Verify result
        result = await alerts_page.get_result_text()
        assert "You clicked: Cancel" in result, f"Expected 'Cancel' result, got: {result}"
        
        # Clean up
        alerts_page.remove_dialog_handlers()
    
    async def test_prompt_with_text(self, page: Page):
        """Test entering text in a JavaScript prompt."""
        alerts_page = AlertsPage(page)
        test_text = "Hello Playwright!"
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Set up prompt handler with text
        alerts_page.page.on("dialog", lambda dialog: dialog.accept(test_text))
        
        # Trigger prompt
        await alerts_page.trigger_prompt()
        
        # Wait for result to update
        await page.wait_for_timeout(1000)
        
        # Verify result
        result = await alerts_page.get_result_text()
        assert f"You entered: {test_text}" in result, f"Expected '{test_text}' in result, got: {result}"
        
        # Clean up
        alerts_page.remove_dialog_handlers()
    
    async def test_prompt_with_empty_text(self, page: Page):
        """Test entering empty text in a JavaScript prompt."""
        alerts_page = AlertsPage(page)
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Set up prompt handler with empty text
        alerts_page.page.on("dialog", lambda dialog: dialog.accept(""))
        
        # Trigger prompt
        await alerts_page.trigger_prompt()
        
        # Wait for result to update
        await page.wait_for_timeout(1000)
        
        # Verify result
        result = await alerts_page.get_result_text()
        assert "You entered:" in result, f"Expected empty prompt result, got: {result}"
        
        # Clean up
        alerts_page.remove_dialog_handlers()
    
    async def test_prompt_dismiss(self, page: Page):
        """Test dismissing a JavaScript prompt."""
        alerts_page = AlertsPage(page)
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Set up prompt handler to dismiss
        alerts_page.page.on("dialog", lambda dialog: dialog.dismiss())
        
        # Trigger prompt
        await alerts_page.trigger_prompt()
        
        # Wait for result to update
        await page.wait_for_timeout(1000)
        
        # Verify result
        result = await alerts_page.get_result_text()
        assert "You entered: null" in result, f"Expected null result, got: {result}"
        
        # Clean up
        alerts_page.remove_dialog_handlers()
    
    async def test_multiple_alerts_sequence(self, page: Page):
        """Test handling multiple alerts in sequence."""
        alerts_page = AlertsPage(page)
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Test sequence: Alert -> Confirm (Accept) -> Prompt with text
        test_scenarios = [
            ("alert", None, "You successfully clicked an alert"),
            ("confirm_accept", None, "You clicked: Ok"),
            ("prompt", "Test Input", "You entered: Test Input")
        ]
        
        for scenario_type, input_text, expected_result in test_scenarios:
            # Set up appropriate handler
            if scenario_type == "alert":
                alerts_page.page.on("dialog", lambda dialog: dialog.accept())
                await alerts_page.trigger_alert()
            elif scenario_type == "confirm_accept":
                alerts_page.page.on("dialog", lambda dialog: dialog.accept())
                await alerts_page.trigger_confirm()
            elif scenario_type == "prompt":
                alerts_page.page.on("dialog", lambda dialog: dialog.accept(input_text))
                await alerts_page.trigger_prompt()
            
            # Wait and verify result
            await page.wait_for_timeout(1000)
            result = await alerts_page.get_result_text()
            assert expected_result in result, f"Expected '{expected_result}', got: {result}"
            
            # Clean up for next iteration
            alerts_page.remove_dialog_handlers()
    
    async def test_dialog_properties(self, page: Page):
        """Test dialog properties and content."""
        alerts_page = AlertsPage(page)
        
        # Navigate to page
        await alerts_page.navigate()
        
        dialog_info = {}
        
        def handle_dialog(dialog: Dialog):
            dialog_info['type'] = dialog.type
            dialog_info['message'] = dialog.message
            dialog_info['default_value'] = dialog.default_value
            dialog.accept()
        
        alerts_page.page.on("dialog", handle_dialog)
        
        # Test alert dialog properties
        await alerts_page.trigger_alert()
        await page.wait_for_timeout(500)
        
        assert dialog_info['type'] == 'alert', f"Expected alert type, got: {dialog_info['type']}"
        assert "I am a JS Alert" in dialog_info['message'], f"Unexpected alert message: {dialog_info['message']}"
        
        # Reset for next test
        dialog_info.clear()
        
        # Test confirm dialog properties
        await alerts_page.trigger_confirm()
        await page.wait_for_timeout(500)
        
        assert dialog_info['type'] == 'confirm', f"Expected confirm type, got: {dialog_info['type']}"
        assert "I am a JS Confirm" in dialog_info['message'], f"Unexpected confirm message: {dialog_info['message']}"
        
        # Reset for next test
        dialog_info.clear()
        
        # Test prompt dialog properties
        await alerts_page.trigger_prompt()
        await page.wait_for_timeout(500)
        
        assert dialog_info['type'] == 'prompt', f"Expected prompt type, got: {dialog_info['type']}"
        assert "I am a JS prompt" in dialog_info['message'], f"Unexpected prompt message: {dialog_info['message']}"
        
        # Clean up
        alerts_page.remove_dialog_handlers()
    
    async def test_alert_buttons_present(self, page: Page):
        """Test that all alert trigger buttons are present."""
        alerts_page = AlertsPage(page)
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Verify all buttons are visible
        alert_button_visible = await alerts_page.is_element_visible(alerts_page.ALERT_BUTTON)
        assert alert_button_visible, "Alert button should be visible"
        
        confirm_button_visible = await alerts_page.is_element_visible(alerts_page.CONFIRM_BUTTON)
        assert confirm_button_visible, "Confirm button should be visible"
        
        prompt_button_visible = await alerts_page.is_element_visible(alerts_page.PROMPT_BUTTON)
        assert prompt_button_visible, "Prompt button should be visible"
        
        # Verify result area is present
        result_visible = await alerts_page.is_element_visible(alerts_page.RESULT_TEXT)
        assert result_visible, "Result text area should be visible"
    
    async def test_prompt_with_special_characters(self, page: Page):
        """Test prompt with special characters."""
        alerts_page = AlertsPage(page)
        special_text = "Hello! @#$%^&*()_+ 你好 🎉"
        
        # Navigate to page
        await alerts_page.navigate()
        
        # Set up prompt handler with special characters
        alerts_page.page.on("dialog", lambda dialog: dialog.accept(special_text))
        
        # Trigger prompt
        await alerts_page.trigger_prompt()
        
        # Wait for result to update
        await page.wait_for_timeout(1000)
        
        # Verify result contains the special text
        result = await alerts_page.get_result_text()
        assert f"You entered: {special_text}" in result, f"Expected special characters in result, got: {result}"
        
        # Clean up
        alerts_page.remove_dialog_handlers()