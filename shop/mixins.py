from django.views.generic import ListView

from shop.models import SaleBanner


class BannerMixin(ListView):
    """
    Отображение рекламного баннера на странице каталога
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = SaleBanner.objects.filter(is_active=True)

        return context
