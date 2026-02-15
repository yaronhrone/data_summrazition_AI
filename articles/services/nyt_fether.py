
import os
import requests
import logging
from articles.models import Article

NYT_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=election&api-key={}".format(os.environ.get("NYT_API_KEY"))

logger = logging.getLogger(__name__)
class ExternalAPIError(Exception):
    """Raised when NYT API fails."""
    pass
def fetch_nyt_articles(keyword="technology"):
    """Fetch latest articles from the New York Times API."""

    api_key = os.environ.get("NYT_API_KEY")

    params = {
        "q": keyword,
        "sort": "newest",
        "api-key": api_key,
    }

    try:
        response = requests.get(NYT_URL, params=params)
        response.raise_for_status()

        data = response.json()
    except requests.Timeout:
        logger.exception("NYT API timeout")
        raise ExternalAPIError("NYT API timeout")
    except requests.RequestException:
        logger.exception("NYT API request failed")
        raise ExternalAPIError("NYT API request failed")
    except ValueError:
        logger.exception("Invalid JSON from NYT")
        raise ExternalAPIError("Invalid response from NYT API")

    docs = data.get("response", {}).get("docs", [])

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
