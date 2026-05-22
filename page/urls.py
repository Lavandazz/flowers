from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'page'

urlpatterns = [
    path('delivery/', cache_page(60*10)(views.DeliveryView.as_view()), name='delivery'),
    path('contacts/', cache_page(60*10)(views.ContactsView.as_view()), name='contacts'),
    # path('delivery/', views.DeliveryView.as_view(), name='delivery'),
    # path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('policy/', views.PolicyView.as_view(), name='policy'),
]
