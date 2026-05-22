from django.core.cache import cache
from .models import CompanyInfo   # или ContactInfo

def company_info(request):
    """
    Добавляет информацию о компании во все шаблоны.
    Устанавливает кэширование на 10 минут для оптимизации производительности.
    """
    company = cache.get('company_info')
    
    if company:
        return {
        'company_info': company,
        }

    else:
        company = CompanyInfo.objects.first()  # Получаем первую запись с контактами компании
        cache.set('company_info', company, 60*10)
        return {
            'company_info': company,
        }
