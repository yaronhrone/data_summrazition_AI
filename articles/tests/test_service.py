
from django.core.cache import cache
from django.test import TestCase

from unittest.mock import patch

from articles.models import Article, Summary
from articles.services.summary_service import get_or_create_summary
from articles.services.nyt_fetcher import fetch_nyt_articles


def create_article():
    return Article.objects.create(
        external_id="nyt_123",
        title="Test Article",
        abstract="This is a test article.",
        author="Test Author",
        published_at="2023-01-01T00:00:00Z",
        url="https://example.com/test-article",
        section_name="Test Section"
    )
class FetchNYTArticlesTests(TestCase):
    """Tests for fetching articles from the New York Times API."""

    @patch('articles.services.nyt_fether.requests.get')
    def test_fetch_nyt_articles(self, mock_fetch):
        """Test fetching articles from the New York Times API."""
        mock_fetch.return_value.status_code = 200
        mock_fetch.return_value.json.return_value = {
            "response": {
                "docs": [
                    {
                        "_id": "nyt_123",
                        "headline": {"main": "Test Article"},
                        "abstract": "This is a test article.",
                        "byline": {"original": "Test Author"},
                        "pub_date": "2023-01-01T00:00:00Z",
                        "web_url": "https://example.com/test-article",
                        "section_name": "Test Section"
                    }
                ]
            }
        }

        fetch_nyt_articles()

        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertEqual(article.external_id, "nyt_123")
        self.assertEqual(article.title, "Test Article")

    @patch('articles.services.nyt_fether.requests.get')
    def test_fetch_does_not_create_duplicate_articles(self, mock_get):
        """Test that fetching articles does not create duplicates."""
        create_article()


        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "response": {
                "docs": [
                    {
                        "_id": "nyt_123",
                        "headline": {"main": "Test Article"},
                        "abstract": "This is a test article.",
                        "byline": {"original": "Test Author"},
                        "pub_date": "2023-01-01T00:00:00Z",
                        "web_url": "https://example.com/test-article",
                        "section_name": "Test Section"
                    }
                ]
            }
        }
        fetch_nyt_articles()

        self.assertEqual(Article.objects.count(), 1)

class SummaryServiceTests(TestCase):
    """Tests for the summary service."""
    @patch('articles.services.summary_service.generate_summary')
    def test_generate_summary_if_not_exists(self, mock_generate_summary):
        """Test that a summary is generated if it does not exist."""
        article = create_article()

        mock_generate_summary.return_value = "This is a summary."
        result = get_or_create_summary(article)
        self.assertEqual(result, "This is a summary.")
        self.assertEqual(mock_generate_summary.call_count, 1)
        mock_generate_summary.assert_called_once()

    @patch('articles.services.summary_service.generate_summary')
    def test_returns_existing_summary_from_db(self, mock_generate_summary):
        """Test that the existing summary is returned from the database."""
        article = create_article()
        Summary.objects.create(article = article ,summary_text="Existing summary")

        result = get_or_create_summary(article)
        self.assertEqual(result, "Existing summary")
        mock_generate_summary.assert_not_called()

    @patch('articles.services.summary_service.generate_summary')
    def test_summary_is_cached(self, mock_generate_summary):
        """Test that the summary is cached after the first request."""
        article = create_article()
        cache_key = f"article_summary_{article.id}"
        cache.set(cache_key, "Cached summary", timeout=300)

        result = get_or_create_summary(article)
        self.assertEqual(result, "Cached summary")
        mock_generate_summary.assert_not_called()

    @patch('articles.services.summary_service.generate_summary')
    def test_ai_failure_does_not_create_summary(self, mock_generate_summary):
        """Test that if the AI service fails, a summary is not created."""
        article = create_article()
        mock_generate_summary.side_effect = Exception("AI failure")
        with self.assertRaises(Exception):
            get_or_create_summary(article)



        self.assertEqual(Summary.objects.count(), 0)