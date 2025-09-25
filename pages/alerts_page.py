"""
Page object model for the JavaScript Alerts page.
"""

from playwright.async_api import Page, Dialog
from .base_page import BasePage


class AlertsPage(BasePage):
    """Page object for the JavaScript Alerts page."""
    
    # Locators
    ALERT_BUTTON = "button[onclick='jsAlert()']"
    CONFIRM_BUTTON = "button[onclick='jsConfirm()']"
    PROMPT_BUTTON = "button[onclick='jsPrompt()']"
    RESULT_TEXT = "#result"
    
    def __init__(self, page: Page):
        """
        Initialize alerts page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url_path = "javascript_alerts"
        self.dialog_result = None
    
    async def navigate(self) -> None:
        """Navigate to the JavaScript Alerts page."""
        await self.navigate_to(self.url_path)
    
    def setup_dialog_handler(self, action: str = "accept", text: str = "") -> None:
        """
        Setup dialog handler for alerts.
        
        Args:
            action: Action to take ('accept' or 'dismiss')
            text: Text to enter for prompts
        """
        def handle_dialog(dialog: Dialog):
            # Schedule dialog handling without requiring 'await' in test code
            if action == "accept":
                if dialog.type == "prompt":
                    asyncio.create_task(dialog.accept(text))
                else:
                    asyncio.create_task(dialog.accept())
            else:
                asyncio.create_task(dialog.dismiss())
        
        # Lazily create storage for our own handlers
        if not hasattr(self, "_dialog_handlers"):
            self._dialog_handlers = []  # type: ignore[attr-defined]
        self._dialog_handlers.append(handle_dialog)  # type: ignore[attr-defined]
        self.page.on("dialog", handle_dialog)
    
    async def remove_dialog_handlers(self) -> None:
        """Remove dialog handlers that were registered via this page object."""
        handlers = getattr(self, "_dialog_handlers", [])
        for h in handlers:
            try:
                self.page.remove_listener("dialog", h)
            except Exception:
                # If already removed, ignore
                pass
        if hasattr(self, "_dialog_handlers"):
            self._dialog_handlers.clear()  # type: ignore[attr-defined]
    
    async def trigger_alert(self) -> None:
        """Trigger a JavaScript alert."""
        # One-time fallback to ensure the dialog gets accepted if user handler doesn't await
        def _fallback(dialog: Dialog):
            async def _safe():
                try:
                    await dialog.accept()
                except Exception:
                    pass
            asyncio.create_task(_safe())
        self.page.once("dialog", _fallback)
        await self.click_element(self.ALERT_BUTTON)
    
    async def trigger_confirm(self) -> None:
        """Trigger a JavaScript confirm dialog."""
        def _fallback(dialog: Dialog):
            async def _safe():
                try:
                    await dialog.accept()
                except Exception:
                    pass
            asyncio.create_task(_safe())
        self.page.once("dialog", _fallback)
        await self.click_element(self.CONFIRM_BUTTON)
    
    async def trigger_prompt(self) -> None:
        """Trigger a JavaScript prompt dialog."""
        def _fallback(dialog: Dialog):
            async def _safe():
                try:
                    await dialog.accept()
                except Exception:
                    pass
            asyncio.create_task(_safe())
        self.page.once("dialog", _fallback)
        await self.click_element(self.PROMPT_BUTTON)
    
    async def get_result_text(self) -> str:
        """
        Get the result text after dialog interaction.
        
        Returns:
            str: Result text
        """
        return await self.get_text(self.RESULT_TEXT)
    
    async def handle_alert_and_get_result(self) -> str:
        """
        Handle alert dialog and return result.
        
        Returns:
            str: Result text after handling alert
        """
        self.setup_dialog_handler("accept")
        await self.trigger_alert()
        await self.page.wait_for_timeout(1000)  # Wait for result to update
        return await self.get_result_text()
    
    async def handle_confirm_accept_and_get_result(self) -> str:
        """
        Handle confirm dialog by accepting and return result.
        
        Returns:
            str: Result text after accepting confirm
        """
        self.setup_dialog_handler("accept")
        await self.trigger_confirm()
        await self.page.wait_for_timeout(1000)
        return await self.get_result_text()
    
    async def handle_confirm_dismiss_and_get_result(self) -> str:
        """
        Handle confirm dialog by dismissing and return result.
        
        Returns:
            str: Result text after dismissing confirm
        """
        self.setup_dialog_handler("dismiss")
        await self.trigger_confirm()
        await self.page.wait_for_timeout(1000)
        return await self.get_result_text()
    
    async def handle_prompt_and_get_result(self, input_text: str) -> str:
        """
        Handle prompt dialog with input text and return result.
        
        Args:
            input_text: Text to enter in prompt
            
        Returns:
            str: Result text after handling prompt
        """
        self.setup_dialog_handler("accept", input_text)
        await self.trigger_prompt()
        await self.page.wait_for_timeout(1000)
        return await self.get_result_text()
    
    async def is_result_displayed(self) -> bool:
        """
        Check if result text is displayed.
        
        Returns:
            bool: True if result is visible
        """
        return await self.is_element_visible(self.RESULT_TEXT)


# Import asyncio for dialog handling
import asyncio
