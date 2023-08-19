from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from django.db.models import Q


@login_required
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
            request.session['user'] = user
            return render(request, "network/index.html")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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

    if load != "allposts":

        queryset = Posts.objects.filter(user=User.objects.get(
            username=load), originalpost=True).order_by("-timestamp")
    else:
        queryset = Posts.objects.filter(
            originalpost=True).order_by("-timestamp")

    paginator = Paginator(queryset, 10)
    posts = paginator.get_page(1)

    data = {
        'data': [post.serialize(request.user) for post in posts],
        'count': User.count_followers_and_following((load if load.isalpha() and load != 'allposts' else request.user)),
        'isCurrentProfile': (True if load != 'allposts' else False),
        'current_user': str(request.user),
        'pages_left': paginator.num_pages}

    return JsonResponse(data, safe=False)


@login_required
def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Add New Post
        Posts.add_post(data.get("comment"), request.user)

        # Fetch only the required fields and paginate the results
        queryset = Posts.objects.filter(
            originalpost=True).order_by("-timestamp")
        paginator = Paginator(queryset, 10)
        posts = paginator.get_page(1)

        data_return = {
            'data': [post.serialize(request.user) for post in posts],
            'count': User.count_followers_and_following(request.user),
            'isCurrentProfile': True,
            'current_user': str(request.user),
            'pages_left': paginator.num_pages
        }
        return JsonResponse(data_return, safe=False)


@login_required
def like_post(request, post_id):
    if request.method == "PUT":
        return JsonResponse({'Newpost': Posts.like_post(post_id, request.user)}, safe=False)


@login_required
def follow(request, username):
    if request.method == "PUT":
        return JsonResponse(User.follow_unfollow(username, request.user), safe=False)


@login_required
def load_page(request, load):
    load_dict = json.loads(load)

    if load_dict['profile'] == 'All Posts':

        paginator = Paginator(Posts.objects.filter(
            originalpost=True).order_by("-timestamp"), 10)
    else:
        paginator = Paginator(Posts.objects.filter(user=User.objects.get(
            username=load_dict['profile']), originalpost=True).order_by("-timestamp"), 10)
    if load_dict['following']:

        paginator = Paginator(Posts.following_list(
            request.user).order_by("-timestamp"), 10)

    return JsonResponse({'data': [post.serialize(request.user) for post in paginator.page(load_dict['page']).object_list],
                        'pages_left': int(paginator.num_pages) - (load_dict['page']),
                         'following': load_dict['following'],
                         'current_user': str(request.user)}, safe=False)


@login_required
def edit_post(request):
    if request.method == "PUT":
        updated_post = json.loads(request.body)
        return JsonResponse({'update': str(Posts.edit_post(updated_post.get('post_id'), updated_post.get('post')))}, safe=False)


@login_required
def following_post(request):

    paginator = Paginator(Posts.following_list(
        request.user).order_by("-timestamp"), 10)

    data_return = {
        'data': [post.serialize(request.user) for post in paginator.page(1).object_list],
        'count': User.count_followers_and_following(request.user),
        'isCurrentProfile': False,
        'current_user': str(request.user),
        'pages_left': int(paginator.num_pages)}
    return JsonResponse(data_return, safe=False)


@login_required
def post_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse({'ChildCommentData': Posts.addComment(data.get("post"), data.get("post_id"), request.user).serialize(request.user), 'current_user': str(request.user)}, safe=False)


@login_required
def LoadChildComments(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    paginator = Paginator(Posts.LoadChldComments(data.get('id')), 10)
    return JsonResponse({'ChildCommentData': [post.serialize(request.user) for post in paginator.page(int(data.get('page'))).object_list],
                         'NextPage': int(data.get('page')) + 1 if int(data.get('page')) + 1 <= paginator.num_pages else 0,
                         'current_user': str(request.user)}, safe=False)
