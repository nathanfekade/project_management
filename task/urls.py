from django.urls import path
from task import views

urlpatterns = [ 
    path('task/', views.TaskList.as_view(), name='task-list'),
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
    path('category/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('categories/<int:category_id>/tasks', views.AddTasksToCategory.as_view(), name='tasks-to-category')

]