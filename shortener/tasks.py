import datetime

from celery import Celery
from django.core.cache import cache

from .constants import CLEAR_OLD_URL_HOURS
from .constants import DAYS_TO_CLEAR_URLS

app = Celery(
    'shortener', backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0'
)

app.autodiscover_tasks()

# todo Не очень было понятно, что поздразумевается под
#  "Очистка старых правил по расписанию"
#  (какие конкретно записи удалять, как часто, каким способом).
#  Сделал очистку через периодическую задачу Celery с установленными
#  параметрами DAYS_TO_CLEAR_URLS и CLEAR_OLD_URL_HOURS.


def start_tasks():
    """Запуск периодических задач Celery"""

    from django_celery_beat.models import IntervalSchedule
    from django_celery_beat.models import PeriodicTask

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=CLEAR_OLD_URL_HOURS, period=IntervalSchedule.HOURS,
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='clear_old_urls_and_cache',
        task='shortener.tasks.clear_old_urls_and_cache',
    )


@app.task
def clear_old_urls_and_cache():
    """
    Очистка старых (старее DAYS_TO_CLEAR_URLS от текущей даты)
    правил редириктов и кеша Redis.
    """
    from .models import ShortUrls

    _now = datetime.datetime.now()
    old_urls = ShortUrls.objects.filter(
        created__lte=_now - datetime.timedelta(days=DAYS_TO_CLEAR_URLS))
    shorts_urls = list(old_urls.values_list('short_url', flat=True))

    old_urls.delete()

    cache.delete_many(shorts_urls)
