from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import (KroyListView, KroyCreateView, KroyUpdateView, KroyDetailListView, KroyDeleteView,
                    KroyDetailCreateView, KroyDetailUpdateView, MasterdataListView, masterdatauser,
                    operation_code_create, operation_code_update, operation_code_delete, KroyDetailView,
                    KroyDetailDeleteView, get_operation_codes, get_operation_list, users)
app_name = 'main'

urlpatterns = [
    #path("", views.index, name="home"),
    path("index", views.index),

    path('users/', users, name='users'),

    path('kroy/', KroyListView.as_view(), name='kroy-list'),
    path('kroy/create/', KroyCreateView.as_view(), name='kroy-create'),
    path('kroy/update/<int:pk>/', KroyUpdateView.as_view(), name='kroy-update'),
    path('kroy/delete/<int:pk>/', KroyDeleteView.as_view(), name='kroy-delete'),

    path('<int:kroy_id>/', views.KroyDetailView, name='kroy-detail-view'),
    path('kroy-detail/', KroyDetailListView.as_view(), name='kroy-detail-list'),
    path('kroy-detail/create/<int:kroy_id>', KroyDetailCreateView.as_view(), name='kroy-detail-create'),
    path('kroy-detail/update/<int:pk>/', KroyDetailUpdateView.as_view(), name='kroy-detail-update'),
    path('kroy-detail/delete/<int:pk>/', KroyDetailDeleteView.as_view(), name='kroy-detail-delete'),
    path('kroy-detail/<int:kroy_id>/', KroyDetailView, name='kroy-detail-view'),



    #path('kroy_details/<int:pk>/', views.KroyDetailView, name='kroy-detail-view'),

    #path('kroy_details/new/<int:kroy_id>/', KroyDetailCreateView.as_view(), name='kroy-detail-create'),
    #path('kroy_details/<int:pk>/', views.KroyDetailView, name='kroy-detail-view'),
    path('masterdata', MasterdataListView.as_view(), name='masterdata_list'),

    #Users page
    #path('main/masterdatauser/', views.masterdatauser_view, name='masterdatauser'),
    path('masterdatauser/', views.masterdatauser, name='masterdatauser'),
    path('get_operation_codes/', get_operation_codes, name='get_operation_codes'),
    path('get_operation_list/', get_operation_list, name='get_operation_list'),
    path('get_operation_price', views.get_operation_price, name='get_operation_price'),

    #Operations
    path('operation_code/create/', views.operation_code_create, name='operation_code_create'),
    path('operation_code/<int:pk>/update/', views.operation_code_update, name='operation_code_update'),
    path('operation_code/<int:pk>/delete/', views.operation_code_delete, name='operation_code_delete'),
    path('operation_code/', views.operation_code_list, name='operation_code_list'),
    path('operation_code/<int:operation_code_id>/operations/', views.operation_list_detail, name='operation_list_detail'),
    path('operation_code/<int:operation_code_id>/operations/create/', views.operation_list_create, name='operation_list_create'),
    path('operation_code/operations/<int:pk>/edit/', views.operation_list_update, name='operation_list_update'),
    path('operation_code/operations/<int:pk>/delete/', views.operation_list_delete, name='operation_list_delete'),
    path('operation-list/<int:operation_code_id>/', views.OperationListView, name='operation_list'),

    #kroy+operation naznachenie operatsii
    path('opercode/', views.kroy_operation_code_list, name='kroy_operation_code_list'),
    path('opercode/new/', views.kroy_operation_code_create, name='kroy_operation_code_create'),
    path('opercode/<int:pk>/edit/', views.kroy_operation_code_edit, name='kroy_operation_code_edit'),
    path('opercode/<int:pk>/delete/', views.kroy_operation_code_delete, name='kroy_operation_code_delete'),
]


