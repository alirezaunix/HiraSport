# -*- encoding: utf-8 -*-
from django import template
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Person, Classi, SessionDate, Peyment, AbsenceDate, Analysis,Trainer,TrainerSeesion
from dal import autocomplete
import jdatetime
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.models import User



def date_maker():
    weekday = {"Sat": "شنبه", "Sun": "یکشنبه", "Mon": "دوشنبه",
        "Tue": "سه شنبه", "Wed": "چهارشنبه", "Thu": "پنجشنبه", "Fri": "جمعه"}
    monthname = {"01": "فروردین", "02": "اردیبهشت", "03": "خرداد", "04": "تیر", "05": "مرداد",
        "06": "شهریور", "07": "مهر", "08": "آبان", "09": "آذر", "10": "دی", "11": "بهمن", "12": "اسفند"}
    jnow = jdatetime.datetime.now()
    jdate = f"{weekday[jnow.strftime('%a')]}\t{jnow.strftime('%d')}\t{monthname[jnow.strftime('%m')]}\t{jnow.strftime('%Y')}"
    return jdate


class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
        #    return Person.objects.none()
        qs = Person.objects.all()
        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)
        return qs


@login_required(login_url="/login/")
def index(request):
   if request.user.is_superuser:
        '''
        print(dir(User))
        
        print("---------------")
        print(request.user.hash_password())
        print("---------------")
        print(dir(Person))'''
        context = {'segment': 'index'}
        context['jdate'] = date_maker()
        person = Person.objects.all()
        context['person'] = person
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
   else:
       person = Person.objects.get(username=request.user.username)
       # personalreport(request, person.id)
       #print(">>>>", person.id)
       return HttpResponseRedirect(f'personalreport/{person.id}')


@login_required(login_url="/login/")
def todayclasslist(request):
    context = {'segment': 'index'}
    context['jdate'] = date_maker()
    weekday = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",]
    wday = weekday[jdatetime.datetime.today().weekday()-1]
    currentclasses = {obj.id: obj.weekdays for obj in Classi.objects.filter(
        weekdays__contains=wday)}
    classesname = []
    classesstarttime = []
    classobj = []
    classtrainer = []

    for item in currentclasses:
        if wday in currentclasses[item]:
            classobj.append(Classi.objects.filter(id=item))

    for obj in classobj:
        classesname.append(obj[0].cname)
        classesstarttime.append(obj[0].starttime.strftime('%H:%m'))
        classtrainer.append(obj[0].tname)
    personcount = []

    for objP in Person.objects.all():
        counter = 0
        for item in classesname:
            if not objP.is_superuser :
                print("******",objP.id)
                if item in objP.classname.cname:
                    counter += 1
        personcount.append(counter)

    row_data = []
    a_row = {}
    for i in range(len(classesname)):
        a_row['classesname'] = classesname[i]
        a_row['classtrainer'] = classtrainer[i]
        a_row['classesstarttime'] = classesstarttime[i]
        row_data.append(a_row)
        a_row = {}
    context['row_data'] = row_data

    html_template = loader.get_template('home/todayclasslist.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def debt(request):
    context = {'segment': 'index'}
    person = Person.objects.all()
    context['person'] = person
    html_template = loader.get_template('home/debt.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def analyzereport(request):
    context = {'segment': 'index'}
    analyze = Analysis.objects.all()
    context['analyze'] = analyze
    html_template = loader.get_template('home/analyzereport.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def classlist(request, ccname):
    if request.method == 'POST':
        print(request.POST)
        for item in request.POST:
            if 'status' in item:
                person_id = request.POST[item].split("_")[-1]
                if request.POST[item].split("_")[0] == 'present':
                    person = Person.objects.get(id=person_id)
                    SessionDate.objects.create(
                        session_person=person, dos=jdatetime.datetime.now())
                elif request.POST[item].split("_")[0] == 'absent':
                    person = Person.objects.get(id=person_id)
                    AbsenceDate.objects.create(
                        absent_person=person, doa=jdatetime.datetime.now())
            elif "trainer" in item:   
                trainer_id = request.POST[item].split("_")[-1]
                trainer=Trainer.objects.get(id=trainer_id)
                TrainerSeesion.objects.create(session_trainer=trainer, dos_trainer=jdatetime.datetime.now(),class_trainer=ccname)
    context = {'segment': 'classlist'}
    person = []
    for obj in Person.objects.all():
        if not obj.is_admin:
            if obj.classname.cname == ccname  :
                person.append(obj)
    context['person'] = person
    context['cname'] = ccname
    trainers=[]
    for obj in Trainer.objects.all():
        trainers.append(obj)
    context['trainers']=trainers
    html_template = loader.get_template('home/classlist.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def personalreport(request, person_id):
    if str(request.user.username) == Person.objects.get(id=person_id).username or request.user.is_superuser:
        person_id = (request.path.split('/')[-1])
        if request.method == 'POST':
            person = Person.objects.get(id=person_id)
            SessionDate.objects.create(
                session_person=person, dos=jdatetime.datetime.now())
        
        person = Person.objects.get(id=person_id)

        analysisperson = Analysis.objects.filter(analysis_person=person_id).latest('dot')
        lastanalysis = str(analysisperson.dot).split("-")
        monti=int(lastanalysis[1])+1
        if monti>12:
            yeari=int(lastanalysis[0])+1
            monti=monti%12
        context = {'segment': 'personalreport'}
        context['nextanalysis'] = f"{yeari}-{monti}-{lastanalysis[2]}"

        context['person'] = person
        context['imglen'] = len(person.simage.name)
        l1 = str(person.insurancedate).split("-")
        context['nextinsurance']=f"{int(l1[0])+1}-{l1[1]}-{l1[2]}"
        context['buttonShow'] = True if request.user.is_superuser else False
        
        session = SessionDate.objects.filter(session_person=person_id)
        context['session'] = session

        absence = AbsenceDate.objects.filter(absent_person=person_id)
        context['absence'] = absence

        peyment = Peyment.objects.filter(peyment_person=person_id)
        context['peyment'] = peyment
        
        analysis=Analysis.objects.filter(analysis_person=person_id)
        context["analysis"] = analysis
        
###############################
        very_distracting_data = [
        { "label": "Sunday", "y": 2.4 },
        { "label": "Monday", "y": .6 },
        { "label": "Tuesday", "y": .8 },
        { "label": "Wednesday", "y": 1.6 },
        { "label": "Thursday", "y": 1.4 },
        { "label": "Friday", "y": 1.4 },
        { "label": "Saturday", "y": 2.6 }
    ]

        distracting_data = [
        { "label": "Sunday", "y": 3.3 },
        { "label": "Monday", "y": 1.6 },
        { "label": "Tuesday", "y": 2.1 },
        { "label": "Wednesday", "y": 1.6 },
        { "label": "Thursday", "y": 1.4 },
        { "label": "Friday", "y": 1.7 },
        { "label": "Saturday", "y": 4.6 }
    ]

        productive_data = [
        { "label": "Sunday", "y": 2.4 },
        { "label": "Monday", "y":  2 },
        { "label": "Tuesday", "y": 2.8 },
        { "label": "Wednesday", "y": 1.6 },
        { "label": "Thursday", "y": 1.4 },
        { "label": "Friday", "y": 1.4 },
        { "label": "Saturday", "y": 1.6 }
    ]

        
        context.update({"very_distracting_data": very_distracting_data, "distracting_data": distracting_data,
                       "productive_data": productive_data, })
###############################


        html_template = loader.get_template('home/personalreport.html')
        return HttpResponse(html_template.render(context, request))
    else:
        context = {}
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def trainerreport(request, trainer_id):
        count=0
        trainer = Trainer.objects.get(id=trainer_id)
        trainerseesion = TrainerSeesion.objects.filter(session_trainer=trainer_id)
        mont=(str(jdatetime.datetime.now()).split("-")[1])     
        for item in trainerseesion:
            if f"-{mont}-" in str(item.dos_trainer):
                count+=1
        context = {'segment': 'trainerreport'}
        context['trainer'] = trainer
        context['trainerseesion'] = trainerseesion
        context['mont']=mont
        context['count']=count
        context['superuserview'] = True if request.user.is_superuser else False
        html_template = loader.get_template('home/trainerreport.html')
        return HttpResponse(html_template.render(context, request))
'''
    else:
        context = {}
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
'''

@login_required(login_url="/login/")
def trainerslist(request):
        colorbg=[
        "bg-red",
        "bg-yellow",
        "bg-aqua",
        "bg-blue",
        "bg-light-blue",
        "bg-green",
        "bg-navy",
        "bg-teal",
        "bg-olive",
        "bg-lime",
        "bg-orange",
        "bg-fuchsia",
        ]
        
        trainers = Trainer.objects.all()
        context = {'segment': 'trainerslist'}
        context['trainers'] = trainers
        context['colorbg'] = colorbg
        context['1'] = "bg-red"
        context['2'] = "bg-yellow"
        context['3'] = "bg-aqua"
        context['4'] = "bg-green"

        html_template = loader.get_template('home/trainerslist.html')
        return HttpResponse(html_template.render(context, request))
    

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # try:
    load_template = request.path.split('/')[-1]
       # load_template_2 = request.path.split('/')[-2]
    if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
       # elif load_template=='debt':
       #     return HttpResponseRedirect(reverse('debt'))
       # #elif load_template=='personalreport':# or load_template_2=='personalreport':
       # #    return HttpResponseRedirect(reverse('personalreport'))
       # elif load_template=='peymentreport':
       #     return HttpResponseRedirect(reverse('peymentreport'))
       # elif load_template=='sessionreport':
       #     return HttpResponseRedirect(reverse('sessionreport'))
       # elif load_template=='classlist':
       #     return HttpResponseRedirect(reverse('classlist'))
       # elif load_template=='tables':
       #     return HttpResponseRedirect(reverse('tables'))

    context['segment'] = load_template
    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))


'''
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
'''
