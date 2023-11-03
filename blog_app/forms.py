from typing import Any
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Article, Tag



class CreateUserForm(UserCreationForm):
    profile_image = forms.ImageField(required=False) 

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "profile_image"]


    def __init__(self, *args: Any, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({'class': "form-control form-control-lg", "placeholder": "Enter Username"})
        self.fields["email"].widget.attrs.update({'class': "form-control form-control-lg", "placeholder": "Enter Email"})
        self.fields["password1"].widget.attrs.update({'class': "form-control form-control-lg", "placeholder": "Enter Password"})
        self.fields["password2"].widget.attrs.update({'class': "form-control form-control-lg", "placeholder": "Enter Password again"})





class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', "placeholder": "Enter username"}))
        
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', "placeholder": "Enter password"}),

    )
    


class PublishForm(forms.ModelForm):
        
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Article
        fields = ("title", "content", "image_link", "tags", "slug")

        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', "placeholder": "Title of the article"}),
            "content": forms.Textarea(attrs={'class': 'form-control', "placeholder": "Write your article here using Markdown syntax"}),
            "image_link": forms.TextInput(attrs={'class': 'form-control', "placeholder": "e.g https://upload.wikimedia......."}),
            "slug": forms.TextInput(attrs={'class': 'form-control', "placeholder": "e.g  the-best-article-2023"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_link'].required = False
