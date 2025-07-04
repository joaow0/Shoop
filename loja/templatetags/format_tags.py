from django import template

register = template.Library()

@register.filter()
def moeda_br(valor):
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return valor

    return f'R$ {valor:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')

@register.filter
def get_user_avaliacao(avaliacoes, user):
    return avaliacoes.filter(cliente__usuario=user).first()



@register.filter
def divisao(valor, divisor):
    """Divide um valor por outro."""
    try:
        return float(valor) / int(divisor)
    except:
        return 0
