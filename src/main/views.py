from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages

from rest_framework.viewsets import ModelViewSet

from main.models import CV
from main.serializers import CVSerializer
from main.services import render_to_pdf, translate_cv
from main.tasks import email_cv_to_user
from main.enums import Language


class CVListView(ListView):
    model = CV
    template_name = "main/cv_list.html"
    context_object_name = "cvs"
    ordering = ["lastname", "firstname"]


class CVDetailView(DetailView):
    model = CV
    template_name = "main/cv_detail.html"
    context_object_name = "cv"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["languages"] = [(lang.value, lang.name) for lang in Language]
        context["translated_cv"] = self.request.session.pop("translated_cv", None)
        return context


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


class SettingsView(TemplateView):
    template_name = "main/settings.html"


def send_cv_email(request: HttpRequest, id: int):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Email is required")
            return redirect("main:cv-detail", pk=id)

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address")
            return redirect("main:cv-detail", pk=id)

        email_cv_to_user.delay(id, email)
        messages.success(request, "Email is being sent")
        return redirect("main:cv-detail", pk=id)

    messages.error(request, "Method not allowed")
    return redirect("main:cv-detail", pk=id)


def translate_cv_view(request: HttpRequest, id: int):
    if request.method == "POST":
        cv_dict = CV.objects.filter(id=id).values().first()
        if not cv_dict:
            messages.error(request, "CV not found")
            return redirect("main:cv-list")

        lang = request.POST.get("lang")
        if not lang:
            messages.error(request, "Language is required")
            return redirect("main:cv-detail", pk=id)

        if not Language.exists(lang):
            messages.error(request, "Invalid language")
            return redirect("main:cv-detail", pk=id)

        try:
            translated_text = translate_cv(cv_dict, Language(lang))
            if translated_text:
                messages.success(request, "CV has been translated successfully")
                request.session["translated_cv"] = translated_text
                return redirect("main:cv-detail", pk=id)
            else:
                messages.error(request, "Translation failed")
        except Exception as e:
            messages.error(request, f"Translation error: {str(e)}")

        return redirect("main:cv-detail", pk=id)

    messages.error(request, "Method not allowed")
    return redirect("main:cv-detail", pk=id)
