from .models import Player, User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class User_FormControl(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(User_FormControl, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class Profile_FormControl(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Profile_FormControl, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input-mini'


class UserForm(User_FormControl):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {'password': widgets.PasswordInput()}


class PlayerForm(Profile_FormControl):
    class Meta:
        model = Player
        fields = ['photo', 'age', 'country']
