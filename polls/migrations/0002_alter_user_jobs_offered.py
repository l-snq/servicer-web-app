# Generated by Django 5.1.2 on 2024-11-09 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='jobs_offered',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.jobs'),
        ),
    ]