# Generated by Django 4.2.3 on 2023-07-31 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_alter_task_author_alter_task_contact_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='contact_link',
        ),
    ]
