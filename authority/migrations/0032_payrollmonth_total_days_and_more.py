# Generated by Django 4.1.5 on 2023-03-17 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authority', '0031_alter_payrollmonth_month_monthlysalary'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollmonth',
            name='total_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='monthlysalary',
            name='festival_bonus',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='festival_bonus', to='authority.festivalbonus'),
        ),
        migrations.AlterField(
            model_name='monthlysalary',
            name='salary_month',
            field=models.ForeignKey(limit_choices_to={'active_status': True}, on_delete=django.db.models.deletion.CASCADE, related_name='salary_month', to='authority.payrollmonth'),
        ),
    ]