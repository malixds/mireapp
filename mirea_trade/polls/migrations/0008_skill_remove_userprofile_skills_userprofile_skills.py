# Generated by Django 4.2.3 on 2023-07-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_userprofile_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='skills',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='skills',
            field=models.ManyToManyField(related_name='providers', to='polls.skill'),
        ),
    ]
