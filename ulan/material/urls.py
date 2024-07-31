from django.urls import path
from . import views

urlpatterns = [
    path('', views.malzeme_listesi, name='malzeme_listesi'),
    path('malzeme/<int:pk>/', views.malzeme_detayi, name='malzeme_detayi'),
    path('giris/', views.malzeme_giris, name='malzeme_giris'),
    path('cikis/', views.malzeme_cikis, name='malzeme_cikis'),
    path('kaydet/', views.malzeme_kaydet, name='malzeme_kaydet'),
]