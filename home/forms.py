from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
class RegistrationForm(forms.Form):
  username = forms.CharField(label='Account', max_length=30)
  email= forms.EmailField(label='Email')
  password1 =forms.CharField(label='password', widget=forms.PasswordInput())
  password2= forms.CharField(label='re pass', widget=forms.PasswordInput())
  
  def clean_password2(self):
    if 'password1' in self.cleaned_data:
      password1= self.cleaned_data['password1']
      password2= self.cleaned_data['password2']
      if password1==password2 and password1:
        return password2
    raise forms.ValidationError("Mk ko hop le")
  def clean_username(self):
    username = self.cleaned_data['username']
    if   not re.search(r'^\w+$', username):
       raise forms.ValidationError("Ten tk co ki tu dac biet")
    try: 
      User.objects.get(username=username)
    except ObjectDoesNotExist:
      return username
    raise forms.ValidationError('tk da ton tai')
  def save(self):
    User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])