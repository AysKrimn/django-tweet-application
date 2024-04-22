from django import forms
# user model
from django.contrib.auth.models import User

# form validation
class UserProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email"]
        help_texts = {

            "username": None
        }