from django.views.generic import TemplateView

class RobotsTxtView(TemplateView):
    template_name = "pages/robots.txt"
