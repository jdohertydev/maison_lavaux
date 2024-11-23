from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product
from django.apps import apps

# Sitemap for static views
class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # List static views here
        return ['home', 'about', 'contact', 'profile']

    def location(self, item):
        return reverse(item)

# Sitemap for products
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

# Optional: Add more sitemaps for other apps (e.g., profiles, blog)
class ProfileSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        UserProfile = apps.get_model('profiles', 'UserProfile')
        return UserProfile.objects.all()

    def location(self, obj):
        return reverse('profile', args=[obj.user.username])

# Combine all sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'profiles': ProfileSitemap,  # Add other sitemaps here
}
