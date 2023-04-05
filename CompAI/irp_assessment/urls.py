from django.urls import path
from . import views 

urlpatterns = [
    path('<int:pk>/<str:stage>/', views.assessment, name= 'assessment'),
    # path('<int:pk>/design', views.assessmentDes, name= 'assessment'),
    # path('<int:pk>/development', views.assessmentDev, name= 'assessment'),
    # path('<int:pk>/evaluation', views.assessmentEval, name= 'assessment'),
    # path('<int:pk>/operation', views.assessmentOps, name= 'assessment'),
    # path('<int:pk>/retirement', views.assessmentRet, name= 'assessment'),
    # path('assessment/<int:pk>/', views.detail, name= 'detail')

] 