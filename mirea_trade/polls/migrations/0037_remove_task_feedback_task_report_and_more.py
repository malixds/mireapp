# Generated by Django 4.2 on 2023-10-10 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0036_remove_task_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='feedback',
        ),
        migrations.AddField(
            model_name='task',
            name='report',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='feedback',
            field=models.IntegerField(default=0),
        ),
    ]