from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path

from rest_framework import routers
from shortener import views

admin.autodiscover()

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.MainPage.as_view(), name='home'),
    url(r'generate_url/', views.generate_url, name='generate_url'),
    re_path(
        r'(?P<subpart>\w+)$', views.short_url_redirect,
        name='short_url_redirect'),
    path('', include('rest_framework.urls')),
    re_path('get-origin-url/(?P<subpart>.+)/$', views.ApiOriginUrl.as_view()),
]
