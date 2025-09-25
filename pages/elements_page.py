"""
Page object models for dynamic elements, checkboxes, dropdown, and file upload pages.
"""

from playwright.async_api import Page
from .base_page import BasePage
import os
from typing import List


class AddRemoveElementsPage(BasePage):
    """Page object for the Add/Remove Elements page."""
    
    # Locators: Essential for TestAddRemoveElements
    ADD_BUTTON = "//button[text()='Add Element']" 
    DELETE_BUTTONS = ".added-manually" 
    
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url_path = "add_remove_elements/"
    
    async def navigate(self) -> None:
        """Navigate to the Add/Remove Elements page."""
        await self.navigate_to(self.url_path)
    
    async def add_element(self) -> None:
        """Click the Add Element button."""
        await self.click_element(self.ADD_BUTTON)
    
    async def add_multiple_elements(self, count: int) -> None:
        """Add multiple elements."""
        for _ in range(count):
            await self.add_element()
            # Removed redundant page.wait_for_timeout(500) for cleaner code.
    
    async def get_delete_buttons(self) -> List:
        """Get all delete buttons."""
        return await self.get_all_elements(self.DELETE_BUTTONS)
    
    async def get_delete_button_count(self) -> int:
        """Get count of delete buttons."""
        buttons = await self.get_delete_buttons()
        return len(buttons)
    
    async def remove_element(self, index: int = 0) -> None:
        """Remove an element by clicking a delete button."""
        buttons = await self.get_delete_buttons()
        if buttons and index < len(buttons):
            await buttons[index].click()
    
    async def remove_all_elements(self) -> None:
        """Remove all elements."""
        # Fix: Use direct locator approach for guaranteed removal until none exist
        while await self.page.is_visible(self.DELETE_BUTTONS):
            await self.page.click(self.DELETE_BUTTONS)


class CheckboxPage(BasePage):
    """Page object for the Checkboxes page."""
    
    # Locators
    CHECKBOXES = "input[type='checkbox']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url_path = "checkboxes"
    
    async def navigate(self) -> None:
        """Navigate to the Checkboxes page."""
        await self.navigate_to(self.url_path)
    
    async def get_checkboxes(self) -> List:
        """Get all checkbox elements."""
        return await self.get_all_elements(self.CHECKBOXES)
    
    async def get_checkbox_count(self) -> int:
        """Get count of checkboxes."""
        checkboxes = await self.get_checkboxes()
        return len(checkboxes)
    
    async def is_checkbox_checked(self, index: int) -> bool:
        """Check if a checkbox is checked."""
        checkboxes = await self.get_checkboxes()
        if checkboxes and index < len(checkboxes):
            return await checkboxes[index].is_checked()
        return False
    
    async def click_checkbox(self, index: int) -> None:
        """Click a checkbox."""
        checkboxes = await self.get_checkboxes()
        if checkboxes and index < len(checkboxes):
            await checkboxes[index].click()
    
    async def check_checkbox(self, index: int) -> None:
        """Check a checkbox (ensure it's checked)."""
        checkboxes = await self.get_checkboxes()
        if checkboxes and index < len(checkboxes):
            await checkboxes[index].check() 
    
    async def uncheck_checkbox(self, index: int) -> None:
        """Uncheck a checkbox (ensure it's unchecked)."""
        checkboxes = await self.get_checkboxes()
        if checkboxes and index < len(checkboxes):
            await checkboxes[index].uncheck()


class DropdownPage(BasePage):
    """Page object for the Dropdown page."""
    
    # Locators
    DROPDOWN = "#dropdown"
    DROPDOWN_OPTIONS = "#dropdown option"
    SELECTED_OPTION = "#dropdown option:checked"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url_path = "dropdown"
    
    async def navigate(self) -> None:
        """Navigate to the Dropdown page."""
        await self.navigate_to(self.url_path)
    
    async def select_option_by_value(self, value: str) -> None:
        """Select an option by value."""
        dropdown = self.page.locator(self.DROPDOWN)
        await dropdown.select_option(value=value)
    
    async def select_option_by_text(self, text: str) -> None:
        """Select an option by visible text."""
        dropdown = self.page.locator(self.DROPDOWN)
        await dropdown.select_option(label=text)
    
    async def select_option_by_index(self, index: int) -> None:
        """Select an option by index."""
        dropdown = self.page.locator(self.DROPDOWN)
        await dropdown.select_option(index=index)
    
    async def get_selected_option_text(self) -> str:
        """
        Get the visible text of the currently selected option in the dropdown.
        This implementation is robust across browsers and Playwright versions.
        """
        return await self.page.eval_on_selector(
            self.DROPDOWN,
            "el => el.selectedOptions && el.selectedOptions.length ? el.selectedOptions[0].textContent.trim() : ''",
        )
    
    async def get_all_option_texts(self) -> List[str]:
        """Get all option texts."""
        options = await self.get_all_elements(self.DROPDOWN_OPTIONS)
        return [await option.inner_text() for option in options]
    
    async def get_dropdown_value(self) -> str:
        """Get the current dropdown value."""
        dropdown = self.page.locator(self.DROPDOWN)
        return await dropdown.input_value()


class FileUploadPage(BasePage):
    """Page object for the File Upload page."""
    
    # Locators
    FILE_INPUT = "#file-upload"
    UPLOAD_BUTTON = "#file-submit"
    UPLOADED_FILES = "#uploaded-files"
    SUCCESS_MESSAGE = "h3"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url_path = "upload"
    
    async def navigate(self) -> None:
        """Navigate to the File Upload page."""
        await self.navigate_to(self.url_path)
    
    async def select_file(self, file_path: str) -> None:
        """Select a file for upload."""
        file_input = self.page.locator(self.FILE_INPUT)
        await file_input.set_input_files(file_path)
    
    async def click_upload_button(self) -> None:
        """Click the upload button."""
        await self.click_element(self.UPLOAD_BUTTON)
    
    async def upload_file(self, file_path: str) -> None:
        """Upload a file (select and click upload)."""
        await self.select_file(file_path)
        await self.click_upload_button()
    
    async def get_success_message(self) -> str:
        """Get the success message text."""
        return await self.get_text(self.SUCCESS_MESSAGE)
    
    async def get_uploaded_files_text(self) -> str:
        """Get the uploaded files text."""
        return await self.get_text(self.UPLOADED_FILES)
    
    async def create_test_file(self, filename: str = "test_upload.txt", content: str = "Test file content") -> str:
        """Create a test file for upload."""
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    
    async def cleanup_test_file(self, file_path: str) -> None:
        """Clean up a test file."""
        if os.path.exists(file_path):
            os.remove(file_path)