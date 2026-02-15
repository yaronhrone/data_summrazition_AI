from django.core.management.base import BaseCommand
from articles.services.nyt_fether import fetch_nyt_articles

class Command(BaseCommand):
    """Fetch NYT articles and store them in the database."""
    help = "Fetch NYT articles and store them in the database."

    def handle(self, *args, **options):
        """Handle the command."""
        fetch_nyt_articles()
        self.stdout.write(self.style.SUCCESS("Successfully fetched NYT articles."))

    def add_arguments(self, parser):
        parser.add_argument("--keyword", type=str, default="technology")

    def handle(self, *args, **options):
        keyword = options["keyword"]
        fetch_nyt_articles(keyword)
        self.stdout.write(self.style.SUCCESS(f"Successfully fetched NYT articles for keyword: {keyword}"))