from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from shop.models import Product, Category


# Create your views here.


def catalogue(request, category_slug=None):  # category_slug для фильтрации
    products = Product.objects.all()  # получаем все товары из БД
    categories = Category.objects.all()  # получаем категории
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    paginator = Paginator(products, 9)  # подключаем пагинацию товаров
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalogue.html', {
        'categories': categories,
        'current_category': current_category,
        'products': products,
        'page_obj': page_obj,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product.html', {'product': product})


def search_product(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query)
    if results:
        print('результаты поиска', results)
    else:
        print('ничего не нашел')
    return render(request, 'search_results.html', {'results': results, 'query': query})
