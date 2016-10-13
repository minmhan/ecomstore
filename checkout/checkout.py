from django.core import urlresolvers


def get_checkout_url(request):
    return urlresolvers.reverse('show_checkout')

def process(request):
    pass

