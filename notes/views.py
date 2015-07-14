from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .models import Note
import re
from django.db.models import Q

def notes_list(request, folder):
    if folder == "":
        allnotes = Note.objects.all().order_by("folder__title")
        total = allnotes.count()
    else:
        allnotes = Note.objects.filter(folder__title__iexact=folder)
        total = allnotes.count();
    return render(request, 'notes/index.html', {'notes': allnotes, 'total':total})

def note(request, note_id):
    note = Note.objects.get(id=note_id)
    return render(request, 'notes/note.html', {'note':note})
    
    
def notes_tags(request, tags):
    pieces = tags.split('/') #extract different tags separated by /
    # allnotes = Note.objects.none() #required when doing normal filter pipe query ... see below
    #for p in pieces:
        #This is to combine results from different querysets from SAME model using normal pipe
        #https://groups.google.com/forum/#!topic/django-users/0i6KjzeM8OI
        #If the querysets are from different models, have to use itertools
        #http://chriskief.com/2015/01/12/combine-2-django-querysets-from-different-models/
        #allnotes = allnotes | Note.objects.filter(tag__title__iexact=p) # can have duplicates ... need another method
        
    #http://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
    # Turn list of values into list of Q objects
    queries = [Q(tag__title__iexact=value) for value in pieces]
    # Take one Q object from the list
    query = queries.pop()
    # Or the Q object with the ones remaining in the list
    for item in queries:
        query |= item
    print(query)
    # Query the model
    allnotes = Note.objects.filter(query).distinct().order_by('folder__title')
    total = allnotes.count();
    return render(request, 'notes/index.html', {'pieces':pieces, 'notes': allnotes, 'total':total})   