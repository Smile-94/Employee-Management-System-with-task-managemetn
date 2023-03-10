from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import F
from datetime import timedelta
import datetime
from datetime import date

# Permissions Classes
from django.contrib.auth.mixins import LoginRequiredMixin

# filters
from reciption.filters import AttendanceFilters


# Class based View
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import ListView


# Models
from employee.models import EmployeeInfo
from reciption.models import Attendance

# forms
from reciption.forms import AttendanceForm


# Create your views here.
class ReceptionView(LoginRequiredMixin, TemplateView):
    template_name = 'reception/reception.html'

    def get_context_data(self, **kwargs):
        total_employee = EmployeeInfo.objects.all().count()
        today = date.today()
        attend_today = Attendance.objects.filter(date=today).count()
        context = super().get_context_data(**kwargs)
        context["title"] = "Receptionist Home"
        
        context["total_employee"] = total_employee
        context["attend_today"] = attend_today
        context["absence_today"] = (total_employee-attend_today)
        context["late_present"] = Attendance.objects.filter(date=date.today(),late_present__gt=timedelta(minutes=30)).count()

        return context


class AddAttendanceView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'reception/add_attendance.html'
    success_url = reverse_lazy('reception:add_attendance')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Attendance" 
        return context

    def form_valid(self, form):
        employee_id = form.cleaned_data['employee_id']
        today = date.today()
        try:
            employee_info = EmployeeInfo.objects.get(employee_id=employee_id)

            if Attendance.objects.filter(date=today, employee_id=employee_id).exists():
                messages.error(self.request, "Employee Attendance already done today")
                return self.form_invalid(form)

            if form.is_valid():
                attendance = form.save(commit=False)
                attendance.attendance_of = employee_info
                
                attendance.save()

            messages.success(self.request, "Attendance Added Successfully")  
            return super().form_valid(form)

        except Exception as e:
            print(e)
            messages.error(self.request, "Something worng try again")
            return self.form_invalid(form)


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    queryset = Attendance.objects.all().order_by('-pk')
    filterset_class = AttendanceFilters
    template_name = 'reception/attendance_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Attendance List" 
        context["attendances"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context
 
        
    
    
        
    
    
            

    
    
