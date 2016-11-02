from django.core import urlresolvers
from cart import cart
from checkout.models import Order, OrderItem
from checkout.forms import CheckoutForm


def get_checkout_url(request):
    return urlresolvers.reverse('show_checkout')

def process(request):
    pass

# TODO
def create_order(request, transaction_id):
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    cart.empty_cart(request)
    # save profile info for future orders
    if request.user.is_authenticated():
        from accounts import profile
        profile.set(request)

    # return the new order object
    return order

