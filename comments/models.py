from django.db import models

# Create your models here.
from accounts.models import User
from blogs.models import BLog


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='student_comments')
    blog = models.ForeignKey(
        BLog, on_delete=models.CASCADE, related_name='student_blog_comment')

    @classmethod
    def get_blog_number_of_comments(cls, blog):
        return cls.objects.filter(blog=blog).count()
