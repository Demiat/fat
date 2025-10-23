from celery import Celery

from fat.core.settings import settings

celery_app = Celery(main="fat", broker=settings.redis_settings.redis_url,
                    backend=settings.redis_settings.redis_url)

celery_app.autodiscover_tasks(packages=["fat.apps"])
