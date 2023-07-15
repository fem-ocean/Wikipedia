from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.showPage, name="showPage" ),
    path("search/", views.searchResult, name="searchResult"),
    path("addNew/", views.addNew, name="addNew"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("saveEdit/", views.saveEdit, name="saveEdit"),
    path("random/", views.findRandom, name="findRandom")
]
