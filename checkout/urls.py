from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^checkout/$', views.show_checkout, {'template_name': 'checkout/checkout.html'}, name='show_checkout'),
    url(r'^receipt/$', views.receipt, {'template_name':'checkout/receipt.html'}, name='checkout_receipt'),
]