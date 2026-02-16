from django.db.models import Q
from django.db.models.manager import BaseManager

from shop.models import Product, Category


def q_search(query) -> BaseManager | None:
    return Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
