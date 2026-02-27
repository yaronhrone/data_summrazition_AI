from django.core.management.base import BaseCommand
from articles.services.nyt_fetcher import fetch_nyt_articles

class Command(BaseCommand):
    """Fetch NYT articles and store them in the database."""
    help = "Fetch NYT articles and store them in the database."


    def add_arguments(self, parser):
        parser.add_argument("--keyword", type=str, default="technology")

    def handle(self, *args, **options):
        keyword = options["keyword"]
        fetch_nyt_articles(keyword= keyword)
        self.stdout.write(self.style.SUCCESS(f"Successfully fetched NYT articles for keyword: {keyword}"))