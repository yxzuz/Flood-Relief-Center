from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import Lower
from django.views.generic import ListView
from django.db.models import Q
from .forms import VictimForm, DonationForm, AffectedAreaForm, ReliefCenterForm
from .models import ReliefCenter, Donation, Victim, AffectedArea, NEEDS_CHOICES

# Create your views here.
STATUS = [('safe', 'Safe'), ('injured', 'Injured'), ('missing', 'Missing')]
RISK_LEVEL = [(1, 'Low'), (2, 'Moderate'), (3, 'High'),
              (4, 'Critical'), (5, 'Severe')]
DONATION_TYPE = [('money', 'Money'), ('supplies',
                                      'Supplies'), ('other', 'Other')]
DAMAGE_LEVEL = [('minor', 'Minor'), ('moderate',
                                     'Moderate'), ('severe', 'Severe')]


def get_center_names():
    return [center.name for center in ReliefCenter.objects.all()]


def index(request):
    return render(request, "flood_relief_center/index.html")


class ReliefCentersListView(ListView):
    model = ReliefCenter
    context_object_name = "relief_centers_lists"
    template_name = "flood_relief_center/relief_centers.html"


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


def delete_relief_center(request, areaID):
    area = ReliefCenter.objects.get(areaID=areaID)
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
                donation_type__icontains=search_query) | Q(package__aid_type__icontains=search_query))
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
        # print(queryset)
        # return queryset
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
    return render(request, "flood_relief_center/edit_victim.html", context)


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
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(victimNumber__icontains=search_query) | Q(address__icontains=search_query) | Q(
                center__name__icontains=search_query) | Q(riskLevel__icontains=search_query) | Q(currentStatus__icontains=search_query))
        return queryset

    def get_queryset(self):
        queryset = Victim.objects.all()

        # Get the query parameters from the request
        search_query = self.request.GET.get("search_query", "")
        selected_donation = self.request.GET.get("selected_donation", "")
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
        if selected_donation:
            queryset = queryset.filter(center__name=selected_donation)

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
        print(aid_packages_data)
        return aid_packages_data

    def risk_level_data(self):
        risk_level_data = Victim.objects.values(
            'riskLevel').annotate(count=Count('victimID'))
        risk_level_data_dict = {level[0]: 0 for level in RISK_LEVEL}
        for entry in risk_level_data:
            risk_level_data_dict[entry['riskLevel']] = entry['count']
        print(risk_level_data)
        return risk_level_data

    def needs_data(self):
        needs_data = Victim.objects.values(
            'needs__name').annotate(count=Count('victimID'))
        print("Needs data", needs_data)
        needs_data_dict = {level[1]: 0 for level in NEEDS_CHOICES}
        for entry in needs_data:
            needs_data_dict[entry['needs__name']] = entry['count']
        print(needs_data)
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


class ReliefCenterDetailView(ListView):
    model = ReliefCenter
    context_object_name = "relief_center_detail"
    template_name = "flood_relief_center/relief_center_detail.html"

    def get_queryset(self):
        # Filter by centerID
        return ReliefCenter.objects.filter(centerID=self.kwargs.get('centerID'))
