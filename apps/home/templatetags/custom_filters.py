from django import template

register = template.Library()


@register.filter(name='format_money')
def format_money(value):
    # Ensure the value is an integer
    value = int(value)
    # Format the integer with underscores
    return '/'.join(f"{value:,}".split(','))

# Remember to replace commas with underscores
