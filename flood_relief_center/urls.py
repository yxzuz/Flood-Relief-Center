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
    path("affected-areas/", views.AffectedAreaListView.as_view(), name="affected-areas"),
    path('volunteers/', views.VolunteersListView.as_view(), name='volunteers')
]
