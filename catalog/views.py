from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from catalog.models import Category, Product
from cart import cart
from catalog.forms import ProductAddToCartForm
from django.conf import settings
from stats import stats
from ecomstore.settings import PRODUCTS_PER_ROW


def index(request, template_name="catalog/index.html"):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    search_recs = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:PRODUCTS_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)
    return render(request, template_name, {'page_title': page_title, 'search_recs': search_recs, 'featured': featured,
                                           'recently_viewed': recently_viewed, 'view_recs': view_recs})


def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    # return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    return render(request, template_name,
                  {'c': c, 'products': products, 'page_title': page_title, 'meta_keywords': meta_keywords,
                   'meta_description': meta_description})


def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)
    stats.log_product_view(request, p)  # TODO: check place
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    if request.method == 'POST':
        # add to cart
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        if form.is_valid():
            print('valid')
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    else:
        form = ProductAddToCartForm(request=request, label_suffix=":")

    form.fields['product_slug'].widget.attrs['value'] = product_slug
    request.session.set_test_cookie()
    return render(request, template_name, {'p': p, 'categories': categories, 'form': form})
