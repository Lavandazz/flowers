from django.views.generic.base import TemplateView

from page.models import CompanyInfo


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
        return context


class PolicyView(TemplateView):
    template_name = 'policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Политика конфиденциальности'

        return context
