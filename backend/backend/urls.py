from api import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("callback/", views.callback, name="callback"),
    path("admin/", admin.site.urls),
]
