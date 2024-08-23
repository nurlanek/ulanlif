from django.urls import path
from . import views

app_name = 'material'

urlpatterns = [
    path('', views.malzeme_listesi, name='malzeme_listesi'),
    path('edit/<int:pk>/', views.malzeme_edit, name='malzeme_edit'),
    path('delete/<int:pk>/', views.malzeme_delete, name='malzeme_delete'),
    path('malzeme/<int:pk>/', views.malzeme_detayi, name='malzeme_detayi'),
    path('giris/', views.malzeme_giris, name='malzeme_giris'),
    path('cikis/', views.malzeme_cikis, name='malzeme_cikis'),
    path('kaydet/', views.malzeme_kaydet, name='malzeme_kaydet'),
]