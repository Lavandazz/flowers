from django.db.models import Q
from django.db.models.manager import BaseManager

from shop.models import Product


def q_search(query) -> BaseManager | None:
    """
    Поиск по сайту в названиях и описании. Не учитывает регистр.
    :param query:
    :return:
    """
    return Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
