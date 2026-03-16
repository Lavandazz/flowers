from django.views.generic.base import TemplateView

from page.models import Requisites


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
    model = Requisites

    def get_context_data(self, **kwargs):
        # Вызываем родительский метод get_context_data для переопределения/дополнения
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['requisites'] = Requisites.objects.first()
        return context
