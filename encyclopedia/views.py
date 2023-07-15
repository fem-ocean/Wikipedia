from django.shortcuts import render
import re
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from . import util
from . import markdown2


class AddNewEntry(forms.Form):
    newEntryTitle = forms.CharField(label="Title")
    newEntryContent = forms.CharField(label="Content", widget=forms.Textarea)


#index page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


#Search bar
def searchResult(request):

    #get the value of the search input query
    q = request.GET.get('q')

    #call the util function on the value of d input query and store in variable x
    x = util.get_entry(q)

    #Show entries that dont exactly match but similar to the searched entry
    if x == None:
            entries = util.list_entries()
            matches = []

            for entry in entries:
                if re.search(rf'{q}',entry, re.IGNORECASE):
                    matches.append(entry)

            return render(request, "encyclopedia/index.html", {
                "entries": matches
            })

    else:
        return render(request, "encyclopedia/content.html", {
            "singleResult":markdown2.markdown(util.get_entry(q)),
            "title": q
        })


#Show content of entry. If none is found, show an error page.
def showPage(request, title):
    x = util.get_entry(title)

    if x == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/content.html", {
            "singleResult":markdown2.markdown(util.get_entry(title)),
            "title": title
        })
    

#Add new page. If entry already exist, show an error
def addNew(request):
    if request.method == "POST":
        form = AddNewEntry(request.POST)

        if form.is_valid():
            title = form.cleaned_data["newEntryTitle"]
            content = form.cleaned_data["newEntryContent"]
            if title in util.list_entries():
                return render(request, "encyclopedia/duplicatepage.html")
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/content.html", {
                    "singleResult":markdown2.markdown(util.get_entry(title)),
                    "title": title
                })
        else:
            return render(request, "encyclopedia/addnew.html", {
                "form": form
            })
        
    return render(request, "encyclopedia/addnew.html", {
        "form": AddNewEntry
    })


#Edit the content of an entry
def edit(request, title):
    entryForEdit = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "singleResult": entryForEdit
    })


#Function to save the edited entry and render
def saveEdit(request):
    if request.method == "POST":
        content = request.POST.get('content')
        title = request.POST.get('title')

        util.save_entry(title, content)
        return render(request, "encyclopedia/content.html", {
            "singleResult":markdown2.markdown(util.get_entry(title)),
            "title": title
        })


#Random function for displaying an entry    
def findRandom(request):
    allEntries = util.list_entries()
    print(allEntries)
    randomEntry = random.choice(allEntries)
    content = markdown2.markdown(util.get_entry(randomEntry))

    return render(request, "encyclopedia/content.html", {
        "singleResult": content,
        "title": randomEntry
    })
    
    