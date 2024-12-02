from django.urls import path
from django.views.generic import TemplateView
from .views import RobotsTxtView  # Import RobotsTxtView

urlpatterns = [
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "privacy-policy/",
        TemplateView.as_view(template_name="pages/privacy_policy.html"),
        name="privacy_policy",
    ),
    path(
        "robots.txt",
        RobotsTxtView.as_view(content_type="text/plain"),
        name="robots",
    ),
]
