from django.urls import path


from . import views
from .views import UserLoginView

app_name = 'user'

# Страница каталога
urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('user-basket/', views.user_basket, name='user_basket'),
    path('logout/', views.logout, name='logout'),

]
