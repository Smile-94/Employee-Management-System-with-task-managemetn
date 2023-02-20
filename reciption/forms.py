from django import forms

# models
from reciption.models import Attendance


class AttendanceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    entering_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    exit_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Attendance
        exclude = ('attendance_of',)
