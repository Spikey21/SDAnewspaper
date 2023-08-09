from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name='articles')

    def __str__(self) -> str:
        return f'{self.title} | {self.owner}'
    
