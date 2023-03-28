from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name="index"),
    path('index', views.index,name="index"),
     path("login",views.Login,name="login"),
    path("Logout",views.Logout,name='Logout'),
    path("Privacy",views.Privacy,name='Privacy'), 
]