import random

from django.http import HttpResponse
from django import forms
from django.shortcuts import render

from . import util

from markdown2 import Markdown

markdowner = Markdown()


class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Title'}))
class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')



def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
           
            return entry(request, item)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
        })


def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page) 

        context = {
            'page': page_converted,
            'title': title,
            'form': Search()
        }

        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"message": "The requested page was not found.", "form":Search()})



def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        
        context = {
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", context)
    else:
     form=Edit(request.POST)
     if form.is_valid():

        text=form.cleaned_data["textarea"]
        util.save_entry(title,text)
        return entry(request,title) 


def creat(request):
    if request.method=="GET":
        return render(request,"encyclopedia/creat.html",{
            "textarea":Post()
        })
    else :
        entries=util.list_entries()
        form=Post(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["textarea"]
            if title in entries:
                return render(request, "encyclopedia/error.html", {"message": "The Title is already Exist", "form":Search()})
            else :
                util.save_entry(title,content)    
                return entry(request,title)


            


