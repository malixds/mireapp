# Generated by Django 4.2.3 on 2023-07-28 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_remove_task_subject_task_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]