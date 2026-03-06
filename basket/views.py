from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.template.loader import render_to_string

from basket.models import Basket
from basket.utils import get_user_baskets
from shop.models import Product


# Create your views here.

def basket_add(request):
    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'Не передан product_id'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)

    # Получаем текущую корзину (создаёт сессию, если нужно)
    user_baskets = get_user_baskets(request)

    # Пытаемся найти уже существующую запись этого товара
    basket_item = user_baskets.filter(product=product).first()
    if basket_item:
        basket_item.quantity += 1
        basket_item.save()
    else:
        # Создаём новую запись
        if request.user.is_authenticated:
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            # Для анонима используем session_key
            session_key = request.session.session_key
            # Привязываем корзину к анонимному ключу
            Basket.objects.create(session_key=session_key, product=product, quantity=1)

    # Получаем обновлённую корзину для ответа
    updated_baskets = get_user_baskets(request)
    basket_items_html = render_to_string("included_basket.html", {'baskets': updated_baskets}, request=request)
    total_quantity = sum(item.quantity for item in updated_baskets)

    return JsonResponse({
        'message': 'Товар добавлен в корзину',
        'basket_items_html': basket_items_html,
        'total_quantity': total_quantity,
        'order': True
    })


def basket_change(request):
    basket_item_id = request.POST.get('basket_item_id')
    action = request.POST.get('action')
    if not basket_item_id or not action:
        return JsonResponse({'error': 'Не переданы обязательные параметры'}, status=400)

    # Берём только те записи, которые принадлежат текущему пользователю/сессии
    user_baskets = get_user_baskets(request)
    try:
        basket_item = user_baskets.get(id=basket_item_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Товар в корзине не найден'}, status=404)

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

    updated_baskets = get_user_baskets(request)
    basket_items_html = render_to_string("included_basket.html", {'baskets': updated_baskets}, request=request)
    total_quantity = sum(item.quantity for item in updated_baskets)

    return JsonResponse({
        'message': 'Количество обновлено',
        'basket_items_html': basket_items_html,
        'total_quantity': total_quantity,
    })


def basket_remove(request):
    basket_item_id = request.POST.get('basket_item_id')
    if not basket_item_id:
        return JsonResponse({'error': 'Не передан basket_item_id'}, status=400)

    user_baskets = get_user_baskets(request)
    try:
        basket_item = user_baskets.get(id=basket_item_id)
        basket_item.delete()
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)

    updated_baskets = get_user_baskets(request)
    basket_items_html = render_to_string("included_basket.html", {'baskets': updated_baskets}, request=request)
    total_quantity = sum(item.quantity for item in updated_baskets)

    return JsonResponse({
        'message': 'Товар удалён из корзины',
        'basket_items_html': basket_items_html,
        'total_quantity': total_quantity,
    })
