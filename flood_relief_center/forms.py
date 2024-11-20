from django.forms import ModelForm
from .models import ReliefCenter, Victim


class VictimForm(ModelForm):
    class Meta:
        model = Victim
        fields = "__all__"