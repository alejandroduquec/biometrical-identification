"""Users URLs."""

# Django
from django.urls import path
from django.views.generic import TemplateView

# View
from users import views


urlpatterns = [
    # Management
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
]