# Generated by Django 4.2 on 2023-09-18 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_rename_commant_worker_comment_comment_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_of_comment', to='polls.userprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker_comment', to='polls.userprofile'),
            preserve_default=False,
        ),
    ]