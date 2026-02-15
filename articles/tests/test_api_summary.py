from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache

import uuid

from rest_framework import status
from rest_framework.test import APITestCase

from articles import models
from articles.services.summary_service import get_or_create_summary
from articles.tests.test_api_article import create_article




class summaryAPITests(APITestCase):
    """Tests for the article summary API."""
    def setUp(self):
        cache.clear()

    @patch('articles.services.summary_service.generate_summary')
    def test_get_article_summary(self, mock_generate_summary):
        """Test retrieving a summary for an article."""
        mock_generate_summary.return_value = "AI summary"
        article = create_article()

        url = reverse("article-summary", args=[article.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary'], mock_generate_summary.return_value)
        self.assertEqual(models.Summary.objects.count(), 1)


    @patch('articles.services.summary_service.generate_summary')
    def test_get_article_summary_uses_existing(self, mock_generate_summary):
        """Test retrieving a summary for an article that already has a summary."""


        mock_generate_summary.return_value = "AI summary"
        article = create_article()
        models.Summary.objects.create(article=article, summary_text="Existing summary")

        url = reverse("article-summary", args=[article.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary'], "Existing summary")
        mock_generate_summary.assert_not_called()

    @patch('articles.services.summary_service.generate_summary')
    def test_summary_uses_cache_on_second_request(self, mock_generate_summary):
        """Test that the summary is cached after the first request."""
        mock_generate_summary.return_value = "AI summary"
        article = create_article()

        url = reverse("article-summary", args=[article.id])
        self.client.get(url)
        self.assertEqual(mock_generate_summary.call_count, 1)

        self.client.get(url)
        self.assertEqual(mock_generate_summary.call_count, 1)


