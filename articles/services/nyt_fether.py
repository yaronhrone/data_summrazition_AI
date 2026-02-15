
import os
import requests
from django.utils import timezone
from articles.models import Article

NYT_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={}".format(os.environ.get("NYT_API_KEY"))


def fetch_nyt_articles(keyword="technology"):
    """Fetch latest articles from the New York Times API."""
    api_key = os.environ.get("NYT_API_KEY")

    params = {
        "q": keyword,
        "sort": "newest",
        "api-key": api_key,
    }

    response = requests.get(NYT_URL, params=params)
    response.raise_for_status()

    data = response.json()
    docs = data["response"]["docs"]

    for doc in docs:
        external_id = doc["_id"]

        if Article.objects.filter(external_id=external_id).exists():
            continue

        Article.objects.create(
            external_id=external_id,
            title=doc.get("headline", {}).get("main", ""),
            abstract=doc.get("abstract") or "",
            url=doc.get("web_url"),
            author=doc.get("byline", {}).get("original", ""),
            section_name=doc.get("section_name") or "",
            published_at=doc.get("pub_date"),
        )
