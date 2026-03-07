from django.urls import path

from . import views

app_name = 'page'

urlpatterns = [
    path('delivery/', views.DeliveryView.as_view(), name='delivery'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]
