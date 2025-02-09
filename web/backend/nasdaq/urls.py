from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("topn", views.topN, name="topN"),
]