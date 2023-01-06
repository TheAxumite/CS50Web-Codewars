import string
import re

from . import util

converter_dict = {
    '**': '<b>', 
    '/n': '<br>',
    '#': ['<h5>','</h5>']}

def index(request):
    html = []
    print(html)
    converted = ''
    page = re.split('[\n]', util.get_entry('CSS'))
    lines = len(page)
     
    for line in page:
        for key, value in converter_dict.items():
            if line:
                if line[0] == key:
                    hold = value[0] + line[1:] + value[1]
                    if re.search(key, line[1:]):
                        hold = hold.replace(key,value)
                    html.append(hold)  
    else:
        html.append(line)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def convert(request):
    if request.method == "POST":
        page = util.get_entry(request.POST)
    else:
        return render(request,"encyclopedia/errorpage.html",
            {"message":request.POST})