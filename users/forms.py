from django import forms
from converter.models import DocumentPDF
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='confirm password')

    class Meta:
        model  = User
        fields = ['username', 'password', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("confirm_password")

        if password and password_confirm and password!=password_confirm:
            self.add_error('password confirm', 'password not match')
            