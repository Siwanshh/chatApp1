from django import forms
from .models import Room
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class RoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields=['topic','name','description']
       
class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields= ['user','room','body'] 
class CustomUserCreationForm(UserCreationForm):
    avatar=forms.ImageField(required=True)
    email=forms.EmailField(required=False)
    class Meta:
        model=User
        fields=['username','email','password1','password2','avatar']

         