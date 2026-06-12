from django.urls import path
from django.contrib.auth.views import LogoutView


from . import views


app_name = 'user'

# Страница каталога
urlpatterns = [
    # path("login/", views.UserLoginView.as_view(), name='login'),
    # path('registration/', views.RegisterView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
]
