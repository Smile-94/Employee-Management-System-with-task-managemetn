from django.shortcuts import redirect
from datetime import timedelta
from datetime import date


# class-based view classes
from django.views.generic import TemplateView

# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin


# Models Employee
from employee.models import EmployeeInfo

# Models Rectiption
from authority.models import Attendance
from authority.models import LatePresentAndLeave
from authority.models import LeaveApplication

# Create your views here.
class AdminView(LoginRequiredMixin, AdminPassesTestMixin, TemplateView):
    template_name = 'authority/admin.html'

    def get_context_data(self, **kwargs):
        try:
            permited_latepresent = LatePresentAndLeave.objects.filter(is_active=True).order_by('-id').first()
            allowd_late_time = permited_latepresent.allowed_time
            total_leave = LeaveApplication.objects.filter(approved_status=True, is_active=True).count()
        except Exception as e:
            print(e)
        total_employee = EmployeeInfo.objects.all().count()
        
        today = date.today()
        attend_today = Attendance.objects.filter(date=today).count()
        context = super().get_context_data(**kwargs)
        context["title"] = "Admin Panel" 
        context["total_employee"] = total_employee
        context["attend_today"] = attend_today
        context["absence_today"] = (total_employee-attend_today)
        context["late_present"] = Attendance.objects.filter(date=date.today(),late_present__gt=allowd_late_time).count() 
        context["total_leave"] = total_leave
        context["leave_applications"] = LeaveApplication.objects.filter(is_active=True, approved_status=True,  declined_status=True).order_by('-id')[:5]
        return context
