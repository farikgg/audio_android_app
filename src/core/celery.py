from celery import Celery

from src.app.config import get_settings

settings = get_settings()
celery_app = Celery(
    main="src",
    broker=settings.redis_settings.redis_url,
    backend=settings.redis_settings.redis_url,
    config_source=settings,
)

celery_app.autodiscover_tasks(['src.worker'])
