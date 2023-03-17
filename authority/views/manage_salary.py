from django.urls import reverse_lazy
from django.shortcuts import redirect


# Permissions Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Generic Classes
from django.views.generic import ListView

# Models
from employee.models import EmployeeInfo

# Filters Classes
from authority.filters import SalaryEmployeeFilters

# Forms 
from authority.forms import MonthlySalaryForm


class SalaryEmployeeListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = EmployeeInfo
    queryset = EmployeeInfo.objects.filter(is_active=True)
    filterset_class = SalaryEmployeeFilters
    template_name = 'authority/employee_list_salary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee List"
        context["form"] = MonthlySalaryForm
        context["employees"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context
