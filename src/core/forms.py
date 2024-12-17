from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Post

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={
        'placeholder':'Email'
    }))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={
        'placeholder':'Passworld'
    }))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={
       'placeholder':'Comfirm Passworld'
    }))
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

    def clean(self):
        data = self.cleaned_data
        email = self.data.get('email')
        qs = User.objects.filter(email=email).exists()
        if qs:
            self.add_error('email',f"{email}'s already exists.")
        return data

class CreateForm(forms.ModelForm):
    image = forms.ImageField(label="",required=True)
    name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Post 😎🥰 '}),required=True)
    class Meta:
        model = Post
        fields = ['name','image']