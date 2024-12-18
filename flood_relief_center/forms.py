from django import forms
from django.forms import ModelForm
from .models import ReliefCenter, Victim, Donation, AffectedArea, RescueTeam, Volunteer



class VictimForm(ModelForm):
    class Meta:
        model = Victim
        fields = "__all__"


class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = "__all__"


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = "__all__"
        widgets = {
            'donationDate': forms.DateInput(attrs={'type': 'date'}),
        }


class AffectedAreaForm(ModelForm):
    class Meta:
        model = AffectedArea
        fields = "__all__"


class ReliefCenterForm(ModelForm):
    class Meta:
        model = ReliefCenter
        fields = "__all__"


class RescueTeamForm(ModelForm):
    class Meta:
        model = RescueTeam
        fields = "__all__"

