from apps.home.models import Person,Classi,SendSMS
from django.core.management.base import BaseCommand
from datetime import datetime
from .melipayamak import Api
from django.db.models import Q
import jdatetime



class Command(BaseCommand):
    help = 'Query today classes and send sms that is remains 1 session'

    def handle(self, *args, **options):
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun",]
        nextdayweekday=weekdays[datetime.today().weekday()+1]
        nextdayclass = Classi.objects.filter(weekdays__contains=nextdayweekday)
        queryset = Person.objects.filter(
            rsession=1, classname__in=nextdayclass, is_active=True).exclude(Q(phone1__isnull=True) | Q(phone1=''))
        #queryset=Person.objects.filter(id=188)
        self.my_custom_function(queryset)
        
    def senderSelection(self,phonenum):
        irancellList = ['0930', '0933', '0935', '0936', '0937',
                        '0938', '0939', '0901', '0902', '0903', '0905']
        if any(phonenum.startswith(prefix) for prefix in irancellList):
            return '50002710063750'
        else:
            return '10003768401579'


    def my_custom_function(self, queryset):
        username = '09396163750'
        password = '9PBO0'
        api = Api(username, password)
        sms = api.sms()

        for item in queryset:
            text = f'''ورزشکار عزیز: خانم/آقای {item.full_name}
فردا جلسه آخر  از دوره {item.classname}  شماست.
در صورت تمایل به شرکت مجدد در کلاس لطفا به کادر اداری باشگاه اطلاع دهید
                            هیرا اسپرت
                            لغو ۱۱'''
            self.stdout.write(f'Processing item with ID: {item.id}')            
            to = item.phone1
            _from = self.senderSelection(item.phone1)
            response = sms.send(to, _from, text)
            jnow = jdatetime.datetime.now().strftime('%Y-%m-%d')
            SendSMS.objects.create(send_person=item, send_dop=jnow)
            
            print(response)
