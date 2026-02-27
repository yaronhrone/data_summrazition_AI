from django.apps import AppConfig
import os
import sys


class ArticlesConfig(AppConfig):
    """Configuration for the articles app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

