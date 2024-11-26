from django.shortcuts import render, redirect

from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q
from .models import ReliefCenter, Donation, Victim, AffectedArea, Volunteer, RescueTeam
from .forms import VolunteerForm

# Create your views here.
CENTER = [center.name for center in ReliefCenter.objects.all()]
STATUS = [('safe', 'Safe'), ('injured', 'Injured'), ('missing', 'Missing')]
RISK_LEVEL = [(1, 'Low'), (2, 'Moderate'), (3, 'High'),
              (4, 'Critical'), (5, 'Severe')]
POSITION = [('staff', 'Staff'), ('volunteer', 'Volunteer')]
AVALIABILITY_STATUS = ['available', 'unavailable']


def index(request):
    return render(request, "flood_relief_center/index.html")


def get_team_name():
    return [team.teamName for team in RescueTeam.objects.all()]


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["centers"] = CENTER
        context["current_status"] = STATUS
        context["risk_level"] = RISK_LEVEL
        return context

    def get_search_query(self, queryset, search_query):
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(victimNumber__icontains=search_query) | Q(address__icontains=search_query) | Q(
                center__name__icontains=search_query) | Q(riskLevel__icontains=search_query) | Q(currentStatus__icontains=search_query))
        return queryset

    def get_queryset(self):
        queryset = Victim.objects.all()

        # Get the query parameters from the request
        search_query = self.request.GET.get("search_query", "")
        selected_center = self.request.GET.get("selected_center", "")
        selected_status = self.request.GET.get("selected_status", "")
        selected_risk_level = self.request.GET.get("selected_risk_level", "")
        ordered_by = self.request.GET.get("orderparam", "name")
        # age_range = self.request.GET.get("age_range", None)

        # Apply search filter
        if search_query:
            queryset = self.get_search_query(queryset, search_query)

        # Apply center filter
        if selected_center:
            queryset = queryset.filter(center__name=selected_center)

        # Apply status filter
        if selected_status:
            queryset = queryset.filter(currentStatus=selected_status)

        # Apply risk level filter
        if selected_risk_level:
            queryset = queryset.filter(riskLevel=selected_risk_level)

        # Apply age range filter (if provided)
        # if age_range:
        #     queryset = queryset.filter(age__lte=age_range)
        print(ordered_by)
        return queryset.order_by(ordered_by)


class AffectedAreaListView(ListView):
    model = AffectedArea
    context_object_name = "affected_area_lists"
    template_name = "flood_relief_center/affected_areas.html"


class ReliefCenterDetailView(ListView):
    model = ReliefCenter
    context_object_name = "relief_center_detail"
    template_name = "flood_relief_center/relief_center_detail.html"

    def get_queryset(self):
        # Filter by centerID
        return ReliefCenter.objects.filter(centerID=self.kwargs.get('centerID'))


class VolunteersListView(ListView):
    model = Volunteer
    context_object_name = "volunteer_list"
    template_name = "flood_relief_center/volunteers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["centers"] = CENTER
        context["position"] = POSITION
        context["avaliability_status"] = AVALIABILITY_STATUS
        context["teams"] = get_team_name()
        return context

    def get_search_query(self, queryset, search_query):
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(position__icontains=search_query)  | Q(team__teamName__icontains=search_query))
        return queryset

    def get_queryset(self):

        # Get the query parameters from the request
        # fixed_center_id = self.kwargs.get("centerID")
        search_query = self.request.GET.get("search_query", "")
        selected_position = self.request.GET.get("selected_position", "")
        selected_avaliability_status = self.request.GET.get(
            "selected_availability_status", "")
        selected_team_name = self.request.GET.get("selected_team_name", "")
        ordered_by = self.request.GET.get("orderparam", "name")
        # age_range = self.request.GET.get("age_range", None)

        print("searchq", search_query)
        print("elect", selected_position)
        print("ava", selected_avaliability_status)
        print("team", selected_team_name)
        queryset = (Volunteer.objects.all())

        # Apply search filter
        if search_query:
            queryset = self.get_search_query(queryset, search_query)

        # Apply position filter
        if selected_position:
            queryset = queryset.filter(position=selected_position)

        # Apply avaliability status filter
        if selected_avaliability_status:
            queryset = queryset.filter(
                availabilityStatus=selected_avaliability_status)

        # Apply team id status filter
        if selected_team_name:
            queryset = queryset.filter(team__teamName=selected_team_name)

        print(queryset)
        return queryset.order_by(ordered_by)


def add_volunteer(request):
    form = VolunteerForm()
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:volunteers"))
    context = {"form": form}
    return render(request, "flood_relief_center/add_volunteer.html", context)
