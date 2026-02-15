from django.urls import path

from . import views


# Главная страница
urlpatterns = [
    path("", views.index, name="index"),
]