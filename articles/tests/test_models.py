""" Tests for the article API. """

from unittest.mock import patch
import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

from articles import models

class ArcticleModelTests(TestCase):
    """Tests Models."""

    def test_create_article(self):
        """Test creating a new article."""
        article = models.Article.objects.create(
            title="Test Article",
            abstract="Some abstract",
            author="Yaron",
            published_at=timezone.now(),
            url="https://example.com",
            section_name="News",
            external_id="abc123"
        )

        self.assertEqual(models.Article.objects.count(), 1)
        self.assertEqual(str(article), "Test Article")

# class SummaryApiTests(APITestCase):

#     @patch("articles.services.ai_service.generate_summary")
#     def test_generate_summary_for_article(self, mock_generate):
#         """Test generating summary for article."""
#         mock_generate.return_value = "AI generated summary"

#         article = models.Article.objects.create(
#             external_id=str(uuid.uuid4()),
#             title="Test Title",
#             abstract="Test abstract",
#             url="https://example.com",
#             author="John Doe",
#             section_name="Tech",
#             published_at=timezone.now(),
#         )

#         url = reverse("article-summary", args=[article.id])
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["summary"], "AI generated summary")