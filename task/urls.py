from django.urls import path
from task import views

urlpatterns = [ 
    path('', views.TaskList.as_view(), name='task-list'),
    path('<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),

]