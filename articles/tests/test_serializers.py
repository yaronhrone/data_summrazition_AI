from django.test import TestCase
from django.utils import timezone

from articles.models import Article
from articles.serializers import ArticleSerializer, ArticleSummarySerializer

from unittest.mock import patch
import uuid


class ArticleSerializerTests(TestCase):
    """Tests for the ArticleSerializer."""
    time = timezone.now()
    def test_article_serializer(self):
        """Test the ArticleSerializer."""
        article = Article.objects.create(
            title="Test Article",
            abstract="Some abstract",
            author="Yaron",
            published_at=self.time,
            url="https://example.com",
            section_name="News",
            external_id=str(uuid.uuid4())
        )

        serializer = ArticleSerializer(article)
        data = serializer.data

        self.assertEqual(data["title"], "Test Article")
        self.assertEqual(data['external_id'], article.external_id)
        self.assertEqual(data["author"], "Yaron")
        self.assertEqual(data["url"], "https://example.com")
        self.assertEqual(data["section_name"], "News")
        self.assertEqual(data["published_at"], self.time.isoformat().replace('+00:00', 'Z'))
class ArticleSummarySerializerTests(TestCase):
    """Tests for the ArticleSummarySerializer."""

    def test_article_summary_serializer(self):
        """Test the ArticleSummarySerializer."""
        summary = "This is a summary of the article."
        serializer = ArticleSummarySerializer({"summary": summary})
        data = serializer.data

        self.assertEqual(data["summary"], summary)
