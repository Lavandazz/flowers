from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'page'

urlpatterns = [
    path('delivery/', cache_page(60)(views.DeliveryView.as_view()), name='delivery'),
    path('contacts/', cache_page(60)(views.ContactsView.as_view()), name='contacts'),
]
