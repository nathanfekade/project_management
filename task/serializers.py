from rest_framework import serializers
from .models import Task

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
