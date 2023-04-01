from django.urls import path

from report.views import TaskPdfView

app_name = 'report'

urlpatterns = [
    path('task-report-pdf/<int:pk>/', TaskPdfView.as_view(), name='task_report_pdf')
]
