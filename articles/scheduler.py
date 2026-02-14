from apscheduler.schedulers.background import BackgroundScheduler
from articles.services.nyt_fether import fetch_nyt_articles

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_nyt_articles, 'interval', seconds=30)
    scheduler.start()