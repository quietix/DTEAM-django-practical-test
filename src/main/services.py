import io
import logging
import json
from typing import Optional

from django.template.loader import get_template
from django.conf import settings

from openai import OpenAI

from xhtml2pdf import pisa
from xhtml2pdf.document import pisaContext

from main.enums import Language


logger = logging.getLogger(__name__)


def render_to_pdf(template_src, context) -> Optional[bytes]:
    template = get_template(template_src)
    html = template.render(context)
    result = io.BytesIO()

    html_str = html if isinstance(html, str) else str(html)
    pdf = pisa.pisaDocument(io.BytesIO(html_str.encode("UTF-8")), result)

    if isinstance(pdf, pisaContext) and not pdf.err:
        pdf_value = result.getvalue()
        result.close()
        return pdf_value

    raise Exception("Failed to render PDF")


def translate_cv(cv: dict, lang: Language) -> Optional[dict]:
    logger.info(f"Translating CV to {lang.value}")
    try:
        client = OpenAI(api_key=getattr(settings, "OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that translates text from English "
                        "to the specified language. Return only the translated text in JSON "
                        "format without any additional notes or comments."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Translate the following text to {lang.value}: {cv}",
                },
            ],
        )

        translated_text = response.choices[0].message.content
        if not translated_text:
            logger.error(
                "Failed to get translated text: no `response.choices[0].message.content` found"
            )
            raise Exception("Failed to get translated text")

        return {
            "original": cv,
            "translated": json.loads(translated_text),
            "language": lang.name,
        }
    except Exception as e:
        logger.error(f"Translate CV Service Error: {e}")
        return None
