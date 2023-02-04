from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user =  models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Profile Images', null=True, blank=True, default='profile.jpg')
    bio = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
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
