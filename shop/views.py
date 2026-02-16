from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from shop.models import Product, Category


# Create your views here.


def catalogue(request, category_slug=None):  # category_slug для фильтрации
    """
    Отображение страницы каталога
    :param request: путь
    :param category_slug: для фильтрации по категориям
    :return:
    """
    # Получаем категории и продукты для страницы
    products = Product.objects.all()
    categories = Category.objects.all()
    current_category = None
    print("вызываю функцию catalogue ")
    # Фильтр по категории (если передан slug в URL)
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    # Фильтр по цене из GET
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Сортировка из GET (минимальная, максимальная цена)
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    # Пагинация
    paginator = Paginator(products, 9)  # подключаем пагинацию товаров
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # Получаем объект, количество страниц Page <Page 1 of 2>
    print('current_category', current_category)
    context = {
        'page_obj': page_obj,  # для пагинации и списка товаров
        'categories': categories,
        'current_category': current_category,
    }
    if not current_category:
        context['products'] = products
    else:
        pass

    return render(request, 'catalogue.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    print("product", product)
    return render(request, 'product.html', {'product': product})


def search_product(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query)
    print("поиск по сайту, получил резы", results)
    return render(request, 'search_results.html', {'results': results, 'query': query})
