from django import template
from cart import cart
from django.contrib.flatpages.models import FlatPage


register = template.Library()


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    return { 'cart_item_count': cart_item_count }


@register.inclusion_tag("tags/footer.html")
def footer_links():
    flatpage_list = FlatPage.objects.all()
    return { 'flatpage_list': flatpage_list }
