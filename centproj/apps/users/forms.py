from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
  username = forms.CharField(required=True, min_length=6)
  password = forms.CharField(required=True, min_length=4)

class DynamicLoginForm(forms.Form):
  mobile = forms.CharField(required=True, min_length=10, max_length=10)
  captcha = CaptchaField()

class DynamicLoginPostForm(forms.Form):
  mobile = forms.CharField(required=True, min_length=10, max_length=10)
  code = forms.CharField(required=True, min_length=4, max_length=4)

class QrLoginPostForm(forms.Form):
  username = forms.CharField(required=True, min_length=6)
  password = forms.CharField(required=True, min_length=4)
  code = forms.CharField(required=True, min_length=4, max_length=4)

class VoiceLoginPostForm(forms.Form):
  username = forms.CharField(required=True, min_length=6)
  password = forms.CharField(required=True, min_length=4)
  secrect = forms.CharField(required=True, min_length=4, max_length=50)