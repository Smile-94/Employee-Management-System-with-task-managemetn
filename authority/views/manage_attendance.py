from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


# Django Generic Classes
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# Models 
from authority.models import Attendance
from employee.models import EmployeeInfo

#Filter Classes
from authority.filters import AttendanceFilter

# Forms
from authority.forms import AuthorityAttendanceForm



class AuthorityAddAttendanceView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model =Attendance
    queryset = Attendance.objects.filter(is_active=True).order_by('-id')
    form_class = AuthorityAttendanceForm
    filterset_class = AttendanceFilter
    template_name = 'authority/attendance_authority.html'
    success_url = reverse_lazy('authority:add_authority_attendance')

    def get_queryset(self):
        queryset = super().get_queryset()

        # Check if form_date or to_date filters are applied
        form_date_filter = self.request.GET.get('from_date', '')
        to_date_filter = self.request.GET.get('to_date', '')
        employee_id_filter = self.request.GET.get('employee_id', '')
        
        if form_date_filter or to_date_filter or employee_id_filter:
            # If either filter is applied, switch the ordering to ascending by date
            queryset = queryset.order_by('date')
        else:
            # Otherwise, keep the original ordering by date in descending order
            queryset = queryset.order_by('-id')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Attendance"
        context["attendances"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())

        return context
    
    
    def form_valid(self, form):
       try:
        employee_id = form.cleaned_data.get('employee_id')
        employee_info = EmployeeInfo.objects.get(employee_id=employee_id)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.attendance_of = employee_info
            form_obj.save()
        messages.success(self.request, "Attendance Added Successfully")
        return super().form_valid(form)
       
       except Exception as e:
           print(e)
           messages.error(self.request, f"{{e}}")
           return self.form_invalid(form)


class AuthorityUpdateAttendanceView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model= Attendance
    form_class= AuthorityAttendanceForm
    template_name = 'authority/attendance_authority.html'
    success_url = reverse_lazy('authority:add_authority_attendance')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Employee Attendance"
        context["updated"] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Employee Attendance Updated Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong please try again!")
        return super().form_invalid(form)

class DeleteAuthorityAttendanceView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model= Attendance
    context_object_name ='attendance'
    template_name = 'authority/attendance_authority.html'
    success_url = reverse_lazy('authority:add_authority_attendance')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Employee Attendance" 
        context["deleted"] = True 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)