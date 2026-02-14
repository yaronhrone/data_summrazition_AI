from django.apps import AppConfig
import os


class ArticlesConfig(AppConfig):
    """Configuration for the articles app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

    def ready(self):
        """Import scheduler when app is ready."""
        if os.environ.get('RUN_MAIN') == 'true':
            return
        from articles.scheduler import start_scheduler
        start_scheduler()