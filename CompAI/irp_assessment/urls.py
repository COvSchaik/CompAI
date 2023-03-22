from django.urls import path
from . import views 

urlpatterns = [
    path('<int:pk>/', views.assessment, name= 'assessment'),
    # path('assessment/<int:pk>/', views.detail, name= 'detail')

] 