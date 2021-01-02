from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """Post added by user"""
    title = models.CharField(max_length=160)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comments to Post added by users"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=240)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return f"{self.text[:40]}..."
