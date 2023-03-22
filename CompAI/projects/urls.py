from django.urls import path
from . import views 

urlpatterns = [
    path('', views.projects, name= 'projects'),
    path('detail/<int:pk>/', views.detail, name= 'detail'),
    path('delete_assessment/<str:pk>', views.delete_assessment, name= 'delete_assessment'),

]