PAGE_TYPES = [
    ('products', 'Каталог товаров'),
    ('delivery', 'Доставка'),
    ('contacts', 'Контакты'),
]


def get_page_display(page_type: str) -> str | None:
    for item in PAGE_TYPES:
        if page_type in item:
            return item[1]

# pages = [item[0] for item in PAGE_TYPES]
# context = ['paginator', 'page_obj', 'is_paginated', 'object_list', 'products', 'view']
