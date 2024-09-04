from django.urls import path
from . import views
from .views import weekly_report, weekly_report_all

app_name = 'reports'
urlpatterns = [
    path("", views.index, name="home"),
    path("index", views.index),
    path('weekly-report/', weekly_report, name='weekly_report'),
    path('weekly-report-all/', weekly_report_all, name='weekly_report_all'),
    path('report/', views.alluser_report, name='alluser_report'),
]