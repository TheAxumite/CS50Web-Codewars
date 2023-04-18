from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
    print("print" + load)
    if load.isalpha() and load != "allposts":

        data = {
            'data': [post.serialize(request.user) for post in Posts.objects.filter(
                user=User.objects.get(username=load)).order_by("-timestamp")[:10]],
            'count': User.count_followers_and_following(load),
            'requester': {'current_profile': str(load)},
            'pages_left': Paginator(Posts.objects.filter(user=User.objects.get(username=load)).order_by("-timestamp"), 10).num_pages}
        return JsonResponse(data, safe=False)
    else:
        data = {
            'data': [Posts.objects.filter(user=request.user).order_by("-timestamp")[:10] if load == 'userprofile' else post.serialize(request.user) for post in Posts.objects.all().order_by("-timestamp")[:10]],
            'count': User.count_followers_and_following(request.user),
            'requester': {'current_profile': str(load)},
            'pages_left': Paginator(Posts.objects.all().order_by("-timestamp"), 10).num_pages}
        return JsonResponse(data, safe=False)


@login_required
def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Posts.add_post(data.get("comment"), request.user)
        load = "userprofile"
        return load_posts(request, load)


@login_required
def like_post(request, post_id):
    if request.method == "PUT":
        return JsonResponse(Posts.like_post(post_id, request.user), safe=False)


@login_required
def follow(request, username):

    if request.method == "PUT":
        return JsonResponse(User.follow_unfollow(username, request.user), safe=False)


@login_required
def load_page(request, load):
    load_dict = json.loads(load)
    if load_dict['profile'] == 'All Posts':
        profile = request.user
        paginator = Paginator(Posts.objects.all().order_by("-timestamp"), 10)
    else:
        profile = load_dict['profile']

        paginator = Paginator(Posts.objects.filter(
            user=User.objects.get(username=profile)).order_by("-timestamp"), 10)
        print(int(paginator.num_pages) - (load_dict['page']))
    return JsonResponse({'data': [post.serialize(request.user) for post in paginator.page(load_dict['page']).object_list],
                        'pages_left': int(paginator.num_pages) - (load_dict['page']),
                        'username': str(profile)}, safe=False)

@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        Posts.edit_post(post_id, request.user)
        return JsonResponse(Posts.objects.get(pk=post_id))