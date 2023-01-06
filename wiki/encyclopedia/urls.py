from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="second"),
    path("newpage", views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("<str:name>", views.conversion, name="convert"),
    

]
