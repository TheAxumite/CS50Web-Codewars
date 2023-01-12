from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .helpers import create_item
from django import forms
from .models import *




class new_listing_form(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea, required=False)
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'money-input'}))
    image_file = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'image-input'}))
    image_url = forms.CharField(label="Image URL")
    category = forms.MultipleChoiceField(choices=(("Fashion","Fashion"), ("Toys","Toys"), ("Electronics","Electronics"), ("Home","Home"), ("Other","Other")), widget=forms.SelectMultiple)
    
    

    
def index(request):
    return render(request, "auctions/index.html", 
    {"active_listing": Item.objects.all()})

def listing(request, item_id):
     file = Item.objects.get(pk=item_id)
     print(file.image_file)
     return render(request, "auctions/listings.html", 
    {"item": Item.objects.get(pk=item_id)})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
       
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def post_item(request):
    if request.method == "POST":
        form = new_listing_form(request.POST, request.FILES)
        if form.is_valid():
            Item.create_item(form.cleaned_data['title'], form.cleaned_data['description'],form.cleaned_data['starting_bid'],form.cleaned_data['image_file'], form.cleaned_data['image_url'], form.cleaned_data['category'], request.user)
            return render(request, "auctions/index.html", 
            {"active_listing": Item.objects.all()})  
        else:
           return render(request, "auctions/new_listing.html",
        {"form": new_listing_form()})
    else:
        return render(request, "auctions/new_listing.html",
        {"form": new_listing_form()})
