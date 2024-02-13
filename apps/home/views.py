# -*- encoding: utf-8 -*-
from django import template
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Person, Classi, SessionDate, Peyment, AbsenceDate, Analysis
from dal import autocomplete
import jdatetime
from django.conf.urls.static import static
from django.conf import settings


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
   if request.user.is_admin:
        context = {'segment': 'index'}
        context['jdate'] = date_maker()
        person = Person.objects.all()
        context['person'] = person
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
   else:
       person = Person.objects.get(username=request.user.username)
       # personalreport(request, person.id)
       print(">>>>", person.id)
       return HttpResponseRedirect(f'personalreport/{person.id}')


@login_required(login_url="/login/")
def tables(request):
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

    html_template = loader.get_template('home/tables.html')
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


'''
@login_required(login_url="/login/")
def peymentreport(request, person_id):
    context = {'segment': 'peymentreport'}
    person = Person.objects.get(id=person_id)
    peyment = Peyment.objects.filter(peyment_person=person_id)
    context['peyment'] = peyment
    context['full_name'] = person.full_name
    html_template = loader.get_template('home/peymentreport.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def sessionreport(request, person_id):
    context = {'segment': 'sessionreport'}
    person = Person.objects.get(id=person_id)
    session = SessionDate.objects.filter(session_person=person_id)
    context['session'] = session
    context['full_name'] = person.full_name
    html_template = loader.get_template('home/sessionreport.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def absencereport(request, person_id):
    context = {'segment': 'absencereport'}
    person = Person.objects.get(id=person_id)
    absence = AbsenceDate.objects.filter(absent_person=person_id)
    context['absence'] = absence
    context['full_name'] = person.full_name
    html_template = loader.get_template('home/absencereport.html')
    return HttpResponse(html_template.render(context, request))
'''

@login_required(login_url="/login/")
def classlist(request, ccname):
    if request.method == 'POST':
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
    context = {'segment': 'classlist'}
    person = []
    for obj in Person.objects.all():
        if obj.classname.cname == ccname:
            person.append(obj)
    context['person'] = person
    context['cname'] = ccname
    html_template = loader.get_template('home/classlist.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def personalreport(request, person_id):
    if str(request.user.username) == Person.objects.get(id=person_id).username or request.user.is_admin:
        person_id = (request.path.split('/')[-1])
        if request.method == 'POST':
            person = Person.objects.get(id=person_id)
            SessionDate.objects.create(
                session_person=person, dos=jdatetime.datetime.now())
        
        person = Person.objects.get(id=person_id)

        analysisperson = Analysis.objects.get(analysis_person=person_id)
        lastanalysis = str(analysisperson.dot).split("-")

        context = {'segment': 'personalreport'}
        context['nextanalysis'] = f"{lastanalysis[0]}-{int(lastanalysis[1])+1}-{lastanalysis[2]}"

        context['person'] = person
        context['imglen'] = len(person.simage.name)
        l1 = str(person.insurancedate).split("-")
        context['nextinsurance']=f"{int(l1[0])+1}-{l1[1]}-{l1[2]}"
        context['buttonShow'] = True if request.user.is_admin else False
        
        session = SessionDate.objects.filter(session_person=person_id)
        context['session'] = session

        absence = AbsenceDate.objects.filter(absent_person=person_id)
        context['absence'] = absence

        peyment = Peyment.objects.filter(peyment_person=person_id)
        context['peyment'] = peyment


        html_template = loader.get_template('home/personalreport.html')
        return HttpResponse(html_template.render(context, request))
    else:
        context = {}
        html_template = loader.get_template('home/page-404.html')
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
