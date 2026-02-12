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

