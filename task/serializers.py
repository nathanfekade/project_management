from rest_framework import serializers
from .models import Task, Category

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user',)
    
    def create(self, validated_data):
        task = Task(**validated_data)

        try:
            task.full_clean()
        except serializers.ValidationError as e:
            raise

        task.save()
        return task
    
    def update(self, instance, validated_data):
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        try:
            instance.full_clean()
        except serializers.ValidationError as e:
            raise

        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):

    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['title', 'user', 'tasks']
        read_only_fields = ('user',)

    def get_tasks(self, obj):
        tasks_instances = obj.tasks.all()
        return[{"title": a.title, "status": a.status }for a in tasks_instances]
    
    def create(self, validated_data):
        category = Category(**validated_data)

        try: 
            category.full_clean()
        except serializers.ValidationError as e:
            raise

        category.save()
        return category
    
    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        try:
            instance.full_clean()
        except serializers.ValidationError as e:
            raise

        instance.save()
        return instance