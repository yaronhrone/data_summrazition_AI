""" Tests for the article API. """

from unittest.mock import patch
import uuid

from django.test import TestCase
from django.utils import timezone

from articles.serializers import ArticleSerializer
from articles import models

class ArcticleModelTests(TestCase):
    """Tests Models."""
    time =  timezone.now()
    def test_create_article(self):
        """Test creating a new article."""
        article = models.Article.objects.create(
            title="Test Article",
            abstract="Some abstract",
            author="Yaron",
            published_at=self.time,
            url="https://example.com",
            section_name="News",
            external_id="abc123"
        )

        self.assertEqual(models.Article.objects.count(), 1)
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.abstract, "Some abstract")
        self.assertEqual(article.author, "Yaron")
        self.assertEqual(article.published_at, self.time)
        self.assertEqual(article.url, "https://example.com")
        self.assertEqual(article.section_name, "News")
        self.assertEqual(article.external_id, "abc123")

    def test_serializer_validation(self):
        payload = {
            "external_id": str(uuid.uuid4()),
            "title": "",
            "abstract": "Test",
            "author": "Yaron",
            "published_at": self.time,
            "url": "https://example.com",
            "section_name": "News",
        }

        serializer = ArticleSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
