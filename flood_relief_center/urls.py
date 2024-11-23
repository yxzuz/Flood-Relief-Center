from django.contrib import admin
from django.urls import path
from . import views

app_name= "flood-relief-center"
urlpatterns = [
    path("", views.index, name="index"),
    path("relief-centers/", views.ReliefCentersListView.as_view(), name="relief-centers"),
    path("donations/", views.DonationListView.as_view(), name="donations"),
    path("add-donation/", views.add_donation, name="add-donation"),
    path("edit-donation/<int:donationID>/", views.edit_donation, name="edit-donation"),
    path("delete-donation/<int:donationID>/", views.delete_donation, name="delete-donation"),
    
    path("relief-centers/<int:centerID>/", views.ReliefCenterDetailView.as_view(), name="relief-center-detail"),
    
    path("victims/", views.VictimsListView.as_view(), name="victims"),
    path("edit-victim/<int:victimID>/", views.edit_victim, name="edit-victim"),
    path("add-victim", views.add_victim, name="add-victim"),
    path("delete-victim/<int:victimID>/", views.delete_victim, name="delete-victim"),
    path("stats-victims/", views.StatsVictim.as_view(), name="stats-victims"),

    
    
    path("affected-areas/", views.AffectedAreaListView.as_view(), name="affected-areas"),
    
]
