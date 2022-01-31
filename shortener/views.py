import uuid

from django.contrib import messages
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import F
from django.db.models import Value
from django.db.models.fields import TextField
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.views.generic import ListView

from rest_framework import generics
from rest_framework import serializers
from shortener.logger import log_on_exception
from shortener.logger import logger

from .constants import PADDING_LIMIT
from .constants import SUBPART_LIMIT
from .models import ShortUrls


class MainPage(ListView):
    """Вью для основной страницы сайта"""

    template_name = 'main.html'

    paginate_by = PADDING_LIMIT

    @log_on_exception
    def get_queryset(self):
        user_urls = []
        session_id = self.request.session.session_key

        if session_id:
            user_urls = ShortUrls.objects.annotate(
                host_short_url=Concat(
                    Value(self.request.META['HTTP_HOST']),
                    F('short_url'), output_field=TextField())
            ).filter(
                session_id=session_id
            )
        return user_urls


@log_on_exception
def generate_url(request):
    """
    Генерация короткого URL для пользователя по его сесси и subpart
    (если он передан).
    :param request: Запрос
    :param request: HttpRequest
    """

    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key

    origin_url = request.POST["origin_url"]

    try:
        URLValidator()(origin_url)
    except ValidationError:
        messages.info(request, 'Введен некорректный URL!')
        logger.info(f'Введен некорректный {origin_url}')
        return redirect('/')

    subpart = request.POST["subpart"]

    if len(subpart) > SUBPART_LIMIT:
        messages.info(
            request,
            f'Ваш вариант сокращения URL прешивает ограничие в '
            f'{SUBPART_LIMIT} символов!'
        )
        logger.info('Превышено ограничие символов в сокращении URL')
        return redirect('/')

    if subpart:
        short_url = '/' + subpart
    else:
        short_url = '/' + str(uuid.uuid4())[:SUBPART_LIMIT]

    subpart_exists = (
        cache.get(short_url) or
        ShortUrls.objects.filter(short_url=short_url).exists()
    )
    if subpart_exists:
        messages.info(request, 'Данный Сокращенный URL уже существует!')
    else:
        ShortUrls.objects.get_or_create(
            origin_url=origin_url,
            short_url=short_url,
            session_id=session_id
        )

        cache.set(short_url, origin_url)

    return redirect('/')


@log_on_exception
def short_url_redirect(request, subpart):
    """
    Производит редерикт пользователя на оригинальный URL, с попыткой найти
    сокращенный URL в кеше.

    :param request: Запрос
    :param request: HttpRequest
    :param subpart: Сокращенная часть для нового URL
    :type subpart: str

    """

    session_id = request.session.session_key
    short_url = '/' + subpart

    cached_origin_url = cache.get(short_url)

    if not cached_origin_url:
        origin_url = ShortUrls.objects.filter(
            session_id=session_id,
            short_url=short_url
        ).values_list('origin_url', flat=True).first()
    else:
        origin_url = cached_origin_url
    if origin_url:
        return redirect(origin_url)
    else:
        return redirect('/')


class ApiOriginUrlSerializer(serializers.ModelSerializer):
    """Сериалайзер для апи ApiOriginUrl"""
    class Meta:
        model = ShortUrls
        fields = ['origin_url']


class ApiOriginUrl(generics.ListAPIView):
    """
    DRF api возвращает оригинальный URL по переданному subpart.

    Пример запроса - http://127.0.0.1:8000/get-origin-url/8ae9031/
    """

    serializer_class = ApiOriginUrlSerializer

    def get_queryset(self):
        short_url = '/' + self.kwargs['subpart']
        return ShortUrls.objects.filter(short_url=short_url)
