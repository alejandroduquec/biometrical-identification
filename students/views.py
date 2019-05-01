"""Students urls"""
# Django
from django.urls import path
from django.views.generic import DetailView, FormView, TemplateView
# Views
from students import views


class IndexView(TemplateView):
    """Index View"""
    template_name = 'base.html'