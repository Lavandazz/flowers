from django.template.loader import render_to_string

from basket.models import Basket
from basket.utils import get_user_baskets


class BasketMixin(object):
    def get_basket(self, request, product=None, basket_id=None):
        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        else:
            # Для анонима используем session_key
            query_kwargs = {'session_key': request.session.session_key}
        # Передаем в фильтр id товара
        if product:
            query_kwargs = {'product': product}

        # Передаем в фильтр id корзины
        if basket_id:
            query_kwargs['id'] = basket_id

        return Basket.objects.filter(**query_kwargs).first()

    def render_basket(self, request):
        user_basket = get_user_baskets(request)
        total_quantity = sum(item.quantity for item in user_basket)
        context = {
            'baskets': user_basket,
        }
        response_html = render_to_string("included_basket.html",
                                         context=context,
                                         request=request)
        return {
            'response_html': response_html,
            'total_quantity': total_quantity,
            'order': True
        }
