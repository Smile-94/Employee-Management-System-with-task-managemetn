from django import forms
from datetime import datetime

# models
from authority.models import OfficeTime
from authority.models import PayrollMonth
from authority.models import FestivalBonus
from authority.models import LeaveType
from authority.models import LeaveApplication
from authority.models import Task
from authority.models import TaskAssigned
from authority.models import TaskFeedback
from authority.models import LatePresentAndLeave
from authority.models import MonthlyHoliDay
from authority.models import WeeklyOffDay
from authority.models import Attendance

# Customs Widgets
from authority.widgets import DurationWidget
from authority.widgets import DurationFormField


# Create form class here
class PayrollMonthForm(forms.ModelForm):
    current_year = datetime.now().year
    year_choices = [(year, year) for year in range(current_year-5, current_year+5)]
    year = forms.ChoiceField(choices=year_choices)
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = PayrollMonth
        fields = ('month','year','from_date','to_date')

class OfficeTimeForm(forms.ModelForm):
    
    office_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    office_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model=OfficeTime
        exclude = ('is_active',)


class FestivalBonusForm(forms.ModelForm):

    class Meta:
        model=FestivalBonus
        exclude=('is_active',)


class LeaveTypeForm(forms.ModelForm):

    class Meta:
        model = LeaveType
        fields = ('leave_name','permited_days','salary_diduct')


class LeaveApplicationForm(forms.ModelForm):
    leave_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    leave_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LeaveApplication
        fields =('leave_from','leave_to','leave_type','leave_description')

class LeaveAcceptForm(forms.ModelForm):
    leave_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    leave_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = LeaveApplication
        fields =('leave_from','leave_to',)


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ('deadline','heading','description')

class TaskAssignedForm(forms.ModelForm):

    class Meta:
        model = TaskAssigned
        fields = ('task_of','task_message',)

class TaskCompletationForm(forms.ModelForm):

    class Meta:
        model = TaskAssigned
        fields = ('completion_report',)


class TaskFeedbackForm(forms.ModelForm):

    class Meta:
        model = TaskFeedback
        fields = ('description', 'feedback_heading')


class LatePresentAndLeaveForm(forms.ModelForm):
    allowed_time = DurationFormField(widget=DurationWidget)

    class Meta:
        model = LatePresentAndLeave
        fields = ('allowed_time','allowed_late', 'over_time_bonus', 'allowed_leave','late_salary_cut','leave_salary_cut')


class MonthlyHolidayForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = MonthlyHoliDay
        exclude = ('is_active',)

class WeeklyOffDayForm(forms.ModelForm):
    
    class Meta:
        model = WeeklyOffDay
        fields = ('first_day','second_day')


