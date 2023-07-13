from django.shortcuts import render
import re
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


class AddNewEntry(forms.Form):
    newEntryTitle = forms.CharField(label="Title")
    newEntryContent = forms.CharField(label="Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def searchResult(request):

    #get the value of the search input query
    q = request.GET.get('q')

    #call the util function on the value of d input query and store in variable x
    x = util.get_entry(q)

    if x == None:
            entries = util.list_entries()
            matches = []

            print(f'{q}')

            for entry in entries:
                if re.search(rf'{q}',entry, re.IGNORECASE):
                    print(entry)
                    matches.append(entry)

            return render(request, "encyclopedia/index.html", {
                "entries": matches
            })

    else:
        return render(request, "encyclopedia/content.html", {
            "singleResult":util.get_entry(q),
            "title": q
        })


def showPage(request, title):
    # request.session['title'] = title
    x = util.get_entry(title)

    if x == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/content.html", {
            "singleResult":util.get_entry(title),
            "title": title
        })
    

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
                    "singleResult":util.get_entry(title),
                    "title": title
                })
        else:
            return render(request, "encyclopedia/addnew.html", {
                "form": form
            })
        
    return render(request, "encyclopedia/addnew.html", {
        "form": AddNewEntry
    })


def edit(request, title):
    # title = request.session.get('title')
    # singleResult = util.get_entry(title)

    # form = AddNewEntry({'newEntryTitle': title, 'newEntryContent': singleResult})

    # return render(request, "encyclopedia/edit.html", {
    #     "form": form
    
    entryForEdit = util.get_entry(title)

    title = "Python"
    singleResult = "page content"

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "singleResult": singleResult
    })


def saveEdit(request):


    if request.method == "POST":
        content = request.POST.get('content')
        title = request.POST.get('title')

        util.save_entry(title, content)
        return render(request, "encyclopedia/content.html", {
            "singleResult":util.get_entry(title),
            "title": title
        })
    
    
