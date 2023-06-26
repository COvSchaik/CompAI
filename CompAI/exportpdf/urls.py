from django.urls import path
from . import views 

urlpatterns = [    
    path('sds/<str:pk>/', views.sds_pdf, name= 'sds_pdf'),
    path('esc/<str:pk>/', views.esc_pdf, name= 'esc_pdf'),
] 