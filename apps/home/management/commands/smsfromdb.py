from apps.home.models import Person,Classi
from django.core.management.base import BaseCommand
from datetime import datetime
from .melipayamak import Api



class Command(BaseCommand):
    help = 'Query today classes and send sms that is remains 1 session'

    def handle(self, *args, **options):
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun",]
        nextdayweekday=weekdays[datetime.today().weekday()+1]
        nextdayclass = Classi.objects.filter(weekdays__contains=nextdayweekday)
        queryset = Person.objects.filter(
            rsession=1, classname__in=nextdayclass, is_active=True)
        #queryset=Person.objects.filter(id=188)
        self.my_custom_function(queryset)
        

    def my_custom_function(self, queryset):
        for item in queryset:
            self.stdout.write(f'Processing item with ID: {item.id}')
            
            username = '09396163750'
            password = '9PBO0'
            api = Api(username, password)
            sms = api.sms()
            to = item.phone1
            _from = '50002710063750'
            text = f'''ورزشکار عزیز: خانم/آقای {item.full_name}
امروز جلسه یازدهم از دوره {item.classname}  شماست.
در صورت تمایل به شرکت مجدد در کلاس لطفا به کادر اداری باشگاه اطلاع دهید
                        هیرا اسپرت'''
            response = sms.send(to, _from, text)
            print(response)
