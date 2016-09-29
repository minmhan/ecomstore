from django.shortcuts import render

# Create your views here.
def register():
    pass

def my_account():
    pass

def order_details():
    pass

def order_info():
    pass

def login(request):
    return render(request, 'accounts/login.html')
