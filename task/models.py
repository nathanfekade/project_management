from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    STATUS_CHOICES = [('todo','TO-DO'), ('inprogress', 'In Progress'), ('done', 'Done')]
    PRIORITY_CHOICES = [('low','Low'), ('medium', 'Medium'), ('high', 'High')]

    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="to-do")
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, default="low")
    user = models.ForeignKey(User, related_name='task_user', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title','user'], name='unique_task_user')
        ]  


class Category(models.Model):
   
    title = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, related_name='categories')
    user = models.ForeignKey(User, related_name='category_user', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title','user'], name='unique_category_user')
        ]    


    