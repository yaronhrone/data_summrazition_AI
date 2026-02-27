from celery import shared_task

from articles.services.nyt_fetcher import fetch_nyt_articles

@shared_task(bind=True, autoretry_for=(Exception,), max_retries=5, retry_backoff=True)
def fetch_nyt_articles_task(self, keyword="technology"):
    fetch_nyt_articles(keyword=keyword)