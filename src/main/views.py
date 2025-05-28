from django.views.generic import ListView, DetailView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from main.models import CV
from main.serializers import CVSerializer
from main.services import render_to_pdf


class CVListView(ListView):
    model = CV
    template_name = "main/cv_list.html"
    context_object_name = "cvs"
    ordering = ["lastname", "firstname"]


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"


def cv_to_pdf(request: HttpRequest, id: int):
    if request.method == "POST":
        cv = get_object_or_404(CV, id=id)
        pdf_value = render_to_pdf("main/cv_pdf.html", {"cv": cv})
        response = HttpResponse(pdf_value, content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=cv.pdf"
        return response
    return HttpResponse("Failed to download CV.", code=400)


class CVViewSet(ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
