"""Project Utilities. """
# Django

from django.http import HttpResponse
from django.template.loader import get_template
from django.core.serializers.json import DjangoJSONEncoder

# Xml to Pdf
from xhtml2pdf import pisa
from xhtml2pdf.config.httpconfig import httpConfig

# Utils
from io import BytesIO
import ssl


def render_to_pdf(template_src, context_dict={}):
    """Render pdf based on context dict"""
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None