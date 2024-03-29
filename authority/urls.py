from django.urls import path

# views
from authority.views import authority_main
from authority.views import manage_employee
from authority.views import admin_settings
from authority.views import payroll_settings
from authority.views import manage_salary
from authority.views import manage_task
from authority.views import manage_leave
from authority.views import manage_attendance


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
    path('delete-employee/<int:pk>/', manage_employee.DeleteEmployeeView.as_view(), name='delete_employee'),
]


# Add, Update, Delete Payroll Months
urlpatterns += [
    #Monthly Salary
    path('employee-lsit-salary/', manage_salary.SalaryEmployeeListView.as_view(), name="employee_list_salary" ),
    path('calculate-monthly-salary/<int:pk>/', manage_salary.CalculateMonthlySalaryView.as_view(), name="calculate_monthly_salary" ),
    path('calculated-monthly-salary/', manage_salary.MonthlyCalculatedSalaryListView.as_view(), name="calculated_monthly_salary" ),
    path('monthly-salary-details/<int:pk>/', manage_salary.MonthlySalaryDetailsView.as_view(), name="monthly_salary_details" ),
    path('monthly-salary-update/<int:pk>/', manage_salary.UpdateCalculatedSalaryView.as_view(), name="monthly_salary_update" ),
    path('delete-calculated-salary/<int:pk>/', manage_salary.DeleteCalculatedSalaryView.as_view(), name="delete_calculated_salary" ),
    #Payroll Month
    path('add-payroll-month/', payroll_settings.AddPayrollMonthView.as_view(), name='add_payrollmonth'),
    path('update-payroll-month/<int:pk>/', payroll_settings.UpdatePayrollMonthView.as_view(), name='update_payrollmonth'), 
    path('delete-payroll-month/<int:pk>/', payroll_settings.DeletePayrollMonthView.as_view(), name='delete_payrollmonth'), 
    path('festival-bonus/', payroll_settings.FestivalBonusView.as_view(), name='festival_bonus'),
    path('festival-update/<int:pk>/', payroll_settings.FestivalBonusUpdateView.as_view(), name='update_festival'),
    path('delete-update/<int:pk>/', payroll_settings.DeleteFestivalBonusView.as_view(), name='delete_festival'),
    # MonthlyHoliDay
    path('add-monthly-holiday/', payroll_settings.AddMonthlyHolidayView.as_view(), name='add_monthly_holiday'),
    path('update-monthly-holiday/<int:pk>/', payroll_settings.UpdateMonthlyHolidayView.as_view(), name='update_monthly_holiday'),
    path('delete-monthly-holiday/<int:pk>/', payroll_settings.DeleteMonthlyHolidayView.as_view(), name='delete_monthly_holiday'),
]

# manage task
urlpatterns += [
    path('add-task/', manage_task.TaskCreateView.as_view(), name='add_task'),
    path('task-details/<int:pk>/', manage_task.TaskDetailView.as_view(), name='task_details'),
    path('update-task/<int:pk>/', manage_task.TaskUpdateView.as_view(), name='update_task'),
    path('delete-task/<int:pk>/', manage_task.TaskDeleteView.as_view(), name='delete_task'),
    path('task-employee-list/', manage_task.EmployeeTaskListView.as_view(), name='task_employee_list'),
    path('task-assigned/<int:pk>/', manage_task.AssignTaskView.as_view(), name='task_assign'),
    path('employee-assigned-task/<int:pk>/', manage_task.EmployeeAssignedTaskListView.as_view(), name='employee_assigned_task'),
    path('assigned-task-list/', manage_task.AssignedTaskView.as_view(), name='assigned_task'),
    path('delete-assigned-task/<int:pk>/', manage_task.DeleteAssignedTaskView.as_view(), name='delete_assigned_task'),
    path('assigned-task-details/<int:pk>/', manage_task.AssginedTaskDetailsView.as_view(), name='assigned_task_details'),
    path('task-feedback/<int:pk>/', manage_task.TaskFeedbackView.as_view(), name='task_feedback'),
    path('task-statics/', manage_task.TaskStaticsView.as_view(), name='task_statics'),
]

# Manage Leave
urlpatterns += [
    path('add-leave-category/', manage_leave.AddLeaveCategoryView.as_view(), name='add_leave_category'),
    path('update-leave-category/<int:pk>/', manage_leave.UpdateLeaveCategory.as_view(), name='update_leave_category'),
    path('delete-leave-category/<int:pk>/', manage_leave.DeleteLeaveCategoryView.as_view(), name='delete_leave_category'),
    path('applied-leave-application-list/', manage_leave.AppliedLeaveApplicationView.as_view(), name='applied_leave_application_list'),
    path('accpted-leave-application-list/', manage_leave.AcceptedLeaveApplicationView.as_view(), name='accepted_leave_application_list'),
    path('rejected-leave-application-list/', manage_leave.RejectedLeaveApplicationView.as_view(), name='rejected_leave_application_list'),
    path('leave-application-details/<int:pk>/', manage_leave.AppliedLeaveApplicationDetailsView.as_view(), name='leave_application_details'),
    path('accept-leave-application/<int:pk>/', manage_leave.AcceptLeaveApplicationView.as_view(), name='accept_leave_application'),
    path('reject-leave-application/<int:pk>/', manage_leave.RejectLeaveApplicationView.as_view(), name='reject_leave_application'),
]

# manage attendance 
urlpatterns += [
    path('add_authority_attendance/', manage_attendance.AuthorityAddAttendanceView.as_view(), name='add_authority_attendance' ),
    path('update_authority_attendance/<int:pk>/', manage_attendance.AuthorityUpdateAttendanceView.as_view(), name='update_authority_attendance' ),
    path('delete_authority_attendance/<int:pk>/', manage_attendance.DeleteAuthorityAttendanceView.as_view(), name='delete_authority_attendance' ),
]




# admin settings
urlpatterns += [
    path('add-desgnation/', admin_settings.AddDesignationView.as_view(), name='add_designation'),
    path('designation-list/', admin_settings.DesignationListView.as_view(), name='designation_list'),
    path('update-designation/<int:pk>/', admin_settings.DesignationUpdateView.as_view(), name='update_designation'),
    path('delete-designation/<int:pk>/', admin_settings.DesignationDeleteView.as_view(), name='delete_designation'),
    path('add-office-time/', admin_settings.AddOfficeTimeView.as_view(), name='add_officetime'),
    path('update-office-time/<int:pk>/', admin_settings.UpdateOfficeTimeView.as_view(), name='update_officetime'),
    path('delete-office-time/<int:pk>/', admin_settings.DeleteOfficeTimeView.as_view(), name='delete_officetime'),
    # Allowed Late Present and Leave
    path('add-late-present-leave/', admin_settings.AddAllowedLatePresentLeaveView.as_view(), name='add_late_present_and_leave'),
    path('update-late-present-leave/<int:pk>/', admin_settings.UpdateAllowedLatePresentLeaveView.as_view(), name='update_late_present_and_leave'),
    path('delete-late-present-leave/<int:pk>/', admin_settings.DeleteAllowedLatePresentLeaveView.as_view(), name='delete_late_present_and_leave'),
    # Weekly offday
    path('add-weekly-offday', admin_settings.AddWeeklyOffDayView.as_view(), name='add_weekly_offday'),
    path('update-weekly-offday/<int:pk>/', admin_settings.UpdateWeeklyOffDay.as_view(), name='update_weekly_offday'),
    path('delete-weekly-offday/<int:pk>/', admin_settings.DeleteWeeklyOffDayView.as_view(), name='delete_weekly_offday'),


]

