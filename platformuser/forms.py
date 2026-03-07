from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "avatar", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Цей email вже використовується")
        return email


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "avatar", "bio"]


