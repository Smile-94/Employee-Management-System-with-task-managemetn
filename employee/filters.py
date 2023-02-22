import django_filters
from django import forms

# models
from authority.models import TaskAssigned
from authority.models import Task


class EmployeeAssignedTaskFilter(django_filters.FilterSet):

    task_of = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': 'Task ID'}))
    
    class Meta:
        model = TaskAssigned
        fields = ('task_of',)
    

    def filter_queryset(self, queryset):
        task_of_value = self.data.get('task_of')

        if task_of_value:
            task_obj = Task.objects.get(task_id=task_of_value)
            queryset = queryset.filter(task_of=task_obj)

        return queryset