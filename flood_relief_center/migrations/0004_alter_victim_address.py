# Generated by Django 5.1.3 on 2024-11-12 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "flood_relief_center",
            "0003_need_rename_type_donation_donation_type_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="victim",
            name="address",
            field=models.TextField(),
        ),
    ]