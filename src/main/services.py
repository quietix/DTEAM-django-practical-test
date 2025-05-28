import io
from typing import Optional
from xhtml2pdf import pisa
from django.template.loader import get_template
from xhtml2pdf.document import pisaContext


def render_to_pdf(template_src, context) -> Optional[bytes]:
    template = get_template(template_src)
    html = template.render(context)
    result = io.BytesIO()

    html_str = html if isinstance(html, str) else str(html)
    pdf = pisa.pisaDocument(
        io.BytesIO(html_str.encode('UTF-8')),
        result
    )
    
    if isinstance(pdf, pisaContext) and not pdf.err:
        pdf_value = result.getvalue()
        result.close()
        return pdf_value
    
    raise Exception("Failed to render PDF")
