from django.urls import path

# views
from authority.views import authority_main
from authority.views import manage_employee
from authority.views import admin_settings
from authority.views import payroll_settings
from authority.views import manage_task
from authority.views import manage_leave


app_name = 'authority'

# authority main
urlpatterns = [
    path('authority/', authority_main.AdminView.as_view(), name='authority'),
]

#manage employee urls
urlpatterns += [
    path('add-employee/', manage_employee.AddEmpolyeeView.as_view(), name='add_employee'),
    path('employee-list/', manage_employee.EmployeeListView.as_view(), name='employee_list'),
    path('employee-details/<int:pk>/', manage_employee.EmployeeDetailView.as_view(), name='employee_details'),
    path('edit_employee/<int:pk>/', manage_employee.EditEmployeeView.as_view(), name='edit_employee'),
    path('edit_address/<int:pk>/', manage_employee.EditEmployeeAddressView.as_view(), name='edit_address'),
    path('edit_salary/<int:pk>/', manage_employee.EditEmployeeSalaryView.as_view(), name='edit_salary'),
]


# Add, Update, Delete Payroll Months
urlpatterns += [
    path('add-payroll-month/', payroll_settings.AddPayrollMonthView.as_view(), name='add_payrollmonth'),
    path('update-payroll-month/<int:pk>/', payroll_settings.UpdatePayrollMonthView.as_view(), name='update_payrollmonth'), 
    path('festival-bonus/', payroll_settings.FestivalBonusView.as_view(), name='festival_bonus'),
    path('festival-update/<int:pk>/', payroll_settings.FestivalBonusUpdateView.as_view(), name='update_festival'),
]

# manage task
urlpatterns += [
    path('add-task/', manage_task.TaskCreateView.as_view(), name='add_task'),
    path('update-task/<int:pk>/', manage_task.TaskUpdateView.as_view(), name='update_task'),
    path('delete-task/<int:pk>/', manage_task.TaskDeleteView.as_view(), name='delete_task'),
    path('task-employee-list/', manage_task.EmployeeTaskListView.as_view(), name='task_employee_list'),
    path('task-assigned/<int:pk>/', manage_task.AssignTaskView.as_view(), name='task_assign'),
    path('employee-assigned-task/<int:pk>/', manage_task.EmployeeAssignedTaskListView.as_view(), name='employee_assigned_task'),
    path('assigned-task-list/', manage_task.AssignedTaskView.as_view(), name='assigned_task'),
    path('delete-assigned-task/<int:pk>/', manage_task.DeleteAssignedTaskView.as_view(), name='delete_assigned_task'),
    path('assigned-task-details/<int:pk>/', manage_task.AssginedTaskDetailsView.as_view(), name='assigned_task_details'),
    path('task-feedback/<int:pk>/', manage_task.TaskFeedbackView.as_view(), name='task_feedback'),
]

# Manage Leave
urlpatterns += [
    path('add-leave-category/', manage_leave.AddLeaveCategoryView.as_view(), name='add_leave_category'),
    path('update-leave-category/<int:pk>/', manage_leave.UpdateLeaveCategory.as_view(), name='update_leave_category'),
    path('delete-leave-category/<int:pk>/', manage_leave.DeleteLeaveCategoryView.as_view(), name='delete_leave_category'),
]




# admin settings
urlpatterns += [
    path('add-desgnation/', admin_settings.AddDesignationView.as_view(), name='add_designation'),
    path('designation-list/', admin_settings.DesignationListView.as_view(), name='designation_list'),
    path('update-designation/<int:pk>/', admin_settings.DesignationUpdateView.as_view(), name='update_designation'),
    path('delete-designation/<int:pk>/', admin_settings.DesignationDeleteView.as_view(), name='delete_designation'),
    path('add-office-time/', admin_settings.AddOfficeTimeView.as_view(), name='add_officetime'),
    path('update-office-time/<int:pk>/', admin_settings.UpdateOfficeTimeView.as_view(), name='update_officetime')
]

