from apscheduler.schedulers.background import BackgroundScheduler
from articles.services.nyt_fether import fetch_nyt_articles




class ExternalAPIError(Exception):
    """Raised when NYT API fails."""
    pass
def start_scheduler():
    """Start the APScheduler."""
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(fetch_nyt_articles, 'interval', hours=6)
        scheduler.start()
    except ExternalAPIError:
        pass