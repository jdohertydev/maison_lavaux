from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.home, name="home"
    ),  # Change this line to point to the home view
]
