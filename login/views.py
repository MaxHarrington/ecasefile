from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import LoginForm, CreateUserForm


# Processes login requests for the filing tool.
def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			user = auth.authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password']
				)
			if not user:
				auth.login(request, user)
				return redirect('/')
			else:
				form = LoginForm()
				failed_login = True
				return render(request, 'login/login.html', {
					'form': form, 
					'failed_login': failed_login
					})
	else:
		form = LoginForm()
	return render(request, 'login/login.html', {'form': form})


# Attempts to logout the user.
@login_required
def logout_user(request):
	auth.logout(request)
	return render(request, 'login/logout.html')


# Creates an account for the user if one doesn't exist.
# Requires a valid email address, and returns error if already exists.
def create_account(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			try:
				user = User.objects.create_user(
					username=form.cleaned_data['username'],
					email=form.cleaned_data['email'],
					password=form.cleaned_data['password']
					)
				return render(request, 'login/account_success.html')
			except auth.IntegrityError:
				form = CreateUserForm()
			return render(request, 'login/create_account.html', {
					'form': form, 
					'username_taken': True
					})
	else:
		form = CreateUserForm()
	return render(request, 'login/create_account.html', {'form': form})
