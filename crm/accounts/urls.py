from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('', views.home,name="home"),
    path('user/', views.userPage, name="user-page"),
    path('doctors/',views.Doctors,name="doctors"),
    path('patient/<str:pk>',views.patient,name="patient"),
    path('available/', views.available, name="available"),
    path('create_order/<str:pk>', views.CreateAPT, name="create_order"),
    path('update_order/<str:pk>/', views.updateAPT, name="update_order"),
    path('delete_order/<str:pk>/', views.cancelAPT, name="delete_order"),
]