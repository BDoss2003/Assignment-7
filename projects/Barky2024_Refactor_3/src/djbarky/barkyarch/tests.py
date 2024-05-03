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


class TestCommands(TestCase):
    def setUp(self):
        right_now = localtime().date()

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
        with self.assertRaises(Exception):  # Adjust the expected exception based on error handling
            add_command.execute(invalid_bookmark)
        self.assertEqual(Bookmark.objects.count(), 0)  # No bookmark should be added
