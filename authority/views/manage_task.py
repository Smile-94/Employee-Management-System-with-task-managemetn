from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
import datetime 


#permission class
from django.contrib.auth.mixins import LoginRequiredMixin
from authority.permissions import AdminPassesTestMixin

# generic class 
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView


# models 
from authority.models import Task
from authority.models import TaskAssigned
from authority.models import TaskFeedback
from employee.models import EmployeeInfo

# forms
from authority.forms import TaskForm
from authority.forms import TaskAssignedForm
from authority.forms import TaskFeedbackForm

# Filters 
from authority.filters import TaskFilter
from authority.filters import TaskEmployeeFilter
from authority.filters import TaskAssignedFileter


class TaskCreateView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    queryset = Task.objects.filter(is_active=True).order_by('-id')
    filterset_class = TaskFilter
    template_name = 'authority/task_list.html'
    success_url = reverse_lazy('authority:add_task')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Task' 
        context["taskes"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context

    def form_valid(self, form):
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.create_by = self.request.user
            form_obj.save()
            messages.success(self.request, "Task Added Successfully")
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, "Task not added try again")
        return super().form_invalid(form)

class TaskDetailView(LoginRequiredMixin, AdminPassesTestMixin, DetailView):
    model = Task
    template_name = 'authority/task_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Task Details" 
        return context
    
    

class TaskUpdateView(LoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'authority/task_list.html'
    success_url = reverse_lazy('authority:add_task')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Task" 
        context["updated"] = True 
        return context

    def form_valid(self, form):
        messages.success(self.request, "Task Updated Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Something Wrong, Try again!')
        return super().form_invalid(form)


class TaskDeleteView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'authority/delete_task.html'
    success_url = reverse_lazy('authority:add_task')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Payroll Month" 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)


class EmployeeTaskListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = EmployeeInfo
    queryset = EmployeeInfo.objects.filter(is_active=True)
    filterset_class = TaskEmployeeFilter
    context_object_name = 'employees'
    template_name = 'authority/task_employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Employee List' 
        context["employees"] = self.filterset_class(self.request.GET, queryset=self.queryset)
        return context


class AssignTaskView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = TaskAssigned
    form_class = TaskAssignedForm
    template_name = 'authority/assigned_task.html'
    success_url = reverse_lazy('authority:task_employee_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Assigned Task" 
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial['other_pk'] = self.kwargs['pk']
        return initial
    
    def form_valid(self, form):
        task = form.cleaned_data.get('task_of')
        try:
            other_object = EmployeeInfo.objects.get(id=self.kwargs['pk'])

            if TaskAssigned.objects.filter(task_of=task, assigned_to=other_object.info_of,completion_status=False, is_active=True).exists():
                messages.warning(self.request, "Task is alredy assigned to this employee")
                return self.form_invalid(form)
        
            if form.is_valid():
                form_obj=form.save(commit=False)
                form_obj.assigned_to = other_object.info_of
                form_obj.assigned_by =self.request.user

                messages.success(self.request, "Task Assigned Successfully!")
                
            return super().form_valid(form)
        
        except Exception as e:
            print(e)
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong try again!")
        return super().form_invalid(form)

class EmployeeAssignedTaskListView(LoginRequiredMixin, AdminPassesTestMixin, ListView):

    Model = TaskAssigned
    queryset = TaskAssigned.objects.filter(is_active=True).order_by("-id")
    template_name = 'authority/employee_assigned_task.html'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = super().get_queryset().filter(assigned_to=pk)
        return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Assigned Task" 
        context["tasks"] = self.get_queryset() 
        return context

class AssignedTaskView(LoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = TaskAssigned
    queryset = TaskAssigned.objects.filter(is_active=True).order_by('-id')
    filterset_class = TaskAssignedFileter
    context_object_name = 'employees'
    template_name = 'authority/assigned_task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Assigned Task List"
        context["assigned_task"] = self.filterset_class(self.request.GET, queryset=self.queryset) 
        return context
    

class DeleteAssignedTaskView(LoginRequiredMixin, AdminPassesTestMixin, DeleteView):
    model = TaskAssigned
    context_object_name = 'task'
    template_name = 'authority/delete_assigned_task.html'
    success_url = reverse_lazy('authority:assigned_task')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Assigned  Task" 
        return context

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect(self.success_url)

class AssginedTaskDetailsView(LoginRequiredMixin, AdminPassesTestMixin, DetailView):
    model = TaskAssigned
    context_object_name = 'task'
    template_name = 'authority/assigned_task_details.html'

    def get_context_data(self, **kwargs):
        try:
            assigned_task=TaskAssigned.objects.get(id=self.kwargs['pk'])
        except Exception as e:
            print(e)

        context = super().get_context_data(**kwargs)
        context["title"] = "Assigned Task Details"
        context["feedbacks"] = TaskFeedback.objects.filter(feedback_of=assigned_task)
        return context

class TaskFeedbackView(LoginRequiredMixin, AdminPassesTestMixin, CreateView):
    model = TaskAssigned
    context_object_name = 'task'
    form_class = TaskFeedbackForm
    template_name = 'authority/task_feedback.html'
    success_url = reverse_lazy('authority:assigned_task')

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


class TaskStaticsView(LoginRequiredMixin, AdminPassesTestMixin, TemplateView):
     template_name = 'authority/task_statics.html'

     def get_context_data(self, **kwargs):
         today = datetime.date.today()
         complte_task = TaskAssigned.objects.filter(is_active=True, completion_status=True).count()
         incomplete_task = TaskAssigned.objects.filter(task_of__deadline__lt=today, completion_status=False).count()
         pending_task = TaskAssigned.objects.filter(task_of__deadline__gte=today, completion_status=False).count()
         context = super().get_context_data(**kwargs)
         context["title"] = "Task Chart"
         context["complete_task"] = complte_task
         context["incomplete_task"] = incomplete_task
         context["Pending_task"] = pending_task
         return context
     
    
    
    
    

    
    
