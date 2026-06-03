from django import template

register = template.Library()


@register.filter
def decimal_input(valor):
    if valor is None:
        return ""

    return str(valor).replace(",", ".")