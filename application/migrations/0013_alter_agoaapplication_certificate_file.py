# Generated by Django 5.2 on 2025-04-30 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_agoaapplication_certificate_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agoaapplication',
            name='certificate_file',
            field=models.FileField(blank=True, null=True, upload_to='media/certificates'),
        ),
    ]
