# Generated by Django 4.1.2 on 2022-11-13 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0016_alter_site_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='allowance_per_day',
        ),
    ]
