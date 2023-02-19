from django.db import models
from datetime import datetime
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Models 
from accounts.models import User

# Create your models here.
class PayrollMonth(models.Model):
    MONTH_CHOICES = [
        ('Jan', 'January'),
        ('Feb', 'February'),
        ('Mar', 'March'),
        ('Apr', 'April'),
        ('May', 'May'),
        ('Jun', 'June'),
        ('Jul', 'July'),
        ('Aug', 'August'),
        ('Sep', 'September'),
        ('Oct', 'October'),
        ('Nov', 'November'),
        ('Dec', 'December'),
    ]

    month=models.CharField(max_length=3, choices=MONTH_CHOICES, default='Jan')
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    from_date=models.DateField(auto_now=False, auto_now_add=False)
    to_date=models.DateField(auto_now=False, auto_now_add=False)
    active_status=models.BooleanField(default=True)

class FestivalBonus(models.Model):
    festival_name=models.CharField(max_length=20, unique=True)
    bonus_percentage= models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

class OfficeTime(models.Model):
    office_start=models.TimeField(auto_now=False, auto_now_add=False)
    office_end=models.TimeField(auto_now=False, auto_now_add=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

class LeaveApplication(models.Model):
    application_of = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_employee')
    approvied_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_by',blank=True, null=True)
    employee_id = models.CharField(max_length=10,null=True)
    leave_from = models.DateField(auto_now=False, auto_now_add=False)
    leave_to = models.DateField(auto_now=False, auto_now_add=False)
    leave_description = models.TextField()
    approved_status = models.BooleanField(default=False)
    declined_status = models.BooleanField(default=False)
    declined_message = models.TextField(null=True)
    is_active = models.BooleanField(default=True)


class Task(models.Model):
    create_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='task')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'task_assigned',null=True)
    task_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    dadeline = models.DateField()
    heading = models.CharField(max_length=100)
    description = models.TextField()
    task_message = models.TextField(null=True)
    completion_report = models.TextField(null=True)
    completion_status = models.BooleanField(default=False)
    completion_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.task_id:
            year = str(datetime.date.today().year)[2:4]
            month = str(datetime.date.today().month)
            day = str(datetime.date.today().day)
            self.task_id = 'TS'+year+month+day+str(self.pk).zfill(4)
            self.save()


class TaskFeedback(models.Model):
    feedback_of = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='feed_back')
    feedback_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'feedback_by')
    feedback_at = models.DateTimeField(auto_now=True)
    feedback_heading = models.CharField(max_length=100, null=True)
    modified_at = models.DateTimeField(auto_now_add=False)
    description = models.TextField()

