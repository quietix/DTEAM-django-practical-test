import io
import logging
import json
from pathlib import Path
from typing import Optional

from django.template.loader import get_template
from django.conf import settings

from openai import OpenAI

from xhtml2pdf import pisa
from xhtml2pdf.document import pisaContext

from main.enums import Language


logger = logging.getLogger(__name__)


def _load_prompt(filename: str) -> str:
    prompt_path = Path("main/prompts") / filename
    try:
        with open(prompt_path, "r") as f:
            return f.read().strip()
    except Exception as e:
        logger.error(f"Failed to load prompt file {filename}: {e}")
        raise e


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


def get_translated_text(cv: dict, lang: Language) -> dict:
    try:
        client = OpenAI(api_key=getattr(settings, "OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": _load_prompt("translation.txt"),
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

        return json.loads(translated_text)
    except Exception as e:
        logger.error(f"Translate CV Service Error: {e}")
        raise e


def translate_cv(cv: dict, lang: Language) -> Optional[dict]:
    logger.info(f"Translating CV to {lang.value}")
    try:
        translated_text = get_translated_text(cv, lang)
        return {
            "translated": translated_text,
        }
    except Exception as e:
        logger.error(f"Translate CV Service Error: {e}")
        raise e
