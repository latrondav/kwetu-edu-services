import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Profile Images', null=True, blank=True, default='profile.jpg')
    bio = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True, default='Normal Member')
    twitter = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Contact(models.Model):
    contact_name = models.CharField(max_length=255, null=False, blank=False)
    contact_email = models.EmailField(null=False, blank=False)
    contact_subject = models.CharField(max_length=255, null=False, blank=False)
    contact_message = models.TextField(max_length=255,)

    def __str__(self):
        return str(self.contact_name)
class Testimonial(models.Model):
    tname = models.CharField(max_length=255, null=False, blank=False)
    ttitle = models.CharField(max_length=255, null=False, blank=False)
    testimonial = models.TextField(max_length=255)

    def __str__(self):
        return str(self.tname)
class Service(models.Model):
    simage = models.ImageField(upload_to='Services Images', null=False, blank=False, default='service.jpg')
    stitle = models.CharField(max_length=255, null=False, blank=False)
    sdescription = models.TextField(max_length=255)

    def __str__(self):
        return str(self.stitle)


class Event(models.Model):
    eimage = models.ImageField(upload_to='Events Images', null=False, blank=False, default='event.jpg')
    ename = models.CharField(max_length=255, null=False, blank=False)
    edate = models.DateField(max_length=255, null=False, blank=False)
    etime = models.TimeField(max_length=255, null=False, blank=False)
    edescription = models.TextField(max_length=255, null=False, blank=False)
    elink = models.CharField(max_length=255, null=False, blank=False)
    eparlink = models.FileField(upload_to='Event Audios', null=False, blank=False, default='eaudios.mp3')
    epytlink = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return str(self.ename)
