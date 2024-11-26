from django.contrib import admin
from django.urls import path
from . import views

app_name = "flood-relief-center"
urlpatterns = [
    path("", views.index, name="index"),

    path("donations/", views.DonationListView.as_view(), name="donations"),
    path("add-donation/", views.add_donation, name="add-donation"),
    path("edit-donation/<int:donationID>/", views.edit_donation, name="edit-donation"),
    path("delete-donation/<int:donationID>/", views.delete_donation, name="delete-donation"),

    path("relief-centers/", views.ReliefCentersListView.as_view(), name="relief-centers"),
    path("relief-centers/<int:centerID>/", views.ReliefCenterDetailView.as_view(), name="relief-center-detail"),
    path("add-relief-center/", views.add_relief_center, name="add-relief-center"),
    path("edit-relief-center/<int:centerID>/", views.edit_relief_center, name="edit-relief-center"),
    path("delete-relief-center/<int:centerID>/", views.delete_relief_center, name="delete-relief-center"),

    path("victims/", views.VictimsListView.as_view(), name="victims"),
    path("edit-victim/<int:victimID>/", views.edit_victim, name="edit-victim"),
    path("add-victim", views.add_victim, name="add-victim"),
    path("delete-victim/<int:victimID>/", views.delete_victim, name="delete-victim"),
    path("stats-victims/", views.StatsVictim.as_view(), name="stats-victims"),

    path("volunteers/<int:centerID>/", views.VolunteersListView.as_view(), name="volunteers"),
    path("edit-volunteer/<int:volunteerID>/", views.edit_volunteer, name="edit-volunteer"),
    path("add-volunteer/<int:centerID>", views.add_volunteer, name="add-volunteer"),
    path("delete-volunteer/<int:volunteerID>/", views.delete_volunteer, name="delete-volunteer"),

    path("affected-areas/", views.AffectedAreaListView.as_view(), name="affected-areas"),
    path("add-affected-area/", views.add_affected_area, name="add-affected-area"),
    path("edit-affected-area/<int:areaID>/", views.edit_affected_area, name="edit-affected-area"),
    path("delete-affected-area/<int:areaID>/", views.delete_affected_area, name="delete-affected-area"),

    
    path("rescue-teams/<int:centerID>/", views.RescueTeamsListView.as_view(), name="rescue-teams"),
    path("add-rescue_team/",views.add_rescue_team, name="add-rescue-teams" )

]

