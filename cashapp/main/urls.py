from django.urls import path
from . import views

urlpatterns = [
    path("", views.handle_home_page, name="Home"),
    path("Home", views.handle_home_page, name="Home"),
    ]
