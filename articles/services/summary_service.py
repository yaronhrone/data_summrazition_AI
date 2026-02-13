from articles.models import Summary
from articles.services.ai_service import generate_summary


def get_or_create_summary(article):
    summary = Summary.objects.filter(article_id=article.id).first()

    if summary:
        return summary.summary_text

    summary_text = generate_summary(article)

    Summary.objects.create(
        article_id=article,
        summary_text=summary_text
    )

    return summary_text
