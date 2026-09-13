from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("", views.home, name="home"),
    path("contact/", views.contact_submit, name="contact_submit"),
]
