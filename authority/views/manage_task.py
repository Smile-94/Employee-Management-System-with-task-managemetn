from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


#permission class
from django.contrib.auth.mixins import LoginRequiredMixin

# generic class 
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView


# models 
from authority.models import Task
from authority.models import TaskAssigned
from employee.models import EmployeeInfo

# forms
from authority.forms import TaskForm
from authority.forms import TaskAssignedForm

# Filters 
from authority.filters import TaskFilter
from authority.filters import TaskEmployeeFilter


class TaskCreateView(LoginRequiredMixin, CreateView):
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
            form_obj=form.save(commit=False)
            form_obj.create_by= self.request.user
            form_obj.save()
            messages.success(self.request, "Task Added Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Task not added try again")
        return super().form_invalid(form)

class TaskDetailView(DetailView):
    pass

class TaskUpdateView(UpdateView):
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
        messages.error('Something Wrong, Try again!')
        return super().form_invalid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
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


class EmployeeTaskListView(LoginRequiredMixin, ListView):
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


class AssignTaskView(LoginRequiredMixin, CreateView):
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
        try:
            other_object = EmployeeInfo.objects.get(id=self.kwargs['pk'])
        
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
    
    

    
    
