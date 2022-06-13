from django import forms
from .models import User
from rest_framework.

class SignUp(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
    def signup(self,request,user):
