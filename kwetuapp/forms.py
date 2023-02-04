from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
                    'image',
                    'bio',
                    'contact',
                    'position',
                    'twitter',
                    'facebook',
                    'instagram',
                    'linkedin',
                )

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
                'first_name',
                'last_name',
                'email',
            )
