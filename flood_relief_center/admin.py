from django.contrib import admin
from .models import ReliefCenter, AffectedArea, RescueTeam, Victim, AidPackage, Volunteer, Donation, Member, Finance, Need
# Register your models here.
admin.site.register(ReliefCenter)
admin.site.register(AffectedArea)
admin.site.register(RescueTeam)
admin.site.register(Victim)
admin.site.register(AidPackage)
admin.site.register(Volunteer)
admin.site.register(Donation)
admin.site.register(Member)
admin.site.register(Finance)
admin.site.register(Need)