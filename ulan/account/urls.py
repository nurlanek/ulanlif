from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [

    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name="logout"),
    path('user-logout/', views.user_logout_request, name='user_logout'),
    path('masterdata_login/', views.masterdata_login, name='masterdata_login'),

]
