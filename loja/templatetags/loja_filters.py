from django import template

register = template.Library()

@register.filter
def remove_page_param(request_get_params):
    """
    Remove o parâmetro 'page' de um QueryDict de request.GET.
    Usado principalmente para links de paginação para evitar duplicidade do parâmetro 'page'.
    """
    cleaned_params = request_get_params.copy()
    if 'page' in cleaned_params:
        del cleaned_params['page']
    return cleaned_params.urlencode()