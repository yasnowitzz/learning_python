from django.contrib import admin
from django.urls import path, re_path, include
from AppTwo import views


app_name = "AppTwo"

urlpatterns = [
    re_path("^$", views.help, name="help"),
    re_path("^register/", views.register, name="register"),
]