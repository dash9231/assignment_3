import re
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from notes.models import Note, Folder, Tag
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from notes.forms import NoteForm
from django.views.generic import DetailView, ListView

def notes_list(request, folder):
    if folder == "":
        allnotes = Note.objects.all().order_by("folder__title")
        total = allnotes.count()
    else:
        allnotes = Note.objects.filter(folder__title__iexact=folder)
        total = allnotes.count();
    return render(request, 'notes/index.html', {'notes': allnotes, 'total':total})

def note(request, pk):
    note = Note.objects.get(id=pk)
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

class NoteList(ListView):
    #https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/
    model = Note
    
    def get_queryset(self):
        folder = self.kwargs['folder']
        if folder == '':
            return Note.objects.all()
        else:
            return Note.objects.filter(folder__title__iexact=folder)

class NoteCreate(CreateView):
    model = Note
    form_class = NoteForm
    
class NoteUpdate(UpdateView):
    model = Note
    form_class = NoteForm

class NoteDetail(DetailView):
    model = Note

class NoteDelete(DeleteView):
    model = Note
    success_url = reverse_lazy('listall')