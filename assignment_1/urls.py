from django.conf.urls import patterns, include, url
from django.contrib import admin
from notes import views

from django.views.generic import ListView, DetailView
from notes.models import Note, Folder, Tag

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Note), name="listall"),
    url(r'^tag/(?P<tags>.*)$', views.notes_tags, name='notes_list'),
    url(r'^note/(?P<pk>\d+)$', views.note, name='detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^listall/$', ListView.as_view(model=Note), name="listall"),
    url(r'^list/(?P<folder>.*)$', views.NoteList.as_view(), name='notes_list'),
    url(r'^note/(?P<pk>\d+)/edit/$', views.NoteUpdate.as_view(),  name='note_update'),
    url(r'^add/$', views.NoteCreate.as_view(), name='note_add'),
    url(r'^note/(?P<pk>\d+)/delete/$', views.NoteDelete.as_view(),  name='note_delete'),

)
