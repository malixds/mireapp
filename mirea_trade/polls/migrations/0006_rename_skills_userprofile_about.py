# Generated by Django 4.2.3 on 2023-07-20 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_userprofile_alter_comment_user_alter_task_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='skills',
            new_name='about',
        ),
    ]
