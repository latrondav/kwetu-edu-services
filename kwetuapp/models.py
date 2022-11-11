from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user =  models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100, null=False, blank=False)
    status = models.CharField(max_length=100, null=False, blank=False, default="NORMAL MEMBER")

    def __str__(self):
        return str(self.user)

class Contacts(models.Model):
    contact_name = models.CharField(max_length=100, null=False, blank=False)
    contact_email = models.EmailField(null=False, blank=False)
    contact_subject = models.CharField(max_length=100, null=False, blank=False)
    contact_message = models.TextField(max_length=100,)

    def __str__(self):
        return str(self.contact_name)