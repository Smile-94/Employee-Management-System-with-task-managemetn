from django.urls import path

# import views
from employee.views import employee_main
from employee.views import manage_leave
from employee.views import manage_task
from employee.views import manage_salary
from employee.views import manage_profile
from employee.views import others_settings

app_name='employee'

urlpatterns = [
    path('employee/', employee_main.EmployeeHomeView.as_view(), name='employee')
    
]

# Manage Profile
urlpatterns += [
    path('profile-details-employee/<int:pk>/', manage_profile.EmployeeProfileDetailsView.as_view(), name='profile_details_emplyee') 
]

# Manage Task
urlpatterns += [
    path('assigned-task/', manage_task.AssignedTaskView.as_view(), name="assigned_task"),
    path('employee-assigned-task-details/<int:pk>/', manage_task.AssginedTaskDetailsView.as_view(), name="employee_assigned_task_detaisl"),
    path('employee-task-feedback/<int:pk>/', manage_task.TaskFeedbackView.as_view(), name="employee_task_feedback"),
    path('task-completation/<int:pk>/', manage_task.TaskCompletationReportView.as_view(), name="task_completation"),
    path('task-completation/', manage_task.CompletedTaskListView.as_view(), name="completed_task"),
    
]


# Manage Leave & Attendance
urlpatterns += [
    path('appliy-leave/', manage_leave.AddLeaveApplicationView.as_view(), name="apply_leave" ),
    path('update-leave-application/<int:pk>/', manage_leave.UpdateLiveApplicationView.as_view(), name="update_leave_application" ),
    path('leave-details/<int:pk>/', manage_leave.LeaveDetailsView.as_view(), name="leave-details" ),
    path('employee-attendance', manage_leave.GiveAttendaneView.as_view(), name="employee_attendance" ),
    path('employee-exit/<int:pk>/', manage_leave.GoOutAttendaneView.as_view(), name="employee_exit" ),
]

# manage Salary
urlpatterns += [
    path('employee-monthly-salary/', manage_salary.MonthlyCalculatedSalaryListView.as_view(), name='employee_monthly_salary' ),
    path('employee-monthly-salary-details/<int:pk>/', manage_salary.MonthlySalaryDetailsView.as_view(), name='employee_monthly_salary_detail' )
    
]

# others
urlpatterns += [
    path('employee-holiday/', others_settings.EmployeeMonthlyHolidayView.as_view(), name='employee_monthly_holiday' ),
    path('employee-yearly-leave/', others_settings.EmployeeYearlyLeaveView.as_view(), name='employee_yearly_leave' )
]


