from django import template
from jdatetime import datetime

register = template.Library()


@register.filter(name='format_money')
def format_money(value):
    # Ensure the value is an integer
    value = int(value)
    # Format the integer with underscores
    return '/'.join(f"{value:,}".split(','))


@register.filter
def date_only(value):
    """
    Extracts the date portion from a datetime string or object.
    """
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')

    try:
        # Assuming the input is a string formatted as "YYYY-M-D H:M:S.microseconds"
        date_part = value.split()[0]
        return datetime.strptime(date_part, "%Y-%m-%d").strftime('%Y-%m-%d')
    except (ValueError, AttributeError):
        return value  # Return the original value if parsing fails
