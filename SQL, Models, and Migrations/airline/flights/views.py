from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, "index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = Flight.objects.get(pk=flight_id) ## Or it can written as (id = flightid) instead
    print(flight)
    return render(request, "flight.html", {
            "flight": flight,
            "passengers": flight.passengers.all(),
            "non_passengers": Passenger.objects.exclude(flights=flight).all()
            
        })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id) #Object is a db table Flight containing the flight based on the flight id  submitted by user
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"])) # Object contains the passenger retrieved from the Passenger data base
        passenger.flights.add(flight) #Passenger is added to the flight since flights column is a manytomany relationship with the flights database
        return HttpResponseRedirect(reverse("flight", args=(flight.id, )))