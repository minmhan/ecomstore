from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request, template_name='accounts/register.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            un = postdata.get('username', '')
            pwd = postdata.get('password1', '')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pwd)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    page_title = 'User Registration'
    return render(request, template_name, {'form': form, 'page_title': page_title})


@login_required
def my_account(request):
    page_title = 'My Account'
    name = request.user.username
    return render(request, 'accounts/my_account.html', {'page_title':page_title, 'name':name})


def order_details():
    pass


def order_info(request):
    return render(request)


def login(request):
    return render(request, 'accounts/login.html')
