"""
File upload tests for Web Automation Test Suite.

This module contains tests for file upload functionality.
"""

import pytest
import os
from playwright.async_api import Page
from pages.elements_page import FileUploadPage


@pytest.mark.asyncio
@pytest.mark.forms
@pytest.mark.slow
class TestFileUpload:
    """Test class for File Upload functionality."""
    
    async def test_upload_text_file(self, page: Page):
        """Test uploading a text file."""
        upload_page = FileUploadPage(page)
        
        # Navigate to page
        await upload_page.navigate()
        
        # Create a test file
        test_file_path = await upload_page.create_test_file()
        
        try:
            # Upload the file
            await upload_page.upload_file(test_file_path)
            
            # Verify success message
            success_message = await upload_page.get_success_message()
            assert "File Uploaded!" in success_message, f"Expected success message, got: {success_message}"
            
            # Verify uploaded file name is displayed
            uploaded_files_text = await upload_page.get_uploaded_files_text()
            assert "test_upload.txt" in uploaded_files_text, f"Expected filename in uploaded files, got: {uploaded_files_text}"
            
        finally:
            # Clean up test file
            await upload_page.cleanup_test_file(test_file_path)
    
    async def test_upload_custom_filename(self, page: Page):
        """Test uploading a file with custom filename."""
        upload_page = FileUploadPage(page)
        
        # Navigate to page
        await upload_page.navigate()
        
        # Create a test file with custom name
        custom_filename = "my_custom_file.txt"
        test_file_path = await upload_page.create_test_file(
            filename=custom_filename,
            content="Custom file content for testing"
        )
        
        try:
            # Upload the file
            await upload_page.upload_file(test_file_path)
            
            # Verify success message
            success_message = await upload_page.get_success_message()
            assert "File Uploaded!" in success_message
            
            # Verify custom filename is displayed
            uploaded_files_text = await upload_page.get_uploaded_files_text()
            assert custom_filename in uploaded_files_text, f"Expected {custom_filename} in uploaded files"
            
        finally:
            # Clean up test file
            await upload_page.cleanup_test_file(test_file_path)
    
    async def test_upload_different_file_types(self, page: Page):
        """Test uploading different file types."""
        upload_page = FileUploadPage(page)
        
        # Navigate to page
        await upload_page.navigate()
        
        # Test different file types
        file_types = [
            ("test.csv", "name,age\\nJohn,25\\nJane,30"),
            ("test.json", '{"name": "test", "value": 123}'),
            ("test.xml", "<?xml version='1.0'?><root><item>test</item></root>")
        ]
        
        for filename, content in file_types:
            test_file_path = await upload_page.create_test_file(filename, content)
            
            try:
                # Upload the file
                await upload_page.upload_file(test_file_path)
                
                # Verify success
                success_message = await upload_page.get_success_message()
                assert "File Uploaded!" in success_message, f"Failed to upload {filename}"
                
                # Verify filename is displayed
                uploaded_files_text = await upload_page.get_uploaded_files_text()
                assert filename in uploaded_files_text, f"Expected {filename} in uploaded files"
                
            finally:
                # Clean up test file
                await upload_page.cleanup_test_file(test_file_path)
            
            # Navigate back for next test
            await upload_page.navigate()
    
    async def test_upload_large_file(self, page: Page):
        """Test uploading a larger file."""
        upload_page = FileUploadPage(page)
        
        # Navigate to page
        await upload_page.navigate()
        
        # Create a larger test file (1KB of content)
        large_content = "This is a larger test file. " * 50  # About 1KB
        test_file_path = await upload_page.create_test_file(
            filename="large_test_file.txt",
            content=large_content
        )
        
        try:
            # Upload the file
            await upload_page.upload_file(test_file_path)
            
            # Verify success message
            success_message = await upload_page.get_success_message()
            assert "File Uploaded!" in success_message
            
            # Verify filename is displayed
            uploaded_files_text = await upload_page.get_uploaded_files_text()
            assert "large_test_file.txt" in uploaded_files_text
            
        finally:
            # Clean up test file
            await upload_page.cleanup_test_file(test_file_path)
    
    async def test_select_file_without_uploading(self, page: Page):
        """Test selecting a file but not uploading it."""
        upload_page = FileUploadPage(page)
        
        # Navigate to page
        await upload_page.navigate()
        
        # Create a test file
        test_file_path = await upload_page.create_test_file()
        
        try:
            # Just select the file without clicking upload
            await upload_page.select_file(test_file_path)
            
            # Verify we're still on the upload page (not on success page)
            current_url = await upload_page.get_url()
            assert "/upload" in current_url, "Should still be on upload page"
            
            # Now click upload
            await upload_page.click_upload_button()
            
            # Verify success
            success_message = await upload_page.get_success_message()
            assert "File Uploaded!" in success_message
            
        finally:
            # Clean up test file
            await upload_page.cleanup_test_file(test_file_path)
    
    async def test_upload_empty_file(self, page: Page):
        """Test uploading an empty file."""
        upload_page = FileUploadPage(page)
        
        # Navigate to page
        await upload_page.navigate()
        
        # Create an empty test file
        test_file_path = await upload_page.create_test_file(
            filename="empty_file.txt",
            content=""
        )
        
        try:
            # Upload the empty file
            await upload_page.upload_file(test_file_path)
            
            # Verify success message (site should still accept empty files)
            success_message = await upload_page.get_success_message()
            assert "File Uploaded!" in success_message
            
            # Verify filename is displayed
            uploaded_files_text = await upload_page.get_uploaded_files_text()
            assert "empty_file.txt" in uploaded_files_text
            
        finally:
            # Clean up test file
            await upload_page.cleanup_test_file(test_file_path)
    
    async def test_file_upload_form_elements(self, page: Page):
        """Test that file upload form elements are present."""
        upload_page = FileUploadPage(page)
        
        # Navigate to page
        await upload_page.navigate()
        
        # Verify file input is present and visible
        file_input_visible = await upload_page.is_element_visible(upload_page.FILE_INPUT)
        assert file_input_visible, "File input should be visible"
        
        # Verify upload button is present and visible
        upload_button_visible = await upload_page.is_element_visible(upload_page.UPLOAD_BUTTON)
        assert upload_button_visible, "Upload button should be visible"
        
        # Verify upload button is enabled
        upload_button_enabled = await upload_page.is_element_enabled(upload_page.UPLOAD_BUTTON)
        assert upload_button_enabled, "Upload button should be enabled"