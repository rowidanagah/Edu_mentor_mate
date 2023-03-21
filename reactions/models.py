from django.db.models import Avg
from sessions.models import Session
from django.db import models

# Create your models here.
from accounts.models import Mentor, Student, User
from blogs.models import BLog


class Likes(models.Model):
    # idk if we can use normal(abs) User as a fkhere or nope ;)"
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reaction")

    blog = models.ForeignKey(BLog, related_name="blog_reaction",
                             on_delete=models.CASCADE)
    isLike = models.BooleanField(default=False)

    @classmethod
    def get_blog_likes(cls, blog):
        return cls.objects.filter(blog=blog, isLike=True)

    @classmethod
    def get_blog_number_of_likes(cls, blog):
        return cls.objects.filter(blog=blog, isLike=True).count()

    @classmethod
    def get_blog_disLikes(cls, blog):
        return cls.objects.filter(blog=blog, isLike=False)

    @classmethod
    def get_blog_number_of_disLikes(cls, blog):
        return cls.objects.filter(blog=blog, isLike=False).count()

    @classmethod
    def get_user_reaction_on_blog(cls, user):
        return cls.objects.filter(user=user)


class SessionRate(models.Model):
    rate = models.IntegerField(min=0, max=5, null=False, blank=False)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_rate_on_session")
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="session_rate")

    @classmethod
    def get_session_avg_rate(cls, session):
        session_rate_lst = cls.objects.filter(
            session=session)
        avg = round(session_rate_lst.aggregate(Avg("rate"))[
                    "score__avg"], 2) if session_rate_lst else 0
        return avg


# class MentorRate(models.Model):
#     rate = models.IntegerField(min=0, max=5, null=False, blank=False)
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name="user_rate_abt_mentor")
#     mentor = models.ForeignKey(
#         Mentor, on_delete=models.CASCADE, related_name="mentor_rate")

#     @classmethod
#     def get_session_avg_rate(cls, mentor):
#         mentor_rate_lst = cls.objects.filter(
#             mentor=mentor)
#         avg = round(mentor_rate_lst.aggregate(Avg("rate"))[
#                     "score__avg"], 2) if mentor_rate_lst else 0
#         return avg


class SessionFeedback(models.Model):
    class Meta:
        unique_together = (('student', 'session'),)

    massage = models.TextField(max_length=200, null=False, blank=False)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user feedback")
    session = models.ForeignKey(Session)

    @classmethod
    def get_user_feedback_about_session(cls, user):
        return cls.objects.filter(user=user)


# class MentorFeedback(models.Model):
#     massage = models.TextField(max_length=200, null=False, blank=False)
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name="student_feedback")
#     mentor = models.ForeignKey(
#         Mentor, on_delete=models.CASCADE, related_name="mentor_feedback")

#     @classmethod
#     def get_user_feedback_about_mentor(cls, student):
#         # list student feedback history
#         return cls.objects.filter(student=student)

#     @classmethod
#     def get_mentor_feedbacks(cls, mentor):
#         return cls.objects.filter(mentor=mentor)


# class Follow(models.Model):
#     class Meta:
#         unique_together = (('student', 'following_mentor'),)

#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name="student_follow")
#     # following_mentor = models.ManyToManyField(
#     #     Mentor, related_name="following_mentors")
#     following_mentor = models.ForeignKey(
#         Mentor, related_name="following_mentors")

#     @ classmethod
#     def get_student_followers(cls, student):
#         return cls.objects.filter(student=student)
