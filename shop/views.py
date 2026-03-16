from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from shop.mixins import BannerMixin
from shop.models import Product, Category, Type, SaleBanner
from shop.utils import q_search


# Create your views here.

class CatalogueListView(BannerMixin, ListView):
    model = Product
    paginate_by = 9
    context_object_name = 'products'
    template_name = 'catalogue.html'

    def get_queryset(self):
        queryset = super().get_queryset()  # все товары

        # 1. Фильтр по категории из URL (например, /catalogue/rozy/)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(categories=category)
            self.current_category = category
        else:
            self.current_category = None

        # 2. Фильтр по типу товара (например, ?type=flowers)
        type_slug = self.request.GET.get('type')
        if type_slug:
            current_type = get_object_or_404(Type, slug=type_slug)
            categories_of_type = current_type.categories.all()
            queryset = queryset.filter(categories__in=categories_of_type).distinct()
            self.current_type = current_type
        else:
            self.current_type = None

        # 3. Фильтр по цене (price_min, price_max)
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        # 4. Сортировка (sort=price_asc или price_desc)
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['types'] = Type.objects.all()

        # Текущие выбранные фильтры (чтобы подсветить активные пункты)
        context['current_category'] = getattr(self, 'current_category', None)

        # Сохраняем значения GET-параметров для подстановки в формы
        context['price_min'] = self.request.GET.get('price_min', '')
        context['price_max'] = self.request.GET.get('price_max', '')
        context['sort'] = self.request.GET.get('sort', '')
        context['query'] = self.request.GET.get('q', '')

        context['title'] = 'Каталог'
        return context


class ProductSearchView(ListView):
    model = Product
    template_name = 'search_results.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:

            return q_search(query)
        # Если запрос пустой, возвращаем пустой QuerySet
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['title'] = 'Результаты поиска'
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        # Вызываем родительский метод get_context_data для переопределения/дополнения
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context




# def catalogue(request, category_slug=None):  # category_slug для фильтрации
#     """
#     Отображение страницы каталога
#     :param request: путь
#     :param category_slug: для фильтрации по категориям
#     :return:
#     """
#     # Получаем категории и продукты для страницы
#     query = request.GET.get('q')  # получаем запрос для поиска search, если есть
#     products = Product.objects.all()
#     categories = Category.objects.all()
#
#     # типы категорий (букеты, шары, подарки)
#     types = Type.objects.prefetch_related('categories').all()
#
#     current_category = None
#     # Фильтр по категории (если передан slug в URL)
#     if category_slug:
#         current_category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(categories=current_category)
#     if query:
#         products = q_search(query)
#
#     # Фильтр по типу из GET-параметра
#     type_slug = request.GET.get('type')
#     if type_slug:
#
#         current_type = get_object_or_404(Type, slug=type_slug)
#         # Получаем все категории этого типа
#         categories_of_type = current_type.categories.all()
#         # Фильтруем товары, которые связаны с любой из этих категорий
#         # Используем distinct(), чтобы избежать дублей, если товар в нескольких категориях одного типа
#         products = products.filter(categories__in=categories_of_type).distinct()
#
#     else:
#         current_type = None
#
#     # Фильтр по цене из GET
#     price_min = request.GET.get('price_min')
#     price_max = request.GET.get('price_max')
#     if price_min:
#         products = products.filter(price__gte=price_min)
#     if price_max:
#         products = products.filter(price__lte=price_max)
#
#     # Сортировка из GET (минимальная, максимальная цена)
#     sort = request.GET.get('sort')
#     if sort == 'price_asc':
#         products = products.order_by('price')
#     elif sort == 'price_desc':
#         products = products.order_by('-price')
#
#     # Пагинация
#     paginator = Paginator(products, 9)  # подключаем пагинацию товаров
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)  # Получаем объект, количество страниц Page <Page 1 of 2>
#
#     context = {
#         'title': 'Каталог',
#         'page_obj': page_obj,  # для пагинации и списка товаров
#         'types': types,
#         'categories': categories,
#         'current_category': current_category,
#         'current_type': current_type,
#
#     }
#     if not current_category:
#         context['products'] = products
#     else:
#         pass
#
#     return render(request, 'catalogue.html', context)


# def search_product(request):
#     query = request.GET.get('q', '')
#     results = Product.objects.filter(name__icontains=query)
#     return render(request, 'search_results.html', {'results': results, 'query': query})
