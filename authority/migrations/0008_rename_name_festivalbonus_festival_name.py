# Generated by Django 4.1.5 on 2023-02-08 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0007_festivalbonus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='festivalbonus',
            old_name='name',
            new_name='festival_name',
        ),
    ]
