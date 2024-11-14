from django.db import models
from django.utils.translation import gettext_lazy as _

from django.forms import ValidationError


NEEDS_CHOICES = [
    ('food and water', 'Food and Water'),
    ('shelter', 'Shelter'),
    ('clothing', 'Clothing'),
    ('medical supplies', 'Medical Supplies'),
    ('medical attention', 'Medical Attention'),
    ('water purification tablets', 'Water Purification Tablets'),
]

class Need(models.Model):
    name = models.CharField(max_length=50, choices=NEEDS_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()  # Display readable name in admin
    
    
# Create your models here.
class ReliefCenter(models.Model):
    centerID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    currentOccupancy = models.PositiveIntegerField()
    centerNumber = models.CharField(max_length=10, unique=True)
    
    def clean(self):
        # Ensure currentOccupancy is not greater than capacity
        if self.currentOccupancy > self.capacity:
            raise ValidationError(
                _('Current occupancy cannot exceed the capacity of the center.'),
                code='invalid_occupancy'
            )
            
    def save(self, *args, **kwargs):
        # Run validation before saving
        self.full_clean()  # This triggers the clean method
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    
class AffectedArea(models.Model):
    areaID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    population = models.PositiveIntegerField()
    damageLevel = models.CharField(max_length=8, choices=[('minor', 'Minor'), ('moderate', 'Moderate'), ('severe', 'Severe')])
    needs = models.ManyToManyField(Need)  # Link to multiple Needs

    def __str__(self):
        return self.name

class RescueTeam(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=100)
    taskType = models.CharField(max_length=100)
    area = models.ForeignKey(AffectedArea, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.teamName
    
class Victim(models.Model):
    victimID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    address = models.TextField()
    familyMembers = models.PositiveIntegerField()
    needs = models.ManyToManyField(Need)  # Link to multiple Needs
    currentStatus = models.CharField(max_length=50,choices=[('safe', 'Safe'), ('injured', 'Injured'), ('missing', 'Missing')])
    center = models.ForeignKey(ReliefCenter, on_delete=models.SET_NULL, null=True)
    riskLevel = models.IntegerField(choices=[(1, 'Low'), (2, 'Moderate'), (3, 'High'), (4, 'Critical'), (5, 'Severe')])
    victimNumber = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    
class AidPackage(models.Model):
    packageID = models.AutoField(primary_key=True)
    aid_type = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    distributionDate = models.DateField()
    center = models.ForeignKey(ReliefCenter, on_delete=models.SET_NULL, null=True, blank=True)
    victim = models.ForeignKey(Victim, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.aid_type} ({self.quantity})"
    

class Volunteer(models.Model):
    volunteerID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=30, choices=[('staff', 'Staff'), ('volunteer', 'Volunteer')])
    availabilityStatus = models.CharField(max_length=50, choices=[('available', 'Available'), ('unavailable', 'Unavailable')])
    team = models.ForeignKey(RescueTeam, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class Donation(models.Model):
    donationID = models.AutoField(primary_key=True)
    donorName = models.CharField(max_length=100)
    donation_type = models.CharField(max_length=50, choices=[('money', 'Money'), ('supplies', 'Supplies'), ('other', 'Other')],null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.ForeignKey(AidPackage, on_delete=models.SET_NULL, null=True, blank=True)
    donationDate = models.DateField()

    def clean(self):
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than 0.')
        
    def save(self, *args, **kwargs):
        # Run validation before saving
        self.full_clean()   
        super().save(*args, **kwargs)
            
    def __str__(self):
        return f"{self.donorName} - {self.donation_type}"
    
class Member(models.Model):
    memberID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    contactInfo = models.CharField(max_length=255)
    team = models.ForeignKey(RescueTeam, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Finance(models.Model):
    financeID = models.AutoField(primary_key=True)
    finance_type = models.CharField(max_length=50, choices=[('donation', 'Donation'), ('grant', 'Grant'), ('expense', 'Expense')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    source = models.CharField(max_length=100, blank=True)
    center = models.ForeignKey(ReliefCenter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.finance_type} - {self.amount} ({self.date})"