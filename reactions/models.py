from tags.models import Tags
from django.db.models import Avg
from roomsession.models import RoomSession
from django.db import models

# Create your models here.
from accounts.models import User
from blogs.models import BLog


class Likes(models.Model):
    # idk if we can use normal(abs) User as a fk here or nope ;)"
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reaction")

    blog = models.ForeignKey(BLog, related_name="blog_reaction",
                             on_delete=models.CASCADE)
    isLike = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'blog']

    def __str__(self):
        return str(str(self.user) + ' likes ' + str(self.blog))

    @classmethod
    def get_blog_likes(cls, blog):
        return cls.objects.filter(blog=blog, isLike=True)

    @classmethod
    def get_blog_number_of_likes(cls, blog):
        return cls.objects.filter(blog=blog, isLike=True).count()

    @classmethod
    def toggle_like(cls, obj):
        obj.isLike = not obj.isLike
        obj.save()
        return obj

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
    def get_user_reaction_on_blog(cls, user, blog):
        return cls.objects.get(user=user, blog=blog)


class SessionRate(models.Model):
    rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=False, null=False)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_rate_on_session")
    session = models.ForeignKey(
        RoomSession, on_delete=models.CASCADE, related_name="session_rate")

    @classmethod
    def get_session_avg_rate(cls, session):
        session_rate_lst = cls.objects.filter(
            session=session)
        avg = round(session_rate_lst.aggregate(Avg("rate"))[
                    "score__avg"], 2) if session_rate_lst else 0
        return avg


class MentorRate(models.Model):
    rate = models.DecimalField(
        max_digits=5, decimal_places=2, blank=False, null=False)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_rate_abt_mentor")
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentor_rate")

    @classmethod
    def get_session_avg_rate(cls, mentor):
        mentor_rate_lst = cls.objects.filter(
            mentor=mentor)
        avg = round(mentor_rate_lst.aggregate(Avg("rate"))[
                    "score__avg"], 2) if mentor_rate_lst else 0
        return avg


class SessionFeedback(models.Model):
    class Meta:
        unique_together = (('student', 'session'),)

    massage = models.TextField(max_length=200, null=False, blank=False)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_feedback")
    session = models.ForeignKey(
        RoomSession, related_name='session_feedback', on_delete=models.CASCADE)

    @classmethod
    def get_user_feedback_about_session(cls, user):
        return cls.objects.filter(user=user)


class MentorFeedback(models.Model):
    massage = models.TextField(max_length=200, null=False, blank=False)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="student_feedback")
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentor_feedback")

    class Meta:
        unique_together = ['student', 'mentor']

    @classmethod
    def get_user_feedback_about_mentor(cls, student, mentor):
        # list student feedback history
        return cls.objects.filter(student=student, mentor=mentor)

    @classmethod
    def get_mentor_feedbacks(cls, mentor):
        # get mentor list of feedbacks
        return cls.objects.filter(mentor=mentor)


class Follow(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="student_follow")
    # following_mentor = models.ManyToManyField(
    #     Mentor, related_name="following_mentors")
    following_mentor = models.ForeignKey(
        User, related_name="following_mentors",  on_delete=models.CASCADE)
    isfollow = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'following_mentor']

    def __str__(self):
        return str(str(self.student) + ' follows ' + str(self.following_mentor))

    @classmethod
    def toggle_follow(cls, obj):
        obj.isfollow = not obj.isfollow
        obj.save()
        return obj

    @classmethod
    def gte_number_of_follow(cls, user):
        return cls.objects.filter(following_mentor=user).count()

    @classmethod
    def get_student_followers_all_state(cls, student):
        # get all users following mentors
        return cls.objects.filter(student=student)

    @classmethod
    def get_student_followers(cls, student, mentor):
        # get all users following mentors
        return cls.objects.filter(student=student, mentor=mentor)

    @classmethod
    def get_is_follow_mentor(cls, student, following_mentor):
        return cls.objects.get(student=student, following_mentor=following_mentor)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BLog, on_delete=models.CASCADE)
    # bin = models.ForeignKey(Bin, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tags)
