from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Bookmark, Snippet
from .views import BookmarkViewSet, SnippetViewSet

import datetime

# Create your tests here.
# test plan


class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )
        
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"][0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }
        response = self.client.put(
            reverse("barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")


# 6. create a snippet
    def test_create_snippet(self):
        """
        Ensure we can create a new snippet object.
        """
        data = {
            "title": "Test Snippet",
            "code": "print('Hello, world!')",
            "linenos": False,
            "language": "python",
            "style": "friendly",
            "owner": self.user.pk,  # Set the owner to an existing user's primary key
        }
        response = self.client.post(reverse("barkyapi:snippet-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# 7. retrieve a snippet
    def test_retrieve_snippet(self):
        """
        Ensure we can retrieve a snippet object.
        """
        snippet = Snippet.objects.create(title="Test Snippet", code="print('Hello, world!')", language="python", owner=self.user)
        response = self.client.get(reverse("barkyapi:snippet-detail", kwargs={"pk": snippet.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# 8. delete a snippet
    def test_delete_snippet(self):
        """
        Ensure we can delete a snippet object.
        """
        snippet = Snippet.objects.create(title="Test Snippet", code="print('Hello, world!')", language="python", owner=self.user)
        response = self.client.delete(reverse("barkyapi:snippet-detail", kwargs={"pk": snippet.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)


# 9. list snippets

# 10. update a snippet
    def test_update_snippet(self):
        """
        Ensure we can update a snippet object.
        """
        snippet = Snippet(title="Test Snippet", code="print('Hello, world!')", language="python", owner=self.user)
        updated_data = {
            "title": "Updated Snippet",
            "code": "print('Updated!')",
            "language": "python",
            "owner": self.user.pk,  # Ensure the owner remains the same
        }
        response = self.client.put(reverse("barkyapi:snippet-detail", kwargs={"pk": snippet.pk}), updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Snippet.objects.get(pk=snippet.pk).title, "Updated Snippet")

# 11. Create a User
    def test_create_user(self):
        url = reverse('barkyapi:user-list')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # 12. Retrieve a User
    def test_retrieve_user(self):
        url = reverse('barkyapi:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    # 13. Delete a User
    def test_delete_user(self):
        url = reverse('barkyapi:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    # 14. List Users
    def test_list_users(self):
        # Create additional users for testing
        User.objects.create_user(username='testuser2', password='testpassword2')
        User.objects.create_user(username='testuser3', password='testpassword3')

        url = reverse('barkyapi:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Assuming there are three users including the test user

    # 15. Update a User
    def test_update_user(self):
        url = reverse('barkyapi:user-detail', kwargs={'pk': self.user.pk})
        updated_data = {'username': 'updateduser', 'password': 'updatedpassword'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.pk).username, 'updateduser')
 # 16. Highlight a Snippet
    def test_highlight_snippet(self):
        snippet = Snippet.objects.create(
            title="Test Snippet",
            code="print('Hello, world!')",
            language="python",
            owner=self.user
        )
        url = reverse('snippet-highlight', kwargs={'pk': snippet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('<div class="highlight">', response.data)  # Check for highlighted HTML content

    # 17. List Bookmarks by User
    def test_list_bookmarks_by_user(self):
        Bookmark.objects.create(
            title="Bookmark 1",
            url="https://dosstroop.com/1",
            notes="Cool Site",
            owner=self.user
        )
        Bookmark.objects.create(
            title="Bookmark 2",
            url="https://wtamu.edu/2",
            notes="What's up!",
            owner=self.user
        )
        url = reverse('bookmark-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming two bookmarks are created by the user

    # 18. List Snippets by User
    def test_list_snippets_by_user(self):
        Snippet.objects.create(
            title="Snippet 1",
            code="print('Snippet 1')",
            language="python",
            owner=self.user
        )
        Snippet.objects.create(
            title="Snippet 2",
            code="print('Snippet 2')",
            language="python",
            owner=self.user
        )
        url = reverse('snippet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming two snippets are created by the user

    # 20. List Bookmarks by Date
    def test_list_bookmarks_by_date(self):
        # Create bookmarks with different dates
        Bookmark.objects.create(
            title="Bookmark 1",
            url="https://www.wtamu.edu/1",
            notes="Note 1",
            owner=self.user,
            date_added=datetime(2024, 4, 15)  # Specific date
        )
        Bookmark.objects.create(
            title="Bookmark 2",
            url="https://dosstroop.com/2",
            notes="Note 2",
            owner=self.user,
            date_added=datetime(2024, 4, 16)  # Another specific date
        )
        url = reverse('bookmark-list') + '?ordering=date_added'  # Ordering by date_added
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming two bookmarks are created and ordered by date

    # 21. List Snippets by Date
    def test_list_snippets_by_date(self):
        # Create snippets with different dates
        Snippet.objects.create(
            title="Snippet 1",
            code="print('Snippet 1')",
            language="python",
            owner=self.user,
            created=datetime(2024, 4, 15)  # Specific date
        )
        Snippet.objects.create(
            title="Snippet 2",
            code="print('Snippet 2')",
            language="python",
            owner=self.user,
            created=datetime(2024, 4, 16)  # Another specific date
        )
        url = reverse('snippet-list') + '?ordering=created'  # Ordering by created date
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming two snippets are created and ordered by date

    # 23. List Bookmarks by Title
    def test_list_bookmarks_by_title(self):
        Bookmark.objects.create(
            title="AAA Bookmark",
            url="https://AAA.org/1",
            notes="Note 1",
            owner=self.user
        )
        Bookmark.objects.create(
            title="BBB Bookmark",
            url="https://BBB.org/2",
            notes="Note 2",
            owner=self.user
        )
        url = reverse('bookmark-list') + '?search=AAA'  # Searching by title
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Assuming one bookmark with title containing "AAA"

    # 24. List Snippets by Title
    def test_list_snippets_by_title(self):
        Snippet.objects.create(
            title="AAA Snippet",
            code="print('AAA Snippet')",
            language="python",
            owner=self.user
        )
        Snippet.objects.create(
            title="BBB Snippet",
            code="print('BBB Snippet')",
            language="python",
            owner=self.user
        )
        url = reverse('snippet-list') + '?search=AAA'  # Searching by title
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Assuming one snippet with title containing "AAA"

    # 26. List Bookmarks by URL
    def test_list_bookmarks_by_url(self):
        Bookmark.objects.create(
            title="Bookmark 1",
            url="https://dosstroop.com/1",
            notes="Note 1",
            owner=self.user
        )
        Bookmark.objects.create(
            title="Bookmark 2",
            url="https://dosstroop.com/2",
            notes="Note 2",
            owner=self.user
        )
        url = reverse('bookmark-list') + '?search=dosstroop.com/1'  # Searching by URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Assuming one bookmark with URL containing "dosstroop.com/1"

    # 27. List Snippets by URL
    def test_list_snippets_by_url(self):
        Snippet.objects.create(
            title="Snippet 1",
            code="print('Snippet 1')",
            language="python",
            owner=self.user
        )
        Snippet.objects.create(
            title="Snippet 2",
            code="print('Snippet 2')",
            language="python",
            owner=self.user
        )
        url = reverse('snippet-list') + '?search=python'  # Searching by language in URL (for demonstration)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming all snippets are related to Python language
