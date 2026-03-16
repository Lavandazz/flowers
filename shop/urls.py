from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'shop'
# Страница каталога
urlpatterns = [
    path('', views.CatalogueListView.as_view(), name='catalogue'),
    path('search/', views.ProductSearchView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogueListView.as_view(), name='catalogue_by_category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
