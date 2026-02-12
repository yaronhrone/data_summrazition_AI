""" Tests for the article API. """
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from articles import models
from django.utils import timezone
import uuid


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

    # def test_create_article(self):
    #     """Test creating a new article."""
    #     url = reverse('article-list')
    #     data = {
    #         'title': 'New Test Article',
    #         'abstract': 'Abstract for the new test article',
    #         'author': 'New Author',
    #         'published_at': timezone.now(),
    #         'url': 'https://example.com/new',
    #         'section_name': 'New Section'
    #     }
    #     response = self.client.post(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(models.Article.objects.count(), 1)
    #     self.assertEqual(Article.objects.get().title, 'New Test Article')

