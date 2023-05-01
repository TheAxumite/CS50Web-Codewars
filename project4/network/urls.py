
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("load_posts/<str:load>", views.load_posts, name="load_posts"),
    path("create_post", views.create_post, name="create_post"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("load_page/<str:load>", views.load_page, name="load_page"),
    path("submit", views.edit_post, name="submit")
    
    

]
