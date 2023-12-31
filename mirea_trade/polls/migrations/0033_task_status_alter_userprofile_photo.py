# Generated by Django 4.2 on 2023-10-10 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0032_alter_userprofile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default='default', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, default='mirea_trade/images/1.png', null=True, upload_to='mirea_trade/images/'),
        ),
    ]
