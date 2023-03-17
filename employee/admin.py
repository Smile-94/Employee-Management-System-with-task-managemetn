from django.contrib import admin
from employee.models import DesignationInfo
from employee.models import EmployeeInfo
from employee.models import EmployeeSalary


# Register your models here.
@admin.register(EmployeeInfo)
class EmployeeInfoAdmin(admin.ModelAdmin):
    list_display=('info_of','position','employee_id','phone')
    search_fields=('employee_id','phone')
    list_per_page=50


@admin.register(DesignationInfo)
class DesignationAdmin(admin.ModelAdmin):
    list_display=('designation','department','created_at','updated_at')
    search_fields=('designation','department')
    list_per_page=50
    
@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(admin.ModelAdmin):
    list_display = ('salary_of', 'basic_salary','conveyance','food_allowance','medical_allowance','house_rent','mobile_allowance')
    search_fields = ('salary_of',)
    list_per_page = 50

