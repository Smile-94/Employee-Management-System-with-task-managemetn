# Generated by Django 4.1.5 on 2023-03-14 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0021_rename_monthlyholyday_monthlyholiday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthlyholiday',
            old_name='holyday_month',
            new_name='holiday_month',
        ),
    ]
