from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user =  models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    contact = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=255, null=False, blank=False, default="NORMAL MEMBER")

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
