# Generated by Django 4.2.3 on 2023-07-28 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_task_date_alter_task_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='subject',
        ),
        migrations.AddField(
            model_name='task',
            name='skills',
            field=models.ManyToManyField(related_name='tasks', to='polls.skill'),
        ),
    ]
