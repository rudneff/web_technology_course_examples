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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrong':
            raise ValidationError('Wrong password!')
        return data


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'test_field', 'password']

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        return CustomUser.objects.create_user(**self.cleaned_data)
