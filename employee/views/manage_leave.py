from django.db.models import Sum
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin


# Import Generic Views
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView

# Models
from authority.models import LeaveApplication
from authority.models import LatePresentAndLeave

# Forms
from authority.forms import LeaveApplicationForm


class AddLeaveApplicationView(LoginRequiredMixin, EmployeePassesTestMixin, CreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = 'employee/leave_application.html'
    success_url = reverse_lazy('employee:apply_leave')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Application"
        context["leaves"] = LeaveApplication.objects.filter(is_active=True).order_by('-id')
        return context

    def form_valid(self, form):
        leave_from = form.cleaned_data.get('leave_from')
        leave_to = form.cleaned_data.get('leave_to')
        if LeaveApplication.objects.filter(is_active=True, approved_status=False, declined_status=False, leave_from__range=[leave_from,leave_to], leave_to__range=[leave_from,leave_to]).exists():
            messages.error(self.request, "You already applied for leave on this date")
            return redirect(reverse('employee:apply_leave'))
        
        if form.is_valid():
            leave_form=form.save(commit=False)
            leave_form.application_of= self.request.user
            leave_form.employee_id = self.request.user.employee_info.employee_id
            leave_form.save()
        messages.success(self.request, "Applied Leave application successfully")
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, "Leave Application not Applied successfully try again")
        return super().form_invalid(form)

class UpdateLiveApplicationView(LoginRequiredMixin, EmployeePassesTestMixin, UpdateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = 'employee/leave_application.html'
    success_url = reverse_lazy('employee:apply_leave')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Application"
        context["updated"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Applied Leave updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong please try again!")
        return super().form_invalid(form)

class LeaveDetailsView(LoginRequiredMixin, EmployeePassesTestMixin, DetailView):
    model = LeaveApplication
    context_object_name = 'leave'
    template_name = 'employee/leave_details.html'

    def get_context_data(self, **kwargs):
        leave_object = self.object # Accessing the query object
        leave_permonth = LatePresentAndLeave.objects.filter(is_active=True).order_by('-id').first()
        total_leave_month = LeaveApplication.objects.filter(application_of=leave_object.application_of,leave_type=leave_object.leave_type, approved_status=True, leave_from__month=datetime.today().month).aggregate(total_days=Sum('total_days'))['total_days'] or 0
        total_leave_year = LeaveApplication.objects.filter(application_of=leave_object.application_of,leave_type=leave_object.leave_type,approved_status=True, leave_from__year=datetime.today().year).aggregate(total_days=Sum('total_days'))['total_days'] or 0
        context = super().get_context_data(**kwargs)
        context["title"] = "Leave Details" 
        context["leave_permonth"] = leave_permonth
        context["total_leave_month"] = total_leave_month
        context["total_leave_year"] = total_leave_year
        return context
    