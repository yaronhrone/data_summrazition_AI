
from django.test import TestCase

from unittest.mock import patch

from articles.models import Article, Summary
from articles.services.nyt_fether import fetch_nyt_articles



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
        Article.objects.create(
            external_id="nyt_123",
            title="Test Article",
            abstract="This is a test article.",
            author="Test Author",
            published_at="2023-01-01T00:00:00Z",
            url="https://example.com/test-article",
            section_name="Test Section"
        )


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