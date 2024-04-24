from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserInfo
import logging


@receiver(post_save, sender=UserInfo)
def create_profile(created, **kwargs):
    if created:
        print('User Created')
