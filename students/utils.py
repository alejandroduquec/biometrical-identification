"""Project Utilities. """
# Django

from django.http import HttpResponse
from django.template.loader import get_template

# Xml to Pdf
from xhtml2pdf import pisa

# Utils
from io import BytesIO


def render_to_pdf(template_src, context_dict={}):
    """Render pdf based on context dict."""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # Only to render
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    return result
