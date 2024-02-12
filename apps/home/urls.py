# -*- encoding: utf-8 -*-


from django.urls import path, re_path
from apps.home import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('debt/', views.debt, name='debt'),
    path('personalreport/<int:person_id>',
         views.personalreport, name='personalreport'),
    path('peymentreport/<int:person_id>',
         views.peymentreport, name='peymentreport'),
    path('sessionreport/<int:person_id>',
         views.sessionreport, name='sessionreport'),
    path('absencereport/<int:person_id>',
         views.absencereport, name='absencereport'),
    path('classlist/<str:ccname>', views.classlist, name='classlist'),
    path('tables/', views.tables, name='tables'),

    # re_path(r'^.*\.*', views.pages, name='pages'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
