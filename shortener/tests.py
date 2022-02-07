from django.test import TestCase

from .models import ShortUrls


class ShortUrlsTestCase(TestCase):
    """Тесты для приложения "Shortener"."""

    def test_valid_origin_url(self):
        """Проверка на валидность введенного origin_url."""
        pass

    def test_subpart_limit(self):
        """Проверка превышения лимита длины введенного subpart."""
        pass

    def test_subpart_exists(self):
        """Проверка существования введенного subpart."""
        pass

    def test_create_short_url(self):
        """Проверка создания сокращенного URL."""
        pass

    def test_redirect_url(self):
        """Проверка редиректа с сокращенного URL."""
        pass

    def test_api_origin_url(self):
        """Проверка API для получения полного URL по сокращенному."""
        pass
