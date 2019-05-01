""" Users view"""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.views.generic import DetailView, FormView, UpdateView
from django.urls import reverse_lazy

# Models
from django.contrib.auth.models import User
from users.models import Profile


class LoginView(auth_views.LoginView):
    """Login view"""
    template_name = 'users/login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """logout view"""
    template_name = 'users/logout.html'
