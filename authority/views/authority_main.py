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
from reciption.models import Attendance



# Create your views here.
class AdminView(LoginRequiredMixin, AdminPassesTestMixin, TemplateView):
    template_name = 'authority/admin.html'

    def get_context_data(self, **kwargs):
        total_employee = EmployeeInfo.objects.all().count()
        today = date.today()
        attend_today = Attendance.objects.filter(date=today).count()
        context = super().get_context_data(**kwargs)
        context["title"] = "Admin Panel" 
        context["total_employee"] = total_employee
        context["attend_today"] = attend_today
        context["absence_today"] = (total_employee-attend_today)
        context["late_present"] = Attendance.objects.filter(date=date.today(),late_present__gt=timedelta(minutes=30)).count() 
        return context
