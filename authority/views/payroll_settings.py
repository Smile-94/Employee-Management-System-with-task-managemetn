from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


# Filters Class
from authority.filters import PayrollMonthListFilter


# class-based view classes
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin


# Models Authority
from authority.models import PayrollMonth
from authority.models import FestivalBonus


# forms 
from authority.forms import PayrollMonthForm
from authority.forms import FestivalBonusForm


class AddPayrollMonthView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = PayrollMonth
    queryset =PayrollMonth.objects.filter(active_status=True).order_by('-id')
    form_class = PayrollMonthForm
    filterset_class = PayrollMonthListFilter
    template_name = 'authority/payroll_month.html'
    success_url = reverse_lazy('authority:add_payrollmonth')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Payroll Month"
        context["months"] = self.filterset_class(self.request.GET, queryset=self.queryset)

        return context
    
    
    def form_valid(self, form):
        messages.success(self.request, "Payroll Month Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again")
        return super().form_invalid(form)

class UpdatePayrollMonthView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model=PayrollMonth
    form_class=PayrollMonthForm
    template_name='authority/payroll_month.html'
    success_url= reverse_lazy('authority:add_payrollmonth')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Payroll Month"
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Payroll Month Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong payroll month not updated")
        return super().form_invalid(form)

class DeletePayrollMonthView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= PayrollMonth
    template_name = "authority/delete_payrollmonth.html"
    success_url = reverse_lazy('authority:payrollmonth_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Payroll Month" 
        return context

    def form_valid(self, form):
        self.object.active_status = False
        self.object.save()
        return redirect(self.success_url)

# Festival Bonus add,update, delete

class FestivalBonusView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = FestivalBonus
    form_class = FestivalBonusForm
    template_name='authority/festival_bonus.html'
    success_url=reverse_lazy('authority:festival_bonus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Festival Bonus" 
        context["festivals"] = FestivalBonus.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Festival Bonus Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Festival not added try again!")
        return super().form_invalid(form)


class FestivalBonusUpdateView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = FestivalBonus
    form_class = FestivalBonusForm
    template_name = 'authority/festival_bonus.html'
    success_url = reverse_lazy('authority:festival_bonus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Festival Bonus" 
        context["updated"] = True 
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Festival Bonus Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Festival Bonus not updated try again !')
        return super().form_invalid(form)
    

    
    
    
    
    

    

