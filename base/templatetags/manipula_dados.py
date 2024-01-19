from django.template import Library
from base.utils import moeda

register = Library()


@register.filter
def formata_moeda(value):
    return moeda.formata(value)


