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
from django.contrib.auth.models import User
from .forms import AttendanceForm
from django.forms import formset_factory
import datetime


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
            qs = qs.filter(full_name__istartswith=self.q)
        return qs


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    context['username']=request.user
    if request.user.is_superuser:
        context['jdate'] = date_maker()
        person = Person.objects.filter(role="student")
        context['person'] = person
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun",]
        wday = weekdays[datetime.datetime.today().weekday()]
        currentclasses = {obj : obj.weekdays for obj in Classi.objects.filter(
            weekdays__contains=wday)}
        context['currentclasses'] = currentclasses
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
    elif request.user.role=="student":
       person = Person.objects.get(username=request.user.username)
       # personalreport(request, person.id)
       #print(">>>>", person.id)
       return HttpResponseRedirect(f'personalreport/{person.id}')
    elif request.user.role=="trainer":
       person = Person.objects.get(username=request.user.username)
       return HttpResponseRedirect(f'trainerreport/{person.id}')


@login_required(login_url="/login/")
def todayclasslist(request):
    context = {'segment': 'index'}
    context['jdate'] = date_maker()
    context['row_data']=Classi.objects.all()
    
    '''
    weekday = [ "Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun",]
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
        #classtrainer.append(obj[0].tname)
    personcount = []

    for objP in Person.objects.filter(role='student'):
        counter = 0
        for item in classesname:
            if not objP.is_superuser :
                print("******",objP.id)
               # if item in objP.classname.cname:
                #    counter += 1
        personcount.append(counter)

    row_data = []
    a_row = {}
    for i in range(len(classesname)):
        a_row['classesname'] = classesname[i]
        #a_row['classtrainer'] = classtrainer[i]
        a_row['classesstarttime'] = classesstarttime[i]
        row_data.append(a_row)
        a_row = {}
    context['row_data'] = row_data
'''
    html_template = loader.get_template('home/todayclasslist.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def debt(request):
    context = {'segment': 'index'}
    context['jdate'] = date_maker()
    person = Person.objects.all()
    context['person'] = person
    html_template = loader.get_template('home/debt.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def analyzereport(request):
    context = {'segment': 'index'}
    context['jdate'] = date_maker()

    analyze = Analysis.objects.all()
    context['analyze'] = analyze
    html_template = loader.get_template('home/analyzereport.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def classlist(request, ccname):
    monthname = {"فروردین": "01",  "اردیبهشت": "02",  "خرداد": "03",  "تیر": "04",  "مرداد": "05",
                 "شهریور": "06",  "مهر": "07",  "آبان": "08",  "آذر": "09",  "دی": "10", "بهمن": "11",  "اسفند": "12"}

    studentList = []
    students=[]
    AttendanceFormSet = formset_factory(AttendanceForm, extra=0)
    for obj in Person.objects.filter(role='student'):
        if not obj.is_admin:
            if obj.classname != None and obj.classname.cname == ccname:
                students.append(obj)
    formset = AttendanceFormSet(request.POST or None, initial=[
                                {'name': student.full_name} for student in students])
    if request.method == 'POST':
        cname_obj = Classi.objects.get(cname=ccname)
        
        inDate=request.POST.get("date").split(",")
        print(inDate)
        di=int(inDate[0])
        mi = int(monthname[inDate[1]])
        yi=int(inDate[2])
        datePost=jdatetime.date(yi,mi,di).togregorian().strftime("%Y-%m-%d")
        print("*****",datePost)
        for student, attendance in request.POST.items():
            #person_id = request.POST[item].split("_")[-1]
            if student.isdigit():
                person = Person.objects.get(id=student)
                if attendance == 'present':
                    SessionDate.objects.create(
                        session_person=person, dos=datePost, classname=cname_obj)
                    studentList.append(person)
                elif attendance == 'absent':
                    AbsenceDate.objects.create(
                        absent_person=person, doa=datePost, classname=cname_obj)
                    studentList = []
        trainer = Person.objects.get(
            id=request.POST.get("trainer_select"))
        sessionObj = SessionDate.objects.create(
        session_person=trainer, dos=jdatetime.datetime.now(), classname=cname_obj)
        for item in studentList:
            sessionObj.sstudent.add(item)
        sessionObj.save()
        return HttpResponseRedirect(f'/classlist/{ccname}')
    
            
    context = {'segment': 'classlist'}
    person = []
    context['person'] = person
    context['cname'] = ccname
    trainers=[]
    for obj in Person.objects.filter(role='trainer'):
        trainers.append(obj)
    context['trainers']=trainers
    context['jdate'] = date_maker()
    context['formset'] = formset
    context['students'] = students

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

        context = {'segment': 'personalreport'}

        context['person'] = person
        context['imglen'] = len(person.simage.name)

        context['buttonShow'] = True if request.user.is_superuser else False
        
        session = SessionDate.objects.filter(session_person=person_id)
        context['session'] = session

        absence = AbsenceDate.objects.filter(absent_person=person_id)
        context['absence'] = absence

        peyment = Peyment.objects.filter(peyment_person=person_id)
        context['peyment'] = peyment
        
        analysis=Analysis.objects.filter(analysis_person=person_id)       
        context["analysis"] = analysis
        try:
            classiname=Classi.objects.get(cname=person.classname)
            context['trainer_id'] = Person.objects.get(
                full_name=classiname.ctrainer).id
        except:
            print("*******^^^^^^^^^***********")
            pass
        weight=[]
        bfm=[]
        smm=[]
        
        for ana in analysis:
            weight.append({"label": ana.dot.strftime("%Y-%m-%d"), "y": ana.current_state_weight})
            bfm.append({"label": ana.dot.strftime(
                "%Y-%m-%d"), "y": ana.current_state_bfm})
            smm.append({"label": ana.dot.strftime(
                "%Y-%m-%d"), "y": ana.current_state_bfm})
        
        context.update({"weight": weight, "bfm": bfm,
                       "smm": smm, })
###############################
        context['jdate'] = date_maker()

        html_template = loader.get_template('home/personalreport.html')
        return HttpResponse(html_template.render(context, request))
    else:
        context = {}
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def trainerreport(request, trainer_id):
        count=0
        trainer = Person.objects.get(id=trainer_id)
        trainerseesion = SessionDate.objects.filter(session_person=trainer_id)
        mont=(str(jdatetime.datetime.now()).split("-")[1])     
        sumi=0
        
        for item in trainerseesion:
            discounts = 0
            if f"-{mont}-" in str(item.dos):
                count+=1
            for i in item.sstudent.all():
                discounts+=i.discount
            sumi+=(item.classname.fee/12*len(item.sstudent.all()) -
                  discounts*(item.classname.fee/12)/100)
        print(sumi/2)
        context = {'segment': 'trainerreport'}
        context['trainer'] = trainer
        context['trainerseesion'] = trainerseesion
        context['mont']=mont
        context['count']=count
        context['sumOfMounth']=sumi/2
        context['superuserview'] = True if request.user.is_superuser or request.user.role=="trainer" else False
        context['jdate'] = date_maker()

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
        "bg-yellow",
        "bg-aqua",
        #"bg-silver",
        #"bg-light-blue",
        #"bg-light-green",
        #"bg-navy",
        "bg-teal",
        "bg-olive",
        "bg-lime",
        "bg-orange",
        "bg-fuchsia",
        ]
        
        trainers = Person.objects.filter(role="trainer")
        context = {'segment': 'trainerslist'}
        context['trainers'] = trainers
        context['colorbg'] = colorbg
        context['1'] = "bg-red"
        context['2'] = "bg-yellow"
        context['3'] = "bg-aqua"
        context['4'] = "bg-green"
        context['jdate'] = date_maker()
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
