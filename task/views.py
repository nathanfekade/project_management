from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, AddTasksToCategoryByTitleSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

class TaskList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.filter(user= request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TaskSerializer, responses={201: TaskSerializer})
    def post(self, request, format=None):
        serializer = TaskSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save(user= request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(Task, pk=pk, user=request.user)
    
    def get(self, request, pk, format=None):
        task = self.get_object(request, pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=TaskSerializer, responses={200: TaskSerializer})
    def put(self, request, pk, format=None):
        task = self.get_object(request, pk)
        serializer = TaskSerializer(task, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        task = self.get_object(request, pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        categories = Category.objects.filter(user = request.user)
        serializer = CategorySerializer(categories, many= True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=CategorySerializer, responses={201: CategorySerializer})
    def post(self, request, format=None):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(Category, pk=pk, user=request.user)
    
    def get(self, request, pk, format=None):
        category = self.get_object(request, pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=CategorySerializer, responses={200: CategorySerializer})
    def put(self, request, pk, format=None):
        category = self.get_object(request, pk)
        serializer = CategorySerializer(category, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        category = self.get_object(request, pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddTasksToCategory(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        
        category = get_object_or_404(Category, id=category_id, user=request.user)
        available_tasks = Task.objects.filter(user=request.user).exclude(id__in=category.tasks.all())

        serializer = TaskSerializer(available_tasks, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=AddTasksToCategoryByTitleSerializer, responses={200: "Task added successfully"})
    def post(self, request, category_id):

        category = get_object_or_404(Category, id=category_id, user=request.user)

        serializer = AddTasksToCategoryByTitleSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            tasks = serializer.validated_data['task_titles']
            category.tasks.add(*tasks)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AddTasksToCategoryByTitleSerializer, responses={200: "Tasks removed successfully"})
    def delete(self, request, category_id):

        category = get_object_or_404(Category, id=category_id, user=request.user)
        serializer = AddTasksToCategoryByTitleSerializer(data=request.data, context={"user": request.user})

        if serializer.is_valid():
            tasks_to_remove = serializer.validated_data['task_titles']
            tasks_in_category = category.tasks.filter(id__in=[task.id for task in tasks_to_remove])

            if not tasks_in_category.exists():
                return Response({"status":"The specified tasks are not in this category"},status=status.HTTP_400_BAD_REQUEST)
            
            category.tasks.remove(*tasks_in_category)

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)