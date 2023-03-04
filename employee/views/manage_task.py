from django.urls import reverse_lazy
from django.contrib import messages


# Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.permission import EmployeePassesTestMixin

# Generic Class
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView


# Models
from authority.models import TaskAssigned
from authority.models import TaskFeedback

# Forms
from authority.forms import TaskFeedbackForm
from authority.forms import TaskCompletationForm

# Filter Class
from employee.filters import EmployeeAssignedTaskFilter




class AssignedTaskView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = TaskAssigned
    queryset = TaskAssigned.objects.filter(is_active=True, completion_status=False).order_by('-id')
    filterset_class = EmployeeAssignedTaskFilter
    template_name = 'employee/assigned_task.html'

    def get_queryset(self):
        return self.queryset.filter(assigned_to=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Assigned Task" 
        context["assigned_task"] = self.filterset_class(self.request.GET, queryset=self.get_queryset()) 
        return context


class AssginedTaskDetailsView(LoginRequiredMixin, EmployeePassesTestMixin, DetailView):
    model = TaskAssigned
    context_object_name = 'task'
    template_name = 'employee/assigned_task_details.html'

    def get_context_data(self, **kwargs):
        try:
            assigned_task=TaskAssigned.objects.get(id=self.kwargs['pk'])
        except Exception as e:
            print(e)

        context = super().get_context_data(**kwargs)
        context["title"] = "Assigned Task Details"
        context["feedbacks"] = TaskFeedback.objects.filter(feedback_of=assigned_task)
        return context


class TaskFeedbackView(LoginRequiredMixin, EmployeePassesTestMixin, CreateView):
    model = TaskAssigned
    context_object_name = 'task'
    form_class = TaskFeedbackForm
    template_name = 'employee/task_feedback.html'
    success_url = reverse_lazy('employee:assigned_task')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Task Feedback"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial['other_pk'] = self.kwargs['pk']
        return initial
    
    def form_valid(self, form):
        try:
            task_of=TaskAssigned.objects.get(id=self.kwargs['pk'])

            if form.is_valid():
                feed_back=form.save(commit=False)
                feed_back.feedback_of=task_of
                feed_back.feedback_by=self.request.user
                feed_back.save()
                messages.success(self.request, "Feedback given successfully")

            return super().form_valid(form)
        except Exception as e:
            print(e)
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something wrong feedback added Faild")
        return super().form_invalid(form)

class TaskCompletationReportView(LoginRequiredMixin, EmployeePassesTestMixin, UpdateView):
    model = TaskAssigned
    form_class = TaskCompletationForm
    template_name = 'employee/task_completation_report.html'
    success_url = reverse_lazy('employee:assigned_task')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Task Completation Report" 
        return context
    
    def form_valid(self, form):
        if form.is_valid():
            form_obj=form.save(commit=False)
            form_obj.completion_status = True
            form_obj.save()
            messages.success(self.request, "Task Completation Report Submited Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Some thing went worng please try again")
        return super().form_invalid(form)


class CompletedTaskListView(LoginRequiredMixin, EmployeePassesTestMixin, ListView):
    model = TaskAssigned
    queryset = TaskAssigned.objects.filter(is_active=True, completion_status=True).order_by('-id')
    filterset_class = EmployeeAssignedTaskFilter
    template_name = 'employee/completed_task_list.html'

    def get_queryset(self):
        return self.queryset.filter(assigned_to=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Completed Task" 
        context["assigned_task"] = self.filterset_class(self.request.GET, queryset=self.get_queryset()) 
        return context
    
        
    
    