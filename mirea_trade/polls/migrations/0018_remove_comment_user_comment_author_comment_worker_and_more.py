# Generated by Django 4.2 on 2023-09-18 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_alter_task_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='author_of_comment', to='polls.userprofile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='worker',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='worker_comment', to='polls.userprofile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=150),
        ),
    ]
