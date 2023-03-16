from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def load_posts(request, load):
    if load == "userprofile":
        all_posts = Posts.objects.filter(user=request.user).order_by("-timestamp").all()
    elif load.isalpha() and load != "allposts":
        all_posts = Posts.objects.filter(user = User.objects.get(username=load)).order_by("-timestamp").all()
    else:
        all_posts = Posts.objects.all().order_by("-timestamp").all()

    data = {
        'posts': [post.serialize() for post in all_posts],
        'count': User.count_followers_and_following(request.user)
    }
    return JsonResponse(data, safe=False)
    
@login_required
def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Posts.add_post(data.get("comment"), request.user)
        return load_posts("userprofile")


@login_required
def like_post(request, post_id):
    if request.method == "PUT":
        return JsonResponse(Posts.like_post(post_id, request.user), safe=False)
        
            
