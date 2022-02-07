from django.contrib.sessions.models import Session
from django.db import models

from coin32_test.logger import log_info


class ShortUrls(models.Model):
    """Модель для хранения сокращенных URL"""

    origin_url = models.TextField('URL')

    short_url = models.CharField('Короткий URL', unique=True, max_length=100)

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

    def create_log_message(self):
        """Создание типового сообщения для лога"""
        msg = (
            f'Session Key: {self.session_id} | '
            f'Short URL: {self.short_url} | '
            f'Origin URL: {self.origin_url}'
        )
        return msg
