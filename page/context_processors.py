from venv import logger

from django.core.cache import cache
from .models import CompanyInfo   # или ContactInfo

def company_info(request):
    """
    Добавляет информацию о компании во все шаблоны.
    Устанавливает кэширование на 10 минут для оптимизации производительности.
    """
    company = cache.get('company_info')
    logger.info("company %s", company)
    if company and company is not None:
        logger.info("получаю данные из кеша %s", company)
        return {
        'company_info': company,
        }

    else:
        try:
            company = CompanyInfo.objects.prefetch_related("phones", "emails").first()
            logger.info("получаю данные из бд %s", company)

            company_data = {
                    'name': "Floristka" if company.name is None else company.name,
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
        except AttributeError as e:
            logger.error("Нет атрибута в CompanyInfo %s", e)
            company_data = {
                    'name': "",
                    'inn': "",
                    'ogrn': "",
                    'street': "",
                    'house': "",
                    'building': "",
                    'phones': "",
                    'emails': "",
                }
            return {
                'company_info': company_data,
            }