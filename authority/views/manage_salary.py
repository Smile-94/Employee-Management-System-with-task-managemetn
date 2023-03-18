from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
import datetime


# Permissions Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Generic Classes
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Models
from authority.models import MonthlySalary
from authority.models import FestivalBonus
from authority.models import PayrollMonth
from authority.models import LatePresentAndLeave
from authority.models import Attendance
from authority.models import MonthlyHoliDay
from employee.models import EmployeeInfo
from employee.models import EmployeeSalary

# Filters Classes
from authority.filters import SalaryEmployeeFilters
from authority.filters import CalculatedMonthlySalaryFilter

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

class CalculateMonthlySalaryView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = MonthlySalary
    form_class = MonthlySalaryForm
    template_name = 'authority/monthly_salarys.html'
    success_url = reverse_lazy('authority:monthly_salary_details', kwargs={'pk': 0})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthily Salary Calculation" 
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['other_pk'] = self.kwargs['pk']
        return initial
    
    def form_valid(self, form):
        try:
            salary_month = form.cleaned_data.get('salary_month')
            print("Salary Month: ", salary_month)

            employee = EmployeeInfo.objects.get(id = self.kwargs['pk'])
            salary = EmployeeSalary.objects.get(salary_of=employee)

            if MonthlySalary.objects.filter(salary_month=salary_month, salary_employee=employee, is_active=True).exists():
                obj_slary = MonthlySalary.objects.get(salary_month=salary_month, salary_employee=employee, is_active=True)
                print(obj_slary)
                messages.warning(self.request, "Salary already calculated in this month")
                return redirect('authority:monthly_salary_details', pk=obj_slary.id)

            else:
                conveyance =float(salary.basic_salary)*float(salary.conveyance/100)
                food_allowance = float(salary.basic_salary)*float(salary.food_allowance/100)
                medical_allowance = float(salary.basic_salary)*float(salary.medical_allowance/100)
                house_rent = float(salary.basic_salary)*float(salary.house_rent/100)
                mobile_allowance = float(salary.basic_salary)* float(salary.mobile_allowance/100)
                
                festival_bonus=0
                if form.cleaned_data.get('festival_bonus') is not None:
                    value = form.cleaned_data.get('festival_bonus')
                    fastival= FestivalBonus.objects.get(festival_name=value)
                    festival_bonus = float(salary.basic_salary)*float(fastival.bonus_percentage/100)

                # Payroll Month
                month = PayrollMonth.objects.get(month=salary_month.month)
                days = month.total_days
                from_date = month.from_date
                to_date = month.to_date

                # Permited Late present and Leave and over-time
                permited_latepresent = LatePresentAndLeave.objects.filter(is_active=True).order_by('-id').first()
                late_permited_time = permited_latepresent.allowed_time
                over_time_bonus = permited_latepresent.over_time_bonus
                late_permited_days = permited_latepresent.allowed_late
                late_present_salary_diduct = permited_latepresent.late_salary_cut
                permited_monthly_leave = permited_latepresent.allowed_leave
                leave_salary_diduct = permited_latepresent.leave_salary_cut

                # Overtime Bonus
                total_over_time = Attendance.objects.filter(
                    attendance_of=employee,
                    date__range=[from_date, to_date],
                    over_time__isnull=False
                ).aggregate(total_overtime=Coalesce(Sum('over_time'), datetime.timedelta()))

                total_over_time_duration = total_over_time['total_overtime']
                total_hours = total_over_time['total_overtime'].total_seconds() / 3600
                total_over_time_bonus = total_hours * over_time_bonus

            
                salary_fields= (conveyance,food_allowance,medical_allowance,house_rent,mobile_allowance,festival_bonus)
                total_salary_value =float(salary.basic_salary)+float(sum(salary_fields))

                # Total Salary Diduction
            
                # Calculated Salary month total holiday
                holiday = 0
                if MonthlyHoliDay.objects.filter(holiday_month=month).exists():
                    holiday =MonthlyHoliDay.objects.filter(holiday_month=month, is_active=True).count()

                # Total Late Present
                late_present = Attendance.objects.filter(attendance_of= employee , date__range=[month.from_date,month.to_date], late_present__gt=late_permited_time).count()

                # Salary of a employee for each day
                per_day_basic_salary = (salary.basic_salary/days)
                
                # Total Salary Diduct for late peresent in a month
                salary_diduct_for_late_present = 0
                late = 0
                if late_present > late_permited_days:
                    late=int(late_present-late_permited_days)
                    diduct_salary = float(per_day_basic_salary)*float(late_present_salary_diduct/100)
                    salary_diduct_for_late_present =diduct_salary*late
                
                # Total Attendance
                month_attendance = Attendance.objects.filter(attendance_of= employee , date__range=[month.from_date,month.to_date]).count()

                # Total Salary Diduct for the extra Leave
                extra_leave = (days-(month_attendance+holiday+permited_monthly_leave+month.totla_offdays))
                diduct_per_day = float(per_day_basic_salary)*float(leave_salary_diduct/100)
                salary_diduct_for_leave = (diduct_per_day*extra_leave)

                total_salary_diduct = (salary_diduct_for_late_present+salary_diduct_for_leave)

                
                
                if form.is_valid():
                    form_obj = form.save(commit=False)
                    form_obj.salary_employee = employee
                    form_obj.prepared_by = self.request.user
                    form_obj.salary_of = salary
                    form_obj.total_conveyance= conveyance
                    form_obj.total_food_allowance = food_allowance
                    form_obj.total_medical_allowance = medical_allowance
                    form_obj.total_house_rent = house_rent
                    form_obj.total_mobile_allowance = mobile_allowance
                    form_obj.total_bonus =festival_bonus
                    form_obj.total_overtime_bonus = total_over_time_bonus
                    form_obj.total_salary = total_salary_value
                    form_obj.total_overtime = total_over_time_duration
                    form_obj.late_present_diduct = salary_diduct_for_late_present
                    form_obj.extra_late_present = late
                    form_obj.extra_leave_diduct = salary_diduct_for_leave
                    form_obj.total_absence = extra_leave
                    form_obj.total_diduct = total_salary_diduct
                    
                    form_obj.save()
                    messages.success(self.request, "Salary Added Successfully")
                    self.object = form_obj
                self.success_url = reverse_lazy('authority:monthly_salary_details', kwargs={'pk': self.object.id})
                
                return super().form_valid(form)
        except Exception as e:
            print(e)
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went worng try aging!")
        return super().form_invalid(form)


class MonthlyCalculatedSalaryListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = MonthlySalary
    queryset = MonthlySalary.objects.filter(is_active=True).order_by('-id')
    filterset_class = CalculatedMonthlySalaryFilter
    template_name = 'authority/calculated_salary_list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context["title"] = "Calculated Salary List"
         context["salarys"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
         return context


class MonthlyCalculatedSalaryListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = MonthlySalary
    queryset = MonthlySalary.objects.filter(is_active=True).order_by('-id')
    filterset_class = CalculatedMonthlySalaryFilter
    template_name = 'authority/calculated_salary_list.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context["title"] = "Calculated Salary List"
         context["salarys"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
         return context


class MonthlySalaryDetailsView(LoginRequiredMixin, AdminPassesTestMixin, DetailView):
    model = MonthlySalary
    context_object_name = 'salary'
    template_name = 'authority/calculated_salary_details.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def get_context_data(self, **kwargs):
        query_obj = self.get_object()
        total_salary = query_obj.total_salary
        total_diduct = query_obj.total_diduct
        over_time_bonus = query_obj.total_overtime_bonus
        context = super().get_context_data(**kwargs)
        context["title"] = "Monthly Salary Details" 
        context["total_salary_pay"] =round(total_salary-total_diduct)
        context["total_salary_with_bonus"] =round(total_salary+over_time_bonus-total_diduct)

        return context

class UpdateCalculatedSalaryView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = MonthlySalary
    form_class = MonthlySalaryForm
    template_name = 'authority/update_calculated_salary.html'
    success_url = reverse_lazy('authority:calculated_monthly_salary')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Calculated Salary"
        context["salary"] = MonthlySalary.objects.get(id=self.kwargs['pk']) 
        return context

    def form_valid(self, form):
        try:
            salary_month = form.cleaned_data.get('salary_month')

            calculated_salary=MonthlySalary.objects.get(id=self.kwargs['pk'])

            employee = calculated_salary.salary_employee
        

            salary = EmployeeSalary.objects.get(salary_of=calculated_salary.salary_employee)
        

            plus_minus_bonus=0
            if form.cleaned_data.get('festival_bonus') is not None:
                value = form.cleaned_data.get('festival_bonus')
                fastival= FestivalBonus.objects.get(festival_name=value)
                plus_minus_bonus =float(salary.basic_salary)*float(fastival.bonus_percentage/100)
            
           
            if form.cleaned_data.get('festival_bonus') is None:
               plus_minus_bonus =  float(calculated_salary.total_bonus)- float(calculated_salary.total_bonus)

            
           # Payroll Month
            month = PayrollMonth.objects.get(month=salary_month.month)
            days = month.total_days
            from_date = month.from_date
            to_date = month.to_date

            # Month Attendance
            month_attendance = Attendance.objects.filter(attendance_of= employee , date__range=[month.from_date,month.to_date]).count()

            # Permited Late present and Leave and over-time
            permited_latepresent = LatePresentAndLeave.objects.filter(is_active=True).order_by('-id').first()
            late_permited_time = permited_latepresent.allowed_time
            over_time_bonus = permited_latepresent.over_time_bonus
            late_permited_days = permited_latepresent.allowed_late
            late_present_salary_diduct = permited_latepresent.late_salary_cut
            permited_monthly_leave = permited_latepresent.allowed_leave
            leave_salary_diduct = permited_latepresent.leave_salary_cut

            # Overtime Bonus
            total_over_time = Attendance.objects.filter(
                attendance_of=employee,
                date__range=[from_date, to_date],
                over_time__isnull=False
            ).aggregate(total_overtime=Coalesce(Sum('over_time'), datetime.timedelta()))

            total_over_time_duration = total_over_time['total_overtime']
            total_hours = total_over_time['total_overtime'].total_seconds() / 3600
            total_over_time_bonus = total_hours * over_time_bonus

            # Total Salary Diduction
            
            # Calculated Salary month total holiday
            holiday = 0
            if MonthlyHoliDay.objects.filter(holiday_month=month).exists():
                holiday =MonthlyHoliDay.objects.filter(holiday_month=month, is_active=True).count()

            # Total Late Present
            late_present = Attendance.objects.filter(attendance_of= employee , date__range=[month.from_date,month.to_date], late_present__gt=late_permited_time).count()

            # Salary of a employee for each day
            per_day_basic_salary = (salary.basic_salary/days)
                
            # Total Salary Diduct for late peresent in a month
            salary_diduct_for_late_present = 0
            late = 0
            if late_present > late_permited_days:
                late=int(late_present-late_permited_days)
                diduct_salary = float(per_day_basic_salary)*float(late_present_salary_diduct/100)
                salary_diduct_for_late_present =diduct_salary*late
                
            # Total Attendance
            month_attendance = Attendance.objects.filter(attendance_of= employee , date__range=[month.from_date,month.to_date]).count()

            # Total Salary Diduct for the extra Leave
            extra_leave = (days-(month_attendance+holiday+permited_monthly_leave+month.totla_offdays))
            diduct_per_day = float(per_day_basic_salary)*float(leave_salary_diduct/100)
            salary_diduct_for_leave = (diduct_per_day*extra_leave)

            if form.is_valid():
                form_obj = form.save(commit=False)

                if calculated_salary.festival_bonus is None:
                    form_obj.total_bonus = plus_minus_bonus
                    form_obj.total_salary = calculated_salary.total_salary+form_obj.total_bonus

                if calculated_salary.festival_bonus is not None:
                    form_obj.total_bonus = form_obj.total_bonus-plus_minus_bonus
                    form_obj.total_salary =  calculated_salary.total_salary - form_obj.total_bonus
                
                form_obj.total_overtime_bonus = total_over_time_bonus
                form_obj.total_overtime = total_over_time_duration
                form_obj.late_present_diduct = salary_diduct_for_late_present
                form_obj.extra_late_present = late
                form_obj.extra_leave_diduct = salary_diduct_for_leave
                form_obj.total_absence = extra_leave
                
                form_obj.save()
                messages.success(self.request, "Salary Updated Successfully")
            return super().form_valid(form)
        
        except Exception as e:
            print(e)
            return self.form_invalid(form)
            

    def form_invalid(self, form):
        messages.error(self.request, "Salary not updated please try again!")
        return super().form_invalid(form)

class DeleteCalculatedSalaryView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= MonthlySalary
    context_object_name ='salary'
    template_name = "authority/delete_calculated_salary.html"
    success_url = reverse_lazy('authority:calculated_monthly_salary')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Calculated Salary" 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)