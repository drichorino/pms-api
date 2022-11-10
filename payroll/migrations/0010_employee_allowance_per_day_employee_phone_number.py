# Generated by Django 4.1.2 on 2022-11-09 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0009_site_projects_alter_dailytimerecord_projects_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='allowance_per_day',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=20, verbose_name="Employee's Allowance Per Day"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(default=None, max_length=11, verbose_name='Employee Name'),
            preserve_default=False,
        ),
    ]
