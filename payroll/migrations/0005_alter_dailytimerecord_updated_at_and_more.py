# Generated by Django 4.1.2 on 2022-10-27 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0004_alter_dailytimerecord_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytimerecord',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='payslip',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
