from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from catalog.models import Category, Product, ProductReview
from cart import cart
from catalog.forms import ProductAddToCartForm, ProductReviewForm
from django.conf import settings
from stats import stats
from ecomstore.settings import PRODUCTS_PER_ROW
import json


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

    product_reviews = ProductReview.approved.filter(product=p).order_by('-date')
    review_form = ProductReviewForm()

    if request.method == 'POST':
        # add to cart
        post_data = request.POST.copy()
        form = ProductAddToCartForm(request, post_data)
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
    return render(request, template_name,
                  {'p': p, 'categories': categories, 'form': form, 'product_reviews': product_reviews,
                   'review_form': review_form})


@login_required
def add_review(request):
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        slug = request.POST.get('slug')
        product = Product.active.get(slug=slug)
        review.user = request.user
        review.product = product
        review.save()

        template = "catalog/product_review.html"
        html = render_to_string(template, {'review': review})
        response = json.dumps({'success': 'True', 'html': html})
    else:
        html = form.errors.as_url()
        response = json.dumps({ 'success':'False', 'html': html})
    return HttpResponse(response, content_type='application/javascript;charset=utf-8')

