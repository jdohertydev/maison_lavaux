from django.views.generic import TemplateView


class RobotsTxtView(TemplateView):
    """View to serve the robots.txt file."""

    template_name = "pages/robots.txt"
