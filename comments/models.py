from django.db import models

# Create your models here.
from accounts.models import User
from blogs.models import BLog


class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='student_comments')
    blog = models.ForeignKey(
        BLog, on_delete=models.CASCADE, related_name='student_blog_comment')
