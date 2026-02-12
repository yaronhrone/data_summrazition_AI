from django.test import TestCase
from django.utils import timezone

from articles.models import Article
from articles.serializers import ArticleSerializer

from rest_framework.test import APITestCase
from rest_framework import status

from unittest.mock import patch
import uuid


class ArticleSerializerTests(TestCase):
    """Tests for the ArticleSerializer."""

    def test_article_serializer(self):
        """Test the ArticleSerializer."""
        article = Article.objects.create(
            title="Test Article",
            abstract="Some abstract",
            author="Yaron",
            published_at=timezone.now(),
            url="https://example.com",
            section_name="News",
            external_id=str(uuid.uuid4())
        )

        serializer = ArticleSerializer(article)
        data = serializer.data

        self.assertEqual(data["title"], "Test Article")
        self.assertEqual(data['external_id'], article.external_id)
        self.assertEqual(data["author"], "Yaron")
