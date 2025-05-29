import logging
from celery import shared_task
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from main.models import CV
from main.services import render_to_pdf

logger = logging.getLogger(__name__)

@shared_task
def email_cv_to_user(cv_id: int, email: str):
    try:
        cv = get_object_or_404(CV, pk=cv_id)
        pdf_value = render_to_pdf("main/cv_pdf.html", {"cv": cv})

        if pdf_value:
            email_subject = f"CV - {cv.firstname} {cv.lastname}"
            email_body = (
                f"Please find attached the CV for {cv.firstname} {cv.lastname}."
            )

            email_message = EmailMessage(
                subject=email_subject, body=email_body, to=[email]
            )

            email_message.attach(
                f"cv_{cv.firstname}_{cv.lastname}.pdf", pdf_value, "application/pdf"
            )

            email_message.send()
            logger.info(f"CV sent to {email}")
            return f"CV successfully sent to {email}"
    except Exception as e:
        logger.error(f"Failed to send CV: {str(e)}")
        return f"Failed to send CV: {str(e)}"
