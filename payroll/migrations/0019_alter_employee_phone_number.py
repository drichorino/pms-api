# Generated by Django 4.1.2 on 2022-11-13 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0018_alter_employee_basic_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(default=None, max_length=11, verbose_name='Employee Name'),
        ),
    ]