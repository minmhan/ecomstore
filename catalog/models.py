from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class ActiveCategoryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)


# Create your models here.
class Category(models.Model):
    objects = models.Manager()
    active = ActiveCategoryManager()

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for product page URL, created from name.')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField("Meta Keywords", max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', args=({self.slug}))


class ActiveProductManager(models.Manager):
    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)


class FeaturedProductManager(models.Manager):
    def all(self):
        return super(FeaturedProductManager, self).all().filter(is_active=True).filter(is_featured=True)


class Product(models.Model):
    object = models.Manager()
    active = ActiveProductManager()
    featured = FeaturedProductManager()

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique value for product page URL, created from name.')
    brand = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='images/products/main')
    thumbnail = models.ImageField(upload_to='images/products/thumbnails')
    image_caption = models.CharField(max_length=200)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        print('get absolute url')
        # return ('category_product', (), { 'product_slug': self.slug })
        return reverse('product', args=(self.slug,))

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def cross_sells(self):
        pass


class ActiveProductReviewManager(models.Manager):
    def all(self):
        return super(ActiveCategoryManager, self).all().filter(is_approved=True)


class ProductReview(models.Model):
    RATINGS = ((5, 5), (4, 4), (3, 3), (2, 2), (1, 1),)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=5, choices=RATINGS)
    is_approved = models.BooleanField(default=True)
    content = models.TextField()

    objects = models.Manager()
    approved = ActiveCategoryManager()
