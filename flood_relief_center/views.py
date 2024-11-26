from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count, Sum, Q, Max, Min
from django.db.models.functions import Lower
from django.views.generic import ListView, DetailView
from .forms import VictimForm, DonationForm, AffectedAreaForm, ReliefCenterForm, ReliefCenterForm, RescueTeamForm, VolunteerForm
from .models import ReliefCenter, Donation, Victim, AffectedArea, NEEDS_CHOICES, Finance, RescueTeam, Member, Volunteer, RescueTeam

# Create your views here.
STATUS = [('safe', 'Safe'), ('injured', 'Injured'), ('missing', 'Missing')]
RISK_LEVEL = [(1, 'Low'), (2, 'Moderate'), (3, 'High'),
              (4, 'Critical'), (5, 'Severe')]

POSITION = [('staff', 'Staff'), ('volunteer', 'Volunteer')]
AVALIABILITY_STATUS = [('available', 'Available'),
                       ('unavailable', 'Unavailable')]

DONATION_TYPE = [('money', 'Money'), ('supplies', 'Supplies'),
                 ('medical', 'Medical'), ('relief', 'Relief')]

DAMAGE_LEVEL = [('minor', 'Minor'), ('moderate',
                                     'Moderate'), ('severe', 'Severe')]
FINANCE_TYPE = [('donation', 'Donation'),
                ('grant', 'Grant'), ('expense', 'Expense')]


def get_center_names():
    return [center.name for center in ReliefCenter.objects.all()]


def get_task_type():
    return [task.taskType for task in RescueTeam.objects.all()]


def index(request):
    return render(request, "flood_relief_center/index.html")


def get_team_name(centerID):
    return [team.teamName for team in RescueTeam.objects.filter(center__centerID=centerID)]


class ReliefCentersListView(ListView):
    model = ReliefCenter
    context_object_name = "relief_centers_lists"
    template_name = "flood_relief_center/relief_centers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("search_query", "")
        return context

    def get_search_query(self, queryset, search_query):
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) |
                                       Q(location__icontains=search_query))
        return queryset

    def get_queryset(self):
        queryset = ReliefCenter.objects.all()

        centerID = self.kwargs.get('centerID')
        search_query = self.request.GET.get("search_query", "")

        # # Apply search filter
        if search_query:
            queryset = self.get_search_query(queryset, search_query)
        return queryset



def edit_relief_center(request, centerID):
    area = ReliefCenter.objects.get(centerID=centerID)
    form = ReliefCenterForm(instance=area)
    if request.method == 'POST':
        form = ReliefCenterForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:relief-centers"))
    context = {"form": form}
    return render(request, "flood_relief_center/edit_relief_center.html", context)


def add_relief_center(request):
    form = ReliefCenterForm()
    if request.method == 'POST':
        form = ReliefCenterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:relief-centers"))
    context = {"form": form}

    return render(request, "flood_relief_center/add_relief_center.html", context)


def delete_relief_center(request, centerID):
    area = ReliefCenter.objects.get(centerID=centerID)
    area.delete()
    return redirect(reverse("flood-relief-center:relief-centers"))


class DonationListView(ListView):
    model = Donation
    context_object_name = "donation_lists"
    template_name = "flood_relief_center/donations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["donation_type"] = DONATION_TYPE
        context["risk_level"] = RISK_LEVEL
        return context

    def get_search_query(self, queryset, search_query):
        if search_query:
            queryset = queryset.filter(Q(donorName__icontains=search_query) | Q(
                donation_type__icontains=search_query))
        return queryset

    def get_queryset(self):
        queryset = Donation.objects.all()

        # Get the query parameters from the request
        search_query = self.request.GET.get("search_query", "")
        selected_donation = self.request.GET.get("selected_donation", "")
        ordered_by = self.request.GET.get("orderparam", "donorName")
        amount_min = self.request.GET.get("min_amount", None)
        amount_max = self.request.GET.get("max_amount", None)

        # # Apply search filter
        if search_query:
            queryset = self.get_search_query(queryset, search_query)

        # # Apply donor name filter
        if selected_donation:
            queryset = queryset.filter(donation_type=selected_donation)

        # # Apply amount range filter (if provided)
        if amount_min:
            queryset = queryset.filter(amount__gte=amount_min)
        if amount_max:
            queryset = queryset.filter(amount__lte=amount_max)

        if ordered_by == "donorName":
            queryset = queryset.annotate(lower_name=Lower(
                "donorName")).order_by("lower_name")
        else:
            queryset = queryset.order_by(ordered_by)

        return queryset


def edit_donation(request, donationID):
    victim = Donation.objects.get(donationID=donationID)
    form = DonationForm(instance=victim)
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=victim)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:donations"))
    context = {"form": form}
    return render(request, "flood_relief_center/edit_donation.html", context)


def delete_donation(request, donationID):
    donation = Donation.objects.get(donationID=donationID)
    donation.delete()
    return redirect(reverse("flood-relief-center:donations"))


def add_donation(request):
    form = DonationForm()
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:donations"))
    context = {"form": form}
    return render(request, "flood_relief_center/add_donation.html", context)


class VictimsListView(ListView):
    model = Victim
    context_object_name = "victim_lists"
    template_name = "flood_relief_center/victims.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["centers"] = get_center_names()
        context["current_status"] = STATUS
        context["risk_level"] = RISK_LEVEL
        return context

    def get_search_query(self, queryset, search_query):
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(victimNumber__icontains=search_query) | Q
                                       (address__icontains=search_query) | Q(
                center__name__icontains=search_query) | Q(riskLevel__icontains=search_query) | Q
                (currentStatus__icontains=search_query))
        return queryset

    def get_queryset(self):
        queryset = Victim.objects.all()

        # Get the query parameters from the request
        search_query = self.request.GET.get("search_query", "")
        selected_center = self.request.GET.get("selected_center", "")
        selected_status = self.request.GET.get("selected_status", "")
        selected_risk_level = self.request.GET.get("selected_risk_level", "")

        ordered_by = self.request.GET.get("orderparam", "name")
        age_range = self.request.GET.get("age", None)

        # checklist
        selected_needs = self.request.GET.getlist("needs")
        if selected_needs:
            queryset = queryset.filter(
                needs__name__in=selected_needs).distinct()

        # Apply search filter
        if search_query:
            queryset = self.get_search_query(queryset, search_query)

        # Apply center filter
        if selected_center:
            queryset = queryset.filter(center__name=selected_center)

        # Apply status filter
        if selected_status:
            queryset = queryset.filter(currentStatus=selected_status)

        # # Apply risk level filter
        if selected_risk_level:
            queryset = queryset.filter(riskLevel=selected_risk_level)

        # # Apply age range filter (if provided)
        if age_range:
            queryset = queryset.filter(age__lte=age_range)
        if ordered_by == "name":
            queryset = queryset.annotate(lower_name=Lower(
                "name")).order_by("lower_name")
        else:
            queryset = queryset.order_by(ordered_by)

        return queryset


def edit_victim(request, victimID):
    victim = Victim.objects.get(victimID=victimID)
    form = VictimForm(instance=victim)
    if request.method == 'POST':
        form = VictimForm(request.POST, instance=victim)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:victims"))
    context = {"form": form}
    return render(request, "flood_relief_center/edit_victim.html", context)


def add_victim(request):
    form = VictimForm()
    if request.method == 'POST':
        # print(request.POST)
        form = VictimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:victims"))
    context = {"form": form}
    return render(request, "flood_relief_center/add_victim.html", context)


def delete_victim(request, victimID):
    victim = Victim.objects.get(victimID=victimID)
    victim.delete()
    return redirect(reverse("flood-relief-center:victims"))


class StatsVictim(ListView):
    model = Victim
    context_object_name = "victim_lists"
    template_name = "flood_relief_center/victim_chart.html"

    def aid_packages_data(self):
        aid_packages_data = Victim.objects.values(
            'currentStatus').annotate(count=Count('victimID'))
        aid_packages_data_dict = {status[0]: 0 for status in STATUS}
        for entry in aid_packages_data:
            aid_packages_data_dict[entry['currentStatus']] = entry['count']
        # print(aid_packages_data)
        return aid_packages_data

    def risk_level_data(self):
        risk_level_data = Victim.objects.values(
            'riskLevel').annotate(count=Count('victimID'))
        risk_level_data_dict = {level[0]: 0 for level in RISK_LEVEL}
        for entry in risk_level_data:
            risk_level_data_dict[entry['riskLevel']] = entry['count']
        # print(risk_level_data)
        return risk_level_data

    def needs_data(self):
        needs_data = Victim.objects.values(
            'needs__name').annotate(count=Count('victimID'))
        # print("Needs data", needs_data)
        needs_data_dict = {level[1]: 0 for level in NEEDS_CHOICES}
        for entry in needs_data:
            needs_data_dict[entry['needs__name']] = entry['count']
        # print(needs_data)
        return needs_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["aid_packages_data"] = self.aid_packages_data()
        context["risk_level_data"] = self.risk_level_data()
        context["needs_data"] = self.needs_data()
        context["current_status"] = STATUS
        context["risk_level"] = RISK_LEVEL
        return context


class AffectedAreaListView(ListView):
    model = AffectedArea
    context_object_name = "affected_area_lists"
    template_name = "flood_relief_center/affected_areas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["damage_level"] = DAMAGE_LEVEL
        return context

    def get_search_query(self, queryset, search_query):
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))
        return queryset

    def get_queryset(self):
        queryset = AffectedArea.objects.all()

        # Get the query parameters from the request
        search_query = self.request.GET.get("search_query", "")
        selected_damage_level = self.request.GET.get(
            "selected_damage_level", "")

        ordered_by = self.request.GET.get("orderparam", "areaID")

        min_population = self.request.GET.get("min_population", None)
        max_population = self.request.GET.get("max_population", None)
        # # Apply population range filter (if provided)
        if min_population:
            queryset = queryset.filter(population__gte=min_population)
        if max_population:
            queryset = queryset.filter(population__lte=max_population)

        # checklist
        selected_needs = self.request.GET.getlist("needs")
        if selected_needs:
            queryset = queryset.filter(
                needs__name__in=selected_needs).distinct()

        # Apply search filter
        if search_query:
            queryset = self.get_search_query(queryset, search_query)

        # Apply status filter
        if selected_damage_level:
            queryset = queryset.filter(damageLevel=selected_damage_level)

        if ordered_by == "name":
            queryset = queryset.annotate(lower_name=Lower(
                "name")).order_by("lower_name")
        else:
            queryset = queryset.order_by(ordered_by)

        return queryset


def edit_affected_area(request, areaID):
    area = AffectedArea.objects.get(areaID=areaID)
    form = AffectedAreaForm(instance=area)
    if request.method == 'POST':
        form = AffectedAreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:affected-areas"))
    context = {"form": form}
    return render(request, "flood_relief_center/edit_affected_area.html", context)


def add_affected_area(request):
    form = AffectedAreaForm()
    if request.method == 'POST':
        form = AffectedAreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:affected-areas"))
    context = {"form": form}

    return render(request, "flood_relief_center/add_affected_area.html", context)


def delete_affected_area(request, areaID):
    area = AffectedArea.objects.get(areaID=areaID)
    area.delete()
    return redirect(reverse("flood-relief-center:affected-areas"))


class ReliefCenterDetailView(DetailView):
    model = ReliefCenter
    context_object_name = "relief_center_detail"
    template_name = "flood_relief_center/relief_center_detail.html"
    pk_url_kwarg = 'centerID'

    def financial_status_data(self):
        center_id = self.kwargs.get('centerID')
        financial_status_data = Finance.objects.filter(center__centerID=center_id).values(
            'finance_type').annotate(total_amount=Sum('amount'))
        # print(financial_status_data)
        return financial_status_data

    def max_min_financial_data(self):
        center_id = self.kwargs.get('centerID')

        # Aggregate maximum and minimum amounts for the given center
        max_min_data = Finance.objects.filter(center__centerID=center_id).values(
            'finance_type').aggregate(
            donation_max=Max('amount', filter=Q(finance_type='donation')),
            donation_min=Min('amount', filter=Q(finance_type='donation')),
            grant_max=Max('amount', filter=Q(finance_type='grant')),
            grant_min=Min('amount', filter=Q(finance_type='grant')),
            expense_max=Max('amount', filter=Q(finance_type='expense')),
            expense_min=Min('amount', filter=Q(finance_type='expense'))
        )

        # print("Filtered financial data:", max_min_data)
        return max_min_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        center = self.object  # The specific `ReliefCenter` object
        context["financial_status_data"] = self.financial_status_data()
        context["max_min_financial_data"] = self.max_min_financial_data()
        context["centerID"] = center.centerID  # self.kwargs.get('centerID')
        # print(context["relief_center_detail"])
        # context["relief_center_detail"].first().name
        context["centerName"] = center.name

        return context

    def get_queryset(self):
        # Filter by centerID
        return ReliefCenter.objects.filter(centerID=self.kwargs.get('centerID'))


class VolunteersListView(ListView):
    model = Volunteer
    context_object_name = "volunteer_list"
    template_name = "flood_relief_center/volunteers.html"
    pk_url_kwarg = 'centerID'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        centerID = self.kwargs.get('centerID')
        context["position"] = POSITION
        context["avaliability_status"] = AVALIABILITY_STATUS
        context["teams"] = get_team_name(centerID)
        context["centerID"] = centerID
        # context["volunteers"] = Volunteer.objects.filter(team__center__centerID=centerID)
        return context

    def get_search_query(self, queryset, search_query):
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(position__icontains=search_query) | Q(team__teamName__icontains=search_query) |
                                       Q(availabilityStatus__icontains=search_query))

        return queryset

    def get_queryset(self):

        # Get the query parameters from the request
        centerID = self.kwargs.get('centerID')
        search_query = self.request.GET.get("search_query", "")
        selected_position = self.request.GET.get("selected_position", "")
        selected_avaliability_status = self.request.GET.get(
            "selected_availability_status", "")
        selected_team_name = self.request.GET.get("selected_team_name", "")
        ordered_by = self.request.GET.get("orderparam", "name")

        # print("searchq", search_query)
        # print("elect", selected_position)
        # print("ava", selected_avaliability_status)
        # print("team", selected_team_name)
        queryset = (Volunteer.objects.filter(team__center__centerID=centerID))

        # Apply search filter
        if search_query:
            queryset = self.get_search_query(queryset, search_query)
            # print("queryset", queryset)

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

        # print("queryset", queryset)
        return queryset


def edit_volunteer(request, volunteerID):
    # Retrieve the volunteer instance based on the provided ID
    volunteer = Volunteer.objects.get(volunteerID=volunteerID)
    form = VolunteerForm(instance=volunteer)

    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:volunteers"))

    context = {"form": form}
    return render(request, "flood_relief_center/edit_volunteer.html", context)


def add_volunteer(request, centerID):
    form = VolunteerForm()
    # print("addcenterID", centerID)
    if request.method == 'POST':
        # print(request.POST)                                                               ~
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:volunteers", kwargs={'centerID': centerID}))


    context = {"form": form, "centerID": centerID}
    return render(request, "flood_relief_center/add_volunteer.html", context)


def delete_volunteer(request, volunteerID):
    volunteer = Volunteer.objects.get(volunteerID=volunteerID)
    volunteer.delete()
    return redirect(reverse("flood-relief-center:volunteers"))


class RescueTeamsListView(ListView):
    model = RescueTeam
    context_object_name = "rescue_team_list"
    template_name = "flood_relief_center/rescue_team.html"

    def get_search_query(self, queryset, search_query):
        if search_query:
            queryset = queryset.filter(Q(teamName__icontains=search_query) | Q(
                taskType__icontains=search_query)  # | Q(center__name__icontains=search_query)
            )

        return queryset

    def get_queryset(self):
        centerID = self.kwargs.get('centerID')
        queryset = RescueTeam.objects.filter(center_id=self.kwargs.get('centerID'))

        # Get the query parameters from the request
        search_query = self.request.GET.get("search_query", "")
        selected_task_type = self.request.GET.get("selected_task_type", "")

        ordered_by = self.request.GET.get("orderparam", "teamName")

        # print("search_query", search_query)
        # print("ordered_by", ordered_by)

        # Apply search filter
        if search_query:
            queryset = self.get_search_query(queryset, search_query)

        # # Apply center filter
        if selected_task_type:
            queryset = queryset.filter(taskType=selected_task_type)

        # print("55555",selected_task_type)

        if ordered_by == "teamName":
            queryset = queryset.annotate(lower_name=Lower(
                "teamName")).order_by("lower_name")
        else:
            queryset = queryset.order_by(ordered_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leader_list"] = Member.objects.all()
        context["volunteer_list"] = Volunteer.objects.all()
        context["task_type_list"] = get_task_type()
        centerID = self.kwargs.get('centerID')
        return context

    # def get_queryset(self):
    # # Filter by centerID
    #     return RescueTeam.objects.filter(center_id=self.kwargs.get('centerID'))


# def edit_affected_area(request, areaID):
#     area = AffectedArea.objects.get(areaID=areaID)
#     form = AffectedAreaForm(instance=area)
#     if request.method == 'POST':
#         form = AffectedAreaForm(request.POST, instance=area)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("flood-relief-center:affected-areas"))
#     context = {"form": form}
#     return render(request, "flood_relief_center/edit_affected_area.html", context)


def add_rescue_team(request):
    form = RescueTeamForm()
    if request.method == 'POST':
        form = RescueTeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("flood-relief-center:rescue-teams"))
    context = {"form": form}

    return render(request, "flood_relief_center/add_rescue_team.html", context)


# def delete_affected_area(request, teamID):
#     area = RescueTeam.objects.get(teamID=teamID)
#     area.delete()
#     return redirect(reverse("flood-relief-center:affected-areas"))
