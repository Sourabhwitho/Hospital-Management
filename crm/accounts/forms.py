from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
	
class OrderForm(ModelForm):
	class Meta:
		model = Appointment
		fields ='__all__'
		exclude=['patient']


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']