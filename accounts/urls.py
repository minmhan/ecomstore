from ecomstore import settings
from django.conf.urls import url
from django.contrib.auth.views import login
from django.contrib.auth.views import logout, password_change, password_change_done
from . import views


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^accounts/my_account/$', views.my_account, name='my_account'),
    url(r'^order_details/(?P<order_id>[-\w]+)/$', views.order_details, name='order_details'),
    url(r'^order_info/$', views.order_info, name='order_info'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, {'template_name': 'accounts/logged_out.html'}, name='logout'),
    url(r'^accounts/password_change/$', password_change, {'template_name': 'accounts/password_change_form.html' }, name='password_change'),
    url(r'^password_change_done/$', password_change_done, {'template_name':'accounts/password_change_done.html'}, name='password_change_done'),
]
