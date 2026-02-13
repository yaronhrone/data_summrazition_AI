from django.core.cache import cache
from articles.models import Summary
from articles.services.ai_service import generate_summary


def get_or_create_summary(article):
    cache_key = f"article_summary_{article.id}"

    cache_summary = cache.get(cache_key)

    if cache_summary:
        return cache_summary


    existing_summary = Summary.objects.filter(article=article).first()

    if existing_summary:
        cache.set(cache_key, existing_summary.summary_text ,timeout=21600)
        return existing_summary.summary_text

    summary_text = generate_summary(article)

    Summary.objects.create(
        article=article,
        summary_text=summary_text
    )
    cache.set(cache_key, summary_text, timeout=21600)

    return summary_text
