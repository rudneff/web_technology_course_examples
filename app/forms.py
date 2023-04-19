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


# class UserForm(forms.ModelForm):
#     username = forms.CharField(widget=forms.Textarea)
#
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrongpassword':
            raise ValidationError("Unacceptable password value!")
        return data


class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(min_length=3, widget=forms.PasswordInput)
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password']

    def clean(self):
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_check']

        if password_1 != password_2:
            raise ValidationError("Passwords do not match!")
        return self.cleaned_data

    def save(self):
        self.cleaned_data.pop('password_check')
        return CustomUser.objects.create_user(**self.cleaned_data)

