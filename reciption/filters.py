import django_filters
from django import forms

# models 
from reciption.models import Attendance


class AttendanceFilters(django_filters.FilterSet):

    date = django_filters.DateFilter(widget=forms.DateInput(attrs={'type': 'date'}))
    employee_id = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Employee ID'}))

    class Meta:
        model = Attendance
        fields = ('employee_id', 'date')


