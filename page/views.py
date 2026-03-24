from django.db.models import Prefetch
from django.views.generic.base import TemplateView

from page.models import CompanyInfo, PointPolicy, Policy


# Create your views here.

class DeliveryView(TemplateView):
    template_name = 'delivery.html'

    def get_context_data(self, **kwargs):
        # Вызываем родительский метод get_context_data для переопределения/дополнения
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка'
        return context


class ContactsView(TemplateView):
    template_name = 'contacts.html'
    model = CompanyInfo

    def get_context_data(self, **kwargs):
        # Вызываем родительский метод get_context_data для переопределения/дополнения
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['requisites'] = CompanyInfo.objects.first()
        return context


class PolicyView(TemplateView):
    template_name = 'policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Политика'
        context['company'] = CompanyInfo.objects.prefetch_related(
        Prefetch('main_points', queryset=PointPolicy.objects.all()),
        Prefetch('main_points__points',
                 queryset=Policy.objects.order_by('order'))
        ).first()
        return context
