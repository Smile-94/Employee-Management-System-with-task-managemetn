from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


# class-based view classes
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin


# Models Employee
from employee.models import DesignationInfo

# Models Authority
from authority.models import OfficeTime
from authority.models import LatePresentAndLeave
from authority.models import WeeklyOffDay


# forms 
from employee.forms import DesignationInfoForm
from authority.forms import OfficeTimeForm
from authority.forms import LatePresentAndLeaveForm
from authority.forms import WeeklyOffDayForm

# Allowed Late Present and Leave
class AddAllowedLatePresentLeaveView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = LatePresentAndLeave
    form_class = LatePresentAndLeaveForm
    template_name = 'authority/late_present_leave.html'
    success_url = reverse_lazy('authority:add_late_present_and_leave')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Late Present and Leave'
        context["lateLeaves"] = LatePresentAndLeave.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Allowed Late Present and Leave Added Successfully ")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong please try again")
        return super().form_invalid(form)
    
    
class UpdateAllowedLatePresentLeaveView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = LatePresentAndLeave
    form_class = LatePresentAndLeaveForm
    template_name = 'authority/late_present_leave.html'
    success_url = reverse_lazy('authority:add_late_present_and_leave')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Update Late Present and Leave'
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Allowed Late Present and Leave Added Successfully ")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong please try again")
        return super().form_invalid(form)
    
    
class DeleteAllowedLatePresentLeaveView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= LatePresentAndLeave
    context_object_name = 'lateLeave'
    template_name = "authority/late_present_leave.html"
    success_url = reverse_lazy('authority:add_late_present_and_leave')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Late Present and Leave" 
        context["deleted"] = True
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)


class AddDesignationView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = DesignationInfo
    form_class = DesignationInfoForm
    template_name = 'authority/add_designation.html'
    success_url = reverse_lazy('authority:add_designation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Designation'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Designation Added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong please try again")
        return super().form_invalid(form)


class DesignationListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = DesignationInfo
    fields = ('designation', 'department', 'created_at', 'updated_at')
    context_object_name = 'designations'
    template_name = 'authority/designation_list.html'

    def get_queryset(self):
        try:
            return DesignationInfo.objects.filter(is_active=True)
        except Exception as e:
            print(e)
            return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Designation List" 
        return context


class DesignationUpdateView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = DesignationInfo
    fields = ('designation', 'department', 'description')
    template_name = 'authority/add_designation.html'
    success_url = reverse_lazy('authority:designation_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Designation" 
        return context

    def form_valid(self, form):
        messages.success(self.request, "Designation Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "some thing went wrong try again")
        return super().form_invalid(form)


class DesignationDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = DesignationInfo
    template_name = 'authority/delete_designation.html'
    context_object_name = 'designation'
    success_url = reverse_lazy('authority:designation_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return redirect(success_url)

class AddOfficeTimeView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model=OfficeTime
    form_class=OfficeTimeForm
    template_name= "authority/add_office_time.html"
    success_url=reverse_lazy('authority:add_officetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Office Time" 
        context["office_time"] = OfficeTime.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Office Time added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Office time not added try again")
        return super().form_invalid(form)


class UpdateOfficeTimeView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model=OfficeTime
    form_class=OfficeTimeForm
    template_name= "authority/add_office_time.html"
    success_url=reverse_lazy('authority:add_officetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Office Time" 
        context["updated"] = True 
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Office Time added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Office time not added try again")
        return super().form_invalid(form)

class DeleteOfficeTimeView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= OfficeTime
    context_object_name = 'officetime'
    template_name= "authority/add_office_time.html"
    success_url=reverse_lazy('authority:add_officetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Weekly Off-day" 
        context["deleted"] = True
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)


class AddWeeklyOffDayView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model=WeeklyOffDay
    form_class=WeeklyOffDayForm
    template_name= "authority/weekly_offday.html"
    success_url=reverse_lazy('authority:add_weekly_offday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Weekly Off-day" 
        context["offdays"] = WeeklyOffDay.objects.filter(is_active=True).order_by('-id')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Weekly Off-day added Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong please try again")
        return super().form_invalid(form)

class UpdateWeeklyOffDay(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model=WeeklyOffDay
    form_class=WeeklyOffDayForm
    template_name= "authority/weekly_offday.html"
    success_url=reverse_lazy('authority:add_weekly_offday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Weekly Off-day"
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Weekly Off-day Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong please try again")
        return super().form_invalid(form)

class DeleteWeeklyOffDayView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= WeeklyOffDay
    context_object_name = 'offday'
    template_name= "authority/weekly_offday.html"
    success_url=reverse_lazy('authority:add_weekly_offday')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Weekly Off-day" 
        context["deleted"] = True
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)