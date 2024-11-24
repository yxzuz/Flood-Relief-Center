from django.forms import ModelForm
from .models import ReliefCenter, Victim, Donation, AffectedArea


class VictimForm(ModelForm):
    class Meta:
        model = Victim
        fields = "__all__"
        
class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = "__all__"
        
class AffectedAreaForm(ModelForm):
    class Meta:
        model = AffectedArea
        fields = "__all__"
        
        
class ReliefCenterForm(ModelForm):
    class Meta:
        model = ReliefCenter
        fields = "__all__"