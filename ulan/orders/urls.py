from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.order_add, name='order_add'),
    path('edit/<int:pk>/', views.order_edit, name='order_edit'),
    path('delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('orderitem_list/', views.orderitem_list, name='orderitem_list'),
    path('orderitem_list/<int:order_id>/', views.orderitem_list_by_order, name='orderitem_list_by_order'),
    path('item/add/<int:order_id>/', views.orderitem_add, name='orderitem_add'),
    path('item/edit/<int:pk>/', views.orderitem_edit, name='orderitem_edit'),
    path('item/delete/<int:pk>/', views.orderitem_delete, name='orderitem_delete'),
]
