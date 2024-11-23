from django.forms import ModelForm
from .models import ReliefCenter, Victim, Donation


class VictimForm(ModelForm):
    class Meta:
        model = Victim
        fields = "__all__"
        
class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = "__all__"