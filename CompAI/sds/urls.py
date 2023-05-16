from django.urls import path
from . import views 

urlpatterns = [
    path('', views.sds, name= 'sds'),
    path('temp/<int:pk>/', views.temp, name= 'temp'),
    path('delete_temp/<str:pk>', views.delete_temp, name= 'delete_temp'),
    path('<str:pk>/', views.create_sds, name= 'create_sds'),
] 