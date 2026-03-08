"""Tests for forum views, permissions, and comment flows."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Comment, Post


class ForumViewTests(TestCase):
    """Test forum list, detail, CRUD permissions, comments, and chat page."""

    def setUp(self):
        """Create reusable users, client, and a sample forum post."""
        self.client = Client()

        # Author of the sample post
        self.author = User.objects.create_user(
            username="author1",
            password="TestPass123",
        )

        # Another user for permission checks
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPass123",
        )

        self.post = Post.objects.create(
            title="My First Forum Post",
            content="This is the body of the first forum post.",
            author=self.author,
        )

    def test_forum_list_page_loads(self):
        """Verify the forum list page renders successfully."""
        response = self.client.get(reverse("forum"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_post_detail_page_loads(self):
        """Verify a single post detail page renders successfully."""
        response = self.client.get(
            reverse("post-detail", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_login_required_for_post_create(self):
        """Verify anonymous users are redirected from the create view."""
        response = self.client.get(reverse("post-create"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_create_post(self):
        """Verify an authenticated user can create a new forum post."""
        self.client.login(username="author1", password="TestPass123")

        response = self.client.post(
            reverse("post-create"),
            {
                "title": "New Test Post",
                "content": "This is a newly created test post.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="New Test Post").exists())

    def test_author_can_update_own_post(self):
        """Verify a post author can update their own post."""
        self.client.login(username="author1", password="TestPass123")

        response = self.client.post(
            reverse("post-update", kwargs={"pk": self.post.pk}),
            {
                "title": "Updated Title",
                "content": "Updated forum content.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")
        self.assertEqual(self.post.content, "Updated forum content.")

    def test_non_author_cannot_update_post(self):
        """Verify a non-author is blocked from updating another user's post."""
        self.client.login(username="otheruser", password="TestPass123")

        response = self.client.get(
            reverse("post-update", kwargs={"pk": self.post.pk})
        )
        self.assertIn(response.status_code, [403, 302])

    def test_author_can_delete_own_post(self):
        """Verify a post author can delete their own post."""
        self.client.login(username="author1", password="TestPass123")

        response = self.client.post(
            reverse("post-delete", kwargs={"pk": self.post.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_non_author_cannot_delete_post(self):
        """Verify a non-author is blocked from deleting another user's post."""
        self.client.login(username="otheruser", password="TestPass123")

        response = self.client.post(
            reverse("post-delete", kwargs={"pk": self.post.pk})
        )
        self.assertIn(response.status_code, [403, 302])
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_logged_in_user_can_add_comment(self):
        """Verify an authenticated user can add a comment to a post."""
        self.client.login(username="otheruser", password="TestPass123")

        response = self.client.post(
            reverse("add_comment_to_post", kwargs={"pk": self.post.pk}),
            {
                "content": "This is a test comment.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(
                post=self.post,
                author=self.other_user,
                content="This is a test comment.",
            ).exists()
        )

    def test_add_comment_requires_login(self):
        """Verify anonymous users are redirected from the comment form."""
        response = self.client.get(
            reverse("add_comment_to_post", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_chat_room_page_loads(self):
        """Verify the chat room page renders for a given room name."""
        response = self.client.get(
            reverse("chat_room", kwargs={"room_name": "general"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "general")