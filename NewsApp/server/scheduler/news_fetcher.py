from apscheduler.schedulers.background import BackgroundScheduler
from services.external_news.external_news_service import ExternalNewsService
from config.config import Config
import atexit
import logging
from utils.exception_handler import handle_exceptions
from datetime import datetime

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

@handle_exceptions()
def start_scheduled_jobs():
    config = Config()
    news_service = ExternalNewsService()

    scheduler.add_job(
        func=news_service.fetch_and_store_all,
        trigger="interval",
        hours=config.FETCH_INTERVAL_HOURS,
        # seconds = 60,
        id="fetch_news_job",
        replace_existing=True
    )

    logger.info(f"Scheduled job 'fetch_news_job' every {config.FETCH_INTERVAL_HOURS} hour(s)")
    scheduler.start()
    atexit.register(scheduler.shutdown)

def format_published_at(published_at):
    try:
        dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return published_at
