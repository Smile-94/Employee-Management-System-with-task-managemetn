from django.contrib import admin

# Models
from reciption.models import Attendance

# Register your models here.


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_of', 'employee_id', 'date', 'entering_time', 'exit_time')
    search_fields = ('attendance_of', 'employee_id')
    list_per_page = 50


