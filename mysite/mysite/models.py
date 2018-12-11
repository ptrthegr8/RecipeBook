from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Bio = models.TextField(max_length=300)

    def __str__(self):
        return self.Name

class Recipe(models.Model):
    Title = models.CharField(max_length=100)
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    Description = models.CharField(max_length=250)
    Time_Required = models.CharField(max_length=50)
    Instructions = models.TextField(max_length=2000)

    def __str__(self):
        return self.Title