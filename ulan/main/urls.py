from django.urls import path
from .views import (KroyListView, KroyCreateView, KroyUpdateView, KroyDetailListView,
                    KroyDetailCreateView, KroyDetailUpdateView, create_masterdata, MasterdataListView,
                    MdataKroyDetailView, MasterdatauserListView)

from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("index", views.index),

    path('kroy/', KroyListView.as_view(), name='kroy-list'),
    path('kroy/create/', KroyCreateView.as_view(), name='kroy-create'),
    path('<int:kroy_id>/', views.KroyDetailView, name='kroy-detail-view'),
    path('kroy/update/<int:pk>/', KroyUpdateView.as_view(), name='kroy-update'),
    path('kroy-detail/', KroyDetailListView.as_view(), name='kroy-detail-list'),
    path('kroy-detail/create/', KroyDetailCreateView.as_view(), name='kroy-detail-create'),
    path('kroy-detail/update/<int:pk>/', KroyDetailUpdateView.as_view(), name='kroy-detail-update'),
    path('create_masterdata', views.create_masterdata, name='create_masterdata'),
    #path('add_masterdata', views.add_masterdata, name='add_masterdata'),
    path('masterdata', MasterdataListView.as_view(), name='masterdata_list'),
    path('masterdatauser', views.MasterdatauserListView, name='masterdatauser_list'),
    path('<int:kroy_id>/', views.MdataKroyDetailView, name='mdata-kroy-detail-view'),



    # Changed the URL path to a different name

]

