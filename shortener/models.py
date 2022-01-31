from django.db import models
from django.contrib.sessions.models import Session


class ShortUrls(models.Model):
    """Модель для хранения сокращенных URL"""

    origin_url = models.TextField('URL')

    short_url = models.TextField('Короткий URL')

    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, verbose_name='Сессия пользователя')

    created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Создан',
    )

    class Meta:
        ordering = ['-id']
