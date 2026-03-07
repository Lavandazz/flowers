from django.urls import path


from . import views
from .views import UserLoginView

app_name = 'user'

# Страница каталога
urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name='login'),
    path('registration/', views.RegisterView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),

]
