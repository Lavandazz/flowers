"""
URL configuration for flower_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home.txt, name='home.txt')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home.txt')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.views.generic import RedirectView
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)


admin.site.site_header = 'Административная панель Flower Shop'
admin.site.index_title = 'Добро пожаловать в панель управления'


urlpatterns = [
    path("flowers-dashboard/", admin.site.urls),
    path('metrics/', metrics_view),
    path("page/", include("page.urls")),
    path("user/", include("users.urls")),
    path("basket/", include("basket.urls")),
    path("orders/", include("orders.urls")),
    # Перенаправление catalogue на главную /, тк удалена страница index
    path('catalogue/', RedirectView.as_view(url='/', permanent=True)),
    path('', include('shop.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Для работы debug_toolbar
if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
                      *urlpatterns,
                  ] + debug_toolbar_urls()

# Обслуживание медиа из корня при Debug=Tr
