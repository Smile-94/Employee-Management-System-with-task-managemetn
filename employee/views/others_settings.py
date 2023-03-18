
# Generic Classes
from django.views.generic import ListView

# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# Models
from authority.models import MonthlyHoliDay
from authority.models import LeaveType

# Filters
from authority.filters import MonthlyHoliDayFilter


class EmployeeMonthlyHolidayView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = MonthlyHoliDay
    queryset = MonthlyHoliDay.objects.filter(is_active=True)
    filterset_class = MonthlyHoliDayFilter
    template_name = 'employee/employee_holiday.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Holiday"
        context["holidays"] = self.filterset_class(self.request.GET, queryset=self.queryset)

        return context


class EmployeeYearlyLeaveView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = LeaveType
    template_name = 'employee/yearly_leave.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Leave Type"
        context["leaves"] = LeaveType.objects.filter(is_active=True)
        return context
