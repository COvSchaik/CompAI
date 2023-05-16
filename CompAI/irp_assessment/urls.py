from django.urls import path
from . import views 

urlpatterns = [
    path('<int:pk>/<str:stage>/', views.assessment, name= 'assessment'),
] 