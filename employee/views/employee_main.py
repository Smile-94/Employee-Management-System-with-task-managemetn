from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime

# Permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin



# Generic Views
from django.views.generic import TemplateView

# Models
from authority.models import PayrollMonth
from authority.models import Attendance
from authority.models import LeaveApplication
from authority.models import LatePresentAndLeave
from authority.models import WeeklyOffDay
from authority.models import OfficeTime


class EmployeeHomeView( LoginRequiredMixin, EmployeePassesTestMixin, TemplateView):
    template_name = 'employee/employee.html'

    def get_context_data(self, **kwargs):
        try:
            current_month_name = datetime.now().strftime('%B')
            current_year_name = datetime.now().strftime('%Y')
            
            to_date =datetime.today().date()

            today = datetime.now()
            first_day_of_month = datetime(today.year, today.month, 1)
            from_date = first_day_of_month.strftime('%Y-%m-%d')
            print("From Date: ",from_date)

    
            this_month_attendance = Attendance.objects.filter(attendance_of=self.request.user.employee_info, date__range=[from_date,to_date]).count()
            total_leave = LeaveApplication.objects.filter(application_of=self.request.user,is_active=True, approved_status=True, leave_from__range=[from_date,to_date]).count()
            permi_late_obje=LatePresentAndLeave.objects.last()
            late_present = Attendance.objects.filter(attendance_of=self.request.user.employee_info,date__range=[from_date,to_date], late_present__gt=permi_late_obje.allowed_time).count()

            
            permited_leave_days=permi_late_obje.allowed_leave
            permited_late_present = permi_late_obje.allowed_late

            
            weekly_offday_obj=WeeklyOffDay.objects.last()
            day1=weekly_offday_obj.first_day
            day2=weekly_offday_obj.second_day

            total_overtime = Attendance.objects.filter(attendance_of=self.request.user.employee_info,date__range=[from_date, to_date]).aggregate(total_overtime=Sum('over_time'))['total_overtime']
        except Exception as e:
            print(e)

        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Home"
        context["total_attendance"] = this_month_attendance
        context["current_month"] = f"{(current_month_name)},{current_year_name}"
        context["leave"] = total_leave
        context["leave_permited"] = permited_leave_days
        context["late"] = late_present
        context["late_permited"] = permited_late_present
        context["off_day1"] = day1
        context["off_day2"] = day2
        context["total_leave"] = total_leave
        context["total_overtime"] =total_overtime
        context["office_time"] = OfficeTime.objects.filter(is_active=True).order_by('-id').first()
        

        return context
    