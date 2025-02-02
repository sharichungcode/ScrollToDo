from django.db import models
from django.contrib.auth.models import User

class TaskList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class ItemList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    item_list = models.CharField(max_length=255, default='default_value')  # Replace 'default_value' with your desired default
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title