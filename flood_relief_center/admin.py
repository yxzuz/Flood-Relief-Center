from django.contrib import admin
from .models import ReliefCenter, AffectedArea, RescueTeam, Victim
# Register your models here.
admin.site.register(ReliefCenter)
admin.site.register(AffectedArea)
admin.site.register(RescueTeam)
admin.site.register(Victim)