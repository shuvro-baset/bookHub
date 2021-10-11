from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Books(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    description = models.TextField()
    uploaded_time = models.DateTimeField(auto_now=True)
    # choices = models.

class BooksReview(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=250, null=True, blank=True)
    star = models.IntegerField()

class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)
    img = models.ImageField()
    created_time = models.DateTimeField()
