"""Students urls"""
# Django
from django.shortcuts import render, redirect
from django.urls import path
from django.views.generic import (
    DetailView,
    FormView,
    TemplateView,
    CreateView,
    DeleteView
)
from django.db.models import Q, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Count
from django.utils import timezone
from django.template.loader import get_template
from django.conf import settings
from django.template import Context

# Views
from students import views

# Model
from students.models import Student, DactilarIdentification, FoodRation, Institution

# Forms
from students.forms import SearchStudentForm, RegisterStudentForm

# Utils
import sweetify
from students.utils import render_to_pdf
import calendar
import datetime
import os
from xhtml2pdf import pisa

weekend = ['Saturday', 'Sunday']


class IndexView(LoginRequiredMixin, TemplateView):
    """Index View"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """add data  to context"""
        context = super().get_context_data(**kwargs)
        students = Student.objects
        dactilar = DactilarIdentification.objects
        user_intitution = self.request.user.profile.institution
        if user_intitution:
            total_students_by_instit = students.filter(
                institution=user_intitution)
            context['total_students'] = total_students_by_instit.count()
            context['total_students_registered'] = dactilar.filter(
                id__in=total_students_by_instit).count()
            active_user = (
                context['total_students_registered']/context['total_students'])*100
            context['users_active'] = round(active_user, 2)
        else:
            context['total_students'] = students.all().count()
            context['total_students_registered'] = students.filter(
                id__in=dactilar.all()).count()
            active_user = (
                context['total_students_registered']/context['total_students'])*100
            context['users_active'] = round(active_user, 2)
        return context


def identification_name(student_data):
    """Search user by firstname or lastname
    [student_data]:user name or lastname
    """
    if student_data.isnumeric():
        students = Student.objects.filter(
            Q(document__icontains=student_data))
    else:
        data = student_data.split(' ')
        if len(data) > 1:
            first_name = data[0]
            last_name = data[1]
            students = Student.objects.filter(
                Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name))
        else:
            students = Student.objects.filter((
                Q(first_name__icontains=student_data) |
                Q(last_name__icontains=student_data) |
                Q(document__icontains=student_data)))
    return students


def exclude_institution(inst):
    """Switch id to exclude institution"""
    if inst.id == 1:
        return 2
    else:
        return 1


class SearchStudent(LoginRequiredMixin, FormView):
    template_name = 'search.html'
    form_class = SearchStudentForm

    def post(self, request, *args, **kwargs):
        """On post to do"""
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            student_data = data.get('student')
            user_institution = request.user.profile.institution
            students = identification_name(student_data)
            if user_institution:
                students = students.exclude(institution=exclude_institution(user_institution))
            if students:
                sweetify.success(
                    request, 'Éxito', text='La busqueda ha finalizado', persistent='Listo')
            else:
                sweetify.error(
                    request, 'Sin Resultado', text='La busqueda ha finalizado', persistent='Listo')
            return render(request, 'search.html', {'form': form, 'students': students})

        else:
            return self.form_invalid(form)


class RegisterStudent(LoginRequiredMixin, CreateView):
    """Register user"""
    template_name = 'register.html'
    form_class = RegisterStudentForm
    success_url = reverse_lazy('students:index')

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        form.save()
        sweetify.success(self.request, 'Registro Exitoso',
                         text='El estudiante ha sido registrado.',
                         persistent='Listo')
        return HttpResponseRedirect(self.success_url)


class ReportStudents(LoginRequiredMixin, TemplateView):
    """Index View"""
    template_name = 'report.html'

    def get_context_data(self, **kwargs):
        """add data  to context"""
        context = super().get_context_data(**kwargs)
        user_institution = self.request.user.profile.institution
        if user_institution:
            students = Student.objects.filter(institution=user_institution.id)
        else:
            students = Student.objects.all()

        context['students'] = students
        return context


class DeleteStudentView(LoginRequiredMixin, DeleteView):
    """Delete Student"""
    template_name = 'users/delete_user.html'
    context_object_name = 'object'

    def get_object(self, queryset=None):
        """Get object to delete"""
        obj = Student.objects.get(pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        """Return to list of  naturaleza"""
        sweetify.success(self.request, 'Usuario eliminado.')
        return reverse_lazy('students:search')


class FoodRationsView(LoginRequiredMixin, TemplateView):
    """Food rations View"""
    template_name = 'rations.html'

    def get_context_data(self, **kwargs):
        """add data  to context"""
        context = super().get_context_data(**kwargs)
        students = Student.objects
        dactilar = DactilarIdentification.objects
        user_institution = self.request.user.profile.institution        
        if user_institution:
            total_students_by_instit = students.filter(
                institution=user_institution)
            context['total_students_registered'] = dactilar.filter(
                id__in=total_students_by_instit).count()
            context['total_rations'] = FoodRation.objects.filter(
                student__in=total_students_by_instit
            ).count()
            context['breakfast'] = FoodRation.objects.filter(
                food_type=1,
                student__in=total_students_by_instit
                ).count()
            context['lunch'] = context['total_rations'] - context['breakfast']

            
        else:
            context['total_students_registered'] = students.filter(
                id__in=dactilar.all()).count()
            context['total_rations'] = FoodRation.objects.all().count()
            context['breakfast'] = FoodRation.objects.filter(
                food_type=1).count()
            context['lunch'] = context['total_rations'] - context['breakfast']

        institution_counter = FoodRation.objects.select_related('id')\
            .all()\
            .annotate(name=F('student__institution__name'))\
            .values('name')\
            .annotate(user_count=Count('name'))
        average = 0
        if len(institution_counter) > 1:
            for inst in list(institution_counter):
                average += inst['user_count']
            institution_counter[0]['user_count'] = round(
                (institution_counter[0]['user_count']/average)*100, 1)
            institution_counter[1]['user_count'] = round(
                (institution_counter[1]['user_count']/average)*100, 1)
        context['institutions_data'] = institution_counter

        return context


class ReportRationsView(LoginRequiredMixin, TemplateView):
    """Reports for food ration View"""
    template_name = 'ration-report.html'

    def get_context_data(self, **kwargs):
        """add data  to context"""
        context = super().get_context_data(**kwargs)
        user_institution = self.request.user.profile.institution        
        if user_institution:
            total_students_by_instit = Student.objects.filter(
                institution=user_institution)
            rations = FoodRation.objects.filter(student__in=total_students_by_instit)
        else:
            rations = FoodRation.objects.all()

        context['rations'] = rations
        return context


def GeneratePDFView(request):
    """Generate PDF Reports"""
    month = timezone.now().month
    institution = Institution.objects.get(id=2)
    # Get week days for month
    max_days = calendar.monthrange(2019, timezone.now().month)[1]
    week_days = []
    for day in range(1, max_days+1):
        evaluated_day = '2019-{}-{}'.format(month, day)
        name_day = datetime.datetime.strptime(evaluated_day, '%Y-%m-%d').strftime("%A")
        if not name_day in weekend:
            week_days.append(datetime.datetime.strptime(evaluated_day, '%Y-%m-%d'))
    if len(week_days) < 23:
        for i in range(len(week_days), 23):
            week_days.append(0)
    
    user_array = []
    students_food = FoodRation.objects.values('student').filter(student__institution=institution)
    students = Student.objects.filter(id__in=students_food).distinct()
    for student in students:
        user_food_days = week_days.copy()
        dates = FoodRation.objects.values('food_time').filter(student=student.pk, food_type=2).order_by('-food_time')
        if dates:  
            for date in dates:
                current = date['food_time'].replace(hour=0, minute=0, second=0, tzinfo=None)
                if current in user_food_days:
                    index = user_food_days.index(current)
                    user_food_days[index] = 'X'
            user_dict = {
                'student': student,
                'user_food_days': user_food_days,
                'type_food': 'CAJT',
                'total': dates.count()

            }
            user_array.append(user_dict)

    #students = FoodRation.objects.annotate(food=Count('student'), aas=Count('food_type')).order_by('food_type')
    
    context = {
        'departament': 'Antioquia',
        'institution': institution,
        'month': timezone.now(),
        'week_days': week_days,
        'user_array': user_array
    }

    template_path = 'format/food.html'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

