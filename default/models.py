from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class User(User):
#     follower=models.ForeignKey(User)

class ImageStore(models.Model):
    name = models.CharField(max_length=150, null=True)
    img = models.ImageField(upload_to='img/%Y/%m/%d')


class Question(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    hitcount = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)


class Reply(models.Model):
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    # hello=models.CharField(max_length=100,default=None)
    content = models.TextField(null=True, blank=True)
    picture = models.ForeignKey(ImageStore, blank=True, null=True)
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    isread = models.BooleanField(default=False)


class Comment(models.Model):
    author = models.ForeignKey(User)
    reply = models.ForeignKey(Reply, null=True)
    content = models.TextField(null=True, blank=True)
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    isread = models.BooleanField(default=False)


class Agree(models.Model):
    author = models.ForeignKey(User)
    reply = models.ForeignKey(Reply, null=True)
    addtime = models.DateTimeField(auto_now_add=True)
    isread = models.BooleanField(default=False)


class Favorite(models.Model):
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    addtime = models.DateTimeField(auto_now_add=True)
    isread = models.BooleanField(default=False)


class Follow(models.Model):
    afollow = models.ForeignKey(User, related_name="a_follow")
    followb = models.ForeignKey(User, related_name="follow_b")
    addtime = models.DateTimeField(auto_now_add=True)
    isread = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    portrait = models.ForeignKey(ImageStore)
