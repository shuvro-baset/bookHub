from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Books(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.FileField(upload_to='pdf')
    book_thumbnail = models.ImageField(upload_to='pdf/thumbnails', null=True)
    book_name = models.CharField(max_length=200, null=True)
    language = models.CharField(max_length=100, null=True)
    author_name = models.CharField(max_length=200, null=True)
    description = models.TextField()
    uploaded_time = models.DateTimeField(auto_now=True)
    book_category = models.CharField(max_length=1000, null=True)
    book_rating = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.book_name + '.pdf'

class BooksReview(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=250, null=True, blank=True)
    star = models.IntegerField(default=0, null=True)

class Blogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='blog_img')
    created_time = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title