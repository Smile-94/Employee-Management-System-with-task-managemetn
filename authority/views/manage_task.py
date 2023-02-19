from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


#permission class
from django.contrib.auth.mixins import LoginRequiredMixin

# generic class 
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


# models 
from authority.models import Task

# forms
from authority.forms import TaskForm

# Filters 
from authority.filters import TaskFilter


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
    
    
