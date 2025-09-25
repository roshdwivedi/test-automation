"""
Page object models for dynamic elements, checkboxes, dropdown, and file upload pages.
"""

from playwright.async_api import Page
from .base_page import BasePage
import os
from typing import List


class AddRemoveElementsPage(BasePage):
    """Page object for the Add/Remove Elements page."""
    
    # Locators
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
        """
        Add multiple elements.
        
        Args:
            count: Number of elements to add
        """
        for _ in range(count):
            await self.add_element()
            await self.page.wait_for_timeout(500)  # Small delay
    
    async def get_delete_buttons(self) -> List:
        """
        Get all delete buttons.
        
        Returns:
            List: List of delete button elements
        """
        return await self.get_all_elements(self.DELETE_BUTTONS)
    
    async def get_delete_button_count(self) -> int:
        """
        Get count of delete buttons.
        
        Returns:
            int: Number of delete buttons
        """
        buttons = await self.get_delete_buttons()
        return len(buttons)
    
    async def remove_element(self, index: int = 0) -> None:
        """
        Remove an element by clicking a delete button.
        
        Args:
            index: Index of the delete button to click
        """
        buttons = await self.get_delete_buttons()
        if buttons and index < len(buttons):
            await buttons[index].click()
    
    async def remove_all_elements(self) -> None:
        """Remove all elements."""
        while True:
            buttons = await self.get_delete_buttons()
            if not buttons:
                break
            await buttons[0].click()


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
        """
        Get all checkbox elements.
        
        Returns:
            List: List of checkbox elements
        """
        return await self.get_all_elements(self.CHECKBOXES)
    
    async def get_checkbox_count(self) -> int:
        """
        Get count of checkboxes.
        
        Returns:
            int: Number of checkboxes
        """
        checkboxes = await self.get_checkboxes()
        return len(checkboxes)
    
    async def is_checkbox_checked(self, index: int) -> bool:
        """
        Check if a checkbox is checked.
        
        Args:
            index: Index of the checkbox
            
        Returns:
            bool: True if checked, False otherwise
        """
        checkboxes = await self.get_checkboxes()
        if checkboxes and index < len(checkboxes):
            return await checkboxes[index].is_checked()
        return False
    
    async def click_checkbox(self, index: int) -> None:
        """
        Click a checkbox.
        
        Args:
            index: Index of the checkbox to click
        """
        checkboxes = await self.get_checkboxes()
        if checkboxes and index < len(checkboxes):
            await checkboxes[index].click()
    
    async def check_checkbox(self, index: int) -> None:
        """
        Check a checkbox (ensure it's checked).
        
        Args:
            index: Index of the checkbox
        """
        if not await self.is_checkbox_checked(index):
            await self.click_checkbox(index)
    
    async def uncheck_checkbox(self, index: int) -> None:
        """
        Uncheck a checkbox (ensure it's unchecked).
        
        Args:
            index: Index of the checkbox
        """
        if await self.is_checkbox_checked(index):
            await self.click_checkbox(index)


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
        """
        Select an option by value.
        
        Args:
            value: Value of the option to select
        """
        dropdown = self.page.locator(self.DROPDOWN)
        await dropdown.select_option(value=value)
    
    async def select_option_by_text(self, text: str) -> None:
        """
        Select an option by visible text.
        
        Args:
            text: Text of the option to select
        """
        dropdown = self.page.locator(self.DROPDOWN)
        await dropdown.select_option(label=text)
    
    async def select_option_by_index(self, index: int) -> None:
        """
        Select an option by index.
        
        Args:
            index: Index of the option to select
        """
        dropdown = self.page.locator(self.DROPDOWN)
        await dropdown.select_option(index=index)
    
    async def get_selected_option_text(self) -> str:
        """
        Get the text of the currently selected option.
        
        Returns:
            str: Text of selected option
        """
        return await self.get_text(self.SELECTED_OPTION)
    
    async def get_all_option_texts(self) -> List[str]:
        """
        Get all option texts.
        
        Returns:
            List[str]: List of option texts
        """
        options = await self.get_all_elements(self.DROPDOWN_OPTIONS)
        return [await option.text_content() for option in options]
    
    async def get_dropdown_value(self) -> str:
        """
        Get the current dropdown value.
        
        Returns:
            str: Current dropdown value
        """
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
        """
        Select a file for upload.
        
        Args:
            file_path: Path to the file to upload
        """
        file_input = self.page.locator(self.FILE_INPUT)
        await file_input.set_input_files(file_path)
    
    async def click_upload_button(self) -> None:
        """Click the upload button."""
        await self.click_element(self.UPLOAD_BUTTON)
    
    async def upload_file(self, file_path: str) -> None:
        """
        Upload a file (select and click upload).
        
        Args:
            file_path: Path to the file to upload
        """
        await self.select_file(file_path)
        await self.click_upload_button()
    
    async def get_success_message(self) -> str:
        """
        Get the success message text.
        
        Returns:
            str: Success message text
        """
        return await self.get_text(self.SUCCESS_MESSAGE)
    
    async def get_uploaded_files_text(self) -> str:
        """
        Get the uploaded files text.
        
        Returns:
            str: Uploaded files text
        """
        return await self.get_text(self.UPLOADED_FILES)
    
    async def create_test_file(self, filename: str = "test_upload.txt", content: str = "Test file content") -> str:
        """
        Create a test file for upload.
        
        Args:
            filename: Name of the test file
            content: Content of the test file
            
        Returns:
            str: Path to the created test file
        """
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    
    async def cleanup_test_file(self, file_path: str) -> None:
        """
        Clean up a test file.
        
        Args:
            file_path: Path to the test file to remove
        """
        if os.path.exists(file_path):
            os.remove(file_path)