from django.urls import path

# import views
from employee.views import employee_main
from employee.views import manage_leave
from employee.views import manage_task

app_name='employee'

urlpatterns = [
    path('employee/', employee_main.EmployeeHomeView.as_view(), name='employee')
    
]

# Manage Task
urlpatterns += [
    path('assigned-task/', manage_task.AssignedTaskView.as_view(), name="assigned_task"),
    path('assigned-task-details/<int:pk>/', manage_task.AssginedTaskDetailsView.as_view(), name="assigned_task_detaisl"),
    path('task_feedback/<int:pk>/', manage_task.TaskFeedbackView.as_view(), name="task_feedback"),
    
]


# Manage Leave
urlpatterns += [
    path('appliy-leave/', manage_leave.AddLeaveApplicationView.as_view(), name="apply_leave" ),
    path('leave-details/<int:pk>/', manage_leave.LeaveDetailsView.as_view(), name="leave-details" ),
]
