from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from maison_lavaux.sitemaps import ProductSitemap

# Define the sitemap dictionary
sitemaps = {
    "products": ProductSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),
    path("products/", include("products.urls")),
    path("bag/", include("bag.urls")),
    path("checkout/", include("checkout.urls")),
    path("profile/", include("profiles.urls")),
    path("contact/", include("contact.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("", include("pages.urls")),  # Include pages at the root
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler400 = "maison_lavaux.views.custom_400_view"
handler403 = "maison_lavaux.views.custom_403_view"
handler404 = "maison_lavaux.views.custom_404_view"
handler500 = "maison_lavaux.views.custom_500_view"
