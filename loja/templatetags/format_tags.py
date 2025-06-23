from django import template

register = template.Library()

@register.filter()
def moeda_br(valor):
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return valor

    return f'R$ {valor:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')
