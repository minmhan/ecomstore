from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render


def file_not_found_404(request):
    print('404 page')
    page_title = 'Page Not Found'
    return render(request, '404.html', {'page_title': page_title})