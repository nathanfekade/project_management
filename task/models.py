from django.db import models

class Task(models.Model):

    STATUS_CHOICES = [('to-do','TO-DO'), ('in progress', 'In Progress'), ('done', 'Done')]
    PRIORITY_CHOICES = [('low','Low'), ('medium', 'Medium'), ('high', 'High')]

    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="to-do")
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, default="low")

class Category(models.Model):
   
    title = models.CharField(max_length=100)
    tasks = models.ManyToManyField(Task, related_name='categories')

    