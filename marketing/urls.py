from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from . import views
from marketing.sitemap import SITEMAPS

urlpatterns = [
    url(r'^robots\.txt$', views.robots, name='robots'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS}),
]