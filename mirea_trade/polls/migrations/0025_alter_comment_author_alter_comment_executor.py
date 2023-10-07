# Generated by Django 4.2 on 2023-09-18 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_remove_comment_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_of_comment', to='polls.userprofile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker_comment', to='polls.userprofile'),
        ),
    ]