""" Tests for the article API. """

from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache

import uuid

from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from articles import models


def create_article(**params):
    defaults = {
        "external_id": str(uuid.uuid4()),
        "title": "Test Article",
        "abstract": "Sample abstract",
        "url": "https://example.com",
        "author": "Author",
        "section_name": "Tech",
        "published_at": timezone.now(),
    }
    defaults.update(params)
    return models.Article.objects.create(**defaults)


class ArticleAPITests(APITestCase):
    """Tests for the article API."""

    def test_get_articles(self):
        """Test retrieving a list of articles."""
        create_article()

        create_article(title="Test Article 2", abstract="Some abstract 2", author="Yaron 2", url="https://example2.com", section_name="Sports", published_at=timezone.now(), external_id=str(uuid.uuid4()))

        url = reverse('article-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Article')
        self.assertEqual(response.data[1]['title'], 'Test Article 2')

    def test_create_article(self):
        """Test creating a new article."""
        url = reverse('article-list')
        payload = {
            'title': 'New Test Article',
            'abstract': 'Abstract for the new test article',
            'author': 'New Author',
            'published_at': timezone.now(),
            'url': 'https://example.com/new',
            'section_name': 'New Section'
        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Article.objects.count(), 1)
        self.assertEqual(models.Article.objects.get().title, 'New Test Article')


    def test_create_article_invalid(self):
        """Test creating a new article with invalid payload."""
        url = reverse('article-list')
        payload = {
            'title': '',
            'abstract': 'Abstract for the new test article',

        }
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ArticleDateilAPITests(APITestCase):
    """Tests for the article withe ID API."""

    def test_get_article_detail(self):
        """Test """
        article = create_article()

        url = reverse("article-detail", args=[article.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'],article.id)
        self.assertEqual(response.data['title'], "Test Article")

    def test_get_article_not_found(self):
        url = reverse("article-detail", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article(self):
        """Test updating an article."""
        article = create_article()

        url = reverse("article-detail", args=[article.id])
        payload = {
             "external_id": article.external_id,
             "title": "Updated Title",
             "abstract": "Updated abstract",
             "url": "https://example.com",
             "author": "Yaron",
             "section_name": "News",
             "published_at": timezone.now(),
        }
        response = self.client.put(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        article.refresh_from_db()
        self.assertEqual(article.title, "Updated Title")

    def test_delete_article(self):
        """Test deleting an article."""
        article = create_article()

        url = reverse("article-detail", args = [article.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Article.objects.filter(id=article.id).exists())


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


