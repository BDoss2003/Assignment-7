import django
from django.conf import settings

from django.utils.timezone import localtime, now, get_current_timezone
from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localtime

from barkyapi.models import Bookmark
from barkyarch.domain.model import DomainBookmark
from barkyarch.services.commands import (
    AddBookmarkCommand,
    ListBookmarksCommand,
    DeleteBookmarkCommand,
    EditBookmarkCommand,
)

from django.utils import timezone
from datetime import datetime

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        # Add your project's apps here
        'barkyapi',
        # Other installed apps
    ],
    
)

# Call django.setup() to initialize Django internals
django.setup()

class TestCommands(TestCase):
    """
    This is to test this program arch
    """
    def setUp(self):
        right_now = datetime.now()


        self.domain_bookmark_1 = DomainBookmark(
            id=1,
            title="Test Bookmark",
            url="http://www.example.com",
            notes="Test notes",
            date_added=right_now,
        )

        self.domain_bookmark_2 = DomainBookmark(
            id=2,
            title="Test Bookmark 2",
            url="http://www.example2.com",
            notes="Test notes 2",
            date_added=right_now,
        )

    #BOOKMARK tests
    def test_command_add(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)

        # run checks

        # one object is inserted
        self.assertEqual(Bookmark.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(Bookmark.objects.get(id=1).url, self.domain_bookmark_1.url)
    
    def test_command_add_duplicate(self):
        add_command = AddBookmarkCommand()
        
        # Add the first bookmark
        add_command.execute(self.domain_bookmark_1)
        self.assertEqual(Bookmark.objects.count(), 1)
        
        # Attempt to add the same bookmark again (duplicate)
        add_command.execute(self.domain_bookmark_1)
        self.assertEqual(Bookmark.objects.count(), 1)  # Should still be 1 (no duplicates)
        
    def test_command_add_invalid_data(self):
        add_command = AddBookmarkCommand()
        
        # Attempt to add a bookmark with missing required data
        invalid_bookmark = DomainBookmark(id=3, title="Invalid Bookmark", url="", notes="")
        with self.assertRaises(Exception):
            add_command.execute(invalid_bookmark)
        self.assertEqual(Bookmark.objects.count(), 0)  # No bookmark should be added

    #LIST tests
    
    def test_command_list_default_order(self):
        list_command = ListBookmarksCommand()
        # Add some bookmarks
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)
        add_command.execute(self.domain_bookmark_2)

        # Retrieve bookmarks and verify default order (by date_added)
        bookmarks = list_command.execute()
        self.assertEqual(len(bookmarks), 2)
        self.assertEqual(bookmarks[0].url, self.domain_bookmark_1.url)
        self.assertEqual(bookmarks[1].url, self.domain_bookmark_2.url)

    def test_command_list_custom_order(self):
        list_command = ListBookmarksCommand(order_by="title")
        # Add some bookmarks
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)
        add_command.execute(self.domain_bookmark_2)

        # Retrieve bookmarks and verify custom order (by title)
        bookmarks = list_command.execute()
        self.assertEqual(len(bookmarks), 2)
        self.assertEqual(bookmarks[0].url, self.domain_bookmark_2.url)
        self.assertEqual(bookmarks[1].url, self.domain_bookmark_1.url)

    def test_command_list_empty_list(self):
        list_command = ListBookmarksCommand()
        # Retrieve bookmarks when the list is empty
        bookmarks = list_command.execute()
        self.assertEqual(len(bookmarks), 0)
    
    # DELETE Tests
    def test_command_delete_existing_bookmark(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)
        
        delete_command = DeleteBookmarkCommand()
        delete_command.execute(self.domain_bookmark_1)
        
        # Verify that the bookmark has been deleted
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_command_delete_nonexistent_bookmark(self):
        delete_command = DeleteBookmarkCommand()
        
        # Attempt to delete a bookmark that does not exist
        with self.assertRaises(Bookmark.DoesNotExist):
            delete_command.execute(self.domain_bookmark_2)
    
    #Edit Tests
    def test_command_edit_existing_bookmark(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)
        
        updated_bookmark = DomainBookmark(
            id=1,
            title="Updated Bookmark",
            url="http://www.updated.com",
            notes="Updated notes",
            date_added=self.domain_bookmark_1.date_added,
        )
        
        edit_command = EditBookmarkCommand()
        edit_command.execute(updated_bookmark)
        
        # Retrieve and verify the updated bookmark
        updated_db_bookmark = Bookmark.objects.get(id=1)
        self.assertEqual(updated_db_bookmark.title, "Updated Bookmark")
        self.assertEqual(updated_db_bookmark.url, "http://www.updated.com")

    def test_command_edit_nonexistent_bookmark(self):
        updated_bookmark = DomainBookmark(
            id=3,
            title="Updated Bookmark",
            url="http://www.updated.com",
            notes="Updated notes",
            date_added=self.domain_bookmark_1.date_added,
        )
        
        edit_command = EditBookmarkCommand()
        
        # Attempt to edit a bookmark that does not exist
        with self.assertRaises(Bookmark.DoesNotExist):
            edit_command.execute(updated_bookmark)
