from django.shortcuts import render
from django.views.generic import ListView
from .models import ReliefCenter

# Create your views here.


def index(request):
    return render(request, "flood_relief_center/index.html")


# def show_relief_centers(request):
#     return render(request, "flood_relief_center/relief_centers.html")

class ReliefCentersListView(ListView):
    model = ReliefCenter
    context_object_name = "relief_centers_lists"
    template_name = "flood_relief_center/relief_centers.html"