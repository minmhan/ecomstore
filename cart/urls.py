from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cart/$', views.show_cart, name='show_cart'),
]