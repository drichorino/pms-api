# Generated by Django 4.1.2 on 2022-11-13 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0019_alter_employee_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(max_length=11, null=True, verbose_name='Employee Name'),
        ),
    ]