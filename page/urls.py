from django.urls import path

from . import views

app_name = 'page'
# Страница каталога
urlpatterns = [
    path('delivery/', views.delivery, name='delivery'),
]
