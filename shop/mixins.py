from django.views.generic import ListView

from page.models import SEO
from shop.models import SaleBanner


class BannerMixin(ListView):
    """
    Отображение рекламного баннера на странице каталога
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = SaleBanner.objects.filter(is_active=True)

        return context


class SeoMixin:
    """
    SEO оптимизация для представлений сайта
    """
    def get_seo_data(self, context, page):
        seo = SEO.objects.filter(page_type=page).first()
        context['title'] = seo.title
        context['description'] = seo.description

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        default_title = 'Купить цветы в Москве – свежие букеты с доставкой'
        default_description = ('Широкий выбор свежих цветов, букетов на заказ, игрушек и сувениров в Москве. '
                               'Быстрая доставка или самовывоз из магазина на Гостиничном проезде, 4Б.')
        context_keys = [k for k in context.keys()]
        context['title'] = ''
        context['description'] = ''
        if 'products' in context_keys:
            seo = SEO.objects.filter(page_type='products').first()
            if seo:
                context['title'] = seo.title
                context['description'] = seo.description
            else:
                context['title'] = default_title
                context['description'] = default_description

        elif 'contacts' in context_keys:
            seo = SEO.objects.filter(page_type='contacts').first()
            if seo:
                context['title'] = seo.title
                context['description'] = seo.description
            else:
                context['title'] = default_title
                context['description'] = default_description
        elif 'delivery' in context_keys:
            seo = SEO.objects.filter(page_type='delivery').first()
            if seo:
                context['title'] = seo.title
                context['description'] = seo.description
            else:
                context['title'] = default_title
                context['description'] = default_description

        else:
            context['title'] = 'Купить цветы в Москве – свежие букеты с доставкой'
            context['description'] = ('Широкий выбор свежих цветов, букетов на заказ, игрушек и сувениров в Москве. '
                                      'Быстрая доставка или самовывоз из магазина на Гостиничном проезде, 4Б.')

        return context
