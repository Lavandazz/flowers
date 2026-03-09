import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View

from basket.mixins import BasketMixin
from basket.models import Basket
from basket.utils import get_user_baskets
from shop.models import Product


# Create your views here.
logger = logging.getLogger(__name__)


class BasketAddView(BasketMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        basket = self.get_basket(request, product=product)

        if basket:
            basket.quantity += 1
            basket.save()
        else:
            # Создаём новую запись
            if request.user.is_authenticated:
                Basket.objects.create(user=request.user, product=product, quantity=1)
            else:
                # Для анонима используем session_key
                session_key = request.session.session_key
                # Привязываем корзину к анонимному ключу
                Basket.objects.create(session_key=session_key, product=product, quantity=1)

        rendered = self.render_basket(request)
        response_data = {
            'message': 'Товар добавлен в корзину',
                'basket_items_html': rendered['response_html'],
                'total_quantity': rendered['total_quantity'],
                'order': rendered['order']
        }
        logger.debug('response_data: %s', response_data)

        return JsonResponse(response_data)


class BasketChangeView(BasketMixin, View):
    def post(self, request):
        # Получаем айди корзины
        basket_item_id = request.POST.get('basket_item_id')

        # Получаем объект корзины по id и проверяем, что он принадлежит текущему пользователю/сессии
        basket_item = self.get_basket(request, basket_id=basket_item_id)
        if not basket_item:
            return JsonResponse({'error': 'Товар в корзине не найден'}, status=404)

        # Получаем вид взаимодействия (+/- increment/decrement)
        action = request.POST.get('action')

        if action == 'increment':
            basket_item.quantity += 1
            basket_item.save()
        elif action == 'decrement':
            if basket_item.quantity > 1:
                basket_item.quantity -= 1
                basket_item.save()
            else:
                basket_item.delete()  # удаляем, если количество становится 0
        else:
            return JsonResponse({'error': 'Некорректное действие'}, status=400)

        rendered = self.render_basket(request)
        return JsonResponse({
            'message': 'Количество обновлено',
            'basket_items_html': rendered['response_html'],
            'total_quantity': rendered['total_quantity'],
        })


class BasketRemoveView(BasketMixin, View):
    def post(self, request):
        basket_item_id = request.POST.get('basket_item_id')
        basket_item = self.get_basket(request, basket_id=basket_item_id)
        try:
            logger.info('Удаляю товар в корзине: %s', basket_item)
            basket_item.delete()
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Товар не найден'}, status=404)

        rendered = self.render_basket(request)
        return JsonResponse({
            'message': 'Количество обновлено',
            'basket_items_html': rendered['response_html'],
            'total_quantity': rendered['total_quantity'],
        })
