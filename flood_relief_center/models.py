from django.db import models
from django.utils.translation import gettext_lazy as _

from django.forms import ValidationError

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
    
    
class AffectedArea(models.Model):
    areaID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    population = models.PositiveIntegerField()
    damageLevel = models.CharField(max_length=50)
    needs = models.TextField()

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
    address = models.CharField(max_length=255)
    familyMembers = models.PositiveIntegerField()
    needs = models.TextField()
    currentStatus = models.CharField(max_length=50)
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
    center = models.ForeignKey(ReliefCenter, on_delete=models.SET_NULL, null=True)
    victim = models.ForeignKey(Victim, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.type} ({self.quantity})"
    

class Volunteer(models.Model):
    volunteerID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    skillSet = models.CharField(max_length=255, blank=True)
    availabilityStatus = models.CharField(max_length=50)
    team = models.ForeignKey(RescueTeam, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class Donation(models.Model):
    donationID = models.AutoField(primary_key=True)
    donorName = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[('money', 'Money'), ('supplies', 'Supplies'), ('other', 'Other')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.ForeignKey(AidPackage, on_delete=models.SET_NULL, null=True)
    donationDate = models.DateField()

    def clean(self):
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than 0.')
        
    def save(self, *args, **kwargs):
        # Run validation before saving
        self.full_clean()   
        super().save(*args, **kwargs)
            
    def __str__(self):
        return f"{self.donorName} - {self.type}"
    
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
        return f"{self.type} - {self.amount} ({self.date})"