from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from shop.mixins import BannerMixin, SeoMixin
from shop.models import Product, Category, Type
from shop.utils import q_search


# Create your views here.

class CatalogueListView(BannerMixin, SeoMixin, ListView):
    model = Product
    paginate_by = 9
    context_object_name = 'products'
    template_name = 'catalogue.html'
    current_category = None
    current_type = None

    def get_queryset(self):
        queryset = super().get_queryset()  # все товары

                # --- ДЕФОЛТНЫЙ ФИЛЬТР: только категория "букеты" ---
        # Применяется, если нет ни category_slug из URL, ни type из GET-параметров
        if not self.kwargs.get('category_slug') and not self.request.GET.get('type'):
            flowers_type = Type.objects.filter(slug='bukety').first()
            if flowers_type:
                categories_of_type = flowers_type.categories.all()
                queryset = queryset.filter(categories__in=categories_of_type).distinct()
                self.current_type = flowers_type
                # self.current_category = bukety_category  # чтобы подсвечивалось в меню

        # 1. Фильтр по категории из URL (например, /catalogue/rozy/)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(categories=category)
            self.current_category = category

        # 2. Фильтр по типу товара (например, ?type=flowers)
        type_slug = self.request.GET.get('type')
        if type_slug:
            current_type = get_object_or_404(Type, slug=type_slug)
            categories_of_type = current_type.categories.all()
            queryset = queryset.filter(categories__in=categories_of_type).distinct()
            self.current_type = current_type

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
        context['current_type'] = getattr(self, 'current_type', None)
        context['current_category'] = getattr(self, 'current_category', None)

        # Сохраняем значения GET-параметров для подстановки в формы
        context['price_min'] = self.request.GET.get('price_min', '')
        context['price_max'] = self.request.GET.get('price_max', '')
        context['sort'] = self.request.GET.get('sort', '')
        context['query'] = self.request.GET.get('q', '')

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
        context['description'] = self.object.name

        # Для отображения одной фотки в og
        first_image = self.object.images.first().image
        if first_image:
            # Формируем абсолютный url
            context['og_image'] = self.request.build_absolute_uri(first_image.url)

        return context
