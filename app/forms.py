from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField


# class UsernameField(CharField):
#     def validate(self, value):
#         super().validate(value)
#         if value == '123':
#             raise ValidationError("No 123!!")
from app.models import CustomUser


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        if self.cleaned_data['username'] == '123':
            raise ValidationError("No 123!!")

        return self.cleaned_data['username']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_repeat']:
            self.add_error(None, "Passwords do not match!")
        return cleaned_data
