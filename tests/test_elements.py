"""
Element interaction tests for Web Automation Test Suite.

This module contains tests for dynamic elements, checkboxes, and dropdowns.
"""

import pytest
from playwright.async_api import Page
from ..pages.elements_page import AddRemoveElementsPage, CheckboxPage, DropdownPage


@pytest.mark.asyncio
@pytest.mark.elements
class TestAddRemoveElements:
    """Test class for Add/Remove Elements functionality."""
    
    async def test_add_single_element(self, page: Page):
        """Test adding a single element."""
        elements_page = AddRemoveElementsPage(page)
        
        # Navigate to page
        await elements_page.navigate()
        
        # Verify initial state (no delete buttons)
        initial_count = await elements_page.get_delete_button_count()
        assert initial_count == 0, f"Expected 0 delete buttons initially, got {initial_count}"
        
        # Add one element
        await elements_page.add_element()
        
        # Verify one delete button is present
        count_after_add = await elements_page.get_delete_button_count()
        assert count_after_add == 1, f"Expected 1 delete button after adding, got {count_after_add}"
    
    async def test_add_multiple_elements(self, page: Page):
        """Test adding multiple elements."""
        elements_page = AddRemoveElementsPage(page)
        
        # Navigate to page
        await elements_page.navigate()
        
        # Add 5 elements
        await elements_page.add_multiple_elements(5)
        
        # Verify 5 delete buttons are present
        count = await elements_page.get_delete_button_count()
        assert count == 5, f"Expected 5 delete buttons, got {count}"
    
    async def test_remove_single_element(self, page: Page):
        """Test removing a single element."""
        elements_page = AddRemoveElementsPage(page)
        
        # Navigate to page and add elements
        await elements_page.navigate()
        await elements_page.add_multiple_elements(3)
        
        # Remove one element
        await elements_page.remove_element(0)
        
        # Verify count decreased
        count = await elements_page.get_delete_button_count()
        assert count == 2, f"Expected 2 delete buttons after removal, got {count}"
    
    async def test_remove_all_elements(self, page: Page):
        """Test removing all elements."""
        elements_page = AddRemoveElementsPage(page)
        
        # Navigate to page and add elements
        await elements_page.navigate()
        await elements_page.add_multiple_elements(3)
        
        # Remove all elements
        await elements_page.remove_all_elements()
        
        # Verify no elements remain
        count = await elements_page.get_delete_button_count()
        assert count == 0, f"Expected 0 delete buttons after removing all, got {count}"
    
    async def test_add_and_remove_sequence(self, page: Page):
        """Test a sequence of adding and removing elements."""
        elements_page = AddRemoveElementsPage(page)
        
        # Navigate to page
        await elements_page.navigate()
        
        # Add 3 elements
        await elements_page.add_multiple_elements(3)
        assert await elements_page.get_delete_button_count() == 3
        
        # Remove 2 elements
        await elements_page.remove_element(0)
        await elements_page.remove_element(0)  # Index 0 again because list shrinks
        assert await elements_page.get_delete_button_count() == 1
        
        # Add 2 more elements
        await elements_page.add_multiple_elements(2)
        assert await elements_page.get_delete_button_count() == 3
        
        # Remove remaining element
        await elements_page.remove_element(0)
        await elements_page.remove_element(0)
        await elements_page.remove_element(0)
        assert await elements_page.get_delete_button_count() == 0


@pytest.mark.asyncio
@pytest.mark.elements
class TestCheckboxes:
    """Test class for Checkbox functionality."""
    
    async def test_checkbox_initial_states(self, page: Page):
        """Test initial states of checkboxes."""
        checkbox_page = CheckboxPage(page)
        
        # Navigate to page
        await checkbox_page.navigate()
        
        # Verify there are 2 checkboxes
        count = await checkbox_page.get_checkbox_count()
        assert count == 2, f"Expected 2 checkboxes, got {count}"
        
        # Verify initial states (first unchecked, second checked)
        assert not await checkbox_page.is_checkbox_checked(0), "First checkbox should be initially unchecked"
        assert await checkbox_page.is_checkbox_checked(1), "Second checkbox should be initially checked"
    
    async def test_click_unchecked_checkbox(self, page: Page):
        """Test clicking an unchecked checkbox."""
        checkbox_page = CheckboxPage(page)
        
        # Navigate to page
        await checkbox_page.navigate()
        
        # Click first checkbox (initially unchecked)
        await checkbox_page.click_checkbox(0)
        
        # Verify it's now checked
        assert await checkbox_page.is_checkbox_checked(0), "First checkbox should be checked after clicking"
    
    async def test_click_checked_checkbox(self, page: Page):
        """Test clicking a checked checkbox."""
        checkbox_page = CheckboxPage(page)
        
        # Navigate to page
        await checkbox_page.navigate()
        
        # Click second checkbox (initially checked)
        await checkbox_page.click_checkbox(1)
        
        # Verify it's now unchecked
        assert not await checkbox_page.is_checkbox_checked(1), "Second checkbox should be unchecked after clicking"
    
    async def test_check_checkbox_method(self, page: Page):
        """Test the check_checkbox method."""
        checkbox_page = CheckboxPage(page)
        
        # Navigate to page
        await checkbox_page.navigate()
        
        # Ensure first checkbox is checked
        await checkbox_page.check_checkbox(0)
        assert await checkbox_page.is_checkbox_checked(0), "First checkbox should be checked"
        
        # Calling check again should keep it checked
        await checkbox_page.check_checkbox(0)
        assert await checkbox_page.is_checkbox_checked(0), "First checkbox should still be checked"
    
    async def test_uncheck_checkbox_method(self, page: Page):
        """Test the uncheck_checkbox method."""
        checkbox_page = CheckboxPage(page)
        
        # Navigate to page
        await checkbox_page.navigate()
        
        # Ensure second checkbox is unchecked
        await checkbox_page.uncheck_checkbox(1)
        assert not await checkbox_page.is_checkbox_checked(1), "Second checkbox should be unchecked"
        
        # Calling uncheck again should keep it unchecked
        await checkbox_page.uncheck_checkbox(1)
        assert not await checkbox_page.is_checkbox_checked(1), "Second checkbox should still be unchecked"
    
    async def test_toggle_all_checkboxes(self, page: Page):
        """Test toggling all checkboxes multiple times."""
        checkbox_page = CheckboxPage(page)
        
        # Navigate to page
        await checkbox_page.navigate()
        
        # Toggle all checkboxes
        await checkbox_page.click_checkbox(0)
        await checkbox_page.click_checkbox(1)
        
        # Verify states changed
        assert await checkbox_page.is_checkbox_checked(0), "First checkbox should be checked"
        assert not await checkbox_page.is_checkbox_checked(1), "Second checkbox should be unchecked"
        
        # Toggle again to restore original states
        await checkbox_page.click_checkbox(0)
        await checkbox_page.click_checkbox(1)
        
        # Verify back to original states
        assert not await checkbox_page.is_checkbox_checked(0), "First checkbox should be back to unchecked"
        assert await checkbox_page.is_checkbox_checked(1), "Second checkbox should be back to checked"


@pytest.mark.asyncio
@pytest.mark.forms
class TestDropdown:
    """Test class for Dropdown functionality."""
    
    async def test_dropdown_initial_state(self, page: Page):
        """Test initial state of dropdown."""
        dropdown_page = DropdownPage(page)
        
        # Navigate to page
        await dropdown_page.navigate()
        
        # Verify initial value is empty
        initial_value = await dropdown_page.get_dropdown_value()
        assert initial_value == "", f"Expected empty initial value, got '{initial_value}'"
    
    async def test_select_by_value(self, page: Page):
        """Test selecting option by value."""
        dropdown_page = DropdownPage(page)
        
        # Navigate to page
        await dropdown_page.navigate()
        
        # Select Option 1 by value
        await dropdown_page.select_option_by_value("1")
        selected_text = await dropdown_page.get_selected_option_text()
        assert selected_text == "Option 1", f"Expected 'Option 1', got '{selected_text}'"
        
        # Select Option 2 by value
        await dropdown_page.select_option_by_value("2")
        selected_text = await dropdown_page.get_selected_option_text()
        assert selected_text == "Option 2", f"Expected 'Option 2', got '{selected_text}'"
    
    async def test_select_by_text(self, page: Page):
        """Test selecting option by visible text."""
        dropdown_page = DropdownPage(page)
        
        # Navigate to page
        await dropdown_page.navigate()
        
        # Select by text
        await dropdown_page.select_option_by_text("Option 1")
        selected_text = await dropdown_page.get_selected_option_text()
        assert selected_text == "Option 1", f"Expected 'Option 1', got '{selected_text}'"
        
        await dropdown_page.select_option_by_text("Option 2")
        selected_text = await dropdown_page.get_selected_option_text()
        assert selected_text == "Option 2", f"Expected 'Option 2', got '{selected_text}'"
    
    async def test_select_by_index(self, page: Page):
        """Test selecting option by index."""
        dropdown_page = DropdownPage(page)
        
        # Navigate to page
        await dropdown_page.navigate()
        
        # Select by index (Option 1 is index 1, Option 2 is index 2)
        await dropdown_page.select_option_by_index(1)
        selected_text = await dropdown_page.get_selected_option_text()
        assert selected_text == "Option 1", f"Expected 'Option 1', got '{selected_text}'"
        
        await dropdown_page.select_option_by_index(2)
        selected_text = await dropdown_page.get_selected_option_text()
        assert selected_text == "Option 2", f"Expected 'Option 2', got '{selected_text}'"
    
    async def test_get_all_options(self, page: Page):
        """Test getting all dropdown options."""
        dropdown_page = DropdownPage(page)
        
        # Navigate to page
        await dropdown_page.navigate()
        
        # Get all option texts
        option_texts = await dropdown_page.get_all_option_texts()
        expected_options = ["Please select an option", "Option 1", "Option 2"]
        assert option_texts == expected_options, f"Expected {expected_options}, got {option_texts}"
    
    async def test_multiple_selections(self, page: Page):
        """Test multiple sequential selections."""
        dropdown_page = DropdownPage(page)
        
        # Navigate to page
        await dropdown_page.navigate()
        
        # Test sequence of selections
        selections = [
            ("1", "Option 1"),
            ("2", "Option 2"),
            ("1", "Option 1")
        ]
        
        for value, expected_text in selections:
            await dropdown_page.select_option_by_value(value)
            selected_text = await dropdown_page.get_selected_option_text()
            assert selected_text == expected_text, f"Expected '{expected_text}', got '{selected_text}'"