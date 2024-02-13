# -*- encoding: utf-8 -*-


from django.urls import path, re_path
from .models import Person
from apps.home import views
from django.conf.urls.static import static
from django.conf import settings
from dal import autocomplete
from django.urls import re_path as url




urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('debt/', views.debt, name='debt'),
    path('personalreport/<int:person_id>',
         views.personalreport, name='personalreport'),
    #path('peymentreport/<int:person_id>',
    #     views.peymentreport, name='peymentreport'),
    #path('sessionreport/<int:person_id>',
    #     views.sessionreport, name='sessionreport'),
    #path('absencereport/<int:person_id>',
    #     views.absencereport, name='absencereport'),
    path('classlist/<str:ccname>', views.classlist, name='classlist'),
    path('tables/', views.tables, name='tables'),

    url(
        r'^autocomplete/$',
        views.PersonAutocomplete.as_view(model=Person),
        name='select2_fk',
    ),
    # re_path(r'^.*\.*', views.pages, name='pages'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
