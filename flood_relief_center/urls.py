from django.contrib import admin
from django.urls import path
from . import views

app_name= "flood-relief-center"
urlpatterns = [
    path("", views.index, name="index"),
    path("relief-centers/", views.ReliefCentersListView.as_view(), name="relief-centers"),
    path("donations/", views.DonationListView.as_view(), name="donations"),
    path("relief-centers/<int:centerID>/", views.ReliefCenterDetailView.as_view(), name="relief-center-detail"),
    path("victims/", views.VictimsListView.as_view(), name="victims"),
    path("edit-victim/<int:victimID>/", views.edit_victim, name="edit-victim"),
    path("add-victim", views.add_victim, name="add-victim"),
    path("affected-areas/", views.AffectedAreaListView.as_view(), name="affected-areas"),
]
