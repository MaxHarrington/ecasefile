from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=100)
	password = forms.CharField(label='password', widget=forms.PasswordInput())


class CreateUserForm(forms.Form):
	username = forms.CharField(label='username', max_length=100)
	password = forms.CharField(label='password', widget=forms.PasswordInput())
	email = forms.EmailField(label='email')


class ChangePasswordForm(forms.Form):
	new_password = forms.CharField(label='new password', widget=forms.PasswordInput())
	confirm_new_password = forms.CharField(label='confirm new password', widget=forms.PasswordInput())
