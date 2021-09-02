from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("index.html", views.index, name="index"),
    path("wiki/<str:entry_name>", views.display_entry, name="display_entry"),
    path("search/", views.search, name="search"),
    path("create_page/", views.create_page, name="create_page"),
    path("edit_page/", views.edit_page, name="edit_page"),
    path("random_page/", views.random_page, name="random_page")
]
