# Generated by Django 4.1.2 on 2022-10-16 07:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='projects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=None, size=None),
        ),
        migrations.AddField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]