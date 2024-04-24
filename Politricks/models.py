from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def send_user_data_when_created(sender, instance, **kwargs):
    user_name = instance.username
    print('User name is', user_name)


class Party(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=256)
    view = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'Party: {self.title}'


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    tag = models.ManyToManyField('Tag')
    photo = models.ImageField(upload_to='profile_pics', blank=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'UserInfo: {self.user.username}'


class PostReaction(models.Model):
    supportCnt = models.ManyToManyField('UserInfo', related_name='post_react_user',)
    unSupportCnt = models.ManyToManyField('UserInfo', related_name='post_antireact_user', blank=True)
    postId = models.ForeignKey('Post', on_delete=models.CASCADE,)

    def __str__(self):
        return f'PostReaction: {self.postId}'


class PartyTestimonial(models.Model):
    title = models.CharField(max_length=205)
    description = models.CharField(max_length=250)
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE,)
    party = models.ForeignKey('Party', on_delete=models.CASCADE, )
    rating = models.IntegerField(blank=True)
    created = models.DateTimeField(null=True, blank=True)
    lastmodified = models.DateTimeField(null=True, blank=True)

    def was_rated_more_than_five(self):
        return self.rating > 5

    def __str__(self):
        return f'PartyTestimonial: {self.title}'


class Status(models.Model):
    label = models.CharField(max_length=120)

    def __str__(self):
        return f'Status: {self.label}'


class Post(models.Model):
    partyID = models.ForeignKey('Party', on_delete=models.CASCADE,)
    locationID = models.ForeignKey('Location', on_delete=models.CASCADE,)
    userID = models.ForeignKey('UserInfo', on_delete=models.CASCADE,)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=256)
    privacy = models.CharField(max_length=120)
    create_at = models.DateTimeField(null=True, blank=True)
    view = models.IntegerField(blank=True, default=0)
    picture = models.ImageField(default='default.jpg', upload_to='post_photos', blank=True)
    postTag = models.ManyToManyField('Tag')
    deleted = models.BooleanField(default=0)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.create_at <= now

    def __str__(self):
        return f'Post: {self.title}'


class Comment(models.Model):
    postID = models.ForeignKey('Post', on_delete=models.CASCADE, default=0)
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, default=0)
    postDate = models.DateTimeField(null=True, blank=True)
    content = models.CharField(max_length=256)

    def __str__(self):
        return f'Comment: {self.postID}'


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'Tag: {self.name}'


class UserTag(models.Model):
    tagId = models.ForeignKey('Tag', on_delete=models.CASCADE,)
    postId = models.ManyToManyField('Post')


class Location(models.Model):
    name = models.CharField(max_length=64)
    shortName = models.CharField(max_length=20)

    def __str__(self):
        return f'Location: {self.name}'
