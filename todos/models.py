from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Todo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    body = models.TextField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo_detail', kwargs={'pk': self.id})


