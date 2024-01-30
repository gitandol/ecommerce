from django.template import Library
from base.utils import moeda, carrinho

register = Library()


@register.filter
def formata_moeda(value):
    return moeda.formata(value)


@register.filter
def total_itens_carrinho(value):
    return carrinho.quantidade_itens(value)


@register.filter
def valor_itens_carrinho(value):
    return carrinho.valor_itens(value)


