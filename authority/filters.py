import django_filters
from django import forms
from datetime import datetime

from accounts.models import User
from authority.models import PayrollMonth
from authority.models import Task
from authority.models import TaskAssigned
from employee.models import EmployeeInfo


class EmployeeListFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = {
            'email': {'exact'},
        }


class TaskFilter(django_filters.FilterSet):
    task_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Task ID'}))
    dadeline = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))
    completion_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ('task_id', 'dadeline', 'completion_date')

class TaskEmployeeFilter(django_filters.FilterSet):
    info_of = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee Email'}))
    employee_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee ID'}))

    class Meta:
        model = EmployeeInfo
        fields =('info_of', 'employee_id')
    
    def filter_queryset(self, queryset):
        info_of_value = self.data.get('info_of')
        employee_id_value = self.data.get('employee_id')

        if info_of_value:
            user = User.objects.get(email=info_of_value)
            queryset = queryset.filter(info_of=user.id)

        if employee_id_value:
            employee_info = EmployeeInfo.objects.get(employee_id=employee_id_value)
            queryset = queryset.filter(employee_id=employee_info.employee_id)
            
        return queryset

class TaskAssignedFileter(django_filters.FilterSet):
    task_of = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Task ID'}))
    assigned_to = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee ID'}))
    completion_status = django_filters.ChoiceFilter(choices=[(True, 'Complete'), (False, 'Incomplete')])
    
    class Meta:
        model = TaskAssigned
        fields = ('task_of', 'assigned_to', 'completion_status')
    

    def filter_queryset(self, queryset):
        task_of_value = self.data.get('task_of')
        employee_id_value = self.data.get('employee_id')
        completion_status_value = self.data.get('completion_status')

        if task_of_value:
            task_id = Task.objects.get(task_id=task_of_value)
            queryset = queryset.filter(task_of=task_id)

        if employee_id_value:
            queryset = queryset.filter(employee_id=employee_id_value)
        
        if completion_status_value:
            completion_status_bool = completion_status_value.lower() == 'true'
            queryset = queryset.filter(completion_status=completion_status_bool)

        return queryset


class PayrollMonthListFilter(django_filters.FilterSet):
    current_year = datetime.now().year
    year_choices = [(year, year) for year in range(current_year-5, current_year+5)]
    year = django_filters.ChoiceFilter(choices=year_choices, empty_label='Year')
    
    class Meta:
       model= PayrollMonth
       fields = {
            'month' : {'exact'},
            'year'  : {'exact'}
       }
        