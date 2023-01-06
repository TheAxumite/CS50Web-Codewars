import string
from django.shortcuts import render
from . import util
from django import forms


def index(request):
    new = []
    for link in util.list_entries():
         new.append('<a href = "/wiki/' + link + '" </a>' + link)
    return render(request, "encyclopedia/index.html", {
        "entries": new
        })
  

def conversion(request, name):
    return render(request, "encyclopedia/Entrypage.html", {"message":util.convert(name)
    })


    
def search(request):
     if request.method == "POST":
        form = request.POST.get("q")
        if util.get_entry(form):
            return render(request, "encyclopedia/Entrypage.html", {"message":util.convert(form) })
        else:
            new = []
            for link in util.list_entries():
                count = 0
                for l in range(len(form)): 
                    if form[l] in link:
                        count += 1         
                if (count/len(link) * 100) > 49:
                    new.append('<a href = "/wiki/' + link + '" </a>' + link)  
            return render(request, "encyclopedia/index.html", {
                "entries": new
                })
  
           
def newpage(request):
        if request.method == "POST":
            form = request.POST.get("q")
            title = request.POST.get("title")
            print(form)
            util.save_entry(title, form)
            return render(request, "encyclopedia/Entrypage.html", {"message":util.convert(title)})
        else:
            return render(request, "encyclopedia/newpage.html")

        

       

       


   
