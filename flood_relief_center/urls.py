from django.contrib import admin
from django.urls import path
from . import views

app_name= "flood_relief_center"
urlpatterns = [
    path("", views.index, name="index"),
    path("relief-centers/", views.ReliefCentersListView.as_view(), name="relief-centers"),
]
