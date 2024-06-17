from django import template
from django_jalali.db import models

register = template.Library()


@register.filter(name='wdayFinder')
def wdayFinder(value):
    weekdayList = [ "شنبه", "یکشنبه",  "دوشنبه",
        "سه شنبه","چهارشنبه",  "پنجشنبه", "جمعه"]
    return weekdayList[value.weekday()]

# Remember to replace commas with underscores
