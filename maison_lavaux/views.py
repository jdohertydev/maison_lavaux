from django.shortcuts import render


def custom_400_view(request, exception):
    """
    Handle 400 Bad Request errors.

    This view renders a custom 400 error page when a bad request is received.
    """
    return render(request, "400.html", status=400)


def custom_403_view(request, exception):
    """
    Handle 403 Forbidden errors.

    This view renders a custom 403 error page when access is forbidden.
    """
    return render(request, "403.html", status=403)


def custom_404_view(request, exception):
    """
    Handle 404 Not Found errors.

    This view renders a custom 404 error page when a page is not found.
    """
    return render(request, "404.html", status=404)


def custom_500_view(request):
    """
    Handle 500 Internal Server errors.

    This view renders a custom 500 error
    page when an internal server error occurs.
    """
    return render(request, "500.html", status=500)
