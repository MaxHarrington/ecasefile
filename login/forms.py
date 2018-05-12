from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=100)
	password = forms.CharField(label='password', widget=forms.PasswordInput())

class CreateUserForm(forms.Form):
	username = forms.CharField(label='username', max_length=100)
	password = forms.CharField(label='password', widget=forms.PasswordInput())
	email = forms.EmailField(label='email')
