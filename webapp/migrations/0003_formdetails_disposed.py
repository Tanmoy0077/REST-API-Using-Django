# Generated by Django 5.1 on 2024-09-08 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_requeststatus_disposal_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdetails',
            name='disposed',
            field=models.BooleanField(default=False),
        ),
    ]
