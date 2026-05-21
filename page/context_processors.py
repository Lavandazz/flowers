from .models import CompanyInfo   # или ContactInfo

def company_info(request):
    """
    Добавляет информацию о компании во все шаблоны.
    """
    return {
        'company_info': CompanyInfo.objects.first(),
    }