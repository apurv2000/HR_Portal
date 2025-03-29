# Generated by Django 5.1.7 on 2025-03-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0003_leave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='availed_leave',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='remaining_leave',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='total_leave',
        ),
        migrations.AddField(
            model_name='employeebisp',
            name='availed_leave',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employeebisp',
            name='remaining_leave',
            field=models.IntegerField(default=12),
        ),
        migrations.AddField(
            model_name='employeebisp',
            name='total_leave',
            field=models.IntegerField(default=12),
        ),
    ]
