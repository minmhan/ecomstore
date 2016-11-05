from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from cart import cart
from checkout import checkout


# Create your views here.
def show_cart(request):
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)

    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)

    return render(request, "cart/cart.html", {'page_title': page_title, 'cart_items': cart_items, 'cart_subtotal':cart_subtotal})