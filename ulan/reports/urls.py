from django.urls import path
from . import views
from .views import weekly_report

app_name = 'reports'
urlpatterns = [
    path("", views.index, name="home"),
    path("index", views.index),
    path('weekly-report/', weekly_report, name='weekly_report'),
]