from django.core.cache import cache
from .models import CompanyInfo   # или ContactInfo

def company_info(request):
    """
    Добавляет информацию о компании во все шаблоны.
    """
    company = CompanyInfo.objects.first()  # Получаем первую запись с контактами компании
    cache.set('company_info', company, 60*10)
    return {
        'company_info': company,
    }
