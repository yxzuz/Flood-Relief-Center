# Generated by Django 5.1.3 on 2024-11-11 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AffectedArea",
            fields=[
                ("areaID", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("population", models.PositiveIntegerField()),
                ("damageLevel", models.CharField(max_length=50)),
                ("needs", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="AidPackage",
            fields=[
                ("packageID", models.AutoField(primary_key=True, serialize=False)),
                ("type", models.CharField(max_length=100)),
                ("quantity", models.PositiveIntegerField()),
                ("distributionDate", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="ReliefCenter",
            fields=[
                ("centerID", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("location", models.CharField(max_length=255)),
                ("capacity", models.PositiveIntegerField()),
                ("currentOccupancy", models.PositiveIntegerField()),
                ("centerNumber", models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Donation",
            fields=[
                ("donationID", models.AutoField(primary_key=True, serialize=False)),
                ("donorName", models.CharField(max_length=100)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("money", "Money"),
                            ("supplies", "Supplies"),
                            ("other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("donationDate", models.DateField()),
                (
                    "package",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="flood_relief_center.aidpackage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Finance",
            fields=[
                ("financeID", models.AutoField(primary_key=True, serialize=False)),
                (
                    "finance_type",
                    models.CharField(
                        choices=[
                            ("donation", "Donation"),
                            ("grant", "Grant"),
                            ("expense", "Expense"),
                        ],
                        max_length=50,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateField()),
                ("source", models.CharField(blank=True, max_length=100)),
                (
                    "center",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="flood_relief_center.reliefcenter",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="aidpackage",
            name="center",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="flood_relief_center.reliefcenter",
            ),
        ),
        migrations.CreateModel(
            name="RescueTeam",
            fields=[
                ("teamID", models.AutoField(primary_key=True, serialize=False)),
                ("teamName", models.CharField(max_length=100)),
                ("taskType", models.CharField(max_length=100)),
                (
                    "area",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="flood_relief_center.affectedarea",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                ("memberID", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("role", models.CharField(max_length=50)),
                ("contactInfo", models.CharField(max_length=255)),
                (
                    "team",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="flood_relief_center.rescueteam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Victim",
            fields=[
                ("victimID", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("age", models.PositiveIntegerField()),
                ("address", models.CharField(max_length=255)),
                ("familyMembers", models.PositiveIntegerField()),
                ("needs", models.TextField()),
                ("currentStatus", models.CharField(max_length=50)),
                (
                    "riskLevel",
                    models.IntegerField(
                        choices=[
                            (1, "Low"),
                            (2, "Moderate"),
                            (3, "High"),
                            (4, "Critical"),
                            (5, "Severe"),
                        ]
                    ),
                ),
                ("victimNumber", models.CharField(max_length=10, unique=True)),
                (
                    "center",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="flood_relief_center.reliefcenter",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="aidpackage",
            name="victim",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="flood_relief_center.victim",
            ),
        ),
        migrations.CreateModel(
            name="Volunteer",
            fields=[
                ("volunteerID", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("skillSet", models.CharField(blank=True, max_length=255)),
                ("availabilityStatus", models.CharField(max_length=50)),
                (
                    "team",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="flood_relief_center.rescueteam",
                    ),
                ),
            ],
        ),
    ]