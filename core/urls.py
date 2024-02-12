# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.urls import path, include, reverse  # add this
from django.urls import re_path as url
from dal import autocomplete
from apps.home.models import Person
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    # Auth routes - login / register
    path("", include("apps.authentication.urls")),


    url(
        'autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(model=Person),
        name='select2_fk',
    ),
    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls"))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
