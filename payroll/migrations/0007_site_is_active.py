# Generated by Django 4.1.2 on 2022-10-28 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0006_alter_dailytimerecord_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
