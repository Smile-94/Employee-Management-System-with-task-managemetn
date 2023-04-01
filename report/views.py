from django.shortcuts import render
from django_xhtml2pdf.views import PdfMixin

# Create your views here.
# for generating pdf
from django.views.generic.detail import DetailView
from django.conf import settings

# Models
from authority.models import TaskAssigned


class TaskPdfView(PdfMixin, DetailView):
    model = TaskAssigned
    context_object_name = 'task'
    template_name = "report/task_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['static_url'] = self.request.build_absolute_uri(settings.STATIC_URL)
        return context
    
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        filename = "report_{0}.pdf".format(self.object.pk)
        response['Content-Disposition'] = 'filename="{}"'.format(filename)
        return response
