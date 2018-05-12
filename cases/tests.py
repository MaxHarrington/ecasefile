from django.test import TestCase
from django.contrib import auth
from django.contrib.auth.models import User
from django.test.client import Client

from .models import Case

class PermissionsTestCase(TestCase):
	def setUp(self):
		password = 'password'

		userEditor = User.objects.create_user('Editor', 'test@test.com', password)
		userViewer = User.objects.create_user('Viewer', 'test@test.com', password)

		self.client.login(username='Editor', password=password)
		Case.objects.create(title='TestCase', text='This is a test')
		self.client.logout()
