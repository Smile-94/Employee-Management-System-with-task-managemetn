from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

# Generic Classes
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Permission Classes
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Models
from authority.models import LeaveType

# Forms
from authority.forms import LeaveTypeForm


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