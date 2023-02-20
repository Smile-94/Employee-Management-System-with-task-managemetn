from django.db import models
import datetime

# models
from employee.models import EmployeeInfo
from accounts.models import User
from authority.models import OfficeTime

# Create your models here.
class Attendance(models.Model):
    attendance_of=models.ForeignKey(EmployeeInfo,on_delete=models.CASCADE,related_name='attendance')
    employee_id=models.CharField(max_length=50)
    date=models.DateField(auto_now=False, auto_now_add=False)
    entering_time=models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    exit_time=models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    late_present = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.late_present:
            office_time = OfficeTime.objects.all().first()
            start_time=datetime.datetime.combine(datetime.date.today(), office_time.office_start)
            entry_time=datetime.datetime.combine(datetime.date.today(), self.entering_time)
            self.late_present = (entry_time-start_time)
            self.save()

    def __str__(self):
        return str(self.attendance_of)
