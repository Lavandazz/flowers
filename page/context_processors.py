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
        company = CompanyInfo.objects.prefetch_related("phones", "emails").first()

        company_data = {
                'name': company.name,
                'inn': company.inn,
                'ogrn': company.ogrn,
                'street': company.street,
                'house': company.house,
                'building': company.building,
                'phones': [phone.telephone for phone in company.phones.all()],
                'emails': [email.email for email in company.emails.all()],
            }
        cache.set('company_info', company_data, 60*10)

        return {
            'company_info': company_data,
        }
