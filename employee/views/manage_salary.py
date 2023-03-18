
# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# Generic Classed
from django.views.generic import ListView
from django.views.generic import DetailView

# Models
from authority.models import MonthlySalary



class MonthlyCalculatedSalaryListView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = MonthlySalary
    template_name = 'employee/monthlysalary_list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context["title"] = "Calculated Salary List"
         context["salarys"] = MonthlySalary.objects.filter(is_active=True,salary_employee=self.request.user.employee_info ).order_by('-id')
         return context


class MonthlySalaryDetailsView(LoginRequiredMixin, EmployeePassesTestMixin, DetailView):
    model = MonthlySalary
    context_object_name = 'salary'
    template_name = 'employee/monthly_salary_details.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def get_context_data(self, **kwargs):
        query_obj = self.get_object()
        total_salary = query_obj.total_salary
        total_diduct = query_obj.total_diduct
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Salary Details" 
        context["total_salary_pay"] =round(total_salary-0)

        return context