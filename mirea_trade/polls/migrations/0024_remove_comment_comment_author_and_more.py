# Generated by Django 4.2 on 2023-09-18 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_alter_comment_comment_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comment_worker',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_of_comment', to='polls.userprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker_comment', to='polls.userprofile'),
            preserve_default=False,
        ),
    ]