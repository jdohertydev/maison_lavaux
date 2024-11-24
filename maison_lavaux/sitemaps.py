from django.contrib.sitemaps import Sitemap
from products.models import Product

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated if hasattr(obj, 'updated') else None
