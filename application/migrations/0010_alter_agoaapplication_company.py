# Generated by Django 5.2 on 2025-04-21 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_alter_machinery_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agoaapplication',
            name='company',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='application.companydetails'),
        ),
    ]
