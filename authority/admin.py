from django.contrib import admin

# models
from authority.models import OfficeTime
from authority.models import PayrollMonth
from authority.models import FestivalBonus
from authority.models import LeaveApplication
from authority.models import Task
from authority.models import TaskAssigned
from authority.models import TaskFeedback


# Register your models here.
@admin.register(PayrollMonth)
class PayrollMonthAdmin(admin.ModelAdmin):
    list_display = ('month','year','from_date','to_date')
    list_filter = ('month',)
    list_per_page= 50

@admin.register(FestivalBonus)
class FestivalBonusAdmin(admin.ModelAdmin):
    list_display=('festival_name','bonus_percentage','created_at','modified_at')

@admin.register(OfficeTime)
class SetOfficeTimeAdmin(admin.ModelAdmin):
    list_display = ('office_start', 'office_end', 'modified_at', 'created_at')


@admin.register(LeaveApplication)
class LeaveApplication(admin.ModelAdmin):
    list_display=('application_of','approvied_by','leave_from','leave_to','approved_status')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('create_by','task_id','created_at','deadline')
    search_fields = ('create_by','task_id')
    list_filter = ('is_active',)
    list_per_page = 50


@admin.register(TaskAssigned)
class TaskAssignedAdmin(admin.ModelAdmin):
    list_display = ('task_of', 'assigned_to','assigned_by', 'completion_status')
    search_fields = ('assigned_to','assigned_by')
    list_per_page = 50


@admin.register(TaskFeedback)
class TaskFeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_of', 'feedback_by', 'feedback_at')
    list_per_page = 50

