from django.db import models
from datetime import datetime
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Models 
from accounts.models import User
from employee.models import EmployeeInfo

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
    is_active = models.BooleanField(default=True)

class LeaveType(models.Model):
    leave_name = models.CharField( max_length=30)
    permited_days = models.PositiveIntegerField()
    salary_diduct = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.leave_name

class LeaveApplication(models.Model):
    application_of = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_employee')
    approvied_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_by',blank=True, null=True)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_type',null=True)
    employee_id = models.CharField(max_length=10,null=True)
    leave_from = models.DateField(auto_now=False, auto_now_add=False)
    leave_to = models.DateField(auto_now=False, auto_now_add=False)
    total_days = models.IntegerField(default=0)
    leave_description = models.TextField()
    approved_status = models.BooleanField(default=False)
    declined_status = models.BooleanField(default=False)
    declined_message = models.TextField(null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.total_days = (self.leave_to - self.leave_from).days + 1
        super(LeaveApplication, self).save(*args, **kwargs)

    def __str__(self):
        return str(f"{self.application_of}'s Application ")


class Task(models.Model):
    create_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='task')
    task_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    deadline = models.DateField()
    heading = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.task_id:
            year = str(datetime.date.today().year)[2:4]
            month = str(datetime.date.today().month)
            day = str(datetime.date.today().day)
            self.task_id = 'TS'+year+month+day+str(self.pk).zfill(4)
            self.save()
    
    def __str__(self):
        return self.task_id+", "+self.heading[:30]


class TaskAssigned(models.Model):
    task_of = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assigned_task')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_by')
    task_message = models.TextField(null=True)
    completion_report = models.TextField(null=True)
    completion_status = models.BooleanField(default=False)
    completion_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.task_of.heading[:20])+", "+str(self.assigned_to)


class TaskFeedback(models.Model):
    feedback_of = models.ForeignKey(TaskAssigned, on_delete=models.CASCADE,related_name='feed_back')
    feedback_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'feedback_by')
    feedback_at = models.DateTimeField(auto_now=True)
    feedback_heading = models.CharField(max_length=100, null=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return str(self.feedback_of)

class LatePresentAndLeave(models.Model):
    allowed_time = models.DurationField()
    allowed_late = models.PositiveIntegerField()
    allowed_leave = models.PositiveIntegerField()
    over_time_bonus = models.PositiveIntegerField(null=True)
    late_salary_cut = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    leave_salary_cut = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)


class MonthlyHoliDay(models.Model):
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
    holiday_name = models.CharField( max_length=50)
    holiday_month = models.CharField(max_length=10, choices=MONTH_CHOICES)
    date = models.DateField()
    is_active = models.BooleanField(default=True)

class WeeklyOffDay(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    first_day = models.CharField(max_length=10, choices=DAY_CHOICES)
    second_day = models.CharField(max_length=10, choices=DAY_CHOICES,null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)


# Create your models here.
class Attendance(models.Model):
    attendance_of=models.ForeignKey(EmployeeInfo,on_delete=models.CASCADE,related_name='attendance')
    employee_id=models.CharField(max_length=50)
    date=models.DateField(auto_now=False, auto_now_add=False)
    entering_time=models.TimeField(auto_now=False, auto_now_add=False,null=True)
    exit_time=models.TimeField(auto_now=False, auto_now_add=False, null=True)
    late_present = models.DurationField(blank=True, null=True)
    over_time = models.DurationField(blank=True, null=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.late_present:
            office_time = OfficeTime.objects.filter(is_active=True).order_by('-id').first()
            start_time = datetime.datetime.combine(datetime.date.today(), office_time.office_start)
            entry_time = datetime.datetime.combine(datetime.date.today(), self.entering_time)
            late_present = entry_time - start_time
            if late_present > datetime.timedelta(0):
                self.late_present = late_present
            else:
                self.late_present = datetime.timedelta(0)
            self.save()

        if not self.over_time and self.exit_time:
            office_time = OfficeTime.objects.filter(is_active=True).order_by('-id').first()
            end_time = datetime.datetime.combine(datetime.date.today(), office_time.office_end)
            exit_time = datetime.datetime.combine(datetime.date.today(), self.exit_time)
            over_time = exit_time - end_time
            if over_time > datetime.timedelta(0):
                self.over_time = over_time
            else:
                self.over_time = datetime.timedelta(0)
            self.save()

    def __str__(self):
        return str(self.attendance_of)



