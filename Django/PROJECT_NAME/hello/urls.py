from django.urls import path
from . import views


urlpatterns = [
    # views.index runs the index function in the views.py module
    # name is optional to give the path a name
    # "" is a default path route
    path("", views.index, name="index"),
    path("brian", views.brian, name="brian"),
    path("david", views.david, name="david"),
    path("<str:name>", views.greet, name="greet")
]