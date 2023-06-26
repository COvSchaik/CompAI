from django.urls import path
from . import views 

urlpatterns = [
    path('', views.esc, name= 'esc'),
    path('esctemp/<int:pk>/', views.esctemp, name= 'esctemp'),
    path('delete_esc/<str:pk>', views.delete_esc, name= 'delete_esc'),
    path('<str:pk>/', views.create_esc, name= 'create_esc'),
] 