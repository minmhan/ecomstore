from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required
#from accounts.forms import UserProfileForm, RegistrationForm
from checkout.models import Order, OrderItem
from accounts import profile
from accounts.forms import UserProfileForm


# Create your views here.
def register(request, template_name='accounts/register.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        #form = RegistrationForm(postdata)
        form = UserCreationForm(postdata)
        if form.is_valid():
            #form.save()
            user = form.save(commit=False)
            user.email = postdata.get('email','')
            user.save()
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
        #form = RegistrationForm()
    page_title = 'User Registration'
    return render(request, template_name, {'form': form, 'page_title': page_title})


@login_required
def my_account(request):
    page_title = 'My Account'
    name = request.user.username
    return render(request, 'accounts/my_account.html', {'page_title':page_title, 'name':name})


@login_required
def order_details(request, order_id, template_name='registration/order_details.html'):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)
    return render(request, template_name, { 'page_title': page_title, 'order_items':order_items })


@login_required
def order_info(request, template_name='registration/order_info.html'):
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = UserProfileForm(post_data)
        if form.is_valid():
            profile.set(request)
            url = urlresolvers.reverse('my_account')
            return HttpResponseRedirect(url)
        else:
            user_profile = profile.retrieve(request)
            form = UserProfileForm(instance=user_profile)
        page_title = 'Edit Order Information'
        return render(request, template_name, { 'user_profile':user_profile, 'page_title':page_title, 'form': form })


def login(request):
    return render(request, 'accounts/login.html')
