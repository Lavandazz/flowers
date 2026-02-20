from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from basket import models
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
            Basket.objects.create(session_key=session_key, product=product, quantity=1)

    # Получаем обновлённую корзину для ответа
    updated_baskets = get_user_baskets(request)
    basket_items_html = render_to_string("included_basket.html", {'baskets': updated_baskets}, request=request)
    total_quantity = sum(item.quantity for item in updated_baskets)

    return JsonResponse({
        'message': 'Товар добавлен в корзину',
        'basket_items_html': basket_items_html,
        'total_quantity': total_quantity,
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

# def basket_add(request):
#     product_id = request.POST.get('product_id')
#     print('получил', product_id)
#     product = Product.objects.get(id=product_id)
#
#     if not product_id:
#         return JsonResponse({'error': 'Не передан product_id'}, status=400)
#
#     if request.user.is_authenticated:
#         # Фильтруем по пользователю и конкретному продукту
#         baskets = Basket.objects.filter(user=request.user, product=product)
#         # если корзина не пустая
#         if baskets.exists():
#             basket = baskets.first()
#             if basket:
#                 basket.quantity += 1
#                 basket.save()
#         else:
#             # если корзина пустая, сохраняем юзера и продукт
#             Basket.objects.create(user=request.user, product=product, quantity=1)
#     # Перенаправление на страницу, где бы пользователь
#
#     user_basket = get_user_baskets(request=request)
#     total_quantity = sum(item.quantity for item in user_basket)
#     basket_items_html = render_to_string(
#         "included_basket.html", {'baskets': user_basket}, request=request
#     )
#
#     response_data = {
#         'message': 'Товар добавлен в корзину',
#         'basket_items_html': basket_items_html,
#         'total_quantity': total_quantity,
#     }
#     return JsonResponse(response_data)
#
#
# def basket_change(request):
#     """
#     Изменяет количество товара в корзине.
#     Принимает basket_item_id (id записи в корзине) и action ('increment' или 'decrement').
#     """
#     basket_item_id = request.POST.get('basket_item_id')
#     action = request.POST.get('action')
#
#     if not basket_item_id or not action:
#         return JsonResponse({'error': 'Не переданы обязательные параметры'}, status=400)
#
#     try:
#         basket_item = Basket.objects.get(id=basket_item_id, user=request.user)
#     except ObjectDoesNotExist:
#         return JsonResponse({'error': 'Товар в корзине не найден'}, status=404)
#
#     if action == 'increment':
#         basket_item.quantity += 1
#     elif action == 'decrement':
#         if basket_item.quantity > 1:
#             basket_item.quantity -= 1
#         else:
#             # Если количество становится 0, удаляем товар (можно оставить 1 или удалить)
#             basket_item.delete()
#             # После удаления получаем обновлённую корзину и возвращаем ответ
#             user_basket = get_user_baskets(request=request)
#             basket_items_html = render_to_string("included_basket.html", {'baskets': user_basket}, request=request)
#             total_quantity = sum(item.quantity for item in user_basket)
#             return JsonResponse({
#                 'message': 'Количество товара уменьшено до 0, товар удалён',
#                 'basket_items_html': basket_items_html,
#                 'total_quantity': total_quantity,
#             })
#     else:
#         return JsonResponse({'error': 'Некорректное действие'}, status=400)
#
#     basket_item.save()
#
#     # Получаем обновлённую корзину
#     user_basket = get_user_baskets(request=request)
#     basket_items_html = render_to_string("included_basket.html", {'baskets': user_basket}, request=request)
#     total_quantity = sum(item.quantity for item in user_basket)
#
#     return JsonResponse({
#         'message': 'Количество обновлено',
#         'basket_items_html': basket_items_html,
#         'total_quantity': total_quantity,
#     })
#
#
# def basket_remove(request):
#     product_id = request.POST.get('basket_item_id')  # берем из js
#     if not product_id:
#         return JsonResponse({'error': 'Не передан product_id'}, status=400)
#     try:
#         basket_item = Basket.objects.get(id=product_id, user=request.user)
#         basket_item.delete()
#     except ObjectDoesNotExist:
#         return JsonResponse({'error': 'Товар не найден'}, status=404)
#
#     user_basket = get_user_baskets(request=request)
#
#     total_quantity = sum(item.quantity for item in user_basket)
#
#     basket_items_html = render_to_string(
#         "included_basket.html", {
#             'baskets': user_basket
#         }, request=request
#     )
#
#     response_data = {
#         'message': 'Товар удален',
#         'basket_items_html': basket_items_html,
#         'total_quantity': total_quantity,
#     }
#     return JsonResponse(response_data)
