from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from catalog.models import Category, Product
from cart import cart
from catalog.forms import ProductAddToCartForm
from django.conf import settings
from django.template import RequestContext


# Create your views here.
def index(request, template_name="catalog/index.html"):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    #return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    #return render(request, 'catalog/index.html')
    return render(request, template_name)


def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    #return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    return render(request, template_name, {'c': c, 'products': products})


def show_product(request, product_slug, template_name="catalog/product.html"):
    print(settings.MEDIA_ROOT)
    print(settings.MEDIA_URL)
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    if request.method == 'POST':
        print('POST')
        # add to cart
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        print(postdata)
        if form.is_valid():
            print('valid')
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            print(url)
            return HttpResponseRedirect(url)
    else:
        form = ProductAddToCartForm(request=request, label_suffix=":")

    form.fields['product_slug'].widget.attrs['value'] = product_slug
    request.session.set_test_cookie()
    return render(request, template_name, {'p': p, 'categories': categories, 'form': form})
