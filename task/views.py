from .models import Task
from .serializers import TaskSerializer
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