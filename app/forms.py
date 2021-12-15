from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField


# class UsernameField(CharField):
#     def validate(self, value):
#         super().validate(value)
#         if value == '123':
#             raise ValidationError("No 123!!")

#
# class UserForm(forms.ModelForm):
#     username = forms.CharField(widget=forms.Textarea)
#
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password']


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


class AskForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()




class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField()
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'avatar']

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.avatar = self.cleaned_data['avatar']
        user.profile.save()
        return user
