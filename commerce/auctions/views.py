from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .helpers import create_item
from django import forms
from .models import *
from django.db.models import Max




class new_listing_form(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea, required=False)
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'money-input'}))
    image_file = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'image-input'}))
    image_url = forms.CharField(label="Image URL")
    category = forms.ChoiceField(choices=(("Fashion","Fashion"), ("Toys","Toys"), ("Electronics","Electronics"), ("Home","Home"), ("Other","Other")), widget=forms.Select)
    
    
 
def index(request):
    return render(request, "auctions/index.html", 
    {"active_listing": Item.objects.all()})

def listing(request, item_id):
     file = Item.objects.get(pk=item_id)
     try:
        Bid.objects.get(item=item_id,is_winning = True)
        current_bid = Bid.objects.get(item=item_id,is_winning = True)
     except Bid.DoesNotExist:
        current_bid = None
     return render(request, "auctions/listings.html", 
    {"item": file,
    "current_bid": current_bid,
    "seller": request.user == file.seller, 
    "bid_closed": file.closed}) #assign a boolean value to seller indicating whether the current user is the seller of the file object.


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



def add_to_watchlist(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        try:
            WatchList.objects.get(user = request.user, item = item_id)
            return render(request,"auctions/listings.html", {"message": "Already added to watchlist", "item": Item.objects.get(pk=item_id)})
        except WatchList.DoesNotExist:
            WatchList.add_watchlist(request.user, item_id)
            watchlist_obj = WatchList.objects.get(user=request.user)
        return render(request, "auctions/watchlist.html", {"list": watchlist_obj.item.all()})


def watchlist(request):
    try:
        watchlist_obj = WatchList.objects.get(user=request.user)
        return render(request, "auctions/watchlist.html", {"list": watchlist_obj.item.all()})
    except WatchList.DoesNotExist:
        return render(request, "auctions/watchlist.html", {"message": "You haven't added any items yet."})



def remove_watchlist(request):
     if request.method == "POST":
        item = request.POST["item_id"]
        watchlist = WatchList.objects.get(user=request.user)
        watchlist.item.remove(item)
        return redirect("watchlist")

def bid(request):
    if request.method == "POST":
        bid_item = request.POST["item_id"]
        starting_price = request.POST["starting_price"]
        amount = request.POST["bid_amount"]
        seller_name = Item.objects.get(pk=bid_item)
        starting_price = request.POST["starting_price"]
        try:
           Bid.objects.filter(item=bid_item)
           current_bid = Bid.objects.get(item=bid_item,is_winning = True)
           highest_bid = Bid.objects.filter(item=bid_item).aggregate(Max('amount'))
           latest_bid = Bid.objects.filter(item=bid_item).latest('amount')
           if highest_bid['amount__max'] is None or highest_bid['amount__max'] <= float(amount) and float(amount) > float(starting_price):
            Bid.change_winning(bid_item)
            is_winning = True
            Bid.make_bid(request.user, Item.objects.get(pk=bid_item), amount, is_winning)
            current_bid = Bid.objects.get(item=bid_item,is_winning = True)
            return render(request, "auctions/listings.html", 
            {"item": seller_name,
            "current_bid": current_bid,
             "seller": request.user == seller_name.seller,
            "bid_closed": seller_name.closed,
            "message_2": "You have made a Bid!"})
           else:
            return render(request, "auctions/listings.html", 
            {"item": seller_name,
            "current_bid": current_bid,
             "seller": request.user == seller_name.seller,
            "bid_closed": seller_name.closed,
            "message": "Your Current bid is to low"})
        except Bid.DoesNotExist:
            item = Item.objects.get(pk=bid_item)
            is_winning = True
            Bid.make_bid(request.user, item, amount, is_winning)
            return render(request, "auctions/listings.html", 
            {"item": seller_name,
            "current_bid": amount,
           "seller": request.user == seller_name.seller,
            "bid_closed": seller_name.closed,
            "message_2": "You have made a Bid!"})

def close_bid(request):
    if request.method == "POST":
        item = request.POST["close_auction"]
        seller_name = Item.objects.get(pk=item)
        Item.close_item(item)
        return render(request, "auctions/listings.html", 
            {"item": seller_name,
            "current_bid": Bid.objects.get(item=item,is_winning = True),
            "seller": request.user == seller_name.seller,
            "bid_closed": seller_name.closed,
            "message_2": "Bid has been closed"})
        


      
    


