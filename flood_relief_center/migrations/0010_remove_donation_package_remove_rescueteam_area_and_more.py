# Generated by Django 5.1.3 on 2024-11-24 07:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flood_relief_center", "0009_alter_donation_package"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="donation",
            name="package",
        ),
        migrations.RemoveField(
            model_name="rescueteam",
            name="area",
        ),
        migrations.AddField(
            model_name="rescueteam",
            name="center",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="flood_relief_center.reliefcenter",
            ),
        ),
        migrations.AlterField(
            model_name="donation",
            name="donation_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("money", "Money"),
                    ("supplies", "Supplies"),
                    ("medical", "Medical"),
                    ("relief", "Relief"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
