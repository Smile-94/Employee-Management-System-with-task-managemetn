from django.urls import path

# Views
from reciption.views import ReceptionView
from reciption.views import AddAttendanceView
from reciption.views import AttendanceListView

app_name = 'reception'

urlpatterns = [
    path('reception/', ReceptionView.as_view(), name='reception_home'),
    path('add-attendance/', AddAttendanceView.as_view(), name='add_attendance'),
    path('attendance-list/', AttendanceListView.as_view(), name='attendance_list'),
]
