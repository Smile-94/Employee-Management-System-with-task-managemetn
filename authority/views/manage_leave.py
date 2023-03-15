from django.db.models import Sum
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

# Generic Classes
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import DetailView

# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Models
from authority.models import LeaveType
from authority.models import LeaveApplication
from authority.models import LatePresentAndLeave

# Forms
from authority.forms import LeaveTypeForm
from authority.forms import LeaveAcceptForm

# Filters
from authority.filters import LeaveApplicationFilter


class AppliedLeaveApplicationView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = LeaveApplication
    queryset = LeaveApplication.objects.filter(is_active = True, approved_status=False, declined_status=False)
    filterset_class = LeaveApplicationFilter
    template_name = 'authority/applied_leave_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Applied Leave'
        context["applications"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context
    
class AcceptedLeaveApplicationView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = LeaveApplication
    queryset = LeaveApplication.objects.filter(is_active = True, approved_status=True, declined_status=False)
    filterset_class = LeaveApplicationFilter
    template_name = 'authority/reviewed_leave_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Applied Leave'
        context["applications"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context
    
class RejectedLeaveApplicationView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = LeaveApplication
    queryset = LeaveApplication.objects.filter(is_active = True, approved_status=False, declined_status=True)
    filterset_class = LeaveApplicationFilter
    template_name = 'authority/reviewed_leave_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Applied Leave'
        context["applications"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        context["rejected"] = True
        return context

class AppliedLeaveApplicationDetailsView(LoginRequiredMixin, AdminPassesTestMixin, DetailView):
    model = LeaveApplication
    context_object_name = 'leave'
    template_name = 'authority/leave_application_details.html'

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

class AcceptLeaveApplicationView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model =  LeaveApplication
    form_class = LeaveAcceptForm
    template_name = 'authority/applied_leave_application.html'
    success_url = reverse_lazy('authority:applied_leave_application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Accept Leave Application"
        context["application"] = LeaveApplication.objects.get(id=self.kwargs['pk'])
        context["accepted"] = True
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.approvied_by = self.request.user
            form_obj.approved_status = True
            form_obj.save()
        messages.success(self.request, "Leave application accepted successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something worg try again")
        return super().form_invalid(form)
    

class RejectLeaveApplicationView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model =  LeaveApplication
    fields = ('declined_message',)
    template_name = 'authority/applied_leave_application.html'
    success_url = reverse_lazy('authority:applied_leave_application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Accept Leave Application"
        context["application"] = LeaveApplication.objects.get(id=self.kwargs['pk'])
        context["rejected"] = True
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.approvied_by = self.request.user
            form_obj.declined_status = True
            form_obj.save()
        messages.warning(self.request, "Leave application rejected")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something worg try again")
        return super().form_invalid(form)
    
class AddLeaveCategoryView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = 'authority/leave_type.html'
    success_url = reverse_lazy('authority:add_leave_category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Leave Type"
        context["leaves"] = LeaveType.objects.filter(is_active=True)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Leave Category Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)

class UpdateLeaveCategory(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = 'authority/leave_type.html'
    success_url = reverse_lazy('authority:add_leave_category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Leave Type"
        context["updated"] = True
        context["leaves"] = self.queryset
        return context

    def form_valid(self, form):
        messages.success(self.request, "Leave Category Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong try again!")
        return super().form_invalid(form)

class DeleteLeaveCategoryView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= LeaveType
    context_object_name = 'leavetype'
    template_name = "authority/leave_type.html"
    success_url = reverse_lazy('authority:add_leave_category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Leave Category" 
        context["deleted"] = True
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)