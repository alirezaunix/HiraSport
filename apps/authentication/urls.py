# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user,logout_view,change_password,change_password_done
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    #path("logout_view/", logout_view, name="logout"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/", change_password, name="change_password"),
    path("change_password_done/", change_password_done, name="change_password_done"),

]
