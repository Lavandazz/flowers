from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'page'

urlpatterns = [
    path('delivery/', cache_page(60*10)(views.DeliveryView.as_view()), name='delivery'),
    path('contacts/', cache_page(60*10)(views.ContactsView.as_view()), name='contacts'),
    path('policy/', cache_page(60*10)(views.PolicyView.as_view()), name='policy'),
    path('marketing/', cache_page(60*10)(views.MarketingView.as_view()), name='marketing'),
    path('agreement/', cache_page(60*10)(views.AgreementView.as_view()), name='agreement'),
    path('agreement-reviews/', cache_page(60*10)(views.AgreementReviewsView.as_view()), name='agreement_reviews'),
    path('agreement-cookies/', cache_page(60*10)(views.CookiesAgreementView.as_view()), name='agreement_cookies'),

]
