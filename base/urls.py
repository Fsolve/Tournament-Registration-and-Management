from django.urls import path
from . import views

 

urlpatterns = [
    path('', views.home, name='home' ),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('createTeam/', views.createTeam, name='create-team'),
    path('toornament/<str:pk>', views.toornament, name='toornament'),
    path('participate/<str:pk>', views.participate, name='participate'),

]

