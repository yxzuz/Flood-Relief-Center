from django.shortcuts import render
from django.views.generic import ListView
from .models import ReliefCenter, Donation, Victim

# Create your views here.


def index(request):
    return render(request, "flood_relief_center/index.html")


class ReliefCentersListView(ListView):
    model = ReliefCenter
    context_object_name = "relief_centers_lists"
    template_name = "flood_relief_center/relief_centers.html"
    
    
class DonationListView(ListView):
    model = Donation
    context_object_name = "donation_lists"
    template_name = "flood_relief_center/donations.html"
    

class VictimsListView(ListView):
    model = Victim
    context_object_name = "victim_lists"
    template_name = "flood_relief_center/victims.html"
    
    
class ReliefCenterDetailView(ListView):
    model = ReliefCenter
    context_object_name = "relief_center_detail"
    template_name = "flood_relief_center/relief_center_detail.html"
    
    def get_queryset(self):
        return ReliefCenter.objects.filter(centerID=self.kwargs.get('centerID'))  # Filter by centerID