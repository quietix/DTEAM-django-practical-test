from django.views.generic import ListView, DetailView
from main.models import CV


class CVListView(ListView):
    model = CV
    template_name = "main/cv_list.html"
    context_object_name = "cvs"
    ordering = ["lastname", "firstname"]


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"
