from django.urls import path

from . import views

app_name = 'shop'
# Страница каталога
urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path('search/', views.search_product, name='search'),
    path('<slug:category_slug>/', views.catalogue, name='catalogue_by_category'),
    # path('search/', views.catalogue, name='search'),

    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
