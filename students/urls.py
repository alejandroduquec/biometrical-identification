"""Students url"""
# Django
from django.urls import path

from students import views

urlpatterns = [
    path(
        route='',
        view=views.IndexView.as_view(),
        name='index'),
    path(
        route='busqueda/',
        view=views.SearchStudent.as_view(),
        name='search'),

    path(
        route='registrar/',
        view=views.RegisterStudent.as_view(),
        name='register'),
    path(
        route='total/',
        view=views.ReportStudents.as_view(),
        name='report'),
    path(
        route='reportes/',
        view=views.ReportRationsView.as_view(),
        name='ration-reports'),
    path(
        route='raciones/',
        view=views.FoodRationsView.as_view(),
        name='rations'),
    path(
        route='eliminar-estudiante/<int:pk>/',
        view=views.DeleteStudentView.as_view(),
        name='delete'),
    path(
        route='generate-pdf/',
        view=views.GeneratePDFView.as_view(),
        name='generate-pdf'),
        




    # path(
    #     route='posts/detail/<int:pk>/',
    #     view=views.DetailPostView.as_view(),
    #     name='detail_post'),
]
